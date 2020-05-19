import datetime
import json
import logging as log
import os

from enums import DataType, FileType
from factory.dataFactory import DataFactory
from model.data import ImageFileData, FileData


class __DataListModelFolderItemService__(object):
	def __init__(self):
		self.path = None


	def setPath(self, path):
		self.path = path


	def save(self, listModelFileItem):
		if self.path is not None:
			dict_ = list(map(lambda data: data.dict(), listModelFileItem.dataList()))
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			with open(filename, 'w') as file:
				jsonInString = json.dumps(dict_)
				file.write(jsonInString)
		else:
			log.warning('Path is not valid while saving in SaveListModelFolderItemService')


	def load(self, listModelFileItem):
		if listModelFileItem.type == FileType.FOLDER:
			return
		if self.path is not None:
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			if listModelFileItem.isRead() is False:
				with open(filename, 'r') as file:
					jsonInString = file.read()
					if jsonInString:
						try:
							dataListInDict = json.loads(jsonInString)
							for dictData in dataListInDict:
								data = DataFactory.fileDataFromJson(dictData)
								if data is not None:
									listModelFileItem.appendData(data)
							listModelFileItem.setRead(True)
						except Exception as e:
							log.error(f'Data list is not loaded successfully in file {filename}. Exception is {e}')

		else:
			log.warning('Path is not valid while loading in SaveListModelFolderItemService')
			return None


	def dataCreator(self, dictData):
		if dictData['type'] == DataType.STYLEDATA:
			data = FileData(dictData['name'], dictData['path'],
							datetime.datetime.fromtimestamp(dictData.get('createDate')))
			data.setType(DataType.STYLEDATA)
		elif dictData['type'] == DataType.IMAGEFILEDATA:
			data = ImageFileData(dictData['name'], dictData['path'],
								 datetime.datetime.fromtimestamp(dictData.get('createDate')))
		else:
			data = None
		return data


	def deleteListModelFileItem(self, listModelFileItem):
		if self.path is not None:
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			os.remove(filename)
			for data in listModelFileItem.dataList():
				self.deleteDataModelItem(data)


	def deleteDataModelItem(self, dataModelItem):
		filename = dataModelItem.path
		os.remove(filename)


__service__ = __DataListModelFolderItemService__()


class DataListModelFolderItemService(object):
	def dataListModelService(self):
		return __service__
