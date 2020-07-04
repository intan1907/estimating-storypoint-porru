import gzip
import sys
import _pickle as pkl
import pandas
import numpy
import operator

# from nltk.corpus import stopwords 
# from nltk.tokenize import word_tokenize

from subprocess import Popen, PIPE
chosen_frequency = 10

try:
    project = sys.argv[1]
except:
    print('No argument, default project: clover')
    project = 'clover'

def normalize(seqs):
    for i, s in enumerate(seqs):
        words = s.split()
        if len(words) < 1:
            seqs[i] = 'nan'
    return seqs


print('Project:' + project)

tokenizer_cmd = ['/usr/bin/perl', 'tokenizer.perl', '-l', 'en', '-q', '-']

def tokenize(sentences):
    print('Tokenizing..'),
    text = bytes('\n'.join(sentences), 'utf-8')
    tokenizer = Popen(tokenizer_cmd, stdin=PIPE, stdout=PIPE) # pass string to perl function for tokenizing
    tok_text, _ = tokenizer.communicate(text)
    toks = tok_text.decode('utf-8').split('\n')[:-1]
    # print(tok_text , "\n\n")
    # print('toks: ' , toks , "\n")

    print('Done')
    return toks

# def tokenize(sentences):
#     print ('Tokenizing..')
#     text = '\n'.join(sentences)
#     toks = word_tokenize(text)
#     # print('toks', toks)
#     print('Done')
#     return toks

# def remove_stop_words(doc):
#     if(type(doc) == list):
#         word_tokens = doc
#     else:
#         word_tokens = tokenize(doc)
#     stop_words = set(stopwords.words('english')) 
#     filtered_sentence = []
#     for w in word_tokens: 
#         if w not in stop_words: 
#             filtered_sentence.append(w)
#     return filtered_sentence


def calculateStoryPointDistribution(sp_list):
    story_count = dict()
    for sp in (sp_list):
        if sp in story_count:
            story_count[sp] += 1
        else:
            story_count[sp] = 1
    print('total data:', len(sp_list))
    print('story point distribution:\n', sorted(story_count.items()))
    
# def grab_data(context, codesnippet, dictionary):
#     context = tokenize(context)
#     codesnippet = tokenize(codesnippet)

#     seqs = [[None] * len(context), [None] * len(codesnippet)]
#     for i, sentences in enumerate([context, codesnippet]):
#         for idx, ss in enumerate(sentences):
#             words = ss.strip().lower().split()
#             seqs[i][idx] = [dictionary[w] if w in dictionary else 0 for w in words]
#             if len(seqs[i][idx]) == 0:
#                 print('len 0: ', i, idx)

#     return seqs[0], seqs[1]

def grab_data(context, dictionary):
    context = tokenize(context)
    
    seqs = [None] * len(context)
    for idx, ss in enumerate(context):
        words = ss.strip().lower().split()
        seqs[idx] = [dictionary[w] if w in dictionary else 0 for w in words]
        if len(seqs[idx]) == 0:
            print('len 0: ', i, idx)

    return seqs

def build_dict(sentences):
    sentences = tokenize(sentences)
    # sentences = remove_stop_words(sentences)

    print('Building dictionary..')
    wordcount = dict()
    for ss in sentences:
        words = ss.strip().lower().split()
        for w in words:
            if w not in wordcount:
                wordcount[w] = 1
            else:
                wordcount[w] += 1

    keys = numpy.array(list(wordcount.keys()))
    counts = numpy.array(list(wordcount.values()))

    sorted_idx = numpy.argsort(counts)[::-1] # index of (element yang di-sort)

    print('number of words in dictionary:', len(keys))

    worddict = dict()

    for idx, ss in enumerate(sorted_idx):
        worddict[keys[ss]] = idx+1  # leave 0 (UNK)

    pos = 0
    for i, key in enumerate(sorted_idx):
        if counts[key] >= chosen_frequency: 
            pos = i
            
    print(numpy.sum(counts), 'total words,', pos, 'words with frequency >=', chosen_frequency)
    # print(worddict)
    return worddict

