class ItemFlags:
	ItemIsEditable = 128
	ItemIsDeletable = 256
	ItemIsSoftLink = 512


class FileType:
	FOLDER = 0
	FILE = 1
	SOFTLINK = 2


class DataType:
	DATA = 0
	FILEDATA = 1
	IMAGEFILEDATA = 2
	STYLEDATA = 3
	PDFFILEDATA = 4
	TEXTFILEDATA = 5
