import gzip
import _pickle
import numpy

import sys

from sklearn.feature_selection import chi2, f_classif

try:
    dataset = sys.argv[1] + '.pkl.gz'
    saving = sys.argv[2]
except:
    # print('No argument, default project = mesos')
    # dataset = 'mesos_porru.pkl.gz'
    # saving = 'test_porru_method'
    print('No argument, default project = clover')
    dataset = 'clover.pkl.gz'
    saving = 'test_clover'

# f = gzip.open('dataset_pickle/' + dataset, 'rb') 
f = gzip.open('dataset_pickle_/' + dataset, 'rb') 

# train_context, train_code, train_binaryfeats, train_y, \
# valid_context, valid_code, valid_binaryfeats, valid_y, \
# test_context, test_code, test_binaryfeats, test_y = numpy.array(_pickle.load(f, encoding='bytes'))

train_context, train_y, \
valid_context, valid_y, \
test_context, test_y = numpy.array(_pickle.load(f, encoding='bytes'))


def listtostring(word_id):
    str_id = []
    for i in range(len(word_id)):
        str_id.append(' '.join(map(str, word_id[i])))
    return str_id


def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0, size):
        list_of_objects.append(list())  # different object reference each time
    return list_of_objects


print('convert word id to text...')

train_context = numpy.array(train_context)
# train_code = numpy.array(train_code)
# train_binaryfeats = numpy.array(train_binaryfeats)
train_y = numpy.array(train_y)

valid_context = numpy.array(valid_context)
# valid_code = numpy.array(valid_code)
# valid_binaryfeats = numpy.array(valid_binaryfeats)
valid_y = numpy.array(valid_y)

test_context = numpy.array(test_context)
# test_code = numpy.array(test_code)
# test_binaryfeats = numpy.array(test_binaryfeats)
test_y = numpy.array(test_y)

from sklearn.feature_extraction.text import TfidfVectorizer

# build TfidfVectorizer for monogram and bi-gram for contexts
tfidf_vectorizer = TfidfVectorizer(stop_words=None, lowercase=False, ngram_range=[1, 2])
tfidf_vectorizer.fit(listtostring(train_context))
train_context_tfidf = tfidf_vectorizer.transform(listtostring(train_context)).toarray()
valid_context_tfidf = tfidf_vectorizer.transform(listtostring(valid_context)).toarray()
test_context_tfidf = tfidf_vectorizer.transform(listtostring(test_context)).toarray()

# build TfidfVectorizer for monogram and bi-gram for codedsnippet
# tfidf_vectorizer = TfidfVectorizer(stop_words=None, lowercase=False, ngram_range=[1, 2])
# tfidf_vectorizer.fit(listtostring(train_code))
# train_code_tfidf = tfidf_vectorizer.transform(listtostring(train_code)).toarray()
# valid_code_tfidf = tfidf_vectorizer.transform(listtostring(valid_code)).toarray()
# test_code_tfidf = tfidf_vectorizer.transform(listtostring(test_code)).toarray()

# concat all features
print(len(train_context_tfidf))
# print(len(train_code_tfidf))
# print(len(train_binaryfeats))

# train_x = numpy.concatenate((train_context_tfidf, train_code_tfidf, train_binaryfeats), axis=1)
# valid_x = numpy.concatenate((valid_context_tfidf, valid_code_tfidf, valid_binaryfeats), axis=1)
# test_x = numpy.concatenate((test_context_tfidf, test_code_tfidf, test_binaryfeats), axis=1)
train_x = train_context_tfidf
valid_x = valid_context_tfidf
test_x = test_context_tfidf

# #############################################################################
# Create a feature-selection transform and an instance of SVM that we
# combine together to have an full-blown estimator

from sklearn.pipeline import Pipeline
from sklearn import svm, feature_selection

transform = feature_selection.SelectKBest(score_func=f_classif, k=50)
clf = Pipeline([('feat_select', transform), ('classifier', svm.SVC())])
clf.fit(train_x, numpy.floor(train_y))
predict = clf.predict(test_x)
# print(test_x)

# save model
# model_file = 'trained_model/' + saving + '.pkl'
model_file = 'trained_model_/' + saving + '.pkl'
with open(model_file, 'wb') as pickle_file:
    _pickle.dump(clf, pickle_file)

# numpy.savetxt('log/output/' + saving + "_actual.csv", test_y, delimiter=",")
# numpy.savetxt('log/output/' + saving + "_estimate.csv", predict, delimiter=",")
numpy.savetxt('log_/output/' + saving + "_actual.csv", test_y, delimiter=",")
numpy.savetxt('log_/output/' + saving + "_estimate.csv", predict, delimiter=",")
