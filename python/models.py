from PySide import QtCore, QtGui

class StyleItem( object ):
    def __init__( self, name, pattern, size, bold, strikeout, color ):
        super( StyleItem, self ).__init__()
        self.name = name
        self.pattern = pattern
        self.size = size
        self.bold = bold
        self.strikeout = strikeout
        self.color = color


    def json( self ):
        return {'pattern': self.pattern, 'size': self.size, 'bold': self.bold, 'strikeout': self.strikeout,
                'color': self.color}


    @staticmethod
    def create( dictItem ):
        return StyleItem( dictItem['name'], dictItem['pattern'], dictItem.get( 'size', 12 ), dictItem['bold'],
                          dictItem.get( 'strikeout', False ),
                          dictItem['color'] )

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
        self.fileList = self.allFileList
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
            if isinstance( newModelItem, basestring ):
                if newModelItem.strip() == '' or newModelItem == oldModelItem.title:
                    return False
                newModelItem = FileListItem( oldModelItem.filename, newModelItem )
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
        self.fileList = filter( lambda item: title.lower() in item.title.lower(), self.allFileList )
        self.dataChanged.emit( 0, len( self.allFileList ) )


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
        return map( lambda data: data.json(), self.fileList )
