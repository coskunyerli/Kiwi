import json
import logging as log
import os

from enums import FileType
from factory.dataFactory import DataFactory


class __DataListModelFolderItemService__(object):
	def __init__(self):
		self.path = None


	def setPath(self, path):
		self.path = path


	def save(self, listModelFileItem):
		if self.path is not None:
			dict_ = list(map(lambda data: data.dict(), listModelFileItem.dataList()))
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			try:
				with open(filename, 'w') as file:
					jsonInString = json.dumps(dict_)
					file.write(jsonInString)
			except Exception as e:
				log.error(f'Error is occurred while saving item in data list model service. '
						  f'Data item is {listModelFileItem}. 'f'Exception is {e}')
		else:
			log.warning(f'Path is not valid while saving data in data list model service. '
						f'Data item is {listModelFileItem}')


	def load(self, listModelFileItem):
		if listModelFileItem.type == FileType.FOLDER:
			return False
		if self.path is not None:
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			if listModelFileItem.isRead() is False:
				try:
					with open(filename, 'r') as file:
						jsonInString = file.read()
						if jsonInString:
							try:
								dataListInDict = json.loads(jsonInString)
								for dictData in dataListInDict:
									data = DataFactory.fileDataFromJson(dictData)
									if data is not None:
										data.setParent(listModelFileItem)
										listModelFileItem.appendData(data)
									else:
										log.warning(f'Data {dictData} is not valid to create ListModelFileItem. '
													f'Filename is {filename}')
								listModelFileItem.setRead(True)
								return True
							except Exception as e:
								log.error(f'Data list is not loaded successfully in file {filename}. Exception is {e}')
								return False
						else:
							log.warning('Read file is empty in list model service while loading file')
							return False
				except FileNotFoundError as e:
					log.error(f'File {filename} is not found in data list model service while loading file')
					return False

		else:
			log.warning('Path is not valid while loading in SaveListModelFolderItemService')
			return False


	def deleteListModelFileItem(self, listModelFileItem):
		if self.path is not None:
			filename = os.path.join(self.path, f'{listModelFileItem.id()}.json')
			try:
				os.remove(filename)
				for data in listModelFileItem.dataList():
					self.__deleteDataModelItem(data)
			except Exception as e:
				log.warning(f'Error occurred while delete file from storage at data list model service. '
							f'Parent file is {filename}. Exception is {e}')
			return True
		else:
			return False


	def deleteDataModelItem(self, dataModelItem):
		try:
			self.__deleteDataModelItem(dataModelItem)
		except Exception as e:
			log.error(f'Error occurred while delete file item from dtorage at data list model service. '
					  f'File is {dataModelItem.path}. Exception is {e}')


	def __deleteDataModelItem(self, dataModelItem):
		filename = dataModelItem.path
		os.remove(filename)


__service__ = __DataListModelFolderItemService__()


class DataListModelFolderItemService(object):
	def dataListModelService(self):
		return __service__
