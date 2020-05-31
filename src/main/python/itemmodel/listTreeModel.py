import core
import static
from PySide2 import QtCore, QtGui

from enums import FileType, ItemFlags
from exceptions.invalidListModelItemException import InvalidListModelItemException
from itemmodel.listModelItem import ListModelFileItem, ListModelFolderItem


class ListTreeModel(QtCore.QAbstractItemModel):
	def __init__(self, parent = None):
		super(ListTreeModel, self).__init__(parent)
		self.rootFolderItem = None
		self.headerList = ['ID', 'Name', 'Display Name', 'Is Fixed', 'Create Date', 'Is Locked', 'Type', 'Child Count',
						   'Update Date', 'Child Number', 'Tags']


	def rootFolder(self):
		return self.rootFolderItem


	def moveRow(self, sourceParent, sourceRow, destinationParent, destinationChild):
		if sourceParent == destinationParent and sourceRow == destinationChild:
			return False
		destinationChild = self.__toValidIndex(destinationChild, destinationChild)
		self.beginMoveRows(sourceParent, sourceRow, sourceRow + 1, destinationParent, destinationChild)
		sourceFolder = self.getFileItem(sourceParent)
		destinationParentItem = self.getFileItem(destinationParent)
		item = sourceFolder.pop(sourceRow)
		item.updateLastUpdateDate()
		destinationParentItem.insert(item, destinationChild)
		self.endMoveRows()
		return True


	def find(self, func):
		# find object with given function
		items = self.rootFolder().find(func, recursive = True)
		if func(self.rootFolder()):
			items.append(self.rootFolder())
		return items


	def setRoot(self, root):
		if isinstance(root, ListModelFileItem) is False:
			raise InvalidListModelItemException('Invalid object in setRoot of tree model')
		self.beginResetModel()
		self.rootFolderItem = root
		self.endResetModel()


	def flags(self, index):
		listModelFileItem = self.getFileItem(index)
		if isinstance(listModelFileItem, ListModelFolderItem):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDropEnabled |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)
		elif listModelFileItem.isFixed is True and isinstance(listModelFileItem, ListModelFileItem):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
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
		# get file item with given index
		oldData = self.getFileItem(index)
		# copy of data
		if oldData.type == FileType.FOLDER:
			copy = ListModelFolderItem(oldData.id(), oldData.name(), oldData.parent(), oldData.displayName,
									   oldData.isFixed)
		else:
			copy = ListModelFileItem(oldData.id(), oldData.name(), oldData.parent(), oldData.isFixed,
									 oldData.lastUpdate, oldData.displayName, oldData.isLocked, oldData.createDate)
		return oldData, copy


	def endEditData(self, index):
		# get object with given index
		item = self.getFileItem(index)
		# update last update date
		item.updateLastUpdateDate()
		self.dataChanged.emit(index, index)


	def getItemIndex(self, fileItem):
		item = fileItem
		# find the root of the file item
		while item.parent() is not None:
			item = item.parent()
		# item should be in rootFolderItem
		if item != self.rootFolderItem:
			return QtCore.QModelIndex()
		else:
			childNumber = fileItem.childNumber()
			if childNumber is not None:
				return self.createIndex(childNumber, 0, fileItem)
			else:
				return QtCore.QModelIndex()


	def rowCount(self, parent = QtCore.QModelIndex()):
		parentItem = self.getFileItem(parent)
		if parentItem is not None:
			return parentItem.childCount()
		else:
			return 0


	def insertData(self, listModelFileItem, index = None, parent = QtCore.QModelIndex()):

		if isinstance(listModelFileItem, ListModelFileItem) is False:
			raise InvalidListModelItemException(f'Data should be ListModelFileItem to insert data to the tree model ')
		if index is None:
			index = self.rowCount()

		parentFolder = self.getFileItem(parent)
		item = static.first_(parentFolder.childItems, lambda child: child.id() == listModelFileItem.id())
		if item is not None:
			raise InvalidListModelItemException(
					f'Data "({listModelFileItem.id()}, {listModelFileItem.name}) " can not insert to model. Because it already exists in the model')
		self.beginInsertRows(parent, index, index)
		checkedIndex = self.__toValidIndex(index, index, parent)
		parentFolder.insert(listModelFileItem, checkedIndex)
		parentFolder.updateLastUpdateDate()
		listModelFileItem.setParent(parentFolder)
		self.endInsertRows()
		return checkedIndex


	def index(self, row, column, parent = QtCore.QModelIndex()):
		parentItem = self.getFileItem(parent)
		if row < parentItem.childCount():
			childItem = parentItem.child(row)
			return self.createIndex(row, column, childItem)
		else:
			return QtCore.QModelIndex()


	def parent(self, index = QtCore.QModelIndex()):
		if index.isValid() is False:
			return QtCore.QModelIndex()
		else:
			childItem = self.getFileItem(index)
			parentItem = childItem.parent()
			childNumber = parentItem.childNumber()
			if childNumber is not None:
				return self.createIndex(childNumber, index.column(), parentItem)
			else:
				return QtCore.QModelIndex()


	def mimeData(self, indices):
		mimeDat = super(ListTreeModel, self).mimeData(indices)
		if indices:
			index = indices[0]
			# index data in set as color data
			mimeDat.setColorData(index)
		return mimeDat


	def dropMimeData(self, mimeData, action, row, column, parent):
		dropIndex = mimeData.colorData()
		if dropIndex is not None and dropIndex.isValid():
			dropParent = self.getFileItem(parent)
			dropFileList = dropIndex.data(QtCore.Qt.UserRole)
			beforeParentObject = dropFileList.parent()
			row = self.rowCount(parent) if row == -1 else row

			index = dropFileList.childNumber()
			# if drop object is dropped to the same place return False
			if dropParent == beforeParentObject and (index == row or index + 1 == row):
				return False
			# move data
			index = dropFileList.childNumber()
			self.beginMoveRows(dropIndex.parent(), index, index, parent, row)
			beforeParentObject.remove(dropFileList)
			dropParent.insert(dropFileList, row)
			dropFileList.setParent(dropParent)
			self.endMoveRows()
			return True
		else:
			return False


	def columnCount(self, parent = QtCore.QModelIndex()):
		return 1


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		item = self.getFileItem(index)
		if role == QtCore.Qt.DisplayRole:
			if item.type == FileType.FOLDER:
				count = item.childCount()
			else:
				count = 0
			data = [item.id(), item.name(), item.displayName, item.isFixed, item.lastUpdate, item.isLocked, item.type,
					count, item.createDate, item.tags]
			return data
		elif role == QtCore.Qt.EditRole:
			return item.displayName
		elif role == QtCore.Qt.UserRole:
			return item
		elif role == QtCore.Qt.DecorationRole:
			if item.type == FileType.FOLDER:
				return QtGui.QIcon(core.fbs.icons('folder.png'))
			else:
				return QtGui.QIcon(core.fbs.icons('baseline_bookmark_white_48dp.png'))
		elif role == QtCore.Qt.ToolTipRole:
			return item.displayName


	def getFileItem(self, index):
		# get item of given index
		if index.isValid() is False:
			return self.rootFolderItem
		else:
			return index.internalPointer()


	def deleteRow(self, index):
		parentItem = self.getFileItem(index.parent())
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		item = parentItem.pop(index.row())
		parentItem.updateLastUpdateDate()
		self.endRemoveRows()
		return item


	def __toValidIndex(self, from_, to, parent = QtCore.QModelIndex()):
		# return a valid index of given index
		# find first index in that element is not fixed
		parentItem = self.getFileItem(parent)
		if from_ < 0 or to >= self.rowCount(parent):
			return to
		isNotValid = True
		item = parentItem.child(to)
		while item and isNotValid:
			item = parentItem.child(to)
			if item.isFixed:
				to += 1
			else:
				isNotValid = False
			if from_ == to:
				return to
		return to
