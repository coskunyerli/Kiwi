import logging as log
import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
from enums import DataType
from model.data import ImageFileData
from widget.imageView import ImageViewer
from widget.toast import Toast
from widget.viewer.baseViewerInterface import BaseViewerInterface


class ImageView(QtWidgets.QWidget, BaseViewerInterface):
	fileSaved = QtCore.Signal(ImageFileData)


	def __init__(self, parent = None):
		super(ImageView, self).__init__(parent)
		self.resize(600, 600)
		self.setStyleSheet('background-color:#303030')
		self.mainWidgetLayout = QtWidgets.QHBoxLayout(self)
		self.imageFileData = None
		self.__isModified = False
		self.__filename = None
		self.__extension = None
		self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.mainWidgetLayout.setSpacing(0)
		self.graphicsView = ImageViewer(self)
		self.mainWidgetLayout.addWidget(self.graphicsView)
		self.initializeShortcuts()


	def initializeShortcuts(self):
		self.saveShortcut = QtWidgets.QShortcut(self.graphicsView)
		self.saveShortcut.setKey(QtGui.QKeySequence.Save)
		self.saveShortcut.activated.connect(self.save)
		self.saveShortcut.setContext(QtCore.Qt.WidgetShortcut)


	def save(self):
		if self.isModified() is True and self.__filename is not None:
			filename = self.__filename
			if self.currentData() is not None:
				path = self.currentData().path
			else:
				path = self.__path
			result = True
			if filename and result is True:
				return self.__save(filename, path)
		return False


	def __save(self, filename, path):
		try:
			self.graphicsView.getPixmap().save(path)
		except Exception as e:
			Toast.error('Image Save Error', 'Text is not saved successfully.')
			log.error(f'Image file is not saved successfully. Path is {path}. Exception is {e}')
			return False

		self.setModified(False)
		if self.currentData() is None:
			newFile = ImageFileData(filename, path)
			newFile.setType(DataType.IMAGEFILEDATA)
			self.imageFileData = newFile
			self.__filename = filename
			self.__path = path
		self.fileSavedSignal().emit(self.currentData())
		return True


	def isExternalWidget(self):
		return False


	def fileSavedSignal(self):
		return self.fileSaved


	def currentData(self):
		return self.imageFileData


	def setCurrentData(self, data):
		self.imageFileData = data
		self.__setCurrentData()


	def __setCurrentData(self):
		# fit in view after viewer open
		if self.currentData() is not None:
			self.graphicsView.setPixmap(self.currentData().pixmap())
			self.graphicsView.fitInView(self.graphicsView.pixmapItem, QtCore.Qt.KeepAspectRatio)
			self.__filename = self.currentData().name()
			self.__path = self.currentData().path


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
		if self.isModified() is True:
			# do not show warning message if current data is valid
			if self.currentData() is None:
				ret = QtWidgets.QMessageBox.warning(self, "Application",
													"The document hasdasas been modified.\n"
													"Do you want to save your changes?",
													QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel |
													QtWidgets.QMessageBox.No)
			else:
				ret = QtWidgets.QMessageBox.Yes

			if ret == QtWidgets.QMessageBox.Yes:
				# save the session before quit
				if self.save() is False:
					# if not saved, not closed
					return False

			elif ret == QtWidgets.QMessageBox.Cancel:
				return False

		return True


	def setModified(self, res):
		self.__isModified = res


	def isModified(self):
		return self.__isModified
