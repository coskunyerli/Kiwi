import core
import static
from PySide2 import QtCore, QtGui

from enums import ItemFlags, FileType
from exceptions.invalidListModelItemException import InvalidListModelItemException
from itemmodel.listModelItem import ListModelFileItem, ListModelFolderItem


class ListModel(QtCore.QAbstractListModel):

	def __init__(self, parent = None):
		super(ListModel, self).__init__(parent)
		self.__fileLisModelFolderItem = None
		self.headerList = ['ID', 'Name', 'Display Name', 'Is Fixed', 'Last Update', 'Is Locked', 'Type', 'Child Count',
						   'Tags']


	def currentFolder(self):
		return self.__fileLisModelFolderItem


	def flags(self, index):
		if index.isValid() is False:
			return QtCore.Qt.ItemIsDropEnabled
		listModelFileItem = self.currentFolder().child(index.row())
		if isinstance(listModelFileItem, ListModelFolderItem):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDropEnabled |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)
		elif isinstance(listModelFileItem, ListModelFileItem):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)


	def beginEditData(self, index):
		oldData = self.currentFolder().child(index.row())
		if oldData.type == FileType.FOLDER:
			copy = ListModelFolderItem(oldData.id(), oldData.name(), oldData.parent(), oldData.displayName,
									   oldData.isFixed)
		else:
			copy = ListModelFileItem(oldData.id(), oldData.name(), oldData.parent(), oldData.isFixed,
									 oldData.lastUpdate, oldData.displayName, oldData.isLocked, oldData.createDate)
		return oldData, copy


	def endEditData(self, index):
		self.dataChanged.emit(index, index)


	def childItemCount(self, index):
		item = index.data(QtCore.Qt.UserRole)
		return item.childCount()


	def mimeData(self, indices):
		mimeDat = super(ListModel, self).mimeData(indices)
		fileListItem = list(map(lambda index: index.data(QtCore.Qt.UserRole), indices))
		mimeDat.setColorData(fileListItem[0] if fileListItem else None)
		return mimeDat


	#
	def dropMimeData(self, mimeData, action, row, column, parent):
		dropObject = mimeData.colorData()
		if dropObject:
			beforeParentObject = dropObject.parent()
			if parent.isValid() and beforeParentObject == self.currentFolder():
				newParentObject = parent.data(QtCore.Qt.UserRole)
				row = self.rowCount()
				index = dropObject.childNumber()
				self.beginRemoveRows(QtCore.QModelIndex(), index, index)
				self.currentFolder().remove(dropObject)
				newParentObject.insert(dropObject, row)
				self.endRemoveRows()

			# move operation
			elif beforeParentObject == self.currentFolder():
				if beforeParentObject.contains(dropObject) is True:
					index = dropObject.childNumber()
					if index == row or index + 1 == row:
						return False
					self.beginMoveRows(QtCore.QModelIndex(), index, index, QtCore.QModelIndex(), row)
					beforeParentObject.insert(dropObject, row)
					beforeParentObject.pop(index)
					self.endMoveRows()
					return True
				else:
					return False
			else:
				if beforeParentObject.contains(dropObject) is True:
					row = row if row > -1 else self.rowCount()
					self.beginInsertRows(QtCore.QModelIndex(), row, row)
					beforeParentObject.remove(dropObject)
					self.currentFolder().insert(dropObject, row)
					self.endInsertRows()
				else:
					return False
			return True
		else:
			return False


	# 	if len(dropObject) > 0:
	# 		folder = self.fileList[parent.row()]
	# 		data = self.fileList[dropObject[0]]
	# 		if folder.filename == data.filename:
	# 			return False
	# 		self.deleteData(data.filename)
	# 		folder.fileListModel.insertData(data)
	# 		oldFilename = data.filename
	# 		_, filename = os.path.split(oldFilename)
	# 		newFileName = ''
	# 		if data.type == FileType.FILE:
	# 			newFileName = folder.generateFileName()
	# 		elif data.type == FileType.FOLDER:
	# 			newFileName = folder.generateFolderName()
	# 			data.setParent(folder)
	# 		os.rename(oldFilename, newFileName)
	# 		data.filename = newFileName
	# 		self.dataUpdated.emit(data, data, folder.fileListModel.rowCount())
	# 		return True
	# 	return False

	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			if role == QtCore.Qt.UserRole:
				return self.currentFolder()
			else:
				return None
		item = self.currentFolder().child(index.row())
		if role == QtCore.Qt.DisplayRole:
			if item.type == FileType.FOLDER:
				count = self.childItemCount(index)
			else:
				count = 0
			return [item.id(), item.name(), item.displayName, item.isFixed, item.lastUpdate, item.isLocked, item.type,
					count, item.tags]
		elif role == QtCore.Qt.EditRole:
			return item.displayName
		elif role == QtCore.Qt.UserRole:
			return item
		elif role == QtCore.Qt.DecorationRole:
			data = self.currentFolder().child(index.row())
			if data.type == FileType.FOLDER:
				return QtGui.QIcon(core.fbs.icons('folder.png'))
			else:
				return QtGui.QIcon(core.fbs.icons('baseline_bookmark_white_48dp.png'))
		elif role == QtCore.Qt.ToolTipRole:
			return item.displayName


	def setData(self, index, item, role = QtCore.Qt.EditRole):
		if index.row() >= self.rowCount() or index.row() < 0 or item is None:
			return False
		if index.isValid() and role == QtCore.Qt.EditRole:
			row = index.row()
			oldModelItem = self.currentFolder().child(row)
			newModelItem = item
			if isinstance(newModelItem, str):
				if newModelItem.strip() == '' or newModelItem == oldModelItem.name():
					return False
				oldModelItem.setName(newModelItem)
				oldModelItem.setDisplayName(newModelItem)
				newModelItem = oldModelItem
			self.currentFolder().childItems[row] = newModelItem
			self.dataChanged.emit(index, index)
			return True
		return False


	# def setClickFunction(self, function):
	# 	self.clickFunction = function

	def isEmpty(self):
		if self.currentFolder() is not None:
			return self.currentFolder().isEmpty()
		else:
			return True


	# def hasClickFunction(self):
	# 	return False if self.clickFunction is None else True

	#
	# def deleteRow(self, filename):
	# 	index = self.getIndex(filename)
	# 	data = self.getItem(index)
	# 	return self.deleteItem(data)
	#
	#
	# def deleteItem(self, data):
	# 	index = self.getList().index(data)
	# 	if index != -1:
	# 		self.beginRemoveRows(QtCore.QModelIndex(), index, index)
	# 		self.fileList.pop(index)
	# 		self.allFileList.remove(data)
	# 		self.endRemoveRows()
	# 		return data
	# 	return None

	def rowCount(self, parent = QtCore.QModelIndex()):
		if self.currentFolder() is not None:
			return self.currentFolder().childCount()
		else:
			return 0


	def columnCount(self, parent = QtCore.QModelIndex()):
		return len(self.headerList)


	def rootFolder(self):
		item = self.currentFolder()
		while item.parent() is not None:
			item = item.parent()

		return item


	def insertData(self, listModelFileItem, index = None):
		if listModelFileItem is None:
			return False
		if index is None:
			index = self.rowCount()
		item = static.first_(self.currentFolder().childItems, lambda child: child.id() == listModelFileItem.id())
		if item is not None:
			raise InvalidListModelItemException(
					f'Data "({listModelFileItem.id()}, {listModelFileItem.name}) " can not insert to model. Because it already exists in the model')
		self.beginInsertRows(QtCore.QModelIndex(), index, index)
		checkedIndex = self.__checkFile(index, index)
		self.currentFolder().insert(listModelFileItem, checkedIndex)
		listModelFileItem.setParent(self.currentFolder())
		self.endInsertRows()
		return checkedIndex


	def deleteRow(self, index):
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		item = self.currentFolder().pop(index.row())
		self.endRemoveRows()
		return item


	def deleteData(self, filename):
		if filename:
			return self.deleteRow(filename)
		else:
			return None


	# def getList(self):
	# 	return self.fileList

	# def search(self, title):
	# 	self.searchTitle = title
	# 	self.beginResetModel()
	# 	self.fileList = list(filter(lambda item: title.lower() in item.title.lower(), self.allFileList))
	# 	self.endResetModel()
	#
	#
	# def setFileList(self, fileList):
	# 	self.beginResetModel()
	# 	self.allFileList = fileList
	# 	self.fileList = copy.copy(self.allFileList)
	# 	self.endResetModel()

	#
	# def getItem(self, index):
	# 	try:
	# 		return self.fileList[index]
	# 	except:
	# 		return None
	#
	#
	# def getIndex(self, filename):
	# 	for i in range(len(self.fileList)):
	# 		item = self.fileList[i]
	# 		if item.filename == filename:
	# 			return i
	# 	return -1
	#
	#
	def moveItem(self, fromItem, to):
		if fromItem == to:
			return
		to = self.__checkFile(fromItem, to)
		if fromItem != to:
			self.beginMoveRows(QtCore.QModelIndex(), fromItem, fromItem, QtCore.QModelIndex(), to)
			item = self.currentFolder().pop(fromItem)
			self.currentFolder().insert(item, to)
			self.endMoveRows()


	#
	#
	def __checkFile(self, from_, to):
		"""
		:param from_: from index
		:param to:  to index
		:return: find to first not fixed index between from_ and to return that index
		"""
		if from_ < 0 or to >= self.rowCount():
			return to
		isNotValid = True
		item = self.currentFolder().child(to)
		while item and isNotValid:
			item = self.currentFolder().child(to)
			if item.isFixed:
				to += 1
			else:
				isNotValid = False
			if from_ == to:
				return to
		return to


	#
	# def stringList(self):
	# 	return list(map(lambda m: m.title, self.fileList))

	def setCurrentFolder(self, folder):
		self.beginResetModel()
		self.__fileLisModelFolderItem = folder
		self.endResetModel()

# def json(self):
# 	fileList = filter(lambda item: item.displayName != '..', self.allFileList)
# 	json = list(map(lambda data: data.json(), fileList))
# 	return json

# def generateFileName(self):
# 	# allTextFilesNumber = len( filter( lambda item: item.type == FileType.FILE, self.allFileList ) )
# 	filename = 'file%s.txt' % ''.join(
# 			random.choice(string.ascii_letters + string.digits) for _ in range(21))
# 	return filename
#
#
# def generateFolderName(self):
# 	# allFolderNumber = len( filter( lambda item: item.type == FileType.FOLDER, self.allFileList ) )
# 	folder = 'folder%s' % ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(21))
# 	return folder
