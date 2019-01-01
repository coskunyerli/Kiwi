from PySide2 import QtGui, QtCore, QtWidgets

from enums import ItemFlags, FileType


class FileViewDelagete( QtWidgets.QStyledItemDelegate ):
	def __init__( self, parent = None ):
		super( FileViewDelagete, self ).__init__( parent )

	def paint( self, painter, option, index ):
		pixmap = index.model().data( index, role = QtCore.Qt.DecorationRole ).pixmap( QtCore.QSize( 40, 40 ) )
		data = index.internalPointer()
		painter.setRenderHint( QtGui.QPainter.Antialiasing, True )
		rect = option.rect

		leftMargin = 16
		lineRect = QtCore.QRect( QtCore.QPoint( leftMargin, rect.bottom() ), QtCore.QSize( rect.width(), 1 ) )
		painter.fillRect( lineRect, QtGui.QColor( '#45464A' ) )

		if option.state & QtWidgets.QStyle.State_HasFocus:
			painter.fillRect( rect, QtGui.QBrush( QtGui.QColor( '#C9942F' ) ) )
		elif option.state & QtWidgets.QStyle.State_Selected:
			painter.fillRect( rect, QtGui.QBrush( QtGui.QColor( '#353639' ) ) )

		iconSize = QtCore.QSize( 16, 16 )
		iconRect = QtCore.QRect(
			rect.topLeft() + QtCore.QPoint( leftMargin, (rect.height() - iconSize.height()) / 2.0 ),
			iconSize )
		painter.drawPixmap( iconRect, pixmap, pixmap.rect() )

		painter.save()
		painter.setPen( QtGui.QColor( '#D3D7E3' ) )
		font = painter.font()
		font.setPointSize( 9 )
		painter.setFont( font )
		fontMetric = painter.fontMetrics()

		if data.type == FileType.FOLDER:

			text = '%d Items' % data.fileCount()
			folderItemRect = QtCore.QRect(
				rect.bottomRight() - QtCore.QPoint( fontMetric.width( text ) + 4, fontMetric.height() + 4 ),
				QtCore.QSize( fontMetric.width( text ), fontMetric.height() ) )

			painter.drawText( folderItemRect, QtCore.Qt.AlignLeft, text )

		elif data.type == FileType.FILE:
			if data.lastUpdate is not None:
				updateRect = QtCore.QRect(
					rect.bottomRight() - QtCore.QPoint( fontMetric.width( data.lastUpdate ) + 4,
														fontMetric.height() + 4 ),
					QtCore.QSize( fontMetric.width( data.lastUpdate ), fontMetric.height() ) )
				painter.drawText( updateRect, QtCore.Qt.AlignLeft, data.lastUpdate )

		painter.restore()

		textRect = rect.adjusted( iconRect.right() + 8, 0, 0, 0 )
		painter.drawText( textRect, QtCore.Qt.AlignVCenter, data.title )

	def sizeHint( self, option, index ):
		size = super( FileViewDelagete, self ).sizeHint( option, index )
		size.setHeight( 55 )
		return size


class ListView( QtWidgets.QListView ):
	currentIndexChanged = QtCore.Signal( QtCore.QModelIndex )

	def __init__( self, parent = None ):
		super( ListView, self ).__init__( parent )
		self.mainWidget = None
		self.setAcceptDrops( True )
		self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
		self.customContextMenuRequested.connect( self.showRightClickPopup )
		delegate = FileViewDelagete( self )
		self.setItemDelegate( delegate )

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


class ColorComboBox( QtWidgets.QComboBox ):
	def __init__( self, parent = None ):
		super( ColorComboBox, self ).__init__( parent )
		self.colors = { 'Red': '#940000', 'Blue': '#001294', 'Green': '#00942C' }
		keys = self.colors.keys()
		for i in range( len( keys ) ):
			colorname = keys[i]
			color = QtGui.QColor( self.colors[colorname] )
			self.addItem( colorname, color )
			index = self.model().index( i, 0 )
			self.model().setData( index, color, QtCore.Qt.BackgroundRole )

		delegate = ComboBoxItemDelegate( self )
		self.setItemDelegate( delegate )

	def getColors( self ):
		return map( lambda c: QtGui.QColor( c ), self.colors )

	def setCurrentIndex( self, index ):
		super( ColorComboBox, self ).setCurrentIndex( index )


class ComboBoxItemDelegate( QtWidgets.QStyledItemDelegate ):

	def paint( self, painter, option, index ):
		color = index.model().data( index, QtCore.Qt.BackgroundRole )
		colorname = index.model().data( index )
		rect = option.rect
		size = rect.size()
		offset = size.width() / 8.0

		if option.state & QtWidgets.QStyle.State_MouseOver:
			painter.fillRect( rect, QtGui.QBrush( QtGui.QColor( '#353639' ) ) )

		colorRect = QtCore.QRect( offset, rect.top() + 2, 1.5 * offset, size.height() - 4 )
		metric = painter.fontMetrics()
		path = QtGui.QPainterPath()
		path.addRoundedRect( colorRect, 5, 5 )
		painter.fillPath( path, color )
		textRect = QtCore.QRect( colorRect.right() + 8, colorRect.top(), metric.width( colorname ), metric.height() )
		painter.drawText( textRect, QtCore.Qt.AlignLeft, colorname )
