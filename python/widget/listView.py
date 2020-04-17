from PySide2 import QtWidgets, QtCore

from python.delegate.fileViewDelegate import FileViewDelegate
from python.enums import ItemFlags


class ListView(QtWidgets.QListView):
	currentIndexChanged = QtCore.Signal(QtCore.QModelIndex)


	def __init__(self, parent = None):
		super(ListView, self).__init__(parent)
		self.mainWidget = None
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.showRightClickPopup)
		delegate = FileViewDelegate(self)
		self.setItemDelegate(delegate)


	def setEditor(self, mainWidget):
		self.mainWidget = mainWidget


	def currentChanged(self, current, old):
		self.currentIndexChanged.emit(current)
		super(ListView, self).currentChanged(current, old)


	def showRightClickPopup(self, pos):
		globalPos = self.mapToGlobal(pos)
		index = self.currentIndex()
		model = self.model()
		data = index.internalPointer()
		contextMenu = QtWidgets.QMenu()
		fixItem = ''
		renameItem = ''
		deleteItem = ''
		passwordItem = ''
		if not model.flags(index) & ItemFlags.ItemIsSoftLink and data is not None:
			fixItem = contextMenu.addAction('Unpin Note' if data.isFixed else 'Pin Note')
			renameItem = contextMenu.addAction("Rename")
			deleteItem = contextMenu.addAction('Delete')
			contextMenu.addSeparator()
			if data.isLocked is None:
				passText = "Set Password"
			else:
				passText = "Remove Password"
				if data.isLocked:
					lockText = 'Unlock'
				else:
					lockText = 'Lock'

				lockItem = contextMenu.addAction(lockText)
			passwordItem = contextMenu.addAction(passText)

		contextMenu.addSeparator()
		newFile = contextMenu.addAction('New Note')
		newFolder = contextMenu.addAction('New Folder')

		action = contextMenu.exec_(globalPos)

		if action == renameItem:
			self.rename()
		elif action == deleteItem:
			self.delete()
		elif action == newFile:
			self.newFile()
		elif action == newFolder:
			self.newFolder()
		elif action == fixItem:
			self.mainWidget.pinnedItem()
		elif action == passwordItem:
			self.setPassword()


	def rename(self):
		index = self.currentIndex()
		model = self.model()
		newText, result = QtWidgets.QInputDialog.getText(self, 'Rename File', 'New file name',
														 QtWidgets.QLineEdit.Normal)
		if result:
			model.setData(index, newText)


	def setPassword(self):
		index = self.currentIndex()
		password, result = QtWidgets.QInputDialog.getText(self, 'Set Password', 'Enter a password',
														  QtWidgets.QLineEdit.Password)
		if password and result and index.isValid():
			data = index.internalPointer()
			data.isLocked = True


	def delete(self):
		self.mainWidget.delete()


	def newFile(self):
		self.mainWidget.newFile()


	def newFolder(self):
		self.mainWidget.newFolder()
