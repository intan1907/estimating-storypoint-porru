import sys
import pandas
import numpy

try:
    project = sys.argv[1]
    data_path = 'csv/' + sys.argv[1] + '_porru.csv'
except:
    print('No argument, default project: mesos')
    project = 'mesos'
    data_path = 'csv/' + 'mesos' + '_porru.csv'

data = pandas.read_csv(data_path).values
labels = data[:, 1].astype('int64')

trainingSize = 60
validationSize = 20
testSize = 20

if trainingSize + validationSize + testSize == 100:
    numData = len(labels)
    
    numValidation = int(round((validationSize * numData) / 100))
    numTest = int(round((testSize * numData) / 100))
    numTrain = numData - (numValidation + numTest)

    print("Total data: ", numData)
    print("Training size: ", numTrain, ", validation size: ", numValidation, ", testing size: ", numTest)
    print("Total: ", (numTrain + numValidation + numTest))

    divided_set = numpy.zeros((len(labels), 3)).astype('int64')

    divided_set[0 : numTrain-1, 0] = 1
    divided_set[numTrain-1: numTrain+numValidation-1, 1] = 1
    divided_set[numTrain+numValidation- 1:numData, 2] = 1

    f = open('dataset_distribution/' + project + '_porru_3sets.txt', 'w')
    f.write('train\tvalid\ttest')
    for s in divided_set:
        f.write('\n%d\t%d\t%d' % (s[0], s[1], s[2]))

    f.close()
else:
    print("check size in source code")