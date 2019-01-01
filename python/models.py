import copy

import os
from PySide2 import QtCore, QtGui, QtWidgets

from enums import ItemFlags, FileType
from path import iconsPath


class StyleItem( object ):
	def __init__( self, name, pattern, family, size, bold, strikeout, italic,
				  color, background, enumarationClass ):
		super( StyleItem, self ).__init__()
		self.name = name
		self.pattern = pattern
		self.enumarationClass = enumarationClass
		self._blockCharFormat = QtGui.QTextCharFormat()
		if family and size:
			font = QtGui.QFont( family, size )
			self._blockCharFormat.setFont( font )
		if italic:
			self._blockCharFormat.setFontItalic( bool( italic ) )
		if bold:
			self._blockCharFormat.setFontWeight( QtGui.QFont.Bold if bold else QtGui.QFont.Normal )
		if strikeout:
			self._blockCharFormat.setFontStrikeOut( bool( strikeout ) )
		if color:
			color = QtGui.QColor( color )
			self._blockCharFormat.setForeground( QtGui.QBrush( color ) )
		if background:
			self._blockCharFormat.setBackground( QtGui.QBrush( QtGui.QColor( background ) ) )
		else:
			self._blockCharFormat.setBackground( QtGui.QBrush() )

	def __str__( self ):
		return '%s %s' % (self.name, self._blockCharFormat.foreground().color().name())

	def __repr__( self ):
		return self.__str__()

	def json( self ):
		background = self.charFormat.background().color().name() if self.charFormat.background().isOpaque() else None
		return { 'name': self.name, 'pattern': self.pattern, 'family': self.charFormat.fontFamily(),
				 'size': self.charFormat.fontPointSize(), 'bold': self.charFormat.fontWeight() == QtGui.QFont.Bold,
				 'strikeout': self.charFormat.fontStrikeOut(), 'italic': self.charFormat.fontItalic(),
				 'color': self.charFormat.foreground().color().name(),
				 'next': self.enumarationClass if self.enumarationClass else None,
				 'background': background }

	@property
	def charFormat( self ):
		return self._blockCharFormat

	def setCharFormat( self, format ):
		self._blockCharFormat = format

	def copy( self ):
		return StyleItem.create( self.json() )

	@staticmethod
	def create( dictItem ):
		return StyleItem( dictItem['name'], dictItem['pattern'], dictItem.get( 'family', 'Courier' ),
						  dictItem.get( 'size', 12 ),
						  dictItem.get( 'bold', False ),
						  dictItem.get( 'strikeout', False ), dictItem.get( 'italic', False ),
						  dictItem.get( 'color', 'white' ), dictItem.get( 'background', None ),
						  dictItem.get( 'next', None ) )


class FileListItem( object ):
	def __init__( self, filename, title, isFixed = False, lastUpdate = None ):
		self.isFixed = isFixed
		self.filename = filename
		self.title = title
		self.type = FileType.FILE
		self.lastUpdate = lastUpdate

	def loadFile( self, **kwargs ):
		editor = kwargs.get( 'editor' )
		editor.setEnabled( True )
		file = open( self.filename, 'r' )

		text = file.read().decode( 'utf-8' )
		if text == '':
			editor.document().blockSignals( True )
			editor.clear()
			editor.document().blockSignals( False )
		else:
			editor.setHtml( text )

		file.close()

	def __str__( self ):
		return '%s_%s' % (self.type, self.title)

	def __repr__( self ):
		return self.__str__()

	def json( self ):
		return { 'filename': self.filename, 'title': self.title, 'type': self.type, 'lastUpdate': self.lastUpdate }

	@classmethod
	def create( cls, dict ):
		return FileListItem( dict['filename'], dict['title'], lastUpdate = dict.get( 'lastUpdate' ) )

	def setFixed( self, result ):
		self.isFixed = result


