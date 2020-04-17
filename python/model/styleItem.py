from PySide2 import QtGui


class StyleItem(object):
	def __init__(self, name, pattern, family, size, bold, strikeout, italic,
				 color, background, enumarationClass):
		super(StyleItem, self).__init__()
		self.name = name
		self.pattern = pattern
		self.enumarationClass = enumarationClass
		self._blockCharFormat = QtGui.QTextCharFormat()
		if family and size:
			font = QtGui.QFont(family, size)
			self._blockCharFormat.setFont(font)
		if italic:
			self._blockCharFormat.setFontItalic(bool(italic))
		if bold:
			self._blockCharFormat.setFontWeight(QtGui.QFont.Bold if bold else QtGui.QFont.Normal)
		if strikeout:
			self._blockCharFormat.setFontStrikeOut(bool(strikeout))
		if color:
			color = QtGui.QColor(color)
			self._blockCharFormat.setForeground(QtGui.QBrush(color))
		if background:
			self._blockCharFormat.setBackground(QtGui.QBrush(QtGui.QColor(background)))
		else:
			self._blockCharFormat.setBackground(QtGui.QBrush())


	def __str__(self):
		return '%s %s' % (self.name, self._blockCharFormat.foreground().color().name())


	def __repr__(self):
		return self.__str__()


	def json(self):
		background = self.charFormat.background().color().name() if self.charFormat.background().isOpaque() else None
		return {'name': self.name, 'pattern': self.pattern, 'family': self.charFormat.fontFamily(),
				'size': self.charFormat.fontPointSize(), 'bold': self.charFormat.fontWeight() == QtGui.QFont.Bold,
				'strikeout': self.charFormat.fontStrikeOut(), 'italic': self.charFormat.fontItalic(),
				'color': self.charFormat.foreground().color().name(),
				'next': self.enumarationClass if self.enumarationClass else None,
				'background': background}


	@property
	def charFormat(self):
		return self._blockCharFormat


	def setCharFormat(self, format):
		self._blockCharFormat = format


	def copy(self):
		return StyleItem.create(self.json())


	@staticmethod
	def create(dictItem):
		return StyleItem(dictItem['name'], dictItem['pattern'], dictItem.get('family', 'Courier'),
						 dictItem.get('size', 12),
						 dictItem.get('bold', False),
						 dictItem.get('strikeout', False), dictItem.get('italic', False),
						 dictItem.get('color', 'white'), dictItem.get('background', None),
						 dictItem.get('next', None))
