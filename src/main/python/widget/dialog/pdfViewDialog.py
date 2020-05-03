import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
from widget.imageView import ImageViewer


class ImageViewDialog(QtWidgets.QDialog):
	def __init__(self, parent = None):
		super(ImageViewDialog, self).__init__(parent)
		self.resize(600, 600)
		self.setStyleSheet('background-color:#303030')
		self.mainWidgetLayout = QtWidgets.QHBoxLayout(self)
		self.imageFileData = None
		self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.mainWidgetLayout.setSpacing(0)
		self.graphicsView = ImageViewer(self)
		self.mainWidgetLayout.addWidget(self.graphicsView)


	def setCurrentData(self, data):
		self.imageFileData = data


	def open(self):
		super(ImageViewDialog, self).open()
		self.graphicsView.setPixmap(self.imageFileData.pixmap())
		self.graphicsView.fitInView(self.graphicsView.pixmapItem, QtCore.Qt.KeepAspectRatio)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F:
			self.graphicsView.fitInView(self.graphicsView.pixmapItem, QtCore.Qt.KeepAspectRatio)
		else:
			super(ImageViewDialog, self).keyPressEvent(event)
