# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created: Sun Jun 10 14:33:14 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import os
import shutil
import re
import json
import datetime
from PySide2 import QtCore, QtGui, QtWidgets
from python.model.HighLighting import HighlightingRule, Highlighter
from python.itemmodel.fileListModel import FileListItem, FolderListItem
from python.model.styleItem import StyleItem
from python.enums import FileType, ItemFlags
from python.path import fileListPath, iconsPath
from python.widget.dialog.preferencesDialogue import Preferences
from python.widget.textEdit import TextEdit
from python.widget.listView import ListView


class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(868, 516)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_3.setSpacing(0)
		self.fileListWidget = QtWidgets.QWidget(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.fileListWidget.sizePolicy().hasHeightForWidth())
		self.fileListWidget.setSizePolicy(sizePolicy)
		self.fileListWidget.setObjectName("fileListWidget")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fileListWidget)
		self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.verticalLayout_2.setSpacing(0)
		self.searchWidgetInFileList = QtWidgets.QWidget(self.fileListWidget)
		self.searchWidgetInFileList.setObjectName("searchWidgetInFileList")
		self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.searchWidgetInFileList)
		self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_4.setSpacing(0)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.horizontalLayout_2.setSpacing(0)
		# spacer = QtWidgets.QSpacerItem( 0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum )
		# self.horizontalLayout_2.addItem(spacer)

		self.searchLineBoxInFileList = QtWidgets.QLineEdit(self.searchWidgetInFileList)
		self.searchLineBoxInFileList.setObjectName("searchLineBoxInFileList")
		self.verticalLayout_4.addLayout(self.horizontalLayout_2)

		# colorCombobox = ColorComboBox(self.searchWidgetInFileList)
		# self.verticalLayout_4.addWidget(colorCombobox)
		self.pathTextLabel = QtWidgets.QLabel(self.searchWidgetInFileList)
		self.pathTextLabel.setIndent(6)
		self.pathTextLabel.setText('/')
		self.pathTextLabel.setStyleSheet('color:gray')

		self.verticalLayout_4.addWidget(self.searchLineBoxInFileList)
		self.verticalLayout_4.addWidget(self.pathTextLabel)

		self.addFileWidget = QtWidgets.QWidget(self.searchWidgetInFileList)
		self.addFileWidget.setObjectName("addFileWidget")
		self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.addFileWidget)
		self.horizontalLayout_6.setSpacing(0)
		self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		self.newFileButton = QtWidgets.QPushButton(self.addFileWidget)
		self.newFileButton.setObjectName("newFileButton")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(iconsPath, 'baseline_insert_drive_file_white_48dp.png')))
		self.newFileButton.setIcon(icon)
		# self.newFileButton.setIconSize( QtCore.QSize( 18, 18 ) )
		self.horizontalLayout_6.addWidget(self.newFileButton)
		self.newFolderButton = QtWidgets.QPushButton(self.addFileWidget)
		self.newFolderButton.setEnabled(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(os.path.join(iconsPath, 'baseline_create_new_folder_white_48dp.png')))
		self.newFolderButton.setIcon(icon)
		# self.newFolderButton.setIconSize( QtCore.QSize( 18, 18 ) )
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		self.searchLineBoxInFileList.setSizePolicy(sizePolicy)
		self.horizontalLayout_6.addWidget(self.newFolderButton)
		self.horizontalLayout_2.addWidget(self.addFileWidget)
		self.verticalLayout_2.addWidget(self.searchWidgetInFileList)
		self.fileListView = ListView(self.fileListWidget)
		self.fileListView.setObjectName("fileListView")
		self.verticalLayout_2.addWidget(self.fileListView)
		self.horizontalLayout_3.addWidget(self.fileListWidget)

		# self.tabFrame = QtWidgets.QFrame( Form )
		# self.tabFrame.setStyleSheet( 'background-color:rgb(42,42,42)' )
		# self.tabFrameLayout = QtWidgets.QVBoxLayout( self.tabFrame )
		# self.tabFrameLayout.setContentsMargins( 0, 8, 0, 0 )
		#
		# #self.tabWidget = QtWidgets.QTabWidget( self.tabFrame )
		# #self.tabFrameLayout.addWidget( self.tabWidget )
		#
		# #self.tabWidget.setObjectName( "tabWidget" )
		# #self.tabWidget.setTabShape( QtWidgets.QTabWidget.Rounded )

		self.editorWidget = QtWidgets.QWidget(Form)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.editorWidget.sizePolicy().hasHeightForWidth())
		self.editorWidget.setSizePolicy(sizePolicy)
		self.editorWidget.setObjectName("editorWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.editorWidget)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.searchWidgetInEditor = QtWidgets.QWidget(self.editorWidget)
		self.searchWidgetInEditor.setObjectName("searchWidgetInEditor")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.searchWidgetInEditor)
		self.verticalLayout_3.setSpacing(0)
		self.verticalLayout_3.setContentsMargins(12, 0, 0, 0)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.searchWidget = QtWidgets.QWidget(self.searchWidgetInEditor)
		self.searchWidget.setObjectName("searchWidget")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.searchWidget)
		self.horizontalLayout_5.setSpacing(0)
		self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.searchLineBoxInEditor = QtWidgets.QLineEdit(self.searchWidget)
		self.searchLineBoxInEditor.setObjectName("searchLineBoxInEditor")
		self.horizontalLayout_5.addWidget(self.searchLineBoxInEditor)
		spacer = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacer)
		self.prevWordButton = QtWidgets.QPushButton(self.searchWidget)
		self.prevWordButton.setObjectName("prevWordButton")
		self.horizontalLayout_5.addWidget(self.prevWordButton)
		self.nextWordButton = QtWidgets.QPushButton(self.searchWidget)
		self.nextWordButton.setEnabled(True)
		self.nextWordButton.setObjectName("nextWordButton")
		self.horizontalLayout_5.addWidget(self.nextWordButton)
		spacer2 = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacer2)

		self.doneButton = QtWidgets.QPushButton(self.searchWidget)
		self.doneButton.setObjectName("doneButton")
		self.horizontalLayout_5.addWidget(self.doneButton)
		spacer3 = QtWidgets.QSpacerItem(12, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacer3)
		self.replaceCheckBox = QtWidgets.QCheckBox(self.searchWidget)
		self.replaceCheckBox.setObjectName("replaceCheckBox")
		self.horizontalLayout_5.addWidget(self.replaceCheckBox)
		self.verticalLayout_3.addWidget(self.searchWidget)
		self.replaceWidget = QtWidgets.QWidget(self.searchWidgetInEditor)
		self.replaceWidget.setObjectName("replaceWidget")
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.replaceWidget)
		self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_4.setSpacing(0)
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.replaceLineEdit = QtWidgets.QLineEdit(self.replaceWidget)
		self.replaceLineEdit.setObjectName("replaceLineEdit")
		self.horizontalLayout_4.addWidget(self.replaceLineEdit)
		spacer4 = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacer4)
		self.replaceButton = QtWidgets.QPushButton(self.replaceWidget)
		self.replaceButton.setObjectName("replaceButton")
		self.horizontalLayout_4.addWidget(self.replaceButton)
		self.replaceAllButton = QtWidgets.QPushButton(self.replaceWidget)
		self.replaceAllButton.setObjectName("replaceAllButton")
		self.horizontalLayout_4.addWidget(self.replaceAllButton)

		self.verticalLayout_3.addWidget(self.replaceWidget)
		self.verticalLayout.addWidget(self.searchWidgetInEditor)

		self.editor = TextEdit(self.editorWidget)
		self.editor.document().setDocumentMargin(16)
		self.editor.setObjectName("editor")
		self.editor.setFrameStyle(QtWidgets.QFrame.NoFrame)
		self.editor.setMinimumWidth(400)
		self.verticalLayout.addWidget(self.editor)

		# self.attachmentWidget = AttachmentWidget( self.tabWidget )
		# self.attachmentWidget.setObjectName( 'attachment' )

		# self.tabWidget.addTab( self.editorWidget, 'Editor' )
		# self.tabWidget.addTab( self.attachmentWidget, 'Attachments' )
		# self.tabFrameLayout.addWidget( self.editorWidget )
		self.horizontalLayout_3.addWidget(self.editorWidget)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)


	def retranslateUi(self, Form):
		Form.setWindowTitle("Form")
		self.newFileButton.setText("File")
		self.newFolderButton.setText("Folder")
		self.searchLineBoxInEditor.setPlaceholderText("Find")
		self.prevWordButton.setText("<")
		self.nextWordButton.setText(">")
		self.doneButton.setText("Done")
		self.replaceCheckBox.setText("Replace")
		self.replaceLineEdit.setPlaceholderText("Replace")
		self.replaceButton.setText("Replace")
		self.replaceAllButton.setText("All")


