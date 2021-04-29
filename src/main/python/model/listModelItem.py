import datetime
import os

from enums import FileType

listModelID = 0


class ListModelFileItem(object):
	def __init__(self, id, name, parent, isFixed = False, lastUpdate = None, displayName = None, isLocked = False,
				 createDate = None):
		self.isFixed = isFixed
		self.__id = id
		self.__name = name
		self.displayName = displayName if displayName else name
		self.type = FileType.FILE
		self.lastUpdate = lastUpdate if lastUpdate is not None else datetime.datetime.now()
		self.createDate = createDate if createDate is not None else datetime.datetime.now()
		self.isLocked = isLocked
		self.__dataList = []
		self.__isRead = False
		self.__parent = parent
		self.tags = set()


	def updateLastUpdateDate(self):
		self.lastUpdate = datetime.datetime.now()


	def setTags(self, tags):
		self.tags = tags


	def childCount(self):
		return 0


	def isRead(self):
		return self.__isRead


	def childNumber(self):
		if self.parent() is not None:
			return self.parent().childItems.index(self)
		else:
			return None


	def setRead(self, res):
		self.__isRead = res


	def dataList(self):
		return self.__dataList.copy()


	def data(self, index):
		return self.__dataList[index]


	def dataCount(self):
		return len(self.__dataList)


	def text(self):
		return self.name()


	@classmethod
	def IDGenerator(cls):
		global listModelID
		id = listModelID
		listModelID += 1
		return id


	@classmethod
	def setListID(cls, id):
		global listModelID
		listModelID = id


	def appendData(self, item):
		self.__dataList.insert(0, item)


	def popData(self, row):
		return self.__dataList.pop(row)


	def name(self):
		return self.__name


	def setName(self, name):
		self.__name = name


	def setDisplayName(self, displayName):
		self.displayName = displayName


	def setParent(self, parent):
		self.__parent = parent


	def parent(self):
		return self.__parent


	def path(self):
		if self.parent() is None:
			return self.name()
		return os.path.join(self.parent().path(), os.path.basename(self.name()))


	def __str__(self):
		return f'ListModelFileItem({self.id()}, {self.name()}, {self.type})'


	def id(self):
		return self.__id


	def __eq__(self, other):
		if other is None:
			return False
		return self.id() == other.id()


	def setFixed(self, result):
		self.isFixed = result


	def __repr__(self):
		return self.__str__()


	def dict(self):
		return {'id': self.id(), 'parentID': self.parent().id() if self.parent() is not None else None,
				'name': self.name(), 'type': self.type,
				'lastUpdate': self.lastUpdate.timestamp(),
				'createDate': self.createDate.timestamp(),
				'tags': ';'.join(self.tags),
				'displayName': self.displayName, 'isFixed': self.isFixed, 'isLocked': self.isLocked}


class ListModelFolderItem(ListModelFileItem):
	def __init__(self, id, name, parent, displayName = None, isFixed = False):
		super(ListModelFolderItem, self).__init__(id, name, parent, isFixed = isFixed, displayName = displayName)
		self.childItems = []
		self.type = FileType.FOLDER


	def find(self, func, recursive = False):
		items = []
		if recursive is False:
			for child in self.childItems:
				if func(child) is True:
					items.append(child)
		else:
			self.__find(self, func, items)
		return items


	def __find(self, folder, func, all):
		folderItems = []
		for childItem in folder.childItems:
			if childItem.type == FileType.FOLDER:
				folderItems.append(childItem)
			if func(childItem) is True:
				all.append(childItem)
		for folderItem in folderItems:
			self.__find(folderItem, func, all)

		return all


	def contains(self, func, recursive = False):
		if recursive is False:
			for child in self.childItems:
				if func(child):
					return True
			return False
		else:
			return self.__contains(self, func)


	def __contains(self, folder, func):
		folderItems = []
		for childItem in folder.childItems:
			if childItem.type == FileType.FOLDER:
				folderItems.append(childItem)
			else:
				if func(childItem):
					return True
		for folderItem in folderItems:
			res = self.__contains(folderItem, func)
			if res is True:
				return True
		return False


	def insert(self, child, index):
		self.childItems.insert(index, child)


	def append(self, child):
		self.childItems.append(child)


	def pop(self, index):
		return self.childItems.pop(index)


	def remove(self, child):
		self.childItems.remove(child)


	def childCount(self):
		return len(self.childItems)


	def isEmpty(self):
		return self.childCount() <= 0


	def child(self, row):
		return self.childItems[row]


	def dict(self):
		return {'id': self.id(), 'parentID': self.parent().id() if self.parent() is not None else None,
				'name': self.name(), 'type': self.type,
				'displayName': self.displayName, 'isFixed': self.isFixed,
				'children': list(map(lambda item: item.dict(), self.childItems))}


	def toSoftLink(self, displayName):
		softLink = ListModelSoftLinkFolderItem(self.id(), self.name(), self.parent(), displayName, self.isFixed)
		softLink.childItems = self.childItems
		return softLink


	def __str__(self):
		return f'FileListModelFolderItem({self.name()})'


class ListModelSoftLinkFolderItem(ListModelFolderItem):
	def __init__(self, id, name, parent, displayName = None, isFixed = False):
		super(ListModelSoftLinkFolderItem, self).__init__(id, name, parent, displayName, isFixed)


class MaskFolderItem(ListModelFolderItem):
	def __init__(self, source, name, parent, displayName = None, isFixed = False):
		super(MaskFolderItem, self).__init__(source.id(), name, parent, displayName = displayName, isFixed = isFixed)
		self.__source = source


	def sourceFolder(self):
		return self.__source
