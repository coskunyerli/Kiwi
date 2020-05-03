import os

import core
from PySide2 import QtWidgets, QtCore, QtGui

from enums import FileType, ItemFlags


class DataViewDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, parent = None):
		super(DataViewDelegate, self).__init__(parent)


	def paint(self, painter, option, index):
		pixmap = index.model().data(index, role = QtCore.Qt.DecorationRole).pixmap(QtCore.QSize(40, 40))
		dataArr = index.data()
		name = dataArr[1]
		createDate = dataArr[2]

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

		painter.setPen(QtGui.QColor('#D3D7E3'))
		textRect = QtCore.QRect(iconRect.right() + 8, rect.top(), rect.width(), rect.height())
		painter.drawText(textRect, QtCore.Qt.AlignVCenter, name)

		fontMetric = painter.fontMetrics()
		painter.save()
		painter.setPen(QtGui.QColor('#D3D7E3'))
		font = painter.font()
		font.setPointSize(9)
		painter.setFont(font)
		if createDate is not None:
			createDateInString = createDate.strftime("%Y-%m-%d %H:%M")
			createDateWidth = fontMetric.width(createDateInString)
			updateRect = QtCore.QRect(
					rect.bottomRight() - QtCore.QPoint(createDateWidth,
													   fontMetric.height() + 4),
					QtCore.QSize(createDateWidth, fontMetric.height()))
			painter.drawText(updateRect, QtCore.Qt.AlignLeft, createDateInString)
		painter.restore()


	def sizeHint(self, option, index):
		size = super(DataViewDelegate, self).sizeHint(option, index)
		size.setHeight(55)
		return size
