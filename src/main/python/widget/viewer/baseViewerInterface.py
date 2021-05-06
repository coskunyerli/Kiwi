import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore


class BaseViewerInterface(object):
	def id(self):
		pass


	def currentData(self):
		pass


	def setCurrentData(self, data):
		pass


	def isExternalWidget(self):
		pass


	def fileSavedSignal(self):
		pass
