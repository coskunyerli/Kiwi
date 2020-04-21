from PySide2 import QtWidgets, QtGui, QtCore

from delegate.comboboxItemDelegate import ComboBoxItemDelegate


class ColorComboBox(QtWidgets.QComboBox):
	def __init__(self, parent = None):
		super(ColorComboBox, self).__init__(parent)
		self.colors = {'Red': '#940000', 'Blue': '#001294', 'Green': '#00942C'}
		keys = self.colors.keys()
		for i in range(len(keys)):
			colorname = keys[i]
			color = QtGui.QColor(self.colors[colorname])
			self.addItem(colorname, color)
			index = self.model().index(i, 0)
			self.model().setData(index, color, QtCore.Qt.BackgroundRole)

		delegate = ComboBoxItemDelegate(self)
		self.setItemDelegate(delegate)


	def getColors(self):
		return map(lambda c: QtGui.QColor(c), self.colors)


	def setCurrentIndex(self, index):
		super(ColorComboBox, self).setCurrentIndex(index)
