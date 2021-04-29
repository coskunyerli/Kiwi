from PySide2 import QtWidgets, QtCore


class ButtonWithRightClick(QtWidgets.QPushButton):
	rightClicked = QtCore.Signal()


	def __init__(self, parent = None):
		super(ButtonWithRightClick, self).__init__(parent)


	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.RightButton:
			self.rightClicked.emit()
		else:
			self.click()