class FolderListItem( FileListItem ):
	def __init__( self, foldername, title, parent ):
		super( FolderListItem, self ).__init__( foldername, title )
		self.fileListModel = FileListModel( None, self )
		self.parent = None
		self.type = FileType.FOLDER
		self.currentFilePath = None
		self.setParent( parent, first = True )

	def fileCount( self ):
		if '..' in self.fileListModel:
			return self.fileListModel.rowCount() - 1
		else:
			return self.fileListModel.rowCount()

	def __eq__( self, other ):
		if other is not None:
			return self.filename == other.filename
		return False

	def setParent( self, parent, first = False ):
		if parent:
			if not first:
				self.fileListModel.deleteItem( self.parent )
			item = parent.copy()
			item.title = '..'
			item.setFixed( True )
			self.fileListModel.insertData( item, index = 0 )
			self.parent = parent

	def generateFileName( self ):
		filename = self.fileListModel.generateFileName()
		return os.path.join( self.filename, filename )

	def generateFolderName( self ):
		folder = self.fileListModel.generateFolderName()
		return os.path.join( self.filename, folder )

	def json( self ):
		json = super( FolderListItem, self ).json()
		json['files'] = self.fileListModel.json()
		json['parent'] = self.parent.filename if self.parent else None
		return json

	def loadFile( self, **kwargs ):
		editor = kwargs.get( 'editor' )
		editor.document().blockSignals( True )
		editor.clear()
		editor.document().blockSignals( False )
		editor.setEnabled( False )

	def copy( self ):
		item = FolderListItem( self.filename, self.title, self.parent )
		item.fileListModel = self.fileListModel
		return item

	def __str__( self ):
		return '[%s_%s => %s]' % (self.type, self.title, self.fileListModel)

	def __repr__( self ):
		return self.__str__()

	def isEmpty( self ):
		return self.fileListModel.isEmpty()

	@classmethod
	def create( cls, dict ):
		return FolderListItem( dict['filename'], dict['title'], None )


