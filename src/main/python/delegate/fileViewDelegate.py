import os

import core
import static
from PySide2 import QtWidgets, QtCore, QtGui

from enums import FileType, ItemFlags


class FileViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super(FileViewDelegate, self).__init__(parent)


	def paint(self, painter, option, index):
		pixmap = index.model().data(index, role = QtCore.Qt.DecorationRole).pixmap(QtCore.QSize(40, 40))
		dataArr = index.data()
		displayName = dataArr[2]
		isFixed = dataArr[3]
		lastUpdate = dataArr[4]
		isLocked = dataArr[5]
		dataType = dataArr[6]
		childCount = dataArr[7]
		createDate = dataArr[8]

		path = index.model().data(index, role = QtCore.Qt.WhatsThisRole)

		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		rect = option.rect

		leftMargin = 16
		lineRect = QtCore.QRect(QtCore.QPoint(leftMargin, rect.bottom()),
								QtCore.QSize(rect.width() - 2 * leftMargin, 1))
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
		pinRect = QtCore.QRect(
				rect.topLeft(),
				QtCore.QSize(0, 0))
		if not index.model().flags(index) & ItemFlags.ItemIsSoftLink:
			if isFixed:
				pinRect = QtCore.QRect(
						rect.topLeft() + QtCore.QPoint(4, 4),
						QtCore.QSize(12, 12))
				pinPixmap = QtGui.QPixmap(core.fbs.icons('pin.png'))
				painter.drawPixmap(pinRect, pinPixmap, pinPixmap.rect())

		if dataType == FileType.FOLDER:

			text = '%d Items' % childCount
			folderItemRect = QtCore.QRect(
					rect.bottomRight() - QtCore.QPoint(fontMetric.width(text) + 4, fontMetric.height() + 4),
					QtCore.QSize(fontMetric.width(text), fontMetric.height()))

			painter.drawText(folderItemRect, QtCore.Qt.AlignLeft, text)

		elif dataType == FileType.FILE:
			if createDate is not None:
				lastUpdateInString = f'{static.passedTime(lastUpdate)} ago'
				lastUpdateWidth = fontMetric.width(lastUpdateInString)
				updateRect = QtCore.QRect(
						rect.bottomRight() - QtCore.QPoint(lastUpdateWidth + 4,
														   fontMetric.height() + 2),
						QtCore.QSize(lastUpdateWidth, fontMetric.height()))
				painter.drawText(updateRect, QtCore.Qt.AlignLeft, lastUpdateInString)
			if lastUpdate is not None:
				createDateInString = createDate.strftime("%Y-%m-%d %H:%M")
				createDateWidth = fontMetric.width(createDateInString)
				updateRect = QtCore.QRect(
						rect.bottomLeft() + QtCore.QPoint(4, -fontMetric.height() - 2),
						QtCore.QSize(createDateWidth, fontMetric.height()))
				painter.drawText(updateRect, QtCore.Qt.AlignLeft, createDateInString)

		painter.restore()
		painter.save()
		fontMetric = painter.fontMetrics()
		painter.setPen(QtGui.QColor('#D3D7E3'))
		textRect = QtCore.QRect(iconRect.right() + 8, rect.top(), rect.right() - (iconRect.right() + 8), rect.height())
		elidedDisplayText = fontMetric.elidedText(displayName, QtCore.Qt.ElideRight, textRect.width())
		painter.drawText(textRect, QtCore.Qt.AlignVCenter, elidedDisplayText)
		painter.restore()

		if path is not None:
			painter.save()
			painter.setPen(QtGui.QColor('#888'))
			font = painter.font()
			font.setPointSize(9)
			painter.setFont(font)
			fontMetric = painter.fontMetrics()
			pathRect = QtCore.QRect(pinRect.right() + 4, rect.top() + 3, rect.right(), fontMetric.height())
			elidedDisplayText = fontMetric.elidedText(path, QtCore.Qt.ElideRight, pathRect.width())
			painter.drawText(pathRect, QtCore.Qt.AlignVCenter, elidedDisplayText)
			painter.restore()


	# if isLocked is not None:
	# if isLocked:
	# 	lockPixmap = QtGui.QPixmap(core.fbs.icons('lock.png'))
	# else:
	# 	lockPixmap = QtGui.QPixmap(core.fbs.icons('lock-open.png'))
	# lockPixmapSize = lockPixmap.size() / 4.5
	# lockRect = QtCore.QRect(
	# 		rect.topLeft() + QtCore.QPoint(4, 4),
	# 		lockPixmapSize)
	# painter.drawPixmap(lockRect, lockPixmap, lockPixmap.rect())

	def sizeHint(self, option, index):
		size = super(FileViewDelegate, self).sizeHint(option, index)
		size.setHeight(55)
		return size
