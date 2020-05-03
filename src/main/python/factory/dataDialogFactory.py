from enums import DataType
from widget.dialog.imageViewDialog import ImageViewDialog
from widget.dialog.textEditorDialog import TextEditorDialog


class DataDialogFactory(object):
	@classmethod
	def create(cls, data, parent):
		if data.type() == DataType.STYLEDATA:
			dialog = TextEditorDialog(parent)
			dialog.setCurrentData(data)
			return dialog
		elif data.type() == DataType.IMAGEFILEDATA:
			dialog = ImageViewDialog(parent)
			dialog.setCurrentData(data)
			return dialog
		elif data.type() == DataType.TEXTFILEDATA:
			dialog = TextEditorDialog(parent, disableStyle = True)
			dialog.setCurrentData(data)
			return dialog
