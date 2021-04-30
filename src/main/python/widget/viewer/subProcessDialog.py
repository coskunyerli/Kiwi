import subprocess
from widget.viewer.baseViewerInterface import BaseViewerInterface


class SubProcessDialog(BaseViewerInterface):
	def __init__(self, executable):
		self.executable = executable
		self.process = None


	def open(self):
		self.process = subprocess.Popen(self.executable)


	def setStyleSheet(self, styleSheet):
		pass

	def isExternalWidget(self):
		return True

	def id(self):
		return '&'.join(self.executable)
