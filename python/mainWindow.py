import json
import os

from PySide2 import QtCore, QtGui, QtWidgets
from mainWidget import MainWidget
from models import FileListItem, FolderListItem
from enums import FileType
from path import editorPath, fileListPath, stylePath, filePath, filesPath


class MainWindow( QtWidgets.QMainWindow ):
	def __init__( self, parent = None ):
		super( MainWindow, self ).__init__( parent )
		self.resize( 800, 600 )
		self.filename = os.path.join( os.getcwd(), 'untitled.txt' )
		self.confFileList = self.readConfFile()
		if self.confFileList is None:
			self.confFileList = { 'patterns': [] }

		if not os.path.isdir( filePath ):
			os.makedirs( filePath )
		if not os.path.isdir( filesPath ):
			os.makedirs( filesPath )

		root = self.readFileList()
		self.mainWidget = MainWidget( self.confFileList, root, self )
		self.editor = self.mainWidget.editor
		self.setupEditor()
		self.setupFileMenu()
		self.setupHelpMenu()
		self.setCentralWidget( self.mainWidget )
		self.setWindowTitle( 'TodoList' )
		self.initSignalsAndSlots()
		self.initialize()
		self.visible = False

	def readConfFile( self ):
		confFile = open( editorPath, 'r' )
		try:
			config = json.load( confFile )
		except:
			confFile.close()
			return None
		return config

	def readFileList( self ):
		try:
			try:
				fileListFile = open( fileListPath, 'r' )
				fileList = json.loads( fileListFile.read() )
			except Exception, e:
				print 'Json Loading Error', str( e )
				fileList = { 'filename': filesPath, 'title': 'root', 'files': [] }
			rootFolder = FolderListItem( fileList['filename'], fileList['title'], None )
			self._readFileList( rootFolder, fileList['files'] )
			return rootFolder
		except Exception, e:
			print 'Process Error', str( e )
			return None

	def _readFileList( self, folder, json ):
		for file in json:
			if file['type'] == FileType.FILE:
				folder.fileListModel.insertData( FileListItem( file.get( 'filename' ), file.get( 'title' ) ) )
			elif file['type'] == FileType.FOLDER:
				subFolder = FolderListItem( file['filename'], file['title'], folder )
				folder.fileListModel.insertData( subFolder )
				self._readFileList( subFolder, file['files'] )

	def initSignalsAndSlots( self ):
		self.editor.document().modificationChanged.connect( self.updateMainWindowTitle )

	def initialize( self ):
		pass

	def setupEditor( self ):
		font = QtGui.QFont()
		font.setFamily( 'Menlo' )
		font.setFixedPitch( True )
		font.setPointSize( 12 )
		self.editor.setFont( font )
		self.setStyleSheet( open( stylePath, 'r' ).read() )

	def setupFileMenu( self ):
		fileMenu = QtWidgets.QMenu( 'File', self )
		self.menuBar().addMenu( fileMenu )
		action = QtWidgets.QAction( self )
		action.triggered.connect( self.mainWidget.newFile )
		action.setShortcut( QtGui.QKeySequence.New )
		action.setText( "New" )
		fileMenu.addAction( action )

		action = QtWidgets.QAction( self )
		action.triggered.connect( self.test )
		action.setShortcut( QtCore.Qt.CTRL + QtCore.Qt.Key_G )
		action.setText( "Save" )
		fileMenu.addAction( action )
		action = QtWidgets.QAction( self )
		action.triggered.connect( self.mainWidget.showSearch )
		action.setShortcut( QtCore.Qt.CTRL + QtCore.Qt.Key_F )
		action.setText( "Search" )
		fileMenu.addAction( action )
		fileMenu.addSeparator()
		action = QtWidgets.QAction( self )
		action.triggered.connect( self.mainWidget.openPreferences )
		action.setShortcut( QtGui.QKeySequence( 'Ctrl+Alt+S' ) )
		action.setText( "Preferences" )
		fileMenu.addAction( action )

	def test( self ):
		block = self.editor.document().begin().next().next().next()
		self.editor.document().documentLayout().setBlockVisible( block, self.visible )
		self.visible = not self.visible

	def setupHelpMenu( self ):
		helpMenu = QtWidgets.QMenu( "&Help", self )
		self.menuBar().addMenu( helpMenu )

		action = QtWidgets.QAction( self )
		action.triggered.connect( self.about )
		action.setText("About" )
		helpMenu.addAction( action )

	@QtCore.Slot()
	def about( self ):
		QtWidgets.QMessageBox.about( self, "About TodoList application",
									 """<p>The <b>TodoList</b> example shows how 
										 to perform simple syntax highlighting by subclassing 
										 the QSyntaxHighlighter class and describing 
										 highlighting rules using regular expressions.</p>""" )

	def updateMainWindowTitle( self, change ):
		if change and self.windowTitle().find( '*' ) == -1:
			self.setWindowTitle( '%s*' % self.windowTitle() )
		elif not change and self.windowTitle().find( '*' ) != -1:
			self.setWindowTitle( '%s' % self.windowTitle()[:-1] )