class MainWidget(Ui_Form, QtWidgets.QWidget):
	def __init__(self, config, root, parent = None):
		super(MainWidget, self).__init__(parent)
		self.rootFolder = root
		self.currentFolder = self.rootFolder
		self.timer = QtCore.QTimer(self)
		self.startFirst = False
		self.startLast = False
		self.config = config
		self.styleItems = map(lambda item: StyleItem.create(item), self.config.get('patterns'))
		self.setupUi(self)
		self.initSignalsAndSlots()
		self.initialize()


	def initialize(self):
		self.editor.setAcceptDrops(True)
		self.fileListView.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
		self.enterFolderShortcut = QtWidgets.QShortcut(self.fileListView)
		self.enterFolderShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.enterFolderShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))
		self.enterFolderShortcut.activated.connect(self.changeNextFolder)

		self.deleteItemShortCut = QtWidgets.QShortcut(self.fileListView)
		self.deleteItemShortCut.setContext(QtCore.Qt.WidgetShortcut)
		self.deleteItemShortCut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Backspace))
		self.deleteItemShortCut.activated.connect(self.delete)

		self.focusListShortCut = QtWidgets.QShortcut(self)
		self.focusListShortCut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.focusListShortCut.setKey(QtGui.QKeySequence('Ctrl+L'))
		self.focusListShortCut.activated.connect(self.changeFocus)

		self.nextWordSearchWordShortcut = QtWidgets.QShortcut(self.searchWidgetInEditor)
		self.nextWordSearchWordShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.nextWordSearchWordShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))
		self.nextWordSearchWordShortcut.activated.connect(self.nextSearchText)
		self.cdShortcut = QtWidgets.QShortcut(self)
		self.cdShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.cdShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Escape))
		self.cdShortcut.activated.connect(self.changePrevFolder)
		self.pinnedFileShortcut = QtWidgets.QShortcut(self.parent())
		self.pinnedFileShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.pinnedFileShortcut.setKey(QtGui.QKeySequence('Ctrl+P'))
		self.pinnedFileShortcut.activated.connect(self.pinnedItem)

		self.fileListView.setModel(self.currentFolder.fileListModel)
		self.fileListView.setEditor(self)
		if self.rootFolder.isEmpty():
			self.newFile()
		else:
			self.loadFile(self.currentFolder.fileListModel.index(0))

		self.highlighter = Highlighter(self.editor, self.styleItems)
		self.searchLineBoxInEditor.setPlaceholderText('Find')
		self.searchLineBoxInFileList.setPlaceholderText('Search')
		self.searchWidgetInEditor.hide()
		self.replaceWidget.hide()
		self.fileListWidget.setMaximumWidth(200)
		searchFormat = QtGui.QTextCharFormat()
		searchFormat.setBackground(QtGui.QColor('yellow'))
		searchStyle = StyleItem('search', '', None, None, None, None, None, None, 'yellow', None)
		self.rule = HighlightingRule(self.editor)
		self.rule.style = searchStyle
		self.highlighter.highlightingRules.append(self.rule)
		self.rule.pattern = re.compile('')
		self.editor.setFocus()
		self.fileListView.setAcceptDrops(True)
		self.fileListView.setDragEnabled(True)
		self.currentFolder.fileListModel.modelReset.connect(self.setCurrentIndexOfListView)


	def initSignalsAndSlots(self):
		self.doneButton.clicked.connect(self.hideSearchWidgetInEditor)
		self.prevWordButton.clicked.connect(self.prevSearchText)
		self.nextWordButton.clicked.connect(self.nextSearchText)
		self.searchLineBoxInEditor.textChanged.connect(self.searchWord)
		self.newFileButton.clicked.connect(self.newFile)
		self.newFolderButton.clicked.connect(self.newFolder)
		self.searchLineBoxInFileList.textChanged.connect(self.searchFileNames)
		self.fileListView.currentIndexChanged.connect(self.loadFile)
		self.currentFolder.fileListModel.dataUpdated.connect(self.titleNameChanged)
		self.timer.timeout.connect(self.saveFile)
		self.fileListView.doubleClicked.connect(self.changeNextFolder)
		self.replaceCheckBox.stateChanged.connect(
				lambda value: self.replaceWidget.show() if value else self.replaceWidget.hide())
		self.replaceAllButton.clicked.connect(self.replaceAllText)
		self.replaceButton.clicked.connect(self.replaceText)
		self.editor.document().contentsChange.connect(self.contentChanged)


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


	def changeFocus(self):
		# changed focus between editor and list
		if self.fileListView.hasFocus():
			self.editor.setFocus()
		else:
			self.fileListView.setFocus()


	def replaceText(self):
		cursor = self.replaceNextText(self.editor.textCursor())
		self.editor.setTextCursor(cursor)
		self.nextSearchText()


	def pinnedItem(self):
		index = self.fileListView.currentIndex()
		data = index.internalPointer()
		data.setFixed(not data.isFixed)
		if data.isFixed:
			index.model().moveItem(index.row(), 0)
		self.fileListView.update()


	def replaceNextText(self, cursor):
		oldWord = self.searchLineBoxInEditor.text()
		if oldWord and cursor.hasSelection():
			newWord = self.replaceLineEdit.text()
			cursor.beginEditBlock()
			cursor.insertText(newWord)
			cursor.endEditBlock()
		return cursor


	def searchWord(self, text):
		self.rule.pattern = re.compile(text)
		self.updateEditor()


	def updateEditor(self):
		cursor = self.editor.textCursor()
		cursor.setPosition(0)
		block = cursor.block()
		position = cursor.position()
		firstPosition = position
		while block.isValid():
			position = block.position() + len(block.text())
			block = block.next()
		self.editor.document().contentsChange.disconnect(self.contentChanged)
		self.editor.document().contentsChange.emit(firstPosition, 0, position)
		self.editor.document().contentsChange.connect(self.contentChanged)


	def showSearch(self):
		self.searchWidgetInEditor.show()
		text = self.editor.textCursor().selectedText()
		self.searchLineBoxInEditor.setText(text)
		self.searchLineBoxInEditor.setFocus()


	def newFile(self):
		filename = self.generateFileName()
		f = open(filename, "w+")
		now = datetime.datetime.now()
		defaultName = 'New Note'
		displayName, result = QtWidgets.QInputDialog.getText(self, 'Note Name', 'Enter a note name',
															 text = defaultName)
		if not result or not displayName:
			return

		index = self.currentFolder.fileListModel.insertData(
				FileListItem(filename, displayName, lastUpdate = now.strftime("%Y-%m-%d %H:%M")), 0)
		self.titleNameChanged()
		f.close()
		index = self.currentFolder.fileListModel.index(index)
		if index.isValid():
			self.loadFile(index)


	def newFolder(self):
		folderName = self.generateFolderName()
		os.makedirs(folderName)
		defaultName = 'New Folder'
		displayName, result = QtWidgets.QInputDialog.getText(self, 'Folder Name', 'Enter a folder name',
															 text = defaultName)
		if not result or not displayName:
			return
		newFolder = FolderListItem(folderName, displayName, self.currentFolder)
		self.currentFolder.fileListModel.insertData(newFolder, 0)
		self.titleNameChanged()


	def changePrevFolder(self):
		parent = self.currentFolder.parent
		if self.searchWidgetInEditor.isVisible():
			self.hideSearchWidgetInEditor()
		elif parent:
			self.saveFile()
			oldFolder = self.currentFolder
			self.currentFolder.currentFilePath = None
			self.searchLineBoxInFileList.setText('')
			self.currentFolder.fileListModel.dataUpdated.disconnect(self.titleNameChanged)
			self.currentFolder = parent
			self.currentFolder.fileListModel.dataUpdated.connect(self.titleNameChanged)
			index = parent.fileListModel.getIndex(oldFolder.filename)
			index = parent.fileListModel.index(index)
			self.fileListView.setModel(parent.fileListModel)
			if index.isValid():
				parent.loadFile(editor = self.editor)
				self.fileListView.setCurrentIndex(index)
			self.pathTextLabel.setText(parent.title)
			self.currentFolder.currentFilePath = None
		else:
			print 'Folder is root folder'
			exit(0)


	def changeNextFolder(self):
		data = self.currentFolder.fileListModel.getItem(self.fileListView.currentIndex().row())
		self.changeFolder(data)


	def changeFolder(self, data):
		if isinstance(data, FolderListItem):
			self.saveFile()
			self.searchLineBoxInFileList.setText('')
			self.editor.document().blockSignals(True)
			self.fileListView.setModel(data.fileListModel)
			self.currentFolder.fileListModel.dataUpdated.disconnect(self.titleNameChanged)
			self.currentFolder.currentFilePath = None
			data.currentFilePath = None
			self.currentFolder = data
			self.currentFolder.fileListModel.dataUpdated.connect(self.titleNameChanged)
			self.editor.clear()
			self.pathTextLabel.setText(data.title)
			self.editor.document().blockSignals(False)


	def searchFileNames(self, text):
		self.currentFolder.fileListModel.search(text)
		self.fileListWidget.update()


	def titleNameChanged(self):
		# fixme ilerde bunu o an degisen klasor icin yap su an herseyi tekrardan yapıyor
		with open(fileListPath, 'w') as outfile:
			json.dump(self.rootFolder.json(), outfile)


	def setCurrentIndexOfListView(self):
		index = self.currentFolder.fileListModel.getIndex(self.currentFolder.currentFilePath)
		if index != -1:
			index = self.currentFolder.fileListModel.index(index)
			if index.isValid():
				self.fileListView.setCurrentIndex(index)


	def saveItemsStyle(self):
		with open('editor.conf', 'w') as outfile:
			dict = {}
			dict['patterns'] = map(lambda item: item.json(), self.styleItems)
			json.dump(dict, outfile)


	def generateFileName(self):
		filename = self.currentFolder.generateFileName()
		return filename


	def generateFolderName(self):
		folder = self.currentFolder.generateFolderName()
		return folder


	def loadFile(self, index):
		if not index.isValid():
			return
		data = self.currentFolder.fileListModel.getItem(index.row())
		self.saveFile()
		self.fileListView.setCurrentIndex(index)
		self.editor.document().contentsChange.disconnect(self.contentChanged)
		data.loadFile(editor = self.editor)
		self.editor.document().contentsChange.connect(self.contentChanged)
		self.currentFolder.currentFilePath = data.filename


	def saveFile(self):
		if self.currentFolder.currentFilePath:
			if os.path.isdir(self.currentFolder.currentFilePath):
				return
			file = open(self.currentFolder.currentFilePath, 'w')
			file.write(self.editor.toHtml())
			file.close()
			self.timer.stop()
			self.editor.document().setModified(False)


	def delete(self):
		index = self.fileListView.currentIndex()
		if self.fileListView.model().flags(index) & ItemFlags.ItemIsSoftLink:
			return
		result = QtWidgets.QMessageBox.warning(self, 'Are you sure?', 'Item will be deleted',
											   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if result == QtWidgets.QMessageBox.No:
			return

		if self.currentFolder.fileListModel.flags(index) & ItemFlags.ItemIsDeletable:
			data = self.currentFolder.fileListModel.getItem(index.row())
			self.currentFolder.fileListModel.deleteItem(data)
			if data:
				try:
					if data.type == FileType.FILE:
						os.remove(data.filename)
					elif data.type == FileType.FOLDER:
						shutil.rmtree(data.filename)
				except OSError as e:
					print "Failed with:", e.strerror

				self.titleNameChanged()
				self.currentFolder.currentFilePath = None
				index = self.currentFolder.fileListModel.index(0)
				if index.isValid():
					self.loadFile(index)


	def contentChanged(self, pos, rem, add):
		index = self.currentFolder.fileListModel.getIndex(self.currentFolder.currentFilePath)
		file_ = self.currentFolder.fileListModel.getItem(index)
		# update date of the file
		now = datetime.datetime.now()
		newDate = now.strftime("%Y-%m-%d %H:%M")
		if file_.lastUpdate != newDate:
			file_.lastUpdate = newDate
			self.fileListView.update()

		if index != -1 and index != 0:
			self.currentFolder.fileListModel.moveItem(index, 0)
			self.titleNameChanged()
		self.timer.start(600)


	def reformatBlocks(self):
		print 'reformated'


	def getFirstVisibleCursor(self):
		return self.editor.cursorForPosition(QtCore.QPoint(0, 0))


	def hideSearchWidgetInEditor(self):
		self.searchWord('')
		self.searchWidgetInEditor.hide()


	def openPreferences(self):
		preferences = Preferences(self, preferences = self.styleItems)
		preferences.acceptPreferences.connect(self.closePreferences)
		preferences.open()


	def closePreferences(self, patterns):
		self.styleItems = patterns
		self.highlighter.updateHighlighterRules(patterns)
		self.highlighter.highlightingRules.append(self.rule)
		self.updateEditor()
		self.saveItemsStyle()
