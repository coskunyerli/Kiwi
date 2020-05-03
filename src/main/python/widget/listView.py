from PySide2 import QtWidgets, QtCore

from delegate.fileViewDelegate import FileViewDelegate
from enums import ItemFlags


class ListView(QtWidgets.QListView):
	currentIndexChanged = QtCore.Signal(QtCore.QModelIndex)


	def __init__(self, parent = None):
		super(ListView, self).__init__(parent)
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


	def currentChanged(self, current, old):
		super(ListView, self).currentChanged(current, old)
		self.currentIndexChanged.emit(current)


	def dragMoveEvent(self, event):
		mimeData = event.mimeData()
		dropObject = mimeData.colorData()
		if dropObject:
			hoverIndex = self.indexAt(event.pos())
			if hoverIndex.isValid() and hoverIndex.data(QtCore.Qt.UserRole) == dropObject:
				return super(ListView, self).dragMoveEvent(event)
			else:
				event.acceptProposedAction()
		else:
			return super(ListView, self).dragMoveEvent(event)
#
#
# def rename(self):
# 	index = self.currentIndex()
# 	model = self.model()
# 	newText, result = QtWidgets.QInputDialog.getText(self, 'Rename File', 'New file name',
# 													 QtWidgets.QLineEdit.Normal)
# 	if result:
# 		model.setData(index, newText)
#
#
# def setPassword(self):
# 	index = self.currentIndex()
# 	password, result = QtWidgets.QInputDialog.getText(self, 'Set Password', 'Enter a password',
# 													  QtWidgets.QLineEdit.Password)
# 	if password and result and index.isValid():
# 		data = index.internalPointer()
# 		data.isLocked = True
#
#
# def delete(self):
# 	self.mainWidget.delete()
#
#
# def newFile(self):
# 	self.mainWidget.newFile()
#
#
# def newFolder(self):
# 	self.mainWidget.newFolder()
