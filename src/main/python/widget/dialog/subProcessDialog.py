import subprocess


class SubProcessDialog(object):
	def __init__(self, executable):
		self.executable = executable
		self.process = None


	def open(self):
		self.process = subprocess.Popen(self.executable)


	def setStyleSheet(self, styleSheet):
		pass
