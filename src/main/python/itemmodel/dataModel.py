import PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
import core
from enums import FileType, DataType


class DataModel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		super(DataModel, self).__init__(parent)
		self.__listModelFileItem = None
		self.__sourceModel = None


	# todo silme ekleme move işleri source model de olacak burada değil.
	# todo data da source model de olacak

	def setSourceModel(self, sourceModel):
		if self.__sourceModel is not None:
			pass

		self.__sourceModel = sourceModel


	# todo: burada sinyal bağlama olacak

	def mapFromSource(self, sourceIndex):
		pass


	def mapToSource(self, index):
		pass


	def sourceModel(self):
		return self.__sourceModel


	def beginEditData(self, index):
		oldData = self.listModelFileItem().data(index.row())
		return oldData


	def endEditData(self, index):
		self.dataChanged.emit(index, index)


	def setListModelFileItem(self, listModelFileItem):
		self.beginResetModel()
		self.__listModelFileItem = listModelFileItem
		self.endResetModel()


	def hasFileItem(self):
		return self.__listModelFileItem is not None and self.__listModelFileItem.type == FileType.FILE


	def listModelFileItem(self):
		return self.__listModelFileItem


	def data(self, index, role = QtCore.Qt.DisplayRole):
		if index.isValid() is False:
			return None
		itemData = self.listModelFileItem().data(index.row())
		if role == QtCore.Qt.DisplayRole:
			dataList = itemData.toArray()
			return dataList
		elif role == QtCore.Qt.UserRole:
			return itemData
		elif role == QtCore.Qt.DecorationRole:
			data = self.listModelFileItem().data(index.row())
			if data.type() == DataType.STYLEDATA:
				return QtGui.QIcon(core.fbs.icons('post_add-black-18dp.svg'))
			elif data.type() == DataType.IMAGEFILEDATA:
				return QtGui.QIcon(core.fbs.icons('baseline_insert_photo_white_48dp.png'))
			elif data.type() == DataType.PDFFILEDATA:
				return QtGui.QIcon(core.fbs.icons('picture_as_pdf-white-18dp.svg'))
			elif data.type() == DataType.TEXTFILEDATA:
				return QtGui.QIcon(core.fbs.icons('baseline_insert_drive_file_white_48dp1.png'))
			else:
				return QtGui.QIcon(core.fbs.icons('baseline_attachment_white_48dp.png'))


	def rowCount(self, parent = QtCore.QModelIndex()):
		if self.listModelFileItem() is not None:
			return self.listModelFileItem().dataCount()
		else:
			return 0


	def insertData(self, data):
		self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
		self.listModelFileItem().appendData(data)
		self.listModelFileItem().updateLastUpdateDate()
		self.endInsertRows()


	def deleteRow(self, index):
		self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
		data = self.listModelFileItem().popData(index.row())
		self.endRemoveRows()
		return data
