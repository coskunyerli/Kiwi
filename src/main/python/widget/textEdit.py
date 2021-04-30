from PySide2 import QtWidgets, QtGui


class TextEdit(QtWidgets.QTextEdit):

	# def focusInEvent(self, event):
	# 	super(TextEdit, self).focusInEvent(event)
	# 	cursor = self.textCursor()
	# 	cursor.movePosition(QtGui.QTextCursor.End)
	# 	self.setTextCursor(cursor)


	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()
		else:
			super(TextEdit, self).dragEnterEvent(event)


	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()
		else:
			super(TextEdit, self).dragMoveEvent(event)


	def dropEvent(self, event):
		# accept insert image to the text editor
		urls = event.mimeData().urls()
		if urls:
			file_ = urls[0].path()
			image = QtGui.QImage(file_)
			if not image.isNull():
				cursor = self.textCursor()
				cursor.beginEditBlock()
				cursor.insertHtml(""" <img src='%s' width='%d'/> """ % (
					file_, self.document().pageSize().width() - 2 * self.document().documentMargin()))
				cursor.insertBlock()
				cursor.endEditBlock()
