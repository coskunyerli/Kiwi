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

		self.highlightCursor = QtGui.QTextCursor(self.editor.document())
		self.highlightCursor.setPosition(0)

		searchStyle = StyleItem('search', 0, '', None, None, 'Menlo', 12, None, None, None, None, None, 'yellow', None,
								None)
		self.rule = HighlightingRule(self.editor)
		self.rule.style = searchStyle
		self.highlighter.highlightingRules.append(self.rule)
		self.rule.pattern = QtCore.QRegExp(fr'{searchStyle.pattern}')
		self.rule.index = searchStyle.index

		self.nextWordSearchWordShortcut = QtWidgets.QShortcut(self.searchWidgetInEditor)
		self.nextWordSearchWordShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.nextWordSearchWordShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))

		self.showSearchWidgetShortcut = QtWidgets.QShortcut(self)
		self.showSearchWidgetShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.showSearchWidgetShortcut.setKey(QtGui.QKeySequence('CTRL+F'))

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


	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape and self.searchWidgetInEditor.isVisible():
			self.hideSearchWidgetInEditor()
		else:
			super(TextEditorWidget, self).keyPressEvent(event)


	def initSignalsAndSlots(self):
		self.doneButton.clicked.connect(self.hideSearchWidgetInEditor)
		self.prevWordButton.clicked.connect(self.previousSearchedWord)
		self.nextWordButton.clicked.connect(self.nextSearchedWord)
		self.nextWordSearchWordShortcut.activated.connect(self.nextWordButton.click)
		self.showSearchWidgetShortcut.activated.connect(self.showSearch)
		self.replaceCheckBox.stateChanged.connect(
			lambda value: self.replaceWidget.show() if value else self.replaceWidget.hide())
		self.replaceAllButton.clicked.connect(self.replaceAllText)
		self.replaceButton.clicked.connect(self.replaceText)
		self.searchLineBoxInEditor.textChanged.connect(self.searchWord)
		self.editor.cursorPositionChanged.connect(self.updateHighlightCursor)


	def setStyleItems(self, styleItems):
		self.styleItems = styleItems
		self.highlighter = Highlighter(self.editor, self.styleItems)
		self.highlighter.highlightingRules.append(self.rule)


	def hideSearchWidgetInEditor(self):
		self.searchWord('')
		self.searchWidgetInEditor.hide()


	def previousSearchedWord(self):
		# find previous text. start from current highlight cursor position
		cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
												  position = self.highlightCursor.selectionStart(),
												  option = QtGui.QTextDocument.FindBackward)
		# if it is found update current cursor
		if cursor is not None:
			self.editor.setTextCursor(cursor)
			self.searchLineBoxInEditor.setFocus()


	def nextSearchedWord(self):
		# find next text. start from current highlight cursor position
		cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
												  position = self.highlightCursor.selectionEnd())
		# if it is found update current cursor
		if cursor is not None:
			self.editor.setTextCursor(cursor)
			self.searchLineBoxInEditor.setFocus()


	def searchTextInCurrentDocument(self, text, position = 0, option = QtGui.QTextDocument.FindFlags()):
		# find text with given text position and option parameters

		if text:
			# if self.wholeWordCheckbox.isChecked():
			# 	option = option | QtGui.QTextDocument.FindWholeWords

			cursor = self.editor.document().find(text, position, option)
			if cursor.isNull() is False:
				return cursor
			else:
				if option & QtGui.QTextDocument.FindBackward:
					c = QtGui.QTextCursor(self.editor.document())
					c.setPosition(self.editor.document().characterCount() - 1)
				else:
					c = QtGui.QTextCursor(self.editor.document())
				return c
		else:
			return None


	def replaceAllText(self):
		# replace all text start from position 0
		cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
												  position = 0)
		oldWord = self.searchLineBoxInEditor.text()
		newWord = self.replaceLineEdit.text()
		# get old and new word, these are should be valid
		cursor.beginEditBlock()
		while oldWord and newWord and cursor.isNull() is False and cursor.hasSelection() is True:
			self.replaceNextText(cursor, newWord)
			cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
													  position = cursor.selectionEnd())
		cursor.endEditBlock()
		# update current cursor
		self.editor.setTextCursor(cursor)


	def replaceText(self):
		# old and new words should be valid
		oldWord = self.searchLineBoxInEditor.text()
		newWord = self.replaceLineEdit.text()
		if oldWord and newWord:
			# find cursor that includes valid text
			cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
													  position = self.highlightCursor.selectionStart())
			# replace the cursor with new text
			self.replaceNextText(cursor, newWord)
			# find next word
			self.nextSearchedWord()


	def replaceNextText(self, cursor, newWord):
		# cursor is not null and has selection. Also new word should be valid
		if newWord and cursor.isNull() is False and cursor.hasSelection():
			cursor.beginEditBlock()
			cursor.insertText(newWord)
			cursor.endEditBlock()
		return cursor


	def searchWord(self, text):
		# search word and update current text
		self.rule.pattern = re.compile(text, re.IGNORECASE)
		# update editor style
		self.updateEditor()
		if text:
			cursor = self.searchTextInCurrentDocument(self.searchLineBoxInEditor.text(),
													  position = self.highlightCursor.selectionStart())
			if cursor is not None:
				self.editor.setTextCursor(cursor)
		else:
			cursor = QtGui.QTextCursor(self.editor.document())
			cursor.setPosition(self.editor.textCursor().selectionStart())
			self.editor.setTextCursor(cursor)


	def showSearch(self):
		# show search widget
		self.searchWidgetInEditor.show()
		text = self.editor.textCursor().selectedText()
		self.searchLineBoxInEditor.setText(text)
		self.searchLineBoxInEditor.setFocus()


	def updateEditor(self):
		# update editor syntax highlighting
		charCount = self.editor.document().characterCount()
		self.editor.document().contentsChange.emit(0, 0, charCount)


	def updateHighlightCursor(self):
		# when cursor position is changed update highlight cursor
		self.highlightCursor = self.editor.textCursor()
