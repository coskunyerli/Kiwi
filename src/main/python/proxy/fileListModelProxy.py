import PySide2.QtCore as QtCore
from enums import FileType, ItemFlags
from model.listModelItem import MaskFolderItem


class FileListModelProxy(QtCore.QAbstractProxyModel):
	def __init__(self, parent = None):
		super(FileListModelProxy, self).__init__(parent)
		self.__currentFolder = None
		self.__maskFolder = None
		self.__searchText = ''
		self.__recursiveSearch = False
		# mapping list
		self.__disableUpdate = False
		self.sourceToProxy = {}
		self.proxyToSource = {}


	def flags(self, index):
		hoverIndex = index
		sourceIndex = self.mapToSource(hoverIndex)
		fileItemList = self.sourceModel().getFileItem(sourceIndex)
		# if fileItemList item is equal to source folder or in its child, drop is not enabled
		if index.isValid() is True and fileItemList.type == FileType.FOLDER and (
				self.sourceFolder() == fileItemList or fileItemList.contains(lambda item: item == self.sourceFolder(),
																			 recursive = True)):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)
		else:
			return super(FileListModelProxy, self).flags(index)


	def searchText(self):
		return self.__searchText


	def hasRecursiveSearch(self):
		# check that has recursive search or not
		return self.__recursiveSearch


	def setRecursiveSearch(self, res):
		# update recursive search flag and update search
		if self.hasRecursiveSearch() != res:
			self.__recursiveSearch = res
			if self.searchText():
				self.setSearchText(self.searchText())


	def isEmpty(self):
		# check that current folder is empty or not
		if self.currentFolder() is not None:
			return self.currentFolder().isEmpty()
		else:
			return True

	def beginEditData(self, index):
		sourceIndex = self.mapToSource(index)
		return self.sourceModel().beginEditData(sourceIndex)


	def endEditData(self, index):
		sourceIndex = self.mapToSource(index)
		self.sourceModel().endEditData(sourceIndex)


	def setCurrentFolder(self, folder):
		# update current folder and update layout
		# all folder is wrapped in nask folder
		if folder is not None and folder.type == FileType.FOLDER:
			maskFolder = MaskFolderItem(folder, folder.name(), None, folder.displayName, folder.isFixed)
			for child in folder.childItems:
				maskFolder.append(child)
			self.__currentFolder = maskFolder
			if self.searchText():
				self.setSearchText(self.searchText())
			else:
				self.__updateIndices()
			self.layoutChanged.emit()


	def mimeData(self, indices):
		mimeDat = super(FileListModelProxy, self).mimeData(indices)
		if indices:
			index = indices[0]
			perminentIndex = QtCore.QPersistentModelIndex(self.mapToSource(index))
			mimeDat.setColorData(perminentIndex)
		return mimeDat


	def dropMimeData(self, mimeData, action, row, column, parent):
		# if parent is not valid set parentIndex as index of sourceFolder
		if parent.isValid() is False:
			sourceParent = self.sourceModel().getItemIndex(self.sourceFolder())
		else:
			sourceParent = self.mapToSource(parent)
		return self.sourceModel().dropMimeData(mimeData, action, row, column, sourceParent)

	def sourceFolder(self):
		return self.currentFolder().sourceFolder()


	def rowCount(self, parent = QtCore.QModelIndex()):
		if self.currentFolder() is not None:
			return self.currentFolder().childCount()
		else:
			return 0


	def columnCount(self, parent = QtCore.QModelIndex()):
		return self.sourceModel().columnCount(parent)


	def mapToSource(self, proxyIndex):
		return self.proxyToSource.get(proxyIndex, QtCore.QModelIndex())


	def mapFromSource(self, sourceIndex):
		return self.sourceToProxy.get(sourceIndex, QtCore.QModelIndex())


	def parent(self, index = QtCore.QModelIndex()):
		return QtCore.QModelIndex()


	def setSourceModel(self, model):
		model.modelReset.connect(self.__modelReset)
		model.rowsInserted.connect(self.__modelInserted)
		model.rowsRemoved.connect(self.__modelRemoved)
		model.dataChanged.connect(self.__dataChanged)
		model.rowsMoved.connect(self.__modelMoved)
		super(FileListModelProxy, self).setSourceModel(model)
		self.setCurrentFolder(self.sourceModel().rootFolder())


	def __modelReset(self):
		self.beginResetModel()
		self.__updateIndices()
		self.endResetModel()


	def __modelInserted(self, parent, first, last):
		self.setCurrentFolder(self.sourceFolder())


	def __modelRemoved(self, parent, first, last):
		self.setCurrentFolder(self.sourceFolder())


	def __modelMoved(self, parent, start, end, destination, index):
		# if self.sourceModel().getFileItem(destination) != self.sourceFolder():
		# 	return

		self.setCurrentFolder(self.sourceFolder())


	def __dataChanged(self, topLeft, bottomRight, role):
		self.__updateIndices()
		self.dataChanged.emit(topLeft, bottomRight, role)

	def index(self, row, column = 0, parent = QtCore.QModelIndex()):
		if parent.isValid() is False:
			return self.createIndex(row, column, None)
		else:
			childItem = self.currentFolder().child(row)
			return self.createIndex(row, column, childItem)


	def setSearchText(self, searchText):
		# update search text
		self.beginResetModel()
		self.__searchText = searchText
		if searchText:
			# create mask folder, file contains searchText
			maskFolder = MaskFolderItem(self.sourceFolder(), self.sourceFolder().name(), None)
			childItems = self.sourceFolder().find(lambda item: self.__searchItem(searchText, item),
												  recursive = self.hasRecursiveSearch())
			for child in childItems:
				maskFolder.append(child)
			# update indices
			self.__currentFolder = maskFolder
			self.__updateIndices()
		else:
			self.setCurrentFolder(self.sourceFolder())
		self.endResetModel()


	def data(self, index, role = QtCore.Qt.UserRole):
		if self.searchText() and self.hasRecursiveSearch() is True and (
				role == QtCore.Qt.WhatsThisRole or role == QtCore.Qt.ToolTipRole):
			item = index.data(QtCore.Qt.UserRole)
			return item.path()
		else:
			return super(FileListModelProxy, self).data(index, role)


	def __searchItem(self, searchText, item):
		return item.type == FileType.FILE and (
				searchText.lower() in item.name().lower() or self.__searchTag(searchText, item.tags))


	def __searchTag(self, searchText, tags):
		searchedTags = searchText.split(';')
		for tag in searchedTags:
			return tag in tags


	def currentFolder(self):
		return self.__currentFolder


	def deleteRow(self, index):
		sourceIndex = self.mapToSource(index)
		return self.sourceModel().deleteRow(sourceIndex)


	def insertData(self, newFile, index = None):
		parentSourceIndex = self.sourceModel().getItemIndex(self.sourceFolder())
		return self.sourceModel().insertData(newFile, index, parentSourceIndex)


	def moveItem(self, from_, to):
		pass


	def __updateIndices(self):
		self.proxyToSource.clear()
		self.sourceToProxy.clear()
		self.__fillTheIndices()


	def __fillTheIndices(self):
		for proxyRow in range(self.currentFolder().childCount()):
			# get child item in current folder
			childItem = self.currentFolder().child(proxyRow)
			# get source index of child item
			sourceIndex = self.sourceModel().getItemIndex(childItem)
			if sourceIndex.isValid() is True:
				sourceParentIndex = self.sourceModel().parent(sourceIndex)
				sourceChildNumber = childItem.childNumber()
				self.__fillColumn(sourceChildNumber, proxyRow, sourceParentIndex)


	def __fillColumn(self, sourceRow, proxyRow, sourceParentIndex):
		for column in range(self.columnCount()):
			sourceIndex = self.sourceModel().index(sourceRow, column, sourceParentIndex)

			proxyIndex = self.createIndex(proxyRow, column, None)
			# every source index has to have a proxy index

			self.sourceToProxy[sourceIndex] = proxyIndex
			# every proxy index has source index except for has same text sequence block media. just top sequence block media
			self.proxyToSource[proxyIndex] = sourceIndex
