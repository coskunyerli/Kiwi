import os
import datetime

from enums import DataType
from model.data import ImageFileData, FileData


class DataFactory(object):
	@classmethod
	def fileDataFromDialogData(cls, data):
		_, extension = os.path.splitext(data.filename)
		if extension in ['.jpg', '.png', '.jpeg']:
			fileData = ImageFileData(data.name, data.filename)
		elif extension == '.pdf':
			fileData = FileData(data.name, data.filename)
			fileData.setType(DataType.PDFFILEDATA)
		elif extension == '.txt':
			fileData = FileData(data.name, data.filename)
			fileData.setType(DataType.TEXTFILEDATA)
		else:
			fileData = None
		return fileData


	@classmethod
	def fileDataFromJson(cls, dictData):
		if dictData['type'] == DataType.STYLEDATA:
			data = FileData(dictData['name'], dictData['path'],
							datetime.datetime.fromtimestamp(dictData.get('createDate')))
			data.setType(DataType.STYLEDATA)

		elif dictData['type'] == DataType.IMAGEFILEDATA:
			data = ImageFileData(dictData['name'], dictData['path'],
								 datetime.datetime.fromtimestamp(dictData.get('createDate')))

		elif dictData['type'] == DataType.PDFFILEDATA:
			data = FileData(dictData['name'], dictData['path'],
							datetime.datetime.fromtimestamp(dictData.get('createDate')))
			data.setType(DataType.PDFFILEDATA)

		elif dictData['type'] == DataType.TEXTFILEDATA:
			data = FileData(dictData['name'], dictData['path'],
							datetime.datetime.fromtimestamp(dictData.get('createDate')))
			data.setType(DataType.TEXTFILEDATA)

		else:
			data = None
		return data
