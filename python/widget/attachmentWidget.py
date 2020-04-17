from PySide2 import QtWidgets


class AttachmentWidget(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(AttachmentWidget, self).__init__(parent)
		self._file = None


	# burada attachment dosyalari olacak, herhangi bir dosya olabilir

	def setFile(self, file_):
		self._file = file_


	def file(self):
		return self._file