def clean_sen(sen):
    sen = ''.join([c if ord(c) < 128 and ord(c) > 32 else ' ' for c in sen])
    return sen

# read data from csv
# data_path = 'csv/' + project + '.csv'
data_path = 'dataset_/' + project + '.csv'

data = pandas.read_csv(data_path).values
labels = data[:, 3].astype('float32')
# labels = data[:, 1].astype('float32')
# context = normalize(data[:, 2].astype('str'))
# codesnippet = normalize(data[:, 3].astype('str'))
summary = normalize(data[:, 1].astype('str'))
description = normalize(data[:, 2].astype('str'))
# binaryFeat = data[:, 4:].astype('float32')

# context = summary + description
context = description
for i in range(len(data)):
    if summary[i] == 'nan':
        if description[i] == 'nan':
            continue
        context[i] = description[i]
    elif description[i] == 'nan':
        # print('len', i, description[i], '\n')
        if summary[i] == 'nan':
            continue
        context[i] = summary[i]
    else: 
        context[i] = summary[i] + ' ' + description[i]

for i in range(len(context)):
    if context[i] is None:
        context[i] = 'None'
    else:
        context[i] = clean_sen(context[i])

calculateStoryPointDistribution(labels)

# for i in range(len(codesnippet)):
#     if codesnippet[i] is None:
#         codesnippet[i] = 'None'
#     else:
#         codesnippet[i] = clean_sen(codesnippet[i])

# read 3 set of data
# f = open('dataset_distribution/' + project + '_3sets.txt', 'r')

f = open('dataset_/' + project + '_mo_3sets.txt', 'r')
train_ids, valid_ids, test_ids = [], [], []
count = -2
for line in f:
    if count == -2:
        count += 1
        continue

    count += 1
    ls = line.split()
    if ls[0] == '1':
        train_ids.append(count)
    if ls[1] == '1':
        valid_ids.append(count)
    if ls[2] == '1':
        test_ids.append(count)

print('ntrain, nvalid, ntest: ', len(train_ids), len(valid_ids), len(test_ids))

#preprocess data and packing
# train_context, train_codesnippet, train_binaryFeat, train_labels = context[train_ids], codesnippet[train_ids], binaryFeat[train_ids], labels[train_ids]
# valid_context, valid_codesnippet, valid_binaryFeat, valid_labels = context[valid_ids], codesnippet[valid_ids], binaryFeat[valid_ids], labels[valid_ids]
# test_context, test_codesnippet, test_binaryFeat, test_labels = context[test_ids], codesnippet[test_ids], binaryFeat[test_ids], labels[test_ids]

train_context, train_labels = context[train_ids], labels[train_ids]
valid_context, valid_labels = context[valid_ids], labels[valid_ids]
test_context, test_labels = context[test_ids], labels[test_ids]
# print(train_context)

# dictionary = build_dict(numpy.concatenate([train_context, train_codesnippet]))
# f = gzip.open('dict/' + project + '.dict.pkl.gz', 'wb')
dictionary = build_dict(train_context)
f = gzip.open('dict_/' + project + '.dict.pkl.gz', 'wb')
pkl.dump(dictionary, f, -1)
f.close()

# train_t, train_d = grab_data(train_context, train_codesnippet, dictionary)
# valid_t, valid_d = grab_data(valid_context, valid_codesnippet, dictionary)
# test_t, test_d = grab_data(test_context, test_codesnippet, dictionary)

train_t = grab_data(train_context, dictionary)
valid_t = grab_data(valid_context, dictionary)
test_t = grab_data(test_context, dictionary)

# f = gzip.open('dataset_pickle/' + project + '.pkl.gz', 'wb')
f = gzip.open('dataset_pickle_/' + project + '.pkl.gz', 'wb')

# pkl.dump((train_t, train_d,train_binaryFeat, train_labels,
#               valid_t, valid_d,valid_binaryFeat, valid_labels,
#               test_t, test_d,test_binaryFeat, test_labels), f, -1)

pkl.dump((train_t, train_labels,
              valid_t, valid_labels,
              test_t, test_labels), f, -1)

f.close()
