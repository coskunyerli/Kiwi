import re

import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtGui as QtGui
from model.highLighting import HighlightingRule, Highlighter
from model.styleItem import StyleItem
from widget.textEdit import TextEdit


class TextEditorWidget(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(TextEditorWidget, self).__init__(parent)
		self.setObjectName("editorWidget")
		self.editorWidgetLayout = QtWidgets.QVBoxLayout(self)
		self.editorWidgetLayout.setSpacing(0)
		self.editorWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.editorWidgetLayout.setObjectName("verticalLayout")

		self.searchWidgetInEditor = QtWidgets.QWidget(self)
		self.searchWidgetInEditor.setObjectName("searchWidgetInEditor")
		self.searchWidgetInEditorLayout = QtWidgets.QVBoxLayout(self.searchWidgetInEditor)
		self.searchWidgetInEditorLayout.setSpacing(0)
		self.searchWidgetInEditorLayout.setContentsMargins(12, 0, 0, 0)
		self.searchWidgetInEditorLayout.setObjectName("verticalLayout_3")
		self.searchWidget = QtWidgets.QWidget(self.searchWidgetInEditor)
		self.searchWidget.setObjectName("searchWidget")
		self.searchWidgetLayout = QtWidgets.QHBoxLayout(self.searchWidget)
		self.searchWidgetLayout.setSpacing(0)
		self.searchWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.searchWidgetLayout.setObjectName("horizontalLayout_5")
		self.searchLineBoxInEditor = QtWidgets.QLineEdit(self.searchWidget)
		self.searchLineBoxInEditor.setObjectName("searchLineBoxInEditor")
		self.searchWidgetLayout.addWidget(self.searchLineBoxInEditor)
		spacer = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.searchWidgetLayout.addItem(spacer)
		self.prevWordButton = QtWidgets.QPushButton(self.searchWidget)
		self.prevWordButton.setObjectName("prevWordButton")
		self.searchWidgetLayout.addWidget(self.prevWordButton)
		self.nextWordButton = QtWidgets.QPushButton(self.searchWidget)
		self.nextWordButton.setEnabled(True)
		self.nextWordButton.setObjectName("nextWordButton")
		self.searchWidgetLayout.addWidget(self.nextWordButton)
		spacer2 = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.searchWidgetLayout.addItem(spacer2)

		self.doneButton = QtWidgets.QPushButton(self.searchWidget)
		self.doneButton.setObjectName("doneButton")
		self.searchWidgetLayout.addWidget(self.doneButton)
		spacer3 = QtWidgets.QSpacerItem(12, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.searchWidgetLayout.addItem(spacer3)
		self.replaceCheckBox = QtWidgets.QCheckBox(self.searchWidget)
		self.replaceCheckBox.setObjectName("replaceCheckBox")
		self.searchWidgetLayout.addWidget(self.replaceCheckBox)
		self.searchWidgetInEditorLayout.addWidget(self.searchWidget)
		self.replaceWidget = QtWidgets.QWidget(self.searchWidgetInEditor)
		self.replaceWidget.setObjectName("replaceWidget")
		self.replaceWidgetLayout = QtWidgets.QHBoxLayout(self.replaceWidget)
		self.replaceWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.replaceWidgetLayout.setSpacing(0)
		self.replaceWidgetLayout.setObjectName("horizontalLayout_4")
		self.replaceLineEdit = QtWidgets.QLineEdit(self.replaceWidget)
		self.replaceLineEdit.setObjectName("replaceLineEdit")
		self.replaceWidgetLayout.addWidget(self.replaceLineEdit)
		spacer4 = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.replaceWidgetLayout.addItem(spacer4)
		self.replaceButton = QtWidgets.QPushButton(self.replaceWidget)
		self.replaceButton.setObjectName("replaceButton")
		self.replaceWidgetLayout.addWidget(self.replaceButton)
		self.replaceAllButton = QtWidgets.QPushButton(self.replaceWidget)
		self.replaceAllButton.setObjectName("replaceAllButton")
		self.replaceWidgetLayout.addWidget(self.replaceAllButton)

		self.searchWidgetInEditorLayout.addWidget(self.replaceWidget)
		self.editorWidgetLayout.addWidget(self.searchWidgetInEditor)

		self.editor = TextEdit(self)
		self.editor.document().setDocumentMargin(16)
		self.editor.setObjectName("editor")
		self.editor.setFrameStyle(QtWidgets.QFrame.NoFrame)
		self.editor.setMinimumWidth(400)
		self.editorWidgetLayout.addWidget(self.editor)

		self.styleItems = []
		self.highlighter = Highlighter(self.editor, self.styleItems)

		searchStyle = StyleItem('search', '', None, None, None, None, None, None, 'yellow', None)
		self.rule = HighlightingRule(self.editor)
		self.rule.style = searchStyle
		self.highlighter.highlightingRules.append(self.rule)
		self.rule.pattern = re.compile('')

		self.nextWordSearchWordShortcut = QtWidgets.QShortcut(self.searchWidgetInEditor)
		self.nextWordSearchWordShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.nextWordSearchWordShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))

		self.initialize()
		self.initSignalsAndSlots()


	def initialize(self):
		self.editor.setAcceptDrops(True)
		self.searchLineBoxInEditor.setPlaceholderText("Find")
		self.prevWordButton.setText("<")
		self.nextWordButton.setText(">")
		self.doneButton.setText("Done")
		self.replaceCheckBox.setText("Replace")
		self.replaceLineEdit.setPlaceholderText("Replace")
		self.replaceButton.setText("Replace")
		self.replaceAllButton.setText("All")
		self.searchWidgetInEditor.hide()
		self.replaceWidget.hide()


	def initSignalsAndSlots(self):
		self.doneButton.clicked.connect(self.hideSearchWidgetInEditor)
		self.prevWordButton.clicked.connect(self.prevSearchText)
		self.nextWordButton.clicked.connect(self.nextSearchText)
		self.nextWordSearchWordShortcut.activated.connect(self.nextSearchText)
		self.replaceCheckBox.stateChanged.connect(
				lambda value: self.replaceWidget.show() if value else self.replaceWidget.hide())
		self.replaceAllButton.clicked.connect(self.replaceAllText)
		self.replaceButton.clicked.connect(self.replaceText)


	# self.editor.document().contentsChange.connect(self.contentChanged)

	def setStyleItems(self, styleItems):
		self.styleItems = styleItems
		self.highlighter = Highlighter(self.editor, self.styleItems)
		self.highlighter.highlightingRules.append(self.rule)


	def hideSearchWidgetInEditor(self):
		self.searchWord('')
		self.searchWidgetInEditor.hide()


	def nextSearchText(self):
		if not self.startFirst:
			if not self._nextSearchText():
				self.startFirst = True
		else:
			self._nextSearchText(0)
			self.startFirst = False


	def _nextSearchText(self, position = None):
		cursor = self.editor.textCursor()
		if position is None:
			cursor.setPosition(cursor.selectionEnd())
		else:
			cursor.setPosition(position)
		block = cursor.block()
		text = block.text()[cursor.positionInBlock():]
		while block.isValid():
			matches = self.rule.search(text)
			for match in matches:
				cursor.setPosition(cursor.positionInBlock() + block.position() + match.start())
				cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor,
									match.end() - match.start())

				self.editor.setTextCursor(cursor)
				return True

			block = block.next()
			cursor.setPosition(block.position())
			text = block.text()
		return False


	def prevSearchText(self):
		if not self.startLast:
			if not self._prevSearchText():
				self.startLast = True
		else:
			self._prevSearchText(self.editor.document().characterCount() - 1)
			self.startLast = False


	def _prevSearchText(self, position = None):
		cursor = self.editor.textCursor()
		if position is None:
			cursor.setPosition(cursor.selectionStart())
		else:
			cursor.setPosition(position)
		block = cursor.block()
		text = block.text()[0:cursor.positionInBlock()]
		while block.isValid():
			matches = list(self.rule.search(text))
			if len(matches) > 0:
				match = matches[-1]
				cursor.setPosition(block.position() + match.end())
				cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor,
									match.end() - match.start())
				self.editor.setTextCursor(cursor)
				return True

			block = block.previous()
			cursor.setPosition(block.position() + len(block.text()))
			text = block.text()
		return False


	def replaceAllText(self):
		oldWord = self.searchLineBoxInEditor.text()
		if oldWord:
			newWord = self.replaceLineEdit.text()
			block = self.editor.document().firstBlock()
			cursor = self.editor.textCursor()
			cursor.beginEditBlock()
			while block.isValid():
				text = block.text()
				if text.find(oldWord) != -1:
					tcursor = QtGui.QTextCursor(block)
					tcursor.select(QtGui.QTextCursor.BlockUnderCursor)
					tcursor.removeSelectedText()
					tcursor.clearSelection()
					newText = text.replace(oldWord, newWord)
					tcursor.insertBlock()
					tcursor.insertText(newText)
				block = block.next()
			cursor.endEditBlock()


	def replaceText(self):
		cursor = self.replaceNextText(self.editor.textCursor())
		self.editor.setTextCursor(cursor)
		self.nextSearchText()


	def searchWord(self, text):
		self.rule.pattern = re.compile(text)
		self.updateEditor()


	def showSearch(self):
		self.searchWidgetInEditor.show()
		text = self.editor.textCursor().selectedText()
		self.searchLineBoxInEditor.setText(text)
		self.searchLineBoxInEditor.setFocus()
