import os

from PySide2 import QtWidgets, QtCore, QtGui

from python.enums import FileType, ItemFlags
from python.path import iconsPath


class FileViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super(FileViewDelegate, self).__init__(parent)


	def paint(self, painter, option, index):
		pixmap = index.model().data(index, role = QtCore.Qt.DecorationRole).pixmap(QtCore.QSize(40, 40))
		data = index.internalPointer()
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		rect = option.rect

		leftMargin = 16
		lineRect = QtCore.QRect(QtCore.QPoint(leftMargin, rect.bottom()), QtCore.QSize(rect.width(), 1))
		painter.fillRect(lineRect, QtGui.QColor('#45464A'))

		if option.state & QtWidgets.QStyle.State_HasFocus:
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#C9942F')))
		elif option.state & QtWidgets.QStyle.State_Selected:
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#353639')))

		iconSize = QtCore.QSize(16, 16)
		iconRect = QtCore.QRect(
				rect.topLeft() + QtCore.QPoint(leftMargin, (rect.height() - iconSize.height()) / 2.0),
				iconSize)
		painter.drawPixmap(iconRect, pixmap, pixmap.rect())

		painter.save()
		painter.setPen(QtGui.QColor('#D3D7E3'))
		font = painter.font()
		font.setPointSize(9)
		painter.setFont(font)
		fontMetric = painter.fontMetrics()

		if data.type == FileType.FOLDER:

			text = '%d Items' % data.fileCount()
			folderItemRect = QtCore.QRect(
					rect.bottomRight() - QtCore.QPoint(fontMetric.width(text) + 4, fontMetric.height() + 4),
					QtCore.QSize(fontMetric.width(text), fontMetric.height()))

			painter.drawText(folderItemRect, QtCore.Qt.AlignLeft, text)

		elif data.type == FileType.FILE:
			if data.lastUpdate is not None:
				updateRect = QtCore.QRect(
						rect.bottomRight() - QtCore.QPoint(fontMetric.width(data.lastUpdate) + 4,
														   fontMetric.height() + 4),
						QtCore.QSize(fontMetric.width(data.lastUpdate), fontMetric.height()))
				painter.drawText(updateRect, QtCore.Qt.AlignLeft, data.lastUpdate)

		painter.restore()

		painter.setPen(QtGui.QColor('#D3D7E3'))
		textRect = rect.adjusted(iconRect.right() + 8, 0, 0, 0)
		painter.drawText(textRect, QtCore.Qt.AlignVCenter, index.model().data(index))

		if not index.model().flags(index) & ItemFlags.ItemIsSoftLink:
			if data.isFixed:
				pinPixmap = QtGui.QPixmap(os.path.join(iconsPath, 'pin.png'))

				pinPixmapSize = pinPixmap.size() / 3.5
				pinRect = QtCore.QRect(
						rect.topRight() + QtCore.QPoint(-pinPixmapSize.width() - 4, 4),
						pinPixmapSize)
				painter.drawPixmap(pinRect, pinPixmap, pinPixmap.rect())
			if data.isLocked is not None:
				if data.isLocked:
					lockPixmap = QtGui.QPixmap(os.path.join(iconsPath, 'lock.png'))
				else:
					lockPixmap = QtGui.QPixmap(os.path.join(iconsPath, 'lock-open.png'))
				lockPixmapSize = lockPixmap.size() / 4.5
				lockRect = QtCore.QRect(
						rect.topLeft() + QtCore.QPoint(4, 4),
						lockPixmapSize)
				painter.drawPixmap(lockRect, lockPixmap, lockPixmap.rect())


	def sizeHint(self, option, index):
		size = super(FileViewDelegate, self).sizeHint(option, index)
		size.setHeight(55)
		return size
