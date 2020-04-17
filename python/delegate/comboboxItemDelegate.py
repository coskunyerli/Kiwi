from PySide2 import QtWidgets, QtCore, QtGui


class ComboBoxItemDelegate(QtWidgets.QStyledItemDelegate):

	def paint(self, painter, option, index):
		color = index.model().data(index, QtCore.Qt.BackgroundRole)
		colorname = index.model().data(index)
		rect = option.rect
		size = rect.size()
		offset = size.width() / 8.0

		if option.state & QtWidgets.QStyle.State_MouseOver:
			painter.fillRect(rect, QtGui.QBrush(QtGui.QColor('#353639')))

		colorRect = QtCore.QRect(offset, rect.top() + 2, 1.5 * offset, size.height() - 4)
		metric = painter.fontMetrics()
		path = QtGui.QPainterPath()
		path.addRoundedRect(colorRect, 5, 5)
		painter.fillPath(path, color)
		textRect = QtCore.QRect(colorRect.right() + 8, colorRect.top(), metric.width(colorname), metric.height())
		painter.drawText(textRect, QtCore.Qt.AlignLeft, colorname)
