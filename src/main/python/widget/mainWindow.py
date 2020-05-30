import os
from PySide2 import QtCore, QtGui, QtWidgets

from service.saveListModelService import SaveListModelFolderItemService
from widget.mainWidget import MainWidget


class MainWindow(QtWidgets.QMainWindow, SaveListModelFolderItemService):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.visible = False

		self.resize(800, 600)

		root = self.readFileList()
		self.mainWidget = MainWidget(root, self)
		self.setting = QtCore.QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope, "TodoList", "todo")
		self.setupEditor()
		self.setupFileMenu()
		self.setupHelpMenu()
		self.setCentralWidget(self.mainWidget)
		self.setWindowTitle('TodoList')
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


	def setupEditor(self):
		font = QtGui.QFont()
		font.setFamily('Menlo')
		font.setFixedPitch(True)
		font.setPointSize(12)


	# self.mainWidget.editor.setFont(font)

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
		folderID = self.setting.value('currentFolderID', '')
		itemID = self.setting.value('currentItemID', '')
		if folderID is not None:
			currentFolderArray = self.mainWidget.fileTreeModel.find(lambda item: item.id() == folderID)
			if currentFolderArray:
				currentFolder = currentFolderArray[0]
				self.mainWidget.fileListProxyModel.setCurrentFolder(currentFolder)
				self.mainWidget.breadCrumb.setPath(currentFolder)
				if itemID is not None:
					currentItemArray = currentFolder.find(lambda item: item.id() == itemID)
					if currentItemArray:
						currentItem = currentItemArray[0]
						itemChildNumber = currentItem.childNumber()
						if itemChildNumber is not None:
							currentItemIndex = self.mainWidget.fileListProxyModel.index(itemChildNumber)
							self.mainWidget.fileListView.setCurrentIndex(currentItemIndex)


	def saveSetting(self):
		folder = self.mainWidget.fileListProxyModel.sourceFolder()
		self.setting.setValue('currentFolderID', folder.id())
		currentItemIndex = self.mainWidget.fileListView.currentIndex()
		if currentItemIndex.isValid():
			itemID = currentItemIndex.data()[0]
			self.setting.setValue('currentItemID', itemID)
