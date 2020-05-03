import os

from fbs_runtime.application_context.PySide2 import ApplicationContext


class TodoListApplicationContext(ApplicationContext):
	def __init__(self):
		super(TodoListApplicationContext, self).__init__()

		if not os.path.isdir(self.filePath):
			os.makedirs(self.filePath)
		if not os.path.isdir(self.filesPath):
			os.makedirs(self.filesPath)


	def qss(self, filename):
		try:
			file = open(self.get_resource(os.path.join('qss', filename)))
			string = file.read()
			return string
		except Exception as e:
			return None


	def icons(self, iconName):
		return self.get_resource(os.path.join('icons', iconName))


	@property
	def conf(self):
		return self.get_resource('editor.conf')


	@property
	def filePath(self):
		return os.path.join(os.path.expanduser('~'), '.todolist')


	@property
	def filesPath(self):
		return os.path.join(self.filePath, 'files')


	@property
	def fileListPath(self):
		return os.path.join(self.filePath, 'fileList.json')
