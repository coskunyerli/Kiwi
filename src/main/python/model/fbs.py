import os

from fbs_runtime.application_context.PySide2 import ApplicationContext


class TodoListApplicationContext(ApplicationContext):
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
