import static
from PySide2 import QtGui


class StyleItem(object):
	def __init__(self, name, index, pattern, patternStart, patternEnd, family, size, bold, strikeout, underline, italic,
				 color, background, blockBackground, enumarationClass):
		super(StyleItem, self).__init__()
		self.name = name
		self.pattern = pattern
		self.patternStart = patternStart
		self.patternEnd = patternEnd
		self.index = index
		self.blockBackgroundColor = blockBackground
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
		if underline:
			self._blockCharFormat.setFontUnderline(True)


	def __str__(self):
		return f'StyleItem({self.name}, {self._blockCharFormat.foreground().color().name()})'


	def __repr__(self):
		return self.__str__()


	def blockBackground(self):
		if self.blockBackgroundColor:
			return QtGui.QBrush(QtGui.QColor(self.blockBackgroundColor))
		else:
			return QtGui.QBrush()


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


	@staticmethod
	def create(dictItem):
		if 'name' not in dictItem:
			raise ValueError('"name" should include dict object to create StyleItem object')
		if 'pattern' not in dictItem and 'patternStart' not in dictItem and 'patternEnd' not in dictItem:
			raise ValueError('"pattern" should include pattern attribute')
		# error function to print
		error = lambda key: f'StyleItem class, key is "{key}"'

		return StyleItem(static.getValueFromDict(dictItem.get('name'), [str], error('name')),
						 static.getValueFromDict(dictItem.get('index'), [int], error('index')),
						 static.getValueFromDict(dictItem.get('pattern'), [str, None.__class__], error('pattern')),
						 static.getValueFromDict(dictItem.get('patternStart'), [str, None.__class__], error('pattern')),
						 static.getValueFromDict(dictItem.get('patternEnd'), [str, None.__class__], error('pattern')),
						 static.getValueFromDict(dictItem.get('family', 'Courier'), [str], error('family')),
						 static.getValueFromDict(dictItem.get('size', 12), [int, float], error('size')),
						 static.getValueFromDict(dictItem.get('bold', False), [bool], error('bold')),
						 static.getValueFromDict(dictItem.get('strikeout', False), [bool], error('strikeout')),
						 static.getValueFromDict(dictItem.get('underline', False), [bool], error('underline')),
						 static.getValueFromDict(dictItem.get('italic', False), [bool], error('italic')),
						 static.getValueFromDict(dictItem.get('color', 'white'), [str], error('color')),
						 static.getValueFromDict(dictItem.get('background', None), [str, type(None)],
												 error('background')),
						 static.getValueFromDict(dictItem.get('blockBackground', None), [str, type(None)],
												 error('blockBackground')),
						 dictItem.get('next', None))
