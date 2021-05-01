import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore
from widget.imageView import ImageViewer
from widget.viewer.baseViewerInterface import BaseViewerInterface


class ImageView(QtWidgets.QWidget, BaseViewerInterface):
	def __init__(self, parent = None):
		super(ImageView, self).__init__(parent)
		self.resize(600, 600)
		self.setStyleSheet('background-color:#303030')
		self.mainWidgetLayout = QtWidgets.QHBoxLayout(self)
		self.imageFileData = None
		self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.mainWidgetLayout.setSpacing(0)
		self.graphicsView = ImageViewer(self)
		self.mainWidgetLayout.addWidget(self.graphicsView)


	def isExternalWidget(self):
		return False


	def currentData(self):
		return self.imageFileData


	def setCurrentData(self, data):
		self.imageFileData = data
		self.__setCurrentData()


	def __setCurrentData(self):
		# fit in view after viewer open
		self.graphicsView.setPixmap(self.imageFileData.pixmap())
		self.graphicsView.fitInView(self.graphicsView.pixmapItem, QtCore.Qt.KeepAspectRatio)


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_F:
			# press F key fit in view
			self.graphicsView.fitInView(self.graphicsView.pixmapItem, QtCore.Qt.KeepAspectRatio)
		else:
			super(ImageView, self).keyPressEvent(event)


	def id(self):
		if self.currentData() is not None:
			return self.currentData().id()
		else:
			return None


	def accept(self):
		return True
