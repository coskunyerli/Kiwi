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

		if notFixedIndex != -1:
			self.removeTab(notFixedIndex)
			self.insertTab(notFixedIndex, widget, f'{data.parent().name()}/{data.name()}')
			self.setFixedTab(notFixedIndex, False)
			self.setCurrentIndex(notFixedIndex)
		else:
			tabIndex = self.currentIndex() + 1
			self.insertTab(tabIndex, widget, f'{data.parent().name()}/{data.name()}')
			self.setFixedTab(tabIndex, False)
			self.setCurrentIndex(tabIndex)


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
