import datetime
import json
import logging as log

from enums import FileType
from itemmodel.listModelItem import ListModelFolderItem, ListModelFileItem


class __SaveListModelFolderItemService__(object):
	def __init__(self):
		self.path = None


	def setPath(self, path):
		self.path = path


	def save(self, listModelFolderItem):
		if self.path is not None:
			dict_ = listModelFolderItem.dict()
			with open(self.path, 'w') as file:
				jsonInString = json.dumps(dict_)
				file.write(jsonInString)
		else:
			log.warning('Path is not valid while saving in SaveListModelFolderItemService')


	def load(self):
		if self.path is not None:
			with open(self.path) as file:
				jsonInString = file.read()
				if jsonInString:
					try:
						folderInDict = json.loads(jsonInString)
						id_ = [folderInDict['id']]
						root = ListModelFolderItem(folderInDict['id'], folderInDict['name'], None)
						# todo :burada read folder bir hata alırsa exception yolla yeni bir tür exception folderInDict valid bir variable olmalı
						self.__readFileList(root, folderInDict.get('children', []), id_)
						ListModelFileItem.setListID(id_[0] + 1)
					except Exception as e:
						log.error(f'File list is not loaded successfully in file {self.path}. Exception is {e}')
						root = ListModelFolderItem(ListModelFileItem.IDGenerator(), '/', None)
				else:
					root = ListModelFolderItem(ListModelFileItem.IDGenerator(), '/', None)
				return root
		else:
			log.warning('Path is not valid while loading in SaveListModelFolderItemService')
			return None


	def __readFileList(self, folder, json, maxID):
		for childrenInJson in json:
			if childrenInJson['type'] == FileType.FILE:
				listModelFileItem = ListModelFileItem(childrenInJson['id'], childrenInJson['name'], folder,
													  lastUpdate = datetime.datetime.fromtimestamp(
															  childrenInJson.get('lastUpdate')),
													  createDate = datetime.datetime.fromtimestamp(
															  childrenInJson.get('createDate',
																				 datetime.datetime.now().timestamp())),
													  isFixed = childrenInJson.get('isFixed', False),
													  isLocked = childrenInJson.get('isLocked', False))
				listModelFileItem.setTags(
						set(filter(lambda item: item != '', childrenInJson.get('tags', '').split(';'))))

				folder.append(listModelFileItem)
				maxID[0] = max(maxID[0], childrenInJson['id'])
			elif childrenInJson['type'] == FileType.FOLDER:
				subFolder = ListModelFolderItem(childrenInJson['id'], childrenInJson['name'], folder,
												isFixed = childrenInJson.get('isFixed', False))
				folder.append(subFolder)
				maxID[0] = max(maxID[0], childrenInJson['id'])
				self.__readFileList(subFolder, childrenInJson.get('children', []), maxID)


__service__ = __SaveListModelFolderItemService__()


class SaveListModelFolderItemService(object):
	def saveListModelService(self):
		return __service__
