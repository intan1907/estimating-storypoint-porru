import _pickle
import sklearn 
import numpy

import sys

try:
    project = sys.argv[1]
    input_path = sys.argv[2]
    model_path = 'trained_model/' + sys.argv[1] + '.pkl'
except:
    print('No argument, default model: mesos')
    project = 'mesos'
    input_path = 'input/mesos.pkl'
    model_path = 'trained_model/' + 'mesos' + '_porru.pkl'

input = numpy.array(_pickle.load(input_path))
clf = _pickle.load(model_path)
predict = clf.predict()

print(predict)