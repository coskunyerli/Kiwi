import subprocess
from PySide2 import QtGui, QtCore, QtWidgets

from enums import ItemFlags


class ListView( QtWidgets.QListView ):
	currentIndexChanged = QtCore.Signal( QtCore.QModelIndex )

	def __init__( self, parent = None ):
		super( ListView, self ).__init__( parent )
		self.mainWidget = None
		self.setAcceptDrops( True )
		self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
		self.customContextMenuRequested.connect( self.showRightClickPopup )

	def setEditor( self, mainWidget ):
		self.mainWidget = mainWidget

	def currentChanged( self, current, old ):
		self.currentIndexChanged.emit( current )
		super( ListView, self ).currentChanged( current, old )

	def showRightClickPopup( self, pos ):
		globalPos = self.mapToGlobal( pos )
		index = self.currentIndex()
		model = self.model()
		contextMenu = QtWidgets.QMenu()
		renameItem = contextMenu.addAction( "Rename" )
		deleteItem = contextMenu.addAction( 'Delete' )
		contextMenu.addSeparator()
		newFile = contextMenu.addAction( 'New Note' )
		newFolder = contextMenu.addAction( 'New Folder' )

		renameItem.setEnabled( model.flags( index ) & ItemFlags.ItemIsEditable )
		deleteItem.setEnabled( model.flags( index ) & ItemFlags.ItemIsDeletable )
		action = contextMenu.exec_( globalPos )

		if action == renameItem:
			self.rename()
		elif action == deleteItem:
			self.delete()
		elif action == newFile:
			self.newFile()
		elif action == newFolder:
			self.newFolder()

	def rename( self ):
		index = self.currentIndex()
		model = self.model()
		newText, result = QtWidgets.QInputDialog.getText( self, 'Rename File', 'New file name',
														  QtWidgets.QLineEdit.Normal )
		if result:
			model.setData( index, newText )

	def delete( self ):
		self.mainWidget.delete()

	def newFile( self ):
		self.mainWidget.newFile()

	def newFolder( self ):
		self.mainWidget.newFolder()


class TextEdit( QtWidgets.QTextEdit ):
	def dragEnterEvent( self, event ):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()
		else:
			super( TextEdit, self ).dragEnterEvent( event )

	def dragMoveEvent( self, event ):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()
		else:
			super( TextEdit, self ).dragMoveEvent( event )

	def dropEvent( self, event ):
		urls = event.mimeData().urls()
		if urls:
			file_ = urls[0].path()
			image = QtGui.QImage( file_ )
			if not image.isNull():
				cursor = self.textCursor()
				cursor.beginEditBlock()
				cursor.insertHtml( """ <img src='%s' width='%d'/> """ % (
					file_, self.document().pageSize().width() - 2 * self.document().documentMargin()) )
				cursor.insertBlock()
				cursor.endEditBlock()
