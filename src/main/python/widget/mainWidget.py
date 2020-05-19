# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created: Sun Jun 10 14:33:14 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import datetime
import logging as log
import os

import core
from PySide2 import QtCore, QtGui, QtWidgets
from delegate.dataViewDelegate import DataViewDelegate
from delegate.fileViewDelegate import FileViewDelegate
from exceptions.invalidListModelItemException import InvalidListModelItemException
from factory.dataDialogFactory import DataDialogFactory
from factory.dataFactory import DataFactory
from itemmodel.dataModel import DataModel
from itemmodel.listTreeModel import ListTreeModel
from enums import FileType, ItemFlags
from itemmodel.listModelItem import ListModelFileItem, ListModelFolderItem
from preferences.storyPreferencesDialogue import Preferences
from proxy.dataModelProxy import DataModelProxy
from proxy.fileListModelProxy import FileListModelProxy
from service.dataListModelService import DataListModelFolderItemService
from service.saveListModelService import SaveListModelFolderItemService
from widget.breadCrumbWidget import BreadCrumb
from widget.dialog.filePickerDialog import FilePickerDialog
from widget.dialog.textEditorDialog import TextEditorDialog
from widget.listView import ListView


class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(868, 516)

		self.breadCrumbWidgetLayout = QtWidgets.QVBoxLayout(Form)
		self.breadCrumbWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.breadCrumbWidgetLayout.setSpacing(0)

		self.breadCrumb = BreadCrumb(Form)
		qss = core.fbs.qss('breadCrumb.qss')
		if qss is not None:
			self.breadCrumb.setStyleSheet(qss)
		else:
			log.warning('breadCrumb.qss is not loaded successfully')
		self.mainWidget = QtWidgets.QWidget(Form)

		self.breadCrumbWidgetLayout.addWidget(self.breadCrumb)
		self.breadCrumbWidgetLayout.addWidget(self.mainWidget)

		self.mainWidgetLayout = QtWidgets.QHBoxLayout(self.mainWidget)
		self.mainWidgetLayout.setObjectName("horizontalLayout_3")
		self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.mainWidgetLayout.setSpacing(0)
		self.fileListWidget = QtWidgets.QWidget(self.mainWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.fileListWidget.sizePolicy().hasHeightForWidth())
		self.fileListWidget.setSizePolicy(sizePolicy)
		self.fileListWidget.setObjectName("fileListWidget")
		self.fileListWidgetLayout = QtWidgets.QVBoxLayout(self.fileListWidget)
		self.fileListWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.fileListWidgetLayout.setObjectName("verticalLayout_2")
		self.fileListWidgetLayout.setSpacing(6)
		self.searchWidgetInFileListWidget = QtWidgets.QWidget(self.fileListWidget)
		qss = core.fbs.qss('searchWidgetInFileList.qss')
		if qss is not None:
			self.searchWidgetInFileListWidget.setStyleSheet(qss)
		else:
			log.warning(f'Qss file is not loaded successfully. Filename is "searchLineBoxInFileList.qss"')

		self.searchWidgetInFileListWidget.setObjectName("searchWidgetInFileList")
		self.searchWidgetInFileListLayout = QtWidgets.QHBoxLayout(self.searchWidgetInFileListWidget)
		self.searchWidgetInFileListLayout.setContentsMargins(4, 0, 0, 0)
		self.searchWidgetInFileListLayout.setSpacing(6)

		self.searchLineBoxInFileList = QtWidgets.QLineEdit(self.searchWidgetInFileListWidget)
		self.searchLineBoxInFileList.setPlaceholderText('Search')
		self.searchLineBoxInFileList.setObjectName("searchLineBoxInFileList")

		self.flattenSearchCheckbox = QtWidgets.QCheckBox(self.searchLineBoxInFileList)
		self.flattenSearchCheckbox.setToolTip('Recursive Search')

		self.addFileWidget = QtWidgets.QWidget(self.fileListWidget)
		self.addFileWidget.setObjectName("addFileWidget")

		self.searchWidgetInFileListLayout.addWidget(self.searchLineBoxInFileList)
		self.searchWidgetInFileListLayout.addWidget(self.flattenSearchCheckbox)

		# self.searchWidgetInFileListLayout.addWidget(self.pathTextLabel)

		self.addFileWidgetLayout = QtWidgets.QHBoxLayout(self.addFileWidget)
		self.addFileWidgetLayout.setSpacing(0)
		self.addFileWidgetLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		self.addFileWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.addFileWidgetLayout.setObjectName("horizontalLayout_6")
		self.newFileButton = QtWidgets.QPushButton(self.addFileWidget)
		self.newFileButton.setObjectName("newFileButton")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(core.fbs.icons('baseline_insert_drive_file_white_48dp.png')))
		self.newFileButton.setIcon(icon)

		self.addFileWidgetLayout.addWidget(self.newFileButton)
		self.newFolderButton = QtWidgets.QPushButton(self.addFileWidget)
		self.newFolderButton.setEnabled(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(core.fbs.icons('baseline_create_new_folder_white_48dp.png')))
		self.newFolderButton.setIcon(icon)

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		self.searchLineBoxInFileList.setSizePolicy(sizePolicy)
		self.addFileWidgetLayout.addWidget(self.newFolderButton)

		self.fileListView = ListView(self.fileListWidget)
		delegate = FileViewDelegate(self)
		self.fileListView.setItemDelegate(delegate)
		self.fileListView.setObjectName("fileListView")

		self.fileListWidgetLayout.addWidget(self.addFileWidget)
		self.fileListWidgetLayout.addWidget(self.searchWidgetInFileListWidget)
		self.fileListWidgetLayout.addWidget(self.fileListView)
		self.mainWidgetLayout.addWidget(self.fileListWidget)

		self.dataViewWidget = QtWidgets.QFrame(self.mainWidget)
		self.dataViewWidget.setObjectName('dataViewWidget')
		self.dataViewWidgetLayout = QtWidgets.QVBoxLayout(self.dataViewWidget)
		self.dataViewWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.dataViewWidgetLayout.setSpacing(0)

		self.dataViewToolBar = QtWidgets.QFrame(self.dataViewWidget)
		self.dataViewToolBar.setObjectName('dataViewToolBar')
		self.dataViewToolBarLayout = QtWidgets.QHBoxLayout(self.dataViewToolBar)
		self.dataViewToolBarLayout.setContentsMargins(4, 4, 4, 0)
		self.dataViewToolBarLayout.setSpacing(0)

		self.addTextDataButton = QtWidgets.QPushButton(self.dataViewToolBar)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(core.fbs.icons('baseline_insert_drive_file_black_48dp.png')))
		self.addTextDataButton.setIcon(icon)

		self.addFileDataButton = QtWidgets.QPushButton(self.dataViewToolBar)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(core.fbs.icons('attach_file-black-18dp.svg')))
		self.addFileDataButton.setIcon(icon)

		self.searchLineEditInData = QtWidgets.QLineEdit(self.dataViewToolBar)
		self.searchLineEditInData.setPlaceholderText('Search')

		self.dataViewToolBarLayout.addWidget(self.addTextDataButton)
		self.dataViewToolBarLayout.addWidget(self.addFileDataButton)
		self.dataViewToolBarLayout.addItem(
				QtWidgets.QSpacerItem(4, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))
		self.dataViewToolBarLayout.addWidget(self.searchLineEditInData)

		self.dataView = ListView(self.dataViewWidget)
		dataViewDelegate = DataViewDelegate(self.dataView)
		self.dataView.setItemDelegate(dataViewDelegate)

		self.dataViewWidgetLayout.addWidget(self.dataViewToolBar)
		self.dataViewWidgetLayout.addWidget(self.dataView)

		qss = core.fbs.qss('dataView.qss')
		if qss is not None:
			self.dataViewWidget.setStyleSheet(qss)
		else:
			log.warning('Qss file is not loaded successfully. Filename is "dataView.qss"')

		self.mainWidgetLayout.addWidget(self.dataViewWidget)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)


	def retranslateUi(self, Form):
		Form.setWindowTitle("Form")
		self.newFileButton.setText("File")
		self.newFolderButton.setText("Folder")


