from PySide2 import QtCore, QtGui, QtWidgets


class TabData(object):
	def __init__(self):
		self.isFixed = False


class TabWidget(QtWidgets.QTabWidget):
	def __init__(self, parent = None):
		super(TabWidget, self).__init__(parent)


	def openWidget(self, widget):
		data = widget.currentData()
		tabBar = self.tabBar()
		notFixedIndex = -1
		for index in range(tabBar.count()):
			if self.isTabFixed(index) is False:
				notFixedIndex = index

		name = f'{data.parent().name()}/{data.name()}'
		if notFixedIndex != -1:
			currentIndex = notFixedIndex
			self.removeTab(notFixedIndex)
		else:
			tabIndex = self.currentIndex() + 1
			currentIndex = tabIndex
		self.insertTab(currentIndex, widget, name)
		self.setFixedTab(currentIndex, False)
		self.setCurrentIndex(currentIndex)
		self.setTabToolTip(currentIndex, f'{data.parent().path()}/{data.name()}')


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
