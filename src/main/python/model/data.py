import datetime
import os
import PySide2.QtGui as QtGui

from enums import DataType


class Data(object):
	def __init__(self, name, createDate = None):
		self.name = name
		self.createDate = createDate if createDate is not None else datetime.datetime.now()
		self.__type = DataType.DATA


	def type(self):
		return self.__type


	def setType(self, type):
		self.__type = type


	def setName(self, name):
		self.name = name


	def toArray(self):
		return [self.type(), self.name, self.createDate]


	def dict(self):
		return {'type': self.type(), 'name': self.name, 'createDate': self.createDate.timestamp()}


	def id(self):
		return self.name


	def __eq__(self, other):
		try:
			if other.id() == self.id():
				return True
			else:
				return False
		except:
			return False


	def __str__(self):
		return f'Data({self.name})'


class FileData(Data):
	def __init__(self, name, path, createDate = None):
		super(FileData, self).__init__(name, createDate)
		self.path = path
		self.__type = DataType.FILEDATA


	def dict(self):
		dict_ = super(FileData, self).dict()
		dict_['path'] = self.path
		return dict_


	def id(self):
		return self.path


	def filename(self):
		return os.path.basename(self.path)


	def toArray(self):
		arr = super(FileData, self).toArray()
		arr.append(self.path)
		return arr


	def __str__(self):
		return f'FileData({self.name}, {self.path}, {self.__type})'


class ImageFileData(FileData):
	def __init__(self, name, path, createDate = None):
		super(ImageFileData, self).__init__(name, path, createDate)
		self.setType(DataType.IMAGEFILEDATA)


	def pixmap(self):
		imageReader = QtGui.QImageReader(self.path)
		imageReader.setAutoTransform(True)
		return QtGui.QPixmap.fromImage(imageReader.read())


	def __str__(self):
		return f'ImageFileData({self.name}, {self.path})'