class MainWidget(Ui_Form, QtWidgets.QWidget, SaveListModelFolderItemService, DataListModelFolderItemService):
	def __init__(self, root, parent = None):
		super(MainWidget, self).__init__(parent)

		self.setupUi(self)

		self.fileTreeModel = ListTreeModel()
		self.fileTreeModel.setRoot(root)

		self.fileListProxyModel = FileListModelProxy()
		# self.fileListProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.fileListProxyModel.setSourceModel(self.fileTreeModel)
		self.dataModel = DataModel(self.fileListProxyModel)

		self.dataProxyModel = DataModelProxy()
		self.dataProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.dataProxyModel.setSourceModel(self.dataModel)

		self.dataView.setModel(self.dataProxyModel)

		self.initializeShortcuts()
		self.initSignalsAndSlots()
		self.initialize()


	def initializeShortcuts(self):
		self.enterFolderShortcut = QtWidgets.QShortcut(self.fileListView)
		self.enterFolderShortcut.setContext(QtCore.Qt.WidgetShortcut)
		self.enterFolderShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Return))

		self.deleteItemShortCut = QtWidgets.QShortcut(self.fileListView)
		self.deleteItemShortCut.setContext(QtCore.Qt.WidgetShortcut)
		self.deleteItemShortCut.setKey(QtGui.QKeySequence('Ctrl+Backspace'))
		self.deleteItemShortCut.activated.connect(self.deleteListModelFileItem)

		self.focusListShortCut = QtWidgets.QShortcut(self)
		self.focusListShortCut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.focusListShortCut.setKey(QtGui.QKeySequence('Ctrl+L'))
		self.focusListShortCut.activated.connect(self.changeFocus)

		self.cdShortcut = QtWidgets.QShortcut(self)
		self.cdShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.cdShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Backspace))
		self.cdShortcut.activated.connect(self.changePrevFolder)

		self.pinnedFileShortcut = QtWidgets.QShortcut(self.parent())
		self.pinnedFileShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.pinnedFileShortcut.setKey(QtGui.QKeySequence('Ctrl+P'))
		self.pinnedFileShortcut.activated.connect(self.pinnedListModelFileItem)

		self.newTextFileShortcut = QtWidgets.QShortcut(self)
		self.newTextFileShortcut.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
		self.newTextFileShortcut.setKey(QtGui.QKeySequence('Ctrl+T'))
		self.newTextFileShortcut.activated.connect(self.createNewTextFile)


	def initialize(self):
		self.fileListView.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
		self.fileListView.setModel(self.fileListProxyModel)

		self.fileListWidget.setMaximumWidth(200)
		self.fileListView.setAcceptDrops(True)
		self.fileListView.setDragEnabled(True)
		self.breadCrumb.setPath(self.fileListProxyModel.currentFolder())

		if self.fileListProxyModel.isEmpty() is False:
			self.fileListView.setCurrentIndex(self.fileListProxyModel.index(0))

		self.flattenSearchCheckbox.setChecked(self.fileListProxyModel.hasRecursiveSearch())


	def initSignalsAndSlots(self):
		self.newFileButton.clicked.connect(self.newFile)
		self.newFolderButton.clicked.connect(self.newFolder)
		self.fileListView.currentIndexChanged.connect(self.loadFile)
		self.fileListView.dragTimeout.connect(self.updateCurrentFolder)

		self.enterFolderShortcut.activated.connect(self.changeNextFolder)
		self.fileListView.doubleClicked.connect(self.changeNextFolder)
		self.dataView.doubleClicked.connect(self.openData)
		self.breadCrumb.clicked.connect(self.clickedBreadCrumb)
		self.fileListView.customContextMenuRequested.connect(self.showRightClickPopupForListView)
		self.dataView.customContextMenuRequested.connect(self.showRightClickPopupForDataView)

		self.searchLineBoxInFileList.textChanged.connect(self.searchFileListView)
		self.searchLineEditInData.textChanged.connect(self.searchDataView)

		self.dataModel.dataChanged.connect(self.saveDataModel)
		self.dataModel.rowsInserted.connect(self.saveDataModel)
		self.dataModel.rowsRemoved.connect(self.saveDataModel)
		self.dataModel.rowsMoved.connect(self.saveDataModel)

		self.addTextDataButton.clicked.connect(self.createNewTextFile)
		self.addFileDataButton.clicked.connect(self.createNewFile)

		self.dataModel.modelReset.connect(self.updateDataWidget)
		self.breadCrumb.dropped.connect(self.dropItemToBreadCrumb)

		self.flattenSearchCheckbox.stateChanged.connect(self.updateRecursiveSearchFlag)


	def updateRecursiveSearchFlag(self, value):
		self.fileListProxyModel.setRecursiveSearch(bool(value))


	def openData(self, index):
		data = index.data(QtCore.Qt.UserRole)
		dialog = DataDialogFactory.create(data, self)
		if dialog is not None:
			qss = core.fbs.qss('dataShowDialog.qss')
			if qss is not None:
				dialog.setStyleSheet(qss)
			else:
				log.warning('dataShowDialog.qss is not loaded successfully')
			dialog.open()
		else:
			QtWidgets.QMessageBox.warning(self, 'Unsupported Data', 'Data is not upsupported')


	def changeFocus(self):
		# changed focus between editor and list
		if self.fileListView.hasFocus():
			self.editor.setFocus()
		else:
			self.fileListView.setFocus()


	def dropItemToBreadCrumb(self, fileItemList, mimeData):
		return
		self.fileListProxyModel.dropMimeData(mimeData, None, -1, -1, QtCore.QModelIndex())


	def pinnedListModelFileItem(self):
		index = self.fileListView.currentIndex()
		data, old = self.fileListProxyModel.beginEditData(index)
		data.setFixed(not data.isFixed)
		if data.isFixed:
			self.fileTreeModel.moveRow(index.parent(), index.row(), index.parent(), 0)

		self.fileListProxyModel.endEditData(index)
		self.fileListView.update()


	def searchFileListView(self):
		text = self.searchLineBoxInFileList.text()
		self.fileListProxyModel.setSearchText(text)
		return


	# self.fileListProxyModel.setFilterRegExp(text)

	def searchDataView(self, text):
		self.dataProxyModel.setFilterRegExp(text)


	def newFile(self):
		now = datetime.datetime.now()
		defaultName = 'New Note'
		displayName, result = QtWidgets.QInputDialog.getText(self, 'Note Name', 'Enter a note name',
															 text = defaultName)
		if not result or not displayName:
			return
		newFile = ListModelFileItem(ListModelFileItem.IDGenerator(), displayName, None, lastUpdate = now)
		try:
			self.dataListModelService().save(newFile)
			i = self.fileListProxyModel.insertData(newFile, 0)
			index = self.fileListProxyModel.index(i)
			self.fileListView.setCurrentIndex(index)
		# Save root file into disc
		except InvalidListModelItemException as e:
			log.warning(e)
		except Exception as e:
			log.warning(f'Data is not inserted successfully, Exception is {e}')


	def newFolder(self):
		defaultName = 'New Folder'
		displayName, result = QtWidgets.QInputDialog.getText(self, 'Folder Name', 'Enter a folder name',
															 text = defaultName)
		if not result or not displayName:
			return

		newFolder = ListModelFolderItem(ListModelFileItem.IDGenerator(), displayName, None)
		try:
			i = self.fileListProxyModel.insertData(newFolder, 0)
			index = self.fileListProxyModel.index(i)
			self.fileListView.setCurrentIndex(index)
		# Save root file into disc
		except InvalidListModelItemException as e:
			log.warning(e)
		except Exception as e:
			log.warning(f'Data is not inserted successfully, Exception is {e}')


	def createNewTextFile(self):
		if self.dataModel.hasFileItem() is True:
			textEditorDialog = TextEditorDialog(self)
			textEditorDialog.fileSaved.connect(self.insertDataToDataModel)
			textEditorDialog.open()


	def createNewFile(self):
		if self.dataModel.hasFileItem() is True:
			dialog = FilePickerDialog(self)
			value = dialog.exec_()
			if value == QtWidgets.QDialog.Accepted and dialog.data.isValid():
				data = dialog.data
				fileData = DataFactory.fileDataFromDialogData(data)
				if fileData is not None:
					self.insertDataToDataModel(fileData)


	def updateDataWidget(self):
		dataListModelItem = self.dataModel.listModelFileItem()
		if dataListModelItem is not None:
			self.dataViewWidget.setEnabled(True)
		else:
			self.dataViewWidget.setDisabled(True)


	def saveDataModel(self):
		self.dataListModelService().save(self.dataModel.listModelFileItem())


	def insertDataToDataModel(self, dataModelItem):
		listFileItem = self.dataModel.listModelFileItem()
		childNumber = listFileItem.childNumber()

		index = self.fileListProxyModel.index(childNumber)
		_, _ = self.fileListProxyModel.beginEditData(index)
		self.dataModel.insertData(dataModelItem)
		self.dataListModelService().save(self.dataModel.listModelFileItem())
		self.fileListProxyModel.endEditData(index)


	def changePrevFolder(self):
		currentFolder = self.fileListProxyModel.currentFolder()
		parent = currentFolder.parent()
		if parent is not None:
			childNumber = currentFolder.childNumber()
			if childNumber is not None:
				self.changeFolder(parent)
				self.fileListView.setCurrentIndex(self.fileListProxyModel.index(childNumber))


	def changeNextFolder(self):
		listModelFileItem = self.fileListView.currentIndex().data(QtCore.Qt.UserRole)
		if listModelFileItem.type == FileType.FOLDER:
			self.fileListView.setCurrentIndex(QtCore.QModelIndex())
			self.changeFolder(listModelFileItem)


	def changeFolder(self, listModelFolderItem):
		if isinstance(listModelFolderItem, ListModelFolderItem):
			self.fileListProxyModel.setCurrentFolder(listModelFolderItem)
			self.updateBreadCrumb()


	def clickedBreadCrumb(self, folder):
		self.fileListView.setCurrentIndex(QtCore.QModelIndex())
		self.changeFolder(folder)


	def updateBreadCrumb(self):
		listModelFileItem = self.fileListProxyModel.sourceFolder()
		if listModelFileItem.type == FileType.FOLDER:
			self.breadCrumb.setPath(listModelFileItem)


	def updateCurrentFolder(self, index):
		if index.isValid() is True:
			fileListItem = index.data(QtCore.Qt.UserRole)
			if fileListItem.type == FileType.FOLDER:
				self.changeFolder(fileListItem)


	def loadFile(self, index):
		if index.isValid() is False:
			self.dataModel.setListModelFileItem(None)
		else:
			fileListItem = index.data(QtCore.Qt.UserRole)
			if fileListItem.type == FileType.FILE:
				self.dataListModelService().load(fileListItem)
				self.dataModel.setListModelFileItem(fileListItem)
			else:
				self.dataModel.setListModelFileItem(None)


	def deleteListModelFileItem(self):
		index = self.fileListView.currentIndex()

		if index.isValid() is False:
			return
		if self.fileListView.model().flags(index) & ItemFlags.ItemIsSoftLink:
			return
		result = QtWidgets.QMessageBox.warning(self, 'Are you sure?', 'Item will be deleted',
											   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if result == QtWidgets.QMessageBox.No:
			return
		if self.fileListProxyModel.flags(index) & ItemFlags.ItemIsDeletable:
			listModelFileItem = self.fileListProxyModel.deleteRow(index)
			self.dataListModelService().deleteListModelFileItem(listModelFileItem)
			if self.fileListProxyModel.isEmpty() is False:
				index = self.fileListProxyModel.index(0)
				self.fileListView.setCurrentIndex(index)


	def deleteDataModelItem(self):
		index = self.dataView.currentIndex()
		result = QtWidgets.QMessageBox.warning(self, 'Are you sure?', 'Item will be deleted',
											   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if result == QtWidgets.QMessageBox.No:
			return

		dataModelItem = self.dataModel.deleteRow(index)
		self.dataListModelService().deleteDataModelItem(dataModelItem)


	def renameDataModelItem(self):
		index = self.dataView.currentIndex()
		if index.isValid():
			data = index.data(QtCore.Qt.UserRole)
			listModelFileItem = self.dataModel.listModelFileItem()
			fileListIndex = self.fileListProxyModel.index(listModelFileItem.childNumber())
			newText, result = QtWidgets.QInputDialog.getText(self, 'Rename File', 'New Data Name', text = data.name)
			if result and fileListIndex.isValid():
				self.fileListProxyModel.beginEditData(fileListIndex)
				self.dataModel.beginEditData(index)
				data.setName(newText)
				self.dataModel.endEditData(index)
				self.fileListProxyModel.endEditData(fileListIndex)


	def openPreferences(self):
		preferences = Preferences(self, None)
		preferences.open()


	#
	#
	# def closePreferences(self, patterns):
	# 	self.styleItems = patterns
	# 	self.highlighter.updateHighlighterRules(patterns)
	# 	self.highlighter.highlightingRules.append(self.rule)
	# 	self.updateEditor()
	# 	self.saveItemsStyle()

	def showRightClickPopupForDataView(self, pos):
		if self.dataModel.listModelFileItem() is None or self.dataModel.listModelFileItem().type == FileType.FOLDER:
			return

		globalPos = self.dataView.mapToGlobal(pos)
		contextMenu = QtWidgets.QMenu()
		index = self.dataView.indexAt(pos)
		rename = ''
		delete = ''
		if index.isValid():
			rename = contextMenu.addAction('Rename')
			delete = contextMenu.addAction('Delete')
			contextMenu.addSeparator()
		newText = contextMenu.addAction('New Text File')
		newText.setShortcut(QtGui.QKeySequence('Ctrl+T'))
		newText.setShortcutVisibleInContextMenu(True)

		newImage = contextMenu.addAction('New Image File')
		newImage.setShortcut(QtGui.QKeySequence('Ctrl+I'))
		newImage.setShortcutVisibleInContextMenu(True)

		newData = contextMenu.addAction('New Data')
		newData.setShortcut(QtGui.QKeySequence('Ctrl+D'))
		newData.setShortcutVisibleInContextMenu(True)
		action = contextMenu.exec_(globalPos)

		if action == newText:
			self.createNewTextFile()
		elif action == rename:
			self.renameDataModelItem()
		elif action == delete:
			self.deleteDataModelItem()
		elif action == newImage:
			self.createNewFile()


	def showRightClickPopupForListView(self, pos):

		globalPos = self.fileListView.mapToGlobal(pos)
		index = self.fileListView.indexAt(pos)
		contextMenu = QtWidgets.QMenu()

		fixItem = ''
		renameItem = ''
		deleteItem = ''
		passwordItem = ''
		addTag = ''
		if index.isValid():
			model = self.fileListProxyModel
			dataList = index.data()
			isFixed = dataList[3]
			isLocked = dataList[5]

			if not model.flags(index) & ItemFlags.ItemIsSoftLink:
				fixItem = contextMenu.addAction('Unpin Note' if isFixed else 'Pin Note')
				addTag = contextMenu.addAction('Add Tag')
				renameItem = contextMenu.addAction("Rename")
				deleteItem = contextMenu.addAction('Delete')
				contextMenu.addSeparator()
				if isLocked is False:
					passText = "Set Password"
				else:
					passText = "Remove Password"
					if isLocked:
						lockText = 'Unlock'
					else:
						lockText = 'Lock'

					lockItem = contextMenu.addAction(lockText)
				passwordItem = contextMenu.addAction(passText)

			contextMenu.addSeparator()
		newFile = contextMenu.addAction('New Note')
		newFolder = contextMenu.addAction('New Folder')

		action = contextMenu.exec_(globalPos)

		if action == renameItem:
			self.renameListModelFileItem()
		elif action == deleteItem:
			self.deleteListModelFileItem()
		elif action == newFile:
			self.newFile()
		elif action == newFolder:
			self.newFolder()
		elif action == fixItem:
			self.pinnedListModelFileItem()

		elif action == addTag:
			self.addTagListModelFileItem()


	# elif action == passwordItem:
	# 	self.setPassword()

	def renameListModelFileItem(self):
		index = self.fileListView.currentIndex()
		model = self.fileListProxyModel
		newText, result = QtWidgets.QInputDialog.getText(self, 'Rename File', 'New file name', text = index.data()[1])
		if result:
			data, old = model.beginEditData(index)
			data.setName(newText)
			data.setDisplayName(newText)
			model.endEditData(index)


	def addTagListModelFileItem(self):
		index = self.fileListView.currentIndex()
		model = self.fileListProxyModel
		listModelFileItem = index.data(QtCore.Qt.UserRole)
		text = ';'.join(listModelFileItem.tags)
		newTagText, result = QtWidgets.QInputDialog.getText(self, 'Tags', 'New tags', text = text)
		if result:
			model.beginEditData(index)
			listModelFileItem.tags = set(filter(lambda item: item != '', newTagText.split(';')))
			model.endEditData(index)
# def setPassword(self):
# 	return
# 	index = self.fileListView.currentIndex()
# 	password, result = QtWidgets.QInputDialog.getText(self, 'Set Password', 'Enter a password',
# 													  QtWidgets.QLineEdit.Password)
# 	if password and result and index.isValid():
# 		data = index.internalPointer()
# 		data.isLocked = True
