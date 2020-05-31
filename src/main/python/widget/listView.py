from PySide2 import QtWidgets, QtCore

from delegate.fileViewDelegate import FileViewDelegate
from enums import ItemFlags


class ListView(QtWidgets.QListView):
	currentIndexChanged = QtCore.Signal(QtCore.QModelIndex)
	dragTimeout = QtCore.Signal(QtCore.QModelIndex)


	def __init__(self, parent = None):
		super(ListView, self).__init__(parent)
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.timerTime = 500
		self.dragTimer = QtCore.QTimer(self)
		self.dragTimer.setSingleShot(True)
		self.dragTimer.timeout.connect(self.clickUsingDragDrop)
		self.__currentDragIndex = QtCore.QModelIndex()


	def clickUsingDragDrop(self):
		index = self.__currentDragIndex
		self.__currentDragIndex = QtCore.QModelIndex()
		self.dragTimeout.emit(index)


	def dragEnterEvent(self, event):
		self.__currentDragIndex = self.indexAt(event.pos())
		self.dragTimer.start(self.timerTime)
		super(ListView, self).dragEnterEvent(event)


	def dragLeaveEvent(self, event):
		self.dragTimer.stop()
		self.__currentDragIndex = QtCore.QModelIndex()
		super(ListView, self).dragLeaveEvent(event)


	def dropEvent(self, event):
		self.dragTimer.stop()
		self.__currentDragIndex = QtCore.QModelIndex()
		super(ListView, self).dropEvent(event)


	def currentChanged(self, current, old):
		super(ListView, self).currentChanged(current, old)
		self.currentIndexChanged.emit(current)


	def dragMoveEvent(self, event):
		mimeData = event.mimeData()
		dropIndex = mimeData.colorData()
		if dropIndex and dropIndex.isValid() is True:
			hoverIndex = self.indexAt(event.pos())
			# if hover data is equal drop data, drop action is not permitted. it is invalid operation
			dataIsEqual = hoverIndex.data(QtCore.Qt.UserRole) == dropIndex.data(QtCore.Qt.UserRole)
			if hoverIndex.isValid() and dataIsEqual is True:
				self.dragTimer.stop()
				self.__currentDragIndex = QtCore.QModelIndex()
				event.ignore()
			else:
				super(ListView, self).dragMoveEvent(event)
			# start drag timer. if drag timer is timeout, signal is emit
			if hoverIndex != self.__currentDragIndex and dataIsEqual is False:
				self.__currentDragIndex = hoverIndex
				self.dragTimer.start(self.timerTime)

		else:
			super(ListView, self).dragMoveEvent(event)
