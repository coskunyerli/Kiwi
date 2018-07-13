import os

import copy
from PySide import QtCore, QtGui

from python.path import iconsPath

class StyleItem( object ):
    def __init__( self, name, pattern, family, size, bold, strikeout, italic,
                  color, background ):
        super( StyleItem, self ).__init__()
        self.name = name
        self.pattern = pattern
        self._blockCharFormat = QtGui.QTextCharFormat()
        font = QtGui.QFont( family, size )
        color = QtGui.QColor( color )
        self._blockCharFormat.setFont( font )
        self._blockCharFormat.setFontItalic( bool( italic ) )
        self._blockCharFormat.setFontWeight( QtGui.QFont.Bold if bold else QtGui.QFont.Normal )
        self._blockCharFormat.setFontStrikeOut( bool( strikeout ) )
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
        return {'name': self.name, 'pattern': self.pattern, 'family': self.charFormat.fontFamily(),
                'size': self.charFormat.fontPointSize(), 'bold': self.charFormat.fontWeight() == QtGui.QFont.Bold,
                'strikeout': self.charFormat.fontStrikeOut(), 'italic': self.charFormat.fontItalic(),
                'color': self.charFormat.foreground().color().name(),
                'background': background}


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
                          dictItem.get( 'color', 'white' ), dictItem.get( 'background', None ) )

class FileListItem( object ):
    def __init__( self, filename, title ):
        self.filename = filename
        self.title = title


    def json( self ):
        return {'filename': self.filename, 'title': self.title}

class FileListModel( QtCore.QAbstractListModel ):
    _updateDataSignal = QtCore.Signal( FileListItem, FileListItem, int )


    def __init__( self, fileList ):

        if fileList:
            self.allFileList = fileList
        else:
            self.allFileList = []
        self.fileList = copy.copy( self.allFileList )
        self.searchTitle = ''
        self.currentFileItem = None
        super( FileListModel, self ).__init__()


    def __iter__( self ):
        return iter( self.fileList )


    def __contains__( self, item ):
        for data in self.fileList:
            if data.title == item:
                return True
        return False


    def flags( self, index ):
        return (
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsEnabled
            # QtCore.Qt.ItemIsDragEnabled |
            # QtCore.Qt.ItemIsDropEnabled
        )


    # def supportedDragActions( self ):
    #     print 'drag'
    #     return QtCore.Qt.MoveAction
    #
    #
    # def supportedDropActions( self ):
    #     print 'drop'
    #     return QtCore.Qt.MoveAction

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


    def hasClickFunction( self ):
        return False if self.clickFunction is None else True


    def removeRow( self, index ):
        self.beginRemoveRows( QtCore.QModelIndex(), index, index )
        data = self.fileList.pop( index )
        self.allFileList.pop( index )
        self.endRemoveRows()
        return data


    def rowCount( self, parent = QtCore.QModelIndex() ):
        return len( self.fileList )


    def insertData( self, data, index = None ):
        if data is None:
            return False
        if index is None:
            index = self.rowCount()
        self.beginInsertRows( QtCore.QModelIndex(), index, index )
        self.allFileList.insert( index, data )
        if self.searchTitle.lower() in data.title.lower():
            self.fileList.insert( index, data )
        self.endInsertRows()
        return True


    def removeData( self, index ):
        if index and index.isValid():
            return self.removeRow( index.row() )

        else:
            return None


    def getList( self ):
        return self.fileList


    def search( self, title ):
        self.searchTitle = title
        self.beginResetModel()
        self.fileList = filter( lambda item: title.lower() in item.title.lower(), self.allFileList )
        self.endResetModel()



    def getItem( self, index ):
        return self.fileList[index]


    def getIndex( self, filename ):
        for i in range( len( self.fileList ) ):
            item = self.fileList[i]
            if item.filename == filename:
                return i
        return -1


    def moveItem( self, fromItem, to ):
        self.beginMoveRows( QtCore.QModelIndex(), fromItem, fromItem, QtCore.QModelIndex(), to )
        self.fileList.insert( to, self.fileList.pop( fromItem ) )
        self.endMoveRows()


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
        return map( lambda data: data.json(), self.allFileList )

class ButtonWithRightClick( QtGui.QToolButton ):
    rightClicked = QtCore.Signal()


    def __init__( self, parent = None ):
        super( ButtonWithRightClick, self ).__init__( parent )


    def mousePressEvent( self, event ):
        if event.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.click()
