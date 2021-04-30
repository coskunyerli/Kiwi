from PySide2 import QtWidgets as QtWidgets, QtCore as QtCore


class TagAction(QtWidgets.QFrame):
	def __init__(self, color, parent = None):
		super(TagAction, self).__init__(parent)

		self.setMinimumWidth(100)
		self.setFixedHeight(24)
		self._layout = QtWidgets.QHBoxLayout(self)
		self._layout.setContentsMargins(4, 2,4, 2)
		self.circle = QtWidgets.QFrame(self)
		self.circle.setStyleSheet('background-color:%s;border-radius:2px' % color)
		self._layout.addWidget(self.circle)