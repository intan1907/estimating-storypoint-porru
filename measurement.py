import sys
import numpy
from sklearn.metrics import mean_absolute_error, accuracy_score

def arg_passing_any(argv):
    i = 1
    arg_dict = {}
    while i < len(argv) - 1:
        arg_dict[argv[i]] = argv[i+1]
        i += 2
    return arg_dict

args = arg_passing_any(sys.argv)

try:
    project = args['-project']
    fileName = args['-fileName']
    note = args['-note']
except:
    # print('No args, default project: mesos')
    # project = 'mesos'
    # fileName = 'test_porru_method'
    # note = 'test'
    print('No args, default project: clover')
    project = 'clover'
    fileName = 'test_clover'
    note = 'test'

# actualFile = 'log/output/' + fileName + '_actual.csv'
# estimateFile = 'log/output/' + fileName + '_estimate.csv'
actualFile = 'log_/output/' + fileName + '_actual.csv'
estimateFile = 'log_/output/' + fileName + '_estimate.csv'


actual = numpy.genfromtxt(actualFile, delimiter=',')
estimate = numpy.genfromtxt(estimateFile, delimiter=',')

# Save absolute error in log/absolute_error
# ar_outputFileName = 'log/absolute_error/' + fileName
ar_outputFileName = 'log_/absolute_error/' + fileName
numpy.savetxt(ar_outputFileName + ".csv", (numpy.absolute(actual - estimate)), delimiter=",", fmt='%1.4f')

# print('actual: ', actual)
MMRE = numpy.mean(2.0*((numpy.absolute(actual - estimate))/(actual + estimate)))
MAE = mean_absolute_error(actual, estimate)
accuracy = accuracy_score(actual.round(), estimate.round())

print(fileName + ", " + note + ", " + str(MMRE) + ", " + str(MAE) + ", " + str(accuracy) + '\n')

# with open('log/performance_all.csv', 'a') as myoutput:
with open('log_/performance_all.csv', 'a') as myoutput:
    myoutput.write('\n' + fileName + "," + note + "," + str(MMRE) + "," + str(MAE) + "," + str(accuracy))