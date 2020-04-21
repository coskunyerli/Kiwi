import os

projectPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
filePath = os.path.join(os.path.expanduser('~'), '.todolist')
filesPath = os.path.join(filePath, 'files')
fileListPath = os.path.join(filePath, 'fileList.json')
