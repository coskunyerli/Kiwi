# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created: Sun Jun 10 14:33:14 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import os
import re
import json
import glob
from PySide import QtCore, QtGui

from HighLighting import HighlightingRule, Highlighter
from python.models import FileListModel, FileListItem, StyleItem
from python.path import filesPath, filePath, fileListPath
from python.preferencesDialogue import Preferences

class Ui_Form( object ):
    def setupUi( self, Form ):
        Form.setObjectName( "Form" )
        Form.resize( 868, 516 )
        self.horizontalLayout_3 = QtGui.QHBoxLayout( Form )
        self.horizontalLayout_3.setObjectName( "horizontalLayout_3" )
        self.fileListWidget = QtGui.QWidget( Form )
        sizePolicy = QtGui.QSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred )
        sizePolicy.setHorizontalStretch( 0 )
        sizePolicy.setVerticalStretch( 0 )
        sizePolicy.setHeightForWidth( self.fileListWidget.sizePolicy().hasHeightForWidth() )
        self.fileListWidget.setSizePolicy( sizePolicy )
        self.fileListWidget.setObjectName( "fileListWidget" )
        self.verticalLayout_2 = QtGui.QVBoxLayout( self.fileListWidget )
        self.verticalLayout_2.setContentsMargins( 0, 0, 0, 0 )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.searchWidgetInFileList = QtGui.QWidget( self.fileListWidget )
        self.searchWidgetInFileList.setObjectName( "searchWidgetInFileList" )
        self.horizontalLayout_2 = QtGui.QHBoxLayout( self.searchWidgetInFileList )
        self.horizontalLayout_2.setContentsMargins( 0, 0, 0, 0 )
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.searchLineBoxInFileList = QtGui.QLineEdit( self.searchWidgetInFileList )
        self.searchLineBoxInFileList.setObjectName( "searchLineBoxInFileList" )
        self.horizontalLayout_2.addWidget( self.searchLineBoxInFileList )
        self.newFileButton = QtGui.QPushButton( self.searchWidgetInFileList )
        self.newFileButton.setObjectName( "newFileButton" )
        self.horizontalLayout_2.addWidget( self.newFileButton )
        self.verticalLayout_2.addWidget( self.searchWidgetInFileList )
        self.fileListView = QtGui.QListView( self.fileListWidget )
        self.fileListView.setObjectName( "fileListView" )
        self.verticalLayout_2.addWidget( self.fileListView )
        self.horizontalLayout_3.addWidget( self.fileListWidget )
        self.editorWidget = QtGui.QWidget( Form )
        sizePolicy = QtGui.QSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred )
        sizePolicy.setHorizontalStretch( 1 )
        sizePolicy.setVerticalStretch( 0 )
        sizePolicy.setHeightForWidth( self.editorWidget.sizePolicy().hasHeightForWidth() )
        self.editorWidget.setSizePolicy( sizePolicy )
        self.editorWidget.setObjectName( "editorWidget" )
        self.verticalLayout = QtGui.QVBoxLayout( self.editorWidget )
        self.verticalLayout.setContentsMargins( 0, 0, 0, 0 )
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.searchWidgetInEditor = QtGui.QWidget( self.editorWidget )
        self.searchWidgetInEditor.setObjectName( "searchWidgetInEditor" )
        self.verticalLayout_3 = QtGui.QVBoxLayout( self.searchWidgetInEditor )
        self.verticalLayout_3.setContentsMargins( 0, 0, 0, 0 )
        self.verticalLayout_3.setObjectName( "verticalLayout_3" )
        self.searchWidget = QtGui.QWidget( self.searchWidgetInEditor )
        self.searchWidget.setObjectName( "searchWidget" )
        self.horizontalLayout = QtGui.QHBoxLayout( self.searchWidget )
        self.horizontalLayout.setContentsMargins( -1, 0, -1, 0 )
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.searchLineBoxInEditor = QtGui.QLineEdit( self.searchWidget )
        self.searchLineBoxInEditor.setObjectName( "searchLineBoxInEditor" )
        self.horizontalLayout.addWidget( self.searchLineBoxInEditor )
        self.prevWordButton = QtGui.QPushButton( self.searchWidget )
        self.prevWordButton.setObjectName( "prevWordButton" )
        self.horizontalLayout.addWidget( self.prevWordButton )
        self.nextWordButton = QtGui.QPushButton( self.searchWidget )
        self.nextWordButton.setObjectName( "nextWordButton" )
        self.horizontalLayout.addWidget( self.nextWordButton )
        self.doneButton = QtGui.QPushButton( self.searchWidget )
        self.doneButton.setObjectName( "doneButton" )
        self.horizontalLayout.addWidget( self.doneButton )
        self.replaceCheckBox = QtGui.QCheckBox( self.searchWidget )
        self.replaceCheckBox.setObjectName( "replaceCheckBox" )
        self.horizontalLayout.addWidget( self.replaceCheckBox )
        self.verticalLayout_3.addWidget( self.searchWidget )
        self.replaceWidget = QtGui.QWidget( self.searchWidgetInEditor )
        self.replaceWidget.setObjectName( "replaceWidget" )
        self.horizontalLayout_4 = QtGui.QHBoxLayout( self.replaceWidget )
        self.horizontalLayout_4.setContentsMargins( -1, 0, -1, 0 )
        self.horizontalLayout_4.setObjectName( "horizontalLayout_4" )
        self.replaceLineEdit = QtGui.QLineEdit( self.replaceWidget )
        self.replaceLineEdit.setObjectName( "replaceLineEdit" )
        self.replaceLineEdit.setPlaceholderText( 'Replace' )
        self.horizontalLayout_4.addWidget( self.replaceLineEdit )
        self.replaceButton = QtGui.QPushButton( self.replaceWidget )
        self.replaceButton.setObjectName( "replaceButton" )
        self.horizontalLayout_4.addWidget( self.replaceButton )
        self.replaceAllButton = QtGui.QPushButton( self.replaceWidget )
        self.replaceAllButton.setObjectName( "replaceAllButton" )
        self.horizontalLayout_4.addWidget( self.replaceAllButton )
        self.verticalLayout_3.addWidget( self.replaceWidget )
        self.verticalLayout.addWidget( self.searchWidgetInEditor )
        self.editor = QtGui.QPlainTextEdit( self.editorWidget )
        self.editor.setObjectName( "editor" )
        self.verticalLayout.addWidget( self.editor )
        self.horizontalLayout_3.addWidget( self.editorWidget )

        self.retranslateUi( Form )
        QtCore.QMetaObject.connectSlotsByName( Form )


    def retranslateUi( self, Form ):
        Form.setWindowTitle( QtGui.QApplication.translate( "Form", "Form", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.newFileButton.setText( QtGui.QApplication.translate( "Form", "+", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.prevWordButton.setText( QtGui.QApplication.translate( "Form", "<", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.nextWordButton.setText( QtGui.QApplication.translate( "Form", ">", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.doneButton.setText( QtGui.QApplication.translate( "Form", "Done", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.replaceCheckBox.setText(
            QtGui.QApplication.translate( "Form", "Replace", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.replaceButton.setText(
            QtGui.QApplication.translate( "Form", "Replace", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.replaceAllButton.setText(
            QtGui.QApplication.translate( "Form", "All", None, QtGui.QApplication.UnicodeUTF8 ) )

class MainWidget( Ui_Form, QtGui.QWidget ):
    def __init__( self, config, fileList, parent = None ):
        super( MainWidget, self ).__init__( parent )
        self.fileList = fileList
        self.currentFileItem = None
        self.fileListModel = FileListModel( self.fileList )
        self.timer = QtCore.QTimer( self )
        self.config = config
        self.styleItems = map( lambda item: StyleItem.create( item ), self.config.get( 'patterns' ) )
        self.setupUi( self )
        self.initSignalsAndSlots()
        self.initialize()


    def initialize( self ):
        self.fileListView.setAttribute( QtCore.Qt.WA_MacShowFocusRect, 0 )
        self.deleteItemShortCut = QtGui.QShortcut( self.fileListView )
        self.deleteItemShortCut.setContext( QtCore.Qt.WidgetShortcut )
        self.deleteItemShortCut.setKey( QtGui.QKeySequence( QtCore.Qt.Key_Backspace ) )
        self.deleteItemShortCut.activated.connect( self.deleteItemFromFileList )
        self.reformatShortCut = QtGui.QShortcut( self.editor )
        self.reformatShortCut.setContext( QtCore.Qt.WidgetShortcut )
        self.reformatShortCut.setKey( QtGui.QKeySequence( 'Ctrl+Alt+K' ) )
        self.reformatShortCut.activated.connect( self.reformatBlocks )
        self.quitSearchWordShortcut = QtGui.QShortcut( self.searchLineBoxInEditor )
        self.quitSearchWordShortcut.setContext( QtCore.Qt.WidgetShortcut )
        self.quitSearchWordShortcut.setKey( QtGui.QKeySequence( QtCore.Qt.Key_Escape ) )
        self.quitSearchWordShortcut.activated.connect( self.hideSearchWidgetInEditor )
        self.fileListView.setModel( self.fileListModel )
        if self.fileList is None or len( self.fileList ) <= 0:
            if not os.path.isdir( filePath ):
                os.makedirs( filePath )
            if not os.path.isdir( filesPath ):
                os.makedirs( filesPath )
            self.newFile()
        self.loadFile( self.fileListModel.index( 0 ) )

        self.highlighter = Highlighter( self.editor, self.styleItems )
        self.searchLineBoxInEditor.setPlaceholderText( 'Search' )
        self.searchLineBoxInFileList.setPlaceholderText( 'Search' )
        self.searchWidgetInEditor.hide()
        self.replaceWidget.hide()
        self.fileListWidget.setMaximumWidth( 200 )
        searchFormat = QtGui.QTextCharFormat()
        searchFormat.setBackground( QtGui.QColor( 'yellow' ) )
        self.rule = HighlightingRule( self.editor )
        self.rule.format = searchFormat
        self.highlighter.highlightingRules.append( self.rule )
        self.rule.pattern = re.compile( '' )
        self.editor.setFocus()
        self.fileListView.setAcceptDrops( True )
        self.fileListView.setDragEnabled( True )
        self.fileListView.setDragDropMode( QtGui.QAbstractItemView.InternalMove )


    def initSignalsAndSlots( self ):
        self.doneButton.clicked.connect( self.hideSearchWidgetInEditor )
        self.prevWordButton.clicked.connect( self.prevSearchText )
        self.nextWordButton.clicked.connect( self.nextSearchText )
        self.searchLineBoxInEditor.textChanged.connect( self.searchWord )
        self.newFileButton.clicked.connect( self.newFile )
        self.searchLineBoxInFileList.textChanged.connect( self.searchFileNames )
        self.fileListView.clicked.connect( self.loadFile )
        self.fileListModel.dataUpdated.connect( self.titleNameChanged )
        self.timer.timeout.connect( self.saveFile )
        self.editor.document().contentsChanged.connect( self.contentChanged )
        self.replaceCheckBox.stateChanged.connect(
            lambda value: self.replaceWidget.show() if value else self.replaceWidget.hide() )
        self.replaceAllButton.clicked.connect( self.replaceAllText )
        self.replaceButton.clicked.connect( self.replaceText )


    def nextSearchText( self ):
        cursor = self.editor.textCursor()
        block = cursor.block()
        text = block.text()[cursor.positionInBlock():]
        while block.isValid():
            matches = self.rule.search( text )
            for match in matches:
                cursor.setPosition( block.position() + match.end() )
                self.editor.setTextCursor( cursor )
                self.editor.setFocus()
                return

            block = block.next()
            text = block.text()


    def prevSearchText( self ):
        cursor = self.editor.textCursor()
        block = cursor.block()
        text = block.text()[0:cursor.positionInBlock()]
        while block.isValid():
            matches = self.rule.search( text )
            for match in matches:
                cursor.setPosition( block.position() + match.end() )
                self.editor.setTextCursor( cursor )
                self.editor.setFocus()
                return

            block = block.previous()
            text = block.text()


    def replaceAllText( self ):
        oldWord = self.searchLineBoxInEditor.text()
        if oldWord:
            newWord = self.replaceLineEdit.text()
            block = self.editor.document().firstBlock()
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            while block.isValid():
                text = block.text()
                if text.find( oldWord ) != -1:
                    tcursor = QtGui.QTextCursor( block )
                    tcursor.select( QtGui.QTextCursor.BlockUnderCursor )
                    tcursor.removeSelectedText()
                    tcursor.clearSelection()
                    newText = text.replace( oldWord, newWord )
                    tcursor.insertBlock()
                    tcursor.insertText( newText )
                block = block.next()
            cursor.endEditBlock()


    def replaceText( self ):
        cursor = self.replaceNextText( self.editor.textCursor() )
        self.editor.setTextCursor( cursor )


    def replaceNextText( self, cursor ):
        oldWord = self.searchLineBoxInEditor.text()
        if oldWord:
            newWord = self.replaceLineEdit.text()
            cursor.beginEditBlock()
            block = cursor.block()
            while block.isValid():
                text = block.text()
                if text.find( oldWord ) != -1:
                    tcursor = QtGui.QTextCursor( block )
                    tcursor.select( QtGui.QTextCursor.BlockUnderCursor )
                    tcursor.removeSelectedText()
                    tcursor.clearSelection()
                    newText = text.replace( oldWord, newWord )
                    tcursor.insertBlock()
                    tcursor.insertText( newText )
                    return tcursor
                block = block.next()
            cursor.endEditBlock()


    def searchWord( self, text ):
        self.rule.pattern = re.compile( text )
        self.updateEditor()


    def updateEditor( self ):
        cursor = self.getFirstVisibleCursor()
        block = cursor.block()
        position = cursor.position()
        firstPosition = position
        while block.isValid():
            position = block.position() + len( block.text() )
            block = block.next()
        self.editor.document().contentsChange.emit( firstPosition, position, position )


    def showSearch( self ):
        self.searchWidgetInEditor.show()
        text = self.editor.textCursor().selectedText()
        self.searchLineBoxInEditor.setText( text )
        self.searchLineBoxInEditor.setFocus()


    def newFile( self ):
        filename = self.generateFileName()
        f = open( filename, "w+" )
        self.fileListModel.insertData( FileListItem( filename, 'New Note' ), 0 )
        self.titleNameChanged( None, None, None )
        f.close()
        index = self.fileListModel.index( 0 )
        if index.isValid():
            self.loadFile( index )


    def searchFileNames( self, text ):
        self.fileListModel.search( text )
        self.fileListWidget.update()


    def titleNameChanged( self, old, new, index ):
        with open( fileListPath, 'w' ) as outfile:
            json.dump( self.fileListModel.json(), outfile )


    def saveItemsStyle( self ):
        with open( 'editor.conf', 'w' ) as outfile:
            dict = {}
            dict['patterns'] = map( lambda item: item.json(), self.styleItems )
            json.dump( dict, outfile )


    def generateFileName( self ):
        allTextFiles = glob.glob( "%s/*.txt" % filesPath )
        filename = '%s/file%d.txt' % (filesPath, len( allTextFiles ))
        return filename


    def loadFile( self, index ):
        self.fileListView.setCurrentIndex( index )
        self.saveFile()
        data = self.fileListModel.getItem( index.row() )
        if self.currentFileItem != data.filename:
            file = open( data.filename, 'r' )
            #
            self.editor.document().contentsChanged.disconnect( self.contentChanged )
            text = file.read().decode( 'utf-8' )
            if text == '':
                self.editor.document().blockSignals( True )
                self.editor.clear()
                self.editor.document().blockSignals( False )
            else:
                self.editor.setPlainText( text )
            self.editor.document().contentsChanged.connect( self.contentChanged )
            file.close()
            self.currentFileItem = data.filename


    def saveFile( self ):
        if self.currentFileItem:
            file = open( self.currentFileItem, 'w' )
            file.write( self.editor.toPlainText() )
            file.close()

        self.editor.document().setModified( False )


    def deleteItemFromFileList( self ):
        index = self.fileListView.currentIndex()
        data = self.fileListModel.removeData( index )

        if data:
            try:
                os.remove( data.filename )
            except OSError as e:  # name the Exception `e`
                print "Failed with:", e.strerror  # look what it says
                print "Error code:", e.code

            self.titleNameChanged( None, None, None )
            self.currentFileItem = None
            self.loadFile( self.fileListModel.index( 0 ) )


    def contentChanged( self ):
        index = self.fileListModel.getIndex( self.currentFileItem )
        if index != -1 and index != 0:
            self.fileListModel.moveItem( index, 0 )
            self.titleNameChanged( None, None, None )
        self.timer.start( 600 )


    def reformatBlocks( self ):
        print 'reformated'


    def getFirstVisibleCursor( self ):
        return self.editor.cursorForPosition( QtCore.QPoint( 0, 0 ) )


    def hideSearchWidgetInEditor( self ):
        self.searchWord( '' )
        self.searchWidgetInEditor.hide()


    def openPreferences( self ):
        preferences = Preferences( self, preferences = self.styleItems )
        preferences.acceptPreferences.connect( self.closePreferences )
        preferences.open()


    def closePreferences( self, patterns ):
        self.styleItems = patterns
        self.highlighter.updateHighlighterRules( patterns )
        self.highlighter.highlightingRules.append( self.rule )
        self.updateEditor()
        self.saveItemsStyle()
