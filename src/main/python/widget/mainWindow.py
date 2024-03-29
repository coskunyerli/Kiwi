import os

import static, logging as log
from PySide2 import QtCore, QtGui, QtWidgets
from service.preferencesService import PreferencesService

from service.saveListModelService import SaveListModelFolderItemService
from widget.mainWidget import MainWidget
from widget.toast import Toast


class MainWindow(QtWidgets.QMainWindow, SaveListModelFolderItemService, PreferencesService):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.visible = False

		self.setMinimumHeight(600)

		root = self.readFileList()
		self.mainWidget = MainWidget(root, self)
		self.setting = QtCore.QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope, "TodoList", "todo")
		self.setupFileMenu()
		self.setupHelpMenu()
		self.setCentralWidget(self.mainWidget)
		self.setWindowTitle('Kiwi')
		self.initSignalsAndSlots()
		self.initShortcuts()
		self.initialize()

		self.readSetting()


	def readFileList(self):
		rootFolder = self.saveListModelService().load()
		return rootFolder


	def initShortcuts(self):
		self.closeAppShortcut = QtWidgets.QShortcut(self)
		self.closeAppShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.closeAppShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Escape))
		self.closeAppShortcut.activated.connect(self.close)


	def initSignalsAndSlots(self):
		self.mainWidget.fileTreeModel.dataChanged.connect(self.saveFileModel)
		self.mainWidget.fileTreeModel.rowsInserted.connect(self.saveFileModel)
		self.mainWidget.fileTreeModel.rowsRemoved.connect(self.saveFileModel)
		self.mainWidget.fileTreeModel.rowsMoved.connect(self.saveFileModel)


	def saveFileModel(self):
		self.saveListModelService().save(self.mainWidget.fileTreeModel.rootFolder())


	def initialize(self):
		pass


	def setupFileMenu(self):
		fileMenu = QtWidgets.QMenu('File', self)
		self.menuBar().addMenu(fileMenu)
		action = QtWidgets.QAction(self)
		action.triggered.connect(self.mainWidget.newFile)
		action.setShortcut(QtGui.QKeySequence.New)
		action.setText("New File")

		actionFolder = QtWidgets.QAction(self)
		actionFolder.triggered.connect(self.mainWidget.newFolder)
		actionFolder.setShortcut(QtGui.QKeySequence('Ctrl+M'))
		actionFolder.setText("New Folder")

		fileMenu.addAction(action)
		fileMenu.addAction(actionFolder)
		fileMenu.addSeparator()
		action = QtWidgets.QAction(self)
		action.triggered.connect(self.mainWidget.openPreferences)
		action.setShortcut(QtGui.QKeySequence('Ctrl+Alt+S'))
		action.setText("Preferences")
		fileMenu.addAction(action)


	def closeEvent(self, event):
		self.saveSetting()
		super(MainWindow, self).closeEvent(event)


	def setupHelpMenu(self):
		helpMenu = QtWidgets.QMenu("&Help", self)
		self.menuBar().addMenu(helpMenu)

		action = QtWidgets.QAction(self)
		action.triggered.connect(self.about)
		action.setText("About")
		helpMenu.addAction(action)


	@QtCore.Slot()
	def about(self):
		QtWidgets.QMessageBox.about(self, "About Kiwi",
									"""<p>The <b>Kiwi</b> example shows how 
										to perform simple syntax highlighting by subclassing 
										the QSyntaxHighlighter class and describing 
										highlighting rules using regular expressions.</p>""")


	def readSetting(self):
		# read settings from setting file,
		# read lastly seen folder id
		error = lambda key: f'Read settings from setting file. Key is {key}'
		self.preferences().read(self.setting)
		try:
			folderID = static.getValueFromDict(self.setting.value('currentFolderID'), [int, None.__class__],
											   error('currentFolderID'))
			# read lastly seen item id
			itemID = static.getValueFromDict(self.setting.value('currentItemID'), [int, None.__class__],
											 error('currentItemID'))
			# if they are not none load it
			if folderID is not None:
				# find last seen folder
				currentFolderArray = self.mainWidget.fileTreeModel.find(lambda item: item.id() == folderID)
				if currentFolderArray:
					currentFolder = currentFolderArray[0]
					# update current folder
					self.mainWidget.fileListProxyModel.setCurrentFolder(currentFolder)
					self.mainWidget.breadCrumb.setPath(currentFolder)
					if itemID is not None:
						# find last item folder in current folder
						currentItemArray = currentFolder.find(lambda item: item.id() == itemID)
						if currentItemArray:
							currentItem = currentItemArray[0]
							itemChildNumber = currentItem.childNumber()
							if itemChildNumber is not None:
								self.mainWidget.fileListView.setCurrentIndex(QtCore.QModelIndex())
								currentItemIndex = self.mainWidget.fileListProxyModel.index(itemChildNumber)
								self.mainWidget.fileListView.setCurrentIndex(currentItemIndex)

			# read recursive search flag
			recursiveSearch = static.getValueFromDict(self.setting.value('enableRecursiveSearch'),
													  [bool, None.__class__],
													  error('enableRecursiveSearch'))
			if recursiveSearch is not None:
				self.mainWidget.flattenSearchCheckbox.setChecked(recursiveSearch)
		except ValueError as e:
			log.error(f'Setting is not loaded succesfully. Exception is {e}')
			Toast.error('Setting Error', 'Setting is not read successfully. Since file is invalid')
		except Exception as e:
			log.error(f'Unexpected value is occurred while reading settings file. Exception is {e}')
			Toast.error('Setting Error', 'Unexpected error is occurred while reading setting file')


	def saveSetting(self):
		# save last current folder, item and recursive search flag
		try:
			self.preferences().write(self.setting)
			folder = self.mainWidget.fileListProxyModel.sourceFolder()
			self.setting.setValue('currentFolderID', folder.id())
			currentItemIndex = self.mainWidget.fileListView.currentIndex()
			if currentItemIndex.isValid():
				itemID = currentItemIndex.data()[0]
				self.setting.setValue('currentItemID', itemID)

			self.setting.setValue('enableRecursiveSearch', self.mainWidget.flattenSearchCheckbox.isChecked())
		except Exception as e:
			log.error(f'Setting file is not ssaved succesfully. Exception is {e}')
