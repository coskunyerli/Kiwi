import os
from PySide2 import QtCore, QtGui, QtWidgets

from service.saveListModelService import SaveListModelFolderItemService
from widget.mainWidget import MainWidget


class MainWindow(QtWidgets.QMainWindow, SaveListModelFolderItemService):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.resize(800, 600)

		root = self.readFileList()
		self.mainWidget = MainWidget(root, self)
		self.setting = QtCore.QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope, "TodoList", "todo")
		self.setupEditor()
		self.setupFileMenu()
		self.setupHelpMenu()
		self.setCentralWidget(self.mainWidget)
		self.setWindowTitle('TodoList')
		self.readSetting()
		self.initSignalsAndSlots()
		self.initShortcuts()
		self.initialize()
		self.visible = False


	def readFileList(self):
		rootFolder = self.saveListModelService().load()
		return rootFolder


	def initShortcuts(self):
		self.closeAppShortcut = QtWidgets.QShortcut(self)
		self.closeAppShortcut.setContext(QtCore.Qt.ApplicationShortcut)
		self.closeAppShortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_Escape))
		self.closeAppShortcut.activated.connect(self.close)


	def initSignalsAndSlots(self):
		self.mainWidget.fileListView.currentIndexChanged.connect(self.updateMainWindowTitle)
		self.mainWidget.fileListModel.dataChanged.connect(self.saveFileModel)
		self.mainWidget.fileListModel.rowsInserted.connect(self.saveFileModel)
		self.mainWidget.fileListModel.rowsRemoved.connect(self.saveFileModel)
		self.mainWidget.fileListModel.rowsMoved.connect(self.saveFileModel)


	def saveFileModel(self):
		self.saveListModelService().save(self.mainWidget.fileListModel.rootFolder())


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
		QtWidgets.QMessageBox.about(self, "About TodoList application",
									"""<p>The <b>TodoList</b> example shows how 
										to perform simple syntax highlighting by subclassing 
										the QSyntaxHighlighter class and describing 
										highlighting rules using regular expressions.</p>""")


	def readSetting(self):
		return
		path = self.setting.value('currentPath', '')


	# list_ = path.split('/')
	# filename = filesPath
	# for folder in list_:
	# 	filename = os.path.join(filename, folder)
	# 	index = self.mainWidget.currentFolder.fileListModel.getIndex(filename)
	# 	if index == -1:
	# 		continue
	# 	folder = self.mainWidget.currentFolder.fileListModel.getItem(index)
	# 	if isinstance(folder, FolderListItem):
	# 		self.mainWidget.changeFolder(folder)
	# 	else:
	# 		self.mainWidget.loadFile(self.mainWidget.currentFolder.fileListModel.index(index))

	def saveSetting(self):
		return


	# folder = self.mainWidget.currentFolder
	# path = os.path.join(folder.path(),
	# 					os.path.basename(folder.currentFilePath) if folder.currentFilePath is not None else '')
	# self.setting.setValue('currentPath', path)

	def updateMainWindowTitle(self, newIndex):
		return
		if newIndex.isValid() is False:
			listModelFileItem = self.mainWidget.fileListModel.currentFolder()
		else:
			listModelFileItem = newIndex.data(QtCore.Qt.UserRole)
		self.setWindowTitle(listModelFileItem.path())
