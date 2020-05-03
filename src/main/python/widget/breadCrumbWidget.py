import static
from PySide2 import QtWidgets as QtWidgets, QtCore as QtCore


class BreadCrumb(QtWidgets.QFrame):
	clicked = QtCore.Signal(object)
	dropped = QtCore.Signal(object, QtCore.QMimeData)
	middleClicked = QtCore.Signal(object)


	def __init__(self, parent = None):
		super(BreadCrumb, self).__init__(parent)
		self.prevX = None
		self.__dragState = None
		self.middleClickedItem = None
		self._layout = QtWidgets.QHBoxLayout(self)
		self._layout.setSpacing(0)
		self._layout.setContentsMargins(0, 0, 0, 0)
		self.__breadCrumbItemList = []
		self.spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self._selectedItem = None
		self._layout.addItem(self.spacer)
		self.clickedItem = None
		self._lastItem = None


	def mousePressEvent(self, event):
		self.clickPosX = event.globalX()
		if event.button() == QtCore.Qt.LeftButton:
			self.clickedItem = self.itemAt(event.pos())

		elif event.button() == QtCore.Qt.MiddleButton:
			self.middleClickedItem = self.itemAt(event.pos())

		super().mousePressEvent(event)


	def mouseMoveEvent(self, event):
		if abs(event.globalX() - self.clickPosX) > 30 or self.__dragState:
			self.setCursor(QtCore.Qt.ClosedHandCursor)

			self.prevX = event.globalX()
			self.__dragState = True
		super().mouseMoveEvent(event)


	def mouseReleaseEvent(self, event):
		super(BreadCrumb, self).mouseReleaseEvent(event)
		if self.__dragState is True:
			self.setCursor(QtCore.Qt.ArrowCursor)
			self.prevX = None
			self.__dragState = False
			return
		breadCrumbItemIndex = self.itemAt(event.pos())
		if breadCrumbItemIndex is not None and breadCrumbItemIndex == self.clickedItem:
			breadCrumbItem = self.__breadCrumbItemList[breadCrumbItemIndex]
			self.clicked.emit(breadCrumbItem.item)

		if breadCrumbItemIndex is not None and breadCrumbItemIndex == self.middleClickedItem:
			breadCrumbItem = self.__breadCrumbItemList[breadCrumbItemIndex]
			self.middleClicked.emit(breadCrumbItem.item)


	def _setSelectedItem(self, item):
		if item is not None:
			if self._selectedItem is not None:
				self._selectedItem.setActive(False)
			item.setActive(True)
			self._selectedItem = item


	def itemAt(self, pos):

		def cmp(item):
			geometry = item.geometry()
			if geometry.contains(pos):
				return 0
			return static.cmp(geometry.left(), pos.x())


		return static.binarySearch(self.__breadCrumbItemList, cmp = lambda item: cmp(item))


	def setPath(self, data):
		if self._lastItem == data:
			return

		self._lastItem = data
		dataList = [item.item for item in self.__breadCrumbItemList]

		# Means user clicked one of the previous items on the breadcrumb
		if data in dataList:
			while data != dataList[-1]:
				dataList.pop()
				self.removeItemFromBreadcrumb(self.__breadCrumbItemList.pop())

			self._setSelectedItem(self.__breadCrumbItemList[-1])
			return

		self._clearItems()
		while data is not None:
			item = BreadCrumbItem(data, self)
			item.setMinimumWidth(50)
			item.setAlignment(QtCore.Qt.AlignCenter)
			item.setText(data.text())

			self.__breadCrumbItemList.insert(0, item)
			self._layout.insertWidget(0, item)
			data = data.parent()
		self._layout.addItem(self.spacer)
		if self.__breadCrumbItemList:
			self._setSelectedItem(self.__breadCrumbItemList[-1])


	def removeItemFromBreadcrumb(self, item):
		self._layout.removeWidget(item)
		item.setParent(None)
		del item


	def _clearItems(self):
		for item in self.__breadCrumbItemList:
			self._layout.removeWidget(item)
			item.setParent(None)
			del item
		self._layout.removeItem(self.spacer)
		self.__breadCrumbItemList = []


class BreadCrumbItem(QtWidgets.QFrame):

	def __init__(self, item, parent = None):
		super(BreadCrumbItem, self).__init__(parent)

		self._layout = QtWidgets.QVBoxLayout(self)
		self._labelLayout = QtWidgets.QHBoxLayout()
		self._labelLayout.setContentsMargins(8, 0, 8, 0)
		self.label = QtWidgets.QLabel(self)
		self.label.setObjectName('breadCrumbItemText')
		self.label.setMaximumWidth(200)
		self._labelLayout.addWidget(self.label)
		self.light = QtWidgets.QFrame(self)
		self.light.setFixedHeight(2)
		self._layout.setContentsMargins(0, 4, 0, 2)
		self._layout.setSpacing(0)
		self._layout.addLayout(self._labelLayout)
		self._layout.addWidget(self.light)
		self.setActive(False)
		self.item = item
		self.dragTimer = QtCore.QTimer(self)
		self.dragTimer.setSingleShot(True)
		self.dragTimer.timeout.connect(self.clickUsingDragDrop)
		self.setAcceptDrops(True)


	def clickUsingDragDrop(self):
		self.parent().clicked.emit(self.item)


	def dragEnterEvent(self, event):
		self.dragTimer.start(500)
		#event.acceptProposedAction()


	def dragLeaveEvent(self, event):
		self.dragTimer.stop()
		super(BreadCrumbItem, self).dragLeaveEvent(event)


	def dropEvent(self, event):
		self.dragTimer.stop()
		mimeData = event.mimeData()
		self.parent().dropped.emit(self.item, mimeData)
		super(BreadCrumbItem, self).dropEvent(event)


	def enterEvent(self, event):
		super(BreadCrumbItem, self).enterEvent(event)
		self.setStyleSheet("background-color:%s" % '#505050')


	def leaveEvent(self, event):
		super(BreadCrumbItem, self).leaveEvent(event)
		self.setStyleSheet("background-color:%s" % 'transparent')


	def setText(self, text):
		text = self.label.fontMetrics().elidedText(text, QtCore.Qt.ElideRight, self.label.maximumWidth())
		self.label.setText(text)


	def text(self):
		return self.label.text()


	def setActive(self, active):
		if active:
			self.light.setStyleSheet('background-color:#DC7D14')
		else:
			self.light.setStyleSheet('background-color:transparent')


	def setAlignment(self, align):
		self.label.setAlignment(align)