class FileListModel( QtCore.QAbstractListModel ):
	_updateDataSignal = QtCore.Signal( FileListItem, FileListItem, int )

	def __init__( self, fileList, parent ):
		super( FileListModel, self ).__init__()
		if fileList:
			self.allFileList = fileList
		else:
			self.allFileList = []
		self.fileList = copy.copy( self.allFileList )
		self.searchTitle = ''
		self._parent = parent

	def __str__( self ):
		fileList = filter( lambda item: item.title != '..', self.allFileList )
		return str( fileList )

	def __iter__( self ):
		return iter( self.fileList )

	def __contains__( self, item ):
		for data in self.fileList:
			if data.title == item:
				return True
		return False

	def flags( self, index ):
		data = self.fileList[index.row()]
		if data == self._parent.parent:
			return (
					QtCore.Qt.ItemIsDropEnabled |
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled
			)
		if isinstance( data, FolderListItem ):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDropEnabled |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)
		elif isinstance( data, FileListItem ):
			return (
					QtCore.Qt.ItemIsSelectable |
					QtCore.Qt.ItemIsEnabled |
					ItemFlags.ItemIsEditable |
					QtCore.Qt.ItemIsDragEnabled |
					ItemFlags.ItemIsDeletable
			)

	def index( self, row, col = 0, parent = QtCore.QModelIndex() ):
		if row >= self.rowCount():
			return QtCore.QModelIndex()
		data = self.fileList[row]
		return self.createIndex( row, col, data )

	def mimeData( self, indices ):
		mimeDat = super( FileListModel, self ).mimeData( indices )
		mimeDat.setText( ''.join( map( lambda index: str( index.row() ), indices ) ) )
		return mimeDat

	def dropMimeData( self, data, action, row, column, parent ):
		# fixme parent folderda bir sorun var ona bak bi parentta sorun var set parent yaparken
		dropObject = map( lambda value: int( value ), data.text().split( ',' ) )
		if len( dropObject ) > 0:
			folder = self.fileList[parent.row()]
			data = self.fileList[dropObject[0]]
			if folder.filename == data.filename:
				return False
			self.deleteData( data.filename )
			folder.fileListModel.insertData( data )
			_, filename = os.path.split( data.filename )
			oldFilename = data.filename
			newFileName = ''
			if data.type == FileType.FILE:
				newFileName = folder.generateFileName()
			elif data.type == FileType.FOLDER:
				newFileName = folder.generateFolderName()
				data.setParent( folder )
			os.rename( oldFilename, newFileName )
			data.filename = newFileName
			self.dataUpdated.emit( data, data, folder.fileListModel.rowCount() )
			return True
		return False

	def data( self, index, role = QtCore.Qt.DisplayRole ):
		if not index.isValid():
			return None
		if index.row() >= len( self.fileList ) or index.row() < 0:
			return None
		item = self.fileList[index.row()]
		if role == QtCore.Qt.DisplayRole:
			return item.title
		elif role == QtCore.Qt.EditRole:
			return item.title
		elif role == QtCore.Qt.DecorationRole:
			data = self.fileList[index.row()]
			if isinstance( data, FolderListItem ):
				return QtGui.QIcon( os.path.join( iconsPath, 'folder.png' ) )
			else:
				return QtGui.QIcon( os.path.join( iconsPath, 'text_file.png' ) )

	def setData( self, index, item, role = QtCore.Qt.EditRole ):
		if index.row() >= self.rowCount() or index.row() < 0 or item is None:
			return False
		if index.isValid() and role == QtCore.Qt.EditRole:
			row = index.row()
			oldModelItem = self.fileList[row]
			newModelItem = item
			if isinstance( newModelItem, unicode ):
				if newModelItem.strip() == '' or newModelItem == oldModelItem.title:
					return False
				oldModelItem.title = newModelItem
				newModelItem = oldModelItem
			self.fileList[row] = newModelItem
			self.dataUpdated.emit( newModelItem, oldModelItem, row )
			self.dataChanged.emit( index, index )
			return True
		return False

	def setClickFunction( self, function ):
		self.clickFunction = function

	def isEmpty( self ):
		return len( self.allFileList ) <= 0

	def hasClickFunction( self ):
		return False if self.clickFunction is None else True

	def deleteRow( self, filename ):
		index = self.getIndex( filename )
		data = self.getItem( index )
		return self.deleteItem( data )

	def deleteItem( self, data ):
		index = self.getList().index( data )
		if index != -1:
			self.beginRemoveRows( QtCore.QModelIndex(), index, index )
			self.fileList.pop( index )
			self.allFileList.remove( data )
			self.endRemoveRows()
			return data
		return None

	def rowCount( self, parent = QtCore.QModelIndex() ):
		return len( self.fileList )

	def insertData( self, data, index = None ):
		if data is None:
			return False
		if index is None:
			index = self.rowCount()
		index = self._checkFile( self.rowCount(), index )
		self.beginInsertRows( QtCore.QModelIndex(), index, index )
		self.allFileList.insert( index, data )
		if self.searchTitle.lower() in data.title.lower():
			self.fileList.insert( index, data )
		self.endInsertRows()
		return index

	def deleteData( self, filename ):
		if filename:
			return self.deleteRow( filename )
		else:
			return None

	def getList( self ):
		return self.fileList

	def search( self, title ):
		self.searchTitle = title
		self.beginResetModel()
		self.fileList = filter( lambda item: title.lower() in item.title.lower(), self.allFileList )
		self.endResetModel()

	def setFileList( self, fileList ):
		self.beginResetModel()
		self.allFileList = fileList
		self.fileList = copy.copy( self.allFileList )
		self.endResetModel()

	def getItem( self, index ):
		try:
			return self.fileList[index]
		except:
			return None

	def getIndex( self, filename ):
		for i in range( len( self.fileList ) ):
			item = self.fileList[i]
			if item.filename == filename:
				return i
		return -1

	def moveItem( self, fromItem, to ):
		to = self._checkFile( fromItem, to )
		if fromItem != to:
			self.beginMoveRows( QtCore.QModelIndex(), fromItem, fromItem, QtCore.QModelIndex(), to )
			item = self.fileList.pop( fromItem )
			self.fileList.insert( to, item )

			self.allFileList.remove( item )
			self.allFileList.insert( to, item )

			self.endMoveRows()

	def _checkFile( self, from_, to ):
		"""
		:param from_: from index
		:param to:  to index
		:return: find to first not fixed index between from_ and to return that index
		"""
		isNotValid = True
		item = self.getItem( to )
		while item and isNotValid:
			item = self.getItem( to )
			if item.isFixed:
				to += 1
			else:
				isNotValid = False
			if from_ == to:
				return to
		return to

	def stringList( self ):
		return map( lambda m: m.title, self.fileList )

	def clear( self ):
		self.beginResetModel()
		self.fileList = []
		self.endResetModel()

	@property
	def dataUpdated( self ):
		return self._updateDataSignal

	def json( self ):
		fileList = filter( lambda item: item.title != '..', self.allFileList )
		json = map( lambda data: data.json(), fileList )
		return json

	def generateFileName( self ):
		allTextFilesNumber = len( filter( lambda item: item.type == FileType.FILE, self.allFileList ) )
		filename = 'file%d.txt' % allTextFilesNumber
		return filename

	def generateFolderName( self ):
		allFolderNumber = len( filter( lambda item: item.type == FileType.FOLDER, self.allFileList ) )
		folder = 'folder%d' % allFolderNumber
		return folder


class ButtonWithRightClick( QtWidgets.QToolButton ):
	rightClicked = QtCore.Signal()

	def __init__( self, parent = None ):
		super( ButtonWithRightClick, self ).__init__( parent )

	def mousePressEvent( self, event ):
		if event.button() == QtCore.Qt.RightButton:
			self.rightClicked.emit()
		else:
			self.click()
