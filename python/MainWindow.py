import json
import os

from PySide import QtCore, QtGui
from MainWidget import MainWidget
from python.models import FileListItem
from python.path import iconPath, editorPath, fileListPath, stylePath, projectPath
from python.preferencesDialogue import Preferences

class MainWindow( QtGui.QMainWindow ):
    def __init__( self, parent = None ):
        super( MainWindow, self ).__init__( parent )
        self.resize( 800, 600 )
        self.filename = os.path.join( os.getcwd(), 'untitled.txt' )
        self.confFileList = self.readConfFile()
        if self.confFileList is None:
            self.confFileList = {'patterns': []}

        self.mainWidget = MainWidget( self.confFileList, self.readFileList(), self )
        self.editor = self.mainWidget.editor
        self.setupEditor()
        self.setupFileMenu()
        self.setupHelpMenu()
        self.setCentralWidget( self.mainWidget )
        self.setWindowTitle( 'TodoList' )
        self.initSignalsAndSlots()
        self.initialize()


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
            fileListFile = open( fileListPath, 'r' )
            fileList = json.load( fileListFile )
            return map( lambda item: FileListItem( item.get( 'filename' ), item.get( 'title' ) ), fileList )
        except:
            return None


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
        fileMenu = QtGui.QMenu( 'File', self )
        self.menuBar().addMenu( fileMenu )
        action = QtGui.QAction( self )
        action.triggered.connect( self.mainWidget.newFile )
        action.setShortcut( QtGui.QKeySequence.New )
        action.setText(
            QtGui.QApplication.translate( "MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8 ) )
        fileMenu.addAction( action )

        action = QtGui.QAction( self )
        action.triggered.connect( self.mainWidget.saveFile )
        action.setShortcut( QtGui.QKeySequence.Save )
        action.setText(
            QtGui.QApplication.translate( "MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8 ) )
        fileMenu.addAction( action )
        action = QtGui.QAction( self )
        action.triggered.connect( self.mainWidget.showSearch )
        action.setShortcut( QtCore.Qt.CTRL + QtCore.Qt.Key_F )
        action.setText(
            QtGui.QApplication.translate( "MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8 ) )
        fileMenu.addAction( action )
        fileMenu.addSeparator()
        action = QtGui.QAction( self )
        action.triggered.connect( self.mainWidget.openPreferences )
        action.setShortcut( QtGui.QKeySequence( 'Ctrl+Alt+S' ) )
        action.setText(
            QtGui.QApplication.translate( "MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8 ) )
        fileMenu.addAction( action )


    def setupHelpMenu( self ):
        helpMenu = QtGui.QMenu( "&Help", self )
        self.menuBar().addMenu( helpMenu )

        action = QtGui.QAction( self )
        action.triggered.connect( self.about )
        action.setText(
            QtGui.QApplication.translate( "MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8 ) )
        helpMenu.addAction( action )


    @QtCore.Slot()
    def about( self ):
        QtGui.QMessageBox.about( self, "About Syntax Highlighter",
                                 """<p>The <b>Syntax Highlighter</b> example shows how 
                                     to perform simple syntax highlighting by subclassing 
                                     the QSyntaxHighlighter class and describing 
                                     highlighting rules using regular expressions.</p>""" )


    def updateMainWindowTitle( self, change ):
        if change and self.windowTitle().find( '*' ) == -1:
            self.setWindowTitle( '%s*' % self.windowTitle() )
        elif not change and self.windowTitle().find( '*' ) != -1:
            self.setWindowTitle( '%s' % self.windowTitle()[:-1] )
