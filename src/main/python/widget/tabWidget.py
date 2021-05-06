from PySide2 import QtCore, QtGui, QtWidgets


class TabData(object):
	def __init__(self):
		self.isFixed = False


class TabWidget(QtWidgets.QTabWidget):
	def __init__(self, parent = None):
		super(TabWidget, self).__init__(parent)
		self.__model = None


	def openWidget(self, widget):
		data = widget.currentData()
		tabBar = self.tabBar()
		notFixedIndex = -1
		for index in range(tabBar.count()):
			if self.isTabFixed(index) is False:
				notFixedIndex = index
		if data is not None:
			name = f'{data.parent().name()}/{data.name()}'
			toolTipText = f'{data.parent().path()}/{data.name()}'
		else:
			name = 'New Tab'
			toolTipText = name

		if notFixedIndex != -1:
			currentIndex = notFixedIndex
			currentWidget = self.widget(currentIndex)
			if currentWidget.accept() is False:
				return
			self.removeTab(notFixedIndex)
		else:
			tabIndex = self.currentIndex() + 1
			currentIndex = tabIndex
		self.insertTab(currentIndex, widget, name)
		self.setFixedTab(currentIndex, False)
		self.setCurrentIndex(currentIndex)
		self.setTabToolTip(currentIndex, toolTipText)


	def getWidgetIndex(self, data):
		currentIndex = -1
		for index in range(0, self.count()):
			tabWidget = self.widget(index)
			if tabWidget.id() == data.id():
				currentIndex = index
				break
		return currentIndex


	def setFixedTab(self, index, result):
		tabBar = self.tabBar()
		if tabBar.tabData(index) is None:
			data = TabData()
			tabBar.setTabData(index, data)
		tabData = tabBar.tabData(index)
		tabData.isFixed = result
		if tabData.isFixed:
			tabBar.setTabTextColor(index, QtGui.QColor('#ddd'))
		else:
			tabBar.setTabTextColor(index, QtGui.QColor('#BBF5C3'))


	def isTabFixed(self, index):
		tabBar = self.tabBar()
		data = tabBar.tabData(index)
		if data is not None and data.isFixed:
			return True
		else:
			return False


	def setModel(self, model):
		if self.__model:
			self.model().dataChanged.disconnect(self.dataChanged)
			self.model().rowsAboutToBeRemoved.disconnect(self.dataRemoved)
			self.model().rowsInserted.disconnect(self.dataInserted)

		self.__model = model
		if self.__model:
			self.model().dataChanged.connect(self.dataChanged)
			self.model().rowsAboutToBeRemoved.connect(self.dataRemoved)
			self.model().rowsInserted.connect(self.dataInserted)


	def model(self):
		return self.__model


	def dataChanged(self, left, right):
		data = left.data(QtCore.Qt.UserRole)
		widgetIndex = self.getWidgetIndex(data)
		if widgetIndex != -1:
			widget = self.widget(widgetIndex)
			widget.setModified(True)
			name = f'{data.parent().name()}/{data.name()}'
			toolTipText = f'{data.parent().path()}/{data.name()}'
			self.setTabToolTip(widgetIndex, toolTipText)
			self.setTabText(widgetIndex, name)


	def dataRemoved(self, parent, first, last):
		if self.model() is None:
			return
		data = self.model().index(first, 0, parent).data(QtCore.Qt.UserRole)
		widgetIndex = self.getWidgetIndex(data)
		if widgetIndex != -1:
			widget = self.widget(widgetIndex)
			widget.setModified(True)
			name = f'{data.parent().name()}/{data.name()} (Deleted)'
			toolTipText = f'{data.parent().path()}/{data.name()} (Deleted)'
			self.setTabToolTip(widgetIndex, toolTipText)
			self.setTabText(widgetIndex, name)
			widget = self.widget(widgetIndex)
			widget.setCurrentData(None)


	def dataInserted(self, parent, first, last):
		if self.model() is None:
			return
		data = self.model().index(first, 0, parent).data(QtCore.Qt.UserRole)
		widgetIndex = self.getWidgetIndex(data)
		if widgetIndex != -1:
			name = f'{data.parent().name()}/{data.name()}'
			toolTipText = f'{data.parent().path()}/{data.name()}'
			self.setTabToolTip(widgetIndex, toolTipText)
			self.setTabText(widgetIndex, name)
