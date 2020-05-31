import os
import datetime

import static
from enums import DataType
from model.data import ImageFileData, FileData


class DataFactory(object):
	@classmethod
	def fileDataFromFilePickerDialog(cls, data):
		# create file data from file picker data widget.
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
		# create data object from json. Data object can be file data, image data, pdf data or text file data
		if 'type' not in dictData or 'path' not in dictData or 'type' not in dictData:
			return None

		error = lambda key: f'File data object creation in fileDataFromJson at DataFactory. Key is {key}'
		try:
			name = static.getValueFromDict(dictData['name'], [str], error('name'))
			path = static.getValueFromDict(dictData['path'], [str], error('path'))
			type_ = static.getValueFromDict(dictData['type'], [int], error('type'))
			if type_ == DataType.STYLEDATA:
				data = FileData(name, path,
								datetime.datetime.fromtimestamp(
										static.getValueFromDict(dictData.get('createDate'), [float],
																error('create time'))))
				data.setType(DataType.STYLEDATA)

			elif type_ == DataType.IMAGEFILEDATA:
				data = ImageFileData(name, path,
									 datetime.datetime.fromtimestamp(
											 static.getValueFromDict(dictData.get('createDate'), [float],
																	 error('create time'))))

			elif type_ == DataType.PDFFILEDATA:
				data = FileData(name, path,
								datetime.datetime.fromtimestamp(
										static.getValueFromDict(dictData.get('createDate'), [float],
																error('create time'))))
				data.setType(DataType.PDFFILEDATA)

			elif type_ == DataType.TEXTFILEDATA:
				data = FileData(name, path,
								datetime.datetime.fromtimestamp(
										static.getValueFromDict(dictData.get('createDate'), [float],
																error('create time'))))
				data.setType(DataType.TEXTFILEDATA)

			else:
				data = None
			return data
		except ValueError as e:
			return None
