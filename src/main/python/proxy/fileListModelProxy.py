import PySide2.QtCore as QtCore
from enums import FileType, ItemFlags
from itemmodel.listModelItem import MaskFolderItem


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
		return self.__recursiveSearch


	def setRecursiveSearch(self, res):
		if self.hasRecursiveSearch() != res:
			self.__recursiveSearch = res
			if self.searchText():
				self.setSearchText(self.searchText())


	def isEmpty(self):
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
		if folder is not None and folder.type == FileType.FOLDER:
			self.beginResetModel()
			maskFolder = MaskFolderItem(folder, folder.name(), None, folder.displayName, folder.isFixed)
			for child in folder.childItems:
				maskFolder.append(child)
			self.__currentFolder = maskFolder
			if self.searchText():
				self.setSearchText(self.searchText())
			else:
				self.__updateIndices()
			self.endResetModel()


	def mimeData(self, indices):
		mimeDat = super(FileListModelProxy, self).mimeData(indices)
		if indices:
			index = indices[0]
			perminentIndex = QtCore.QPersistentModelIndex(self.mapToSource(index))
			mimeDat.setColorData(perminentIndex)
		return mimeDat


	def dropMimeData(self, mimeData, action, row, column, parent):
		if parent.isValid() is False:
			sourceParent = self.sourceModel().getItemIndex(self.sourceFolder())
		else:
			sourceParent = self.mapToSource(parent)
		# print(sourceParent, 'proxy')
		# print(sourceParent, 'proxy')
		return self.sourceModel().dropMimeData(mimeData, action, row, column, sourceParent)


	# return super(FileListModelProxy, self).dropMimeData(mimeData, action, row, column, parent)

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


	# blockMedia = topLeft.data(QtCore.Qt.UserRole)
	# # update proxy model if top left index is the sequence index otherwise just emit data changed signal
	# if isinstance(blockMedia, SequenceBlockMedia):
	# 	oldCount = self.rowCount()
	# 	self.__updateIndices()
	# 	if self.rowCount() < oldCount:
	# 		self.__modelRemoved(QtCore.QModelIndex(), 0, self.rowCount())
	# 	elif self.rowCount() > oldCount:
	# 		self.__modelInserted(QtCore.QModelIndex(), 0, self.rowCount())
	# 	else:
	# 		proxyLeft = self.mapFromSource(topLeft)
	# 		proxyRight = self.mapFromSource(bottomRight)
	# 		self.dataChanged.emit(proxyLeft, proxyRight, roles)
	# else:
	# 	proxyLeft = self.mapFromSource(topLeft)
	# 	proxyRight = self.mapFromSource(bottomRight)
	# 	self.dataChanged.emit(proxyLeft, proxyRight, roles)

	def index(self, row, column = 0, parent = QtCore.QModelIndex()):
		if parent.isValid() is False:
			return self.createIndex(row, column, None)
		else:
			childItem = self.currentFolder().child(row)
			return self.createIndex(row, column, childItem)


	def setSearchText(self, searchText):
		self.beginResetModel()
		self.__searchText = searchText
		if searchText:
			maskFolder = MaskFolderItem(self.sourceFolder(), self.sourceFolder().name(), None)
			childItems = self.sourceFolder().find(lambda item: self.__searchItem(searchText, item),
												  recursive = self.hasRecursiveSearch())
			for child in childItems:
				maskFolder.append(child)
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


