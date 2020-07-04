import os

# This is a run script for Porru's method.
dataset = ['appceleratorstudio', 'aptanastudio', 'bamboo', 'clover', 
    'datamanagement', 'duracloud', 'jirasoftware', 'mesos', 
    'moodle', 'mule', 'mulestudio', 'springxd', 
    'talenddataquality', 'talendesb', 'titanium', 'usergrid']

# run divide data
for project in dataset:
    cmd = 'python divide_data_sortdate.py ' + project
    print(cmd)
    os.system(cmd)

# run preprocess
for project in dataset:
    cmd = 'python preprocess.py ' + project
    print(cmd)
    os.system(cmd)

# run Porru's model
note = 'exp'
for project in dataset:
    cmd = 'python porrumethod.py ' + project + ' ' + project + '_porru_method'
    print(cmd)
    os.system(cmd)
    
    print('compute error')
    cmd = 'python measurement.py -project ' + project + ' -fileName ' + project + '_porru_method' + ' -note ' + note
    os.system(cmd)
