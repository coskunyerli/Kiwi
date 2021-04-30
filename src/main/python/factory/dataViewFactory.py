from enums import DataType
from widget.viewer.imageView import ImageView
from widget.viewer.subProcessDialog import SubProcessDialog
from widget.viewer.textEditor import TextEditor


class DataViewFactory(object):
	# create a view object to show data
	@classmethod
	def create(cls, data, parent):
		if data.type() == DataType.STYLEDATA:
			widget = TextEditor(parent)
			widget.setCurrentData(data)
			return widget
		elif data.type() == DataType.IMAGEFILEDATA:
			widget = ImageView(parent)
			widget.setCurrentData(data)
			return widget
		elif data.type() == DataType.TEXTFILEDATA:
			widget = TextEditor(parent, disableStyle = True)
			widget.setCurrentData(data)
			return widget
		elif data.type() == DataType.PDFFILEDATA:
			widget = SubProcessDialog(['open', '-a', 'Preview', '-e', data.path])
			return widget
