import datetime
import json
import logging as log

from enums import FileType
from model.listModelItem import ListModelFolderItem, ListModelFileItem


class __SaveListModelFolderItemService__(object):
	def __init__(self):
		self.path = None


	def setPath(self, path):
		self.path = path


	def save(self, listModelFolderItem):
		if self.path is not None:
			dict_ = listModelFolderItem.dict()
			try:
				with open(self.path, 'w') as file:
					jsonInString = json.dumps(dict_)
					file.write(jsonInString)
			except Exception as e:
				log.warning(f'Exception is occurred while saving data in save list model folder item service. '
							f'Item is {listModelFolderItem}. Exception is {e}')
		else:
			log.warning('Path is not valid while saving in SaveListModelFolderItemService')


	def load(self):
		if self.path is not None:
			with open(self.path) as file:
				jsonInString = file.read()
				if jsonInString:
					try:
						folderInDict = json.loads(jsonInString)
						# this is calc max id
						id_ = [folderInDict['id']]
						# create root folder item using with id and name
						root = ListModelFolderItem(folderInDict['id'], folderInDict['name'], None)
						# read child of root folder
						self.__readFileList(root, folderInDict.get('children', []), id_)
						ListModelFileItem.setListID(id_[0] + 1)
					except Exception as e:
						log.error(f'File list is not loaded successfully in file {self.path}. Data is {folderInDict}. '
								  f'Exception is {e}')
						root = ListModelFolderItem(ListModelFileItem.IDGenerator(), '/', None)
				else:
					root = ListModelFolderItem(ListModelFileItem.IDGenerator(), '/', None)
				return root
		else:
			log.warning('Path is not valid while loading in SaveListModelFolderItemService')
			return None


	def __readFileList(self, folder, json, maxID):
		# convert json to ListModelFileItem
		for childrenInJson in json:
			if childrenInJson['type'] == FileType.FILE:
				# if type is file create file item
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
				# if type is folder create folder item and fill its children
				subFolder = ListModelFolderItem(childrenInJson['id'], childrenInJson['name'], folder,
												isFixed = childrenInJson.get('isFixed', False))
				folder.append(subFolder)
				maxID[0] = max(maxID[0], childrenInJson['id'])
				# read children of folder
				self.__readFileList(subFolder, childrenInJson.get('children', []), maxID)


__service__ = __SaveListModelFolderItemService__()


class SaveListModelFolderItemService(object):
	def saveListModelService(self):
		return __service__
