import os

from fbs_runtime.application_context.PySide2 import ApplicationContext


class TodoListApplicationContext(ApplicationContext):
	def __init__(self):
		super(TodoListApplicationContext, self).__init__()

		if not os.path.isdir(self.filePath):
			os.makedirs(self.filePath)
		if not os.path.isdir(self.filesPath):
			os.makedirs(self.filesPath)
		if not os.path.exists(self.fileListPath):
			with open(self.fileListPath, 'w') as file:
				file.write('{}')


	def qss(self, filename):
		try:
			file = open(self.get_resource(os.path.join('qss', filename)))
			string = file.read()
			return self.qssFromString(string)
		except Exception as e:
			return None


	def qssFromString(self, qss):
		# Replacement of some %....% strings is done before

		qss = qss.replace('%PATH%', self.icons())

		# Reading possible functions is done afterwards
		shouldRead = False
		functionString = ''
		commentLine = False

		# Get all functions inside qss e.g &join(%PATH%, add.svg);&
		for i in range(len(qss)):
			if qss.startswith('/*', i):
				commentLine = True

			elif qss.startswith('*/', i) and commentLine:
				commentLine = False

			if not commentLine:
				if qss.startswith('&', i):
					if shouldRead:
						splitString = functionString.split('(')
						funcToUse = splitString[0]
						parameterString = splitString[1]
						parameters = parameterString.split(',')
						parameters[-1] = parameters[-1].split(')')[0]

						if funcToUse == 'join':
							stringToReplace = join([param.replace(' ', '') for param in parameters])
							qss = qss.replace('&' + functionString + '&', stringToReplace.replace('\\', '/'))

						# .. Here other functions can be filled ..

						# ----------------------------------------
						functionString = ''

					shouldRead = not shouldRead

				elif shouldRead:
					functionString = functionString + qss[i]

		return qss


	def icons(self, iconName = ''):
		return self.get_resource(os.path.join('icons', iconName))


	@property
	def conf(self):
		return self.get_resource('editor.json')


	@property
	def filePath(self):
		return os.path.join(os.path.expanduser('~'), '.todolist')


	@property
	def filesPath(self):
		return os.path.join(self.filePath, 'files')


	@property
	def fileListPath(self):
		return os.path.join(self.filePath, 'fileList.json')


# This function is called from Ive.qss with the same name with the usage of: &join(param1, param2, ...)&
def join(pathList):
	joinedPath = ''
	for path in pathList:
		joinedPath = os.path.join(joinedPath, path)

	return joinedPath