"""
import PySide2.QtCore as QtCore
from model.proxy.data import __Data__
from model.proxy.index import __Index__
from model.textBlockMedia import SequenceBlockMedia, ShotBlockMedia


class ShotSequenceProxyModel(QtCore.QAbstractProxyModel):
	# info: this is not used.
	def __init__(self, parent = None):
		super(ShotSequenceProxyModel, self).__init__(parent)
		self.sourceToProxy = {}
		self.proxyToSource = {}
		self.sequenceText = {}
		self.__updatedColumnIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

		self.__rootIndex = __Index__(QtCore.QModelIndex())
		self.sourceModelChanged.connect(self.__updateIndices)


	@property
	def undoCommandAdded(self):
		return self.sourceModel().undoCommandAdded


	def stopMerging(self):
		return self.sourceModel().stopMerging()


	def head(self, text):
		# return the head of sequence block media given text
		__data__ = self.sequenceText.get(text)
		if __data__ is not None:
			return __data__.head()
		else:
			return None


	def getBlockMediaWithIndex(self, blockIndex):
		return self.sourceModel().getBlockMediaWithIndex(blockIndex)


	def getIndexWithBlockIndex(self, blockIndex):
		index = self.sourceModel().getIndexWithBlockIndex(blockIndex)
		return self.mapFromSource(index)


	def getIndex(self, media):
		index = self.sourceModel().getIndex(media)
		return self.mapFromSource(index)


	def getBlockMedia(self, index):
		sourceIndex = self.mapToSource(index)
		return self.sourceModel().getBlockMedia(sourceIndex)


	def setData(self, index, func, role = QtCore.Qt.EditRole):
		sourceIndex = self.mapToSource(index)
		return self.sourceModel().setData(sourceIndex, func, role)


	def __updateIndices(self):
		self.proxyToSource.clear()
		self.sourceToProxy.clear()
		self.sequenceText.clear()
		self.__rootIndex = __Index__(QtCore.QModelIndex())
		self.__fillTheIndices(QtCore.QModelIndex())


	def __fillTheIndices(self, sourceParentIndex):
		for sourceRow in range(self.sourceModel().rowCount(sourceParentIndex)):
			sourceIndex = self.sourceModel().index(sourceRow, 0, sourceParentIndex)
			blockMedia = sourceIndex.data(QtCore.Qt.UserRole)
			self.__fillColumn(sourceRow, sourceRow, sourceParentIndex)
			if blockMedia.childCount() > 0:
				self.__fillTheIndices(sourceIndex)

			self.__updateName(sourceIndex.siblingAtColumn(2))


	def __fillColumn(self, sourceRow, proxyRow, sourceParentIndex):
		for column in self.__updatedColumnIndices:
			sourceIndex = self.sourceModel().index(sourceRow, column, sourceParentIndex)
			if sourceParentIndex.isValid() is False:
				data = None
			else:
				data = sourceParentIndex.data(QtCore.Qt.UserRole)

			proxyIndex = self.createIndex(proxyRow, column, data)
			# every source index has to have a proxy index

			self.sourceToProxy[sourceIndex] = proxyIndex
			# every proxy index has source index except for has same text sequence block media. just top sequence block media
			self.proxyToSource[proxyIndex] = sourceIndex


	def setSourceModel(self, model):
		model.modelReset.connect(self.__modelReset)
		model.rowsInserted.connect(self.__modelInserted)
		model.rowsRemoved.connect(self.__modelRemoved)
		model.dataChanged.connect(self.__dataChanged)
		super(ShotSequenceProxyModel, self).setSourceModel(model)


	def __modelReset(self):
		self.beginResetModel()
		self.__updateIndices()
		self.endResetModel()


	def __modelInserted(self, parent, first, last):
		# if parent.isValid():
		# 	proxyParent = self.mapFromSource(parent)
		# else:
		self.beginInsertRows(QtCore.QModelIndex(), 0, self.rowCount())
		self.__updateIndices()
		self.endInsertRows()


	def __modelRemoved(self, parent, first, last):
		# if parent.isValid():
		# 	pass
		# else:
		proxyParent = self.mapFromSource(parent)
		self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount(proxyParent))
		self.__updateIndices()
		self.endRemoveRows()


	def __dataChanged(self, topLeft, bottomRight, roles):
		blockMedia = topLeft.data(QtCore.Qt.UserRole)
		# update proxy model if top left index is the sequence index otherwise just emit data changed signal
		if isinstance(blockMedia, SequenceBlockMedia):
			oldCount = self.rowCount()
			self.__updateIndices()
			if self.rowCount() < oldCount:
				self.__modelRemoved(QtCore.QModelIndex(), 0, self.rowCount())
			elif self.rowCount() > oldCount:
				self.__modelInserted(QtCore.QModelIndex(), 0, self.rowCount())
			else:
				proxyLeft = self.mapFromSource(topLeft)
				proxyRight = self.mapFromSource(bottomRight)
				self.dataChanged.emit(proxyLeft, proxyRight, roles)
		else:
			proxyLeft = self.mapFromSource(topLeft)
			proxyRight = self.mapFromSource(bottomRight)
			self.dataChanged.emit(proxyLeft, proxyRight, roles)


	def __updateName(self, index):
		blockMedia = index.data(QtCore.Qt.UserRole)
		if isinstance(blockMedia, SequenceBlockMedia):
			text = index.data().lower()
			if text not in self.sequenceText:
				__data__ = __Data__(index.siblingAtColumn(1).data())
				self.sequenceText[text] = __data__
			else:
				__data__ = self.sequenceText[text]

			__data__.setSiblingData(blockMedia, len(__data__.siblings()) + 1)

			number = len(__data__.items()) + 1
			for child in blockMedia.children():
				if child.isChanged() is False:
					n = number
					s = ''
					number += 1
				else:
					n = child.number()
					s = child.suffix()

				__data__.setItem(child, (n, s))


	def mapToSource(self, proxyIndex):
		return self.proxyToSource.get(proxyIndex, QtCore.QModelIndex())


	def mapFromSource(self, sourceIndex):
		return self.sourceToProxy.get(sourceIndex, QtCore.QModelIndex())


	def columnCount(self, parent = QtCore.QModelIndex()):
		return self.sourceModel().columnCount(parent)


	def rowCount(self, parent = QtCore.QModelIndex()):
		sourceParentIndex = self.mapToSource(parent)
		return self.sourceModel().rowCount(sourceParentIndex)


	def parent(self, index = QtCore.QModelIndex()):
		if index.isValid() is False:
			return QtCore.QModelIndex()
		sourceParentBlockMedia = index.internalPointer()
		sourceParentIndex = self.sourceModel().getIndex(sourceParentBlockMedia)

		return self.mapFromSource(sourceParentIndex)


	def data(self, index, role = QtCore.Qt.DisplayRole):
		sourceIndex = self.mapToSource(index)
		if role == QtCore.Qt.DisplayRole:
			if index.column() == 1:
				blockMedia = index.data(QtCore.Qt.UserRole)
				if isinstance(blockMedia, SequenceBlockMedia):
					text = index.siblingAtColumn(2).data().lower()
					__index__ = self.sequenceText[text]
					return '%s (%s)' % (__index__.data(), __index__.siblings().get(blockMedia))
				else:
					return ShotBlockMedia.format(index.siblingAtColumn(7).data(), index.siblingAtColumn(8).data(),
												 index.siblingAtColumn(9).data())
			elif index.column() == 3:
				parentIndex = index.parent()
				if parentIndex.isValid() is True:
					shotMedia = index.data(QtCore.Qt.UserRole)
					if shotMedia.isChanged():
						return True
					# this is for shot
					text = parentIndex.siblingAtColumn(2).data().lower()
					__data__ = self.sequenceText[text]
					return __data__.head().isChanged()
				else:
					blockMedia = index.data(QtCore.Qt.UserRole)
					if isinstance(blockMedia, SequenceBlockMedia):
						text = index.siblingAtColumn(2).data().lower()
						__data__ = self.sequenceText[text]
						return __data__.head().isChanged()

			elif index.column() == 4:
				# this is for shot
				parentIndex = index.parent()
				if parentIndex.isValid() is True:
					text = parentIndex.siblingAtColumn(2).data().lower()
					__data__ = self.sequenceText[text]
					return __data__.head().isLocked()
				else:
					blockMedia = index.data(QtCore.Qt.UserRole)
					if isinstance(blockMedia, SequenceBlockMedia):
						text = index.siblingAtColumn(2).data().lower()
						__data__ = self.sequenceText[text]
						return __data__.head().isLocked()

			elif index.column() == 7:
				# this is for shot name
				parentIndex = index.parent()
				if parentIndex.isValid() is True:
					text = parentIndex.siblingAtColumn(2).data().lower()
					__data__ = self.sequenceText[text]
					return __data__.data()

			elif index.column() == 8:
				# this is for shot number
				blockMedia = index.data(QtCore.Qt.UserRole)
				parentIndex = index.parent()
				if parentIndex.isValid() is True:
					text = parentIndex.siblingAtColumn(2).data().lower()
					__data__ = self.sequenceText[text]
					if blockMedia.isChanged() is False:
						number, _ = __data__.items().get(blockMedia)
						return number
			elif index.column() == 9:
				# this is for shot suffix
				blockMedia = index.data(QtCore.Qt.UserRole)
				parentIndex = index.parent()
				if parentIndex.isValid() is True:
					text = parentIndex.siblingAtColumn(2).data().lower()
					__data__ = self.sequenceText[text]
					if blockMedia.isChanged() is False:
						_, suffix = __data__.items().get(blockMedia)
						return suffix

		elif role == QtCore.Qt.ForegroundRole:
			return self.sourceModel().color(index)

		return self.sourceModel().data(sourceIndex, role)


	def index(self, row, column, parent = QtCore.QModelIndex()):
		if parent.isValid() is False:
			return self.createIndex(row, column, None)
		else:
			return self.createIndex(row, column, self.mapToSource(parent).internalPointer())


	def headerData(self, section, orientation, role):
		return self.sourceModel().headerData(section, orientation, role)


"""
