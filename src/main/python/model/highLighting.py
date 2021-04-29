import re
import model.enumeration

from PySide2 import QtGui, QtCore

from static import get_classes


class Highlighter(QtGui.QSyntaxHighlighter):
	def __init__(self, editor, patterns):
		super(Highlighter, self).__init__(editor.document())
		self.editor = editor
		self.__updateHighlighterRules(patterns)
		self.editor.document().blockCountChanged.connect(self.setEnumaration)
		self.enumClasses = get_classes(model.enumeration.__name__)


	def setEnumaration(self):
		return
		block = self.editor.textCursor().block().previous()
		if block.isValid() and block.next().text() == '':
			text = block.text()
			for rule in self.highlightingRules:
				matches = re.finditer(rule.pattern, text)
				for _ in matches:
					if rule.style.enumarationClass is not None:
						klass = self.enumClasses.get(rule.style.enumarationClass)
						if klass:
							cursor = QtGui.QTextCursor(block.next())
							enum = klass.create()
							t = enum.next(block.text())
							if t is not None:
								cursor.insertText(t)
							else:
								self.editor.document().blockCountChanged.disconnect(self.setEnumaration)
								cursor.setPosition(block.position(), QtGui.QTextCursor.KeepAnchor)
								cursor.removeSelectedText()
								self.editor.document().blockCountChanged.connect(self.setEnumaration)
							del enum


	def highlightBlock(self, text):
		# highlight of current block
		for rule in self.highlightingRules:
			if rule.pattern is not None:
				index = rule.pattern.indexIn(text)
				while index >= 0 and rule.pattern.isEmpty() is False:
					# We actually want the index of the nth match
					index = rule.pattern.pos(rule.index)
					length = len(rule.pattern.cap(rule.index))
					self.setFormat(index, length, rule.style.charFormat)
					index = rule.pattern.indexIn(text, index + length)
			elif rule.patternStart is not None and rule.patternEnd is not None:
				self.setCurrentBlockState(0)
				# Do multi-line strings
				self.matchMultiline(text, rule.patternStart, rule.patternEnd, rule.index,
									rule.style)


	def matchMultiline(self, text, patternStart, patternEnd, inState, style):
		if self.previousBlockState() == inState:
			start = 0
			add = 0
		else:
			start = patternStart.indexIn(text)
			add = patternStart.matchedLength()
		while start >= 0:
			end = patternEnd.indexIn(text)
			if end >= add:
				length = end - start + add + patternEnd.matchedLength()
				self.setCurrentBlockState(0)
			else:
				self.setCurrentBlockState(inState)
				length = len(text) - start + add
			self.setFormat(start, length, style.charFormat)
			start = patternStart.indexIn(text, start + length)


	def __updateHighlighterRules(self, patterns):
		self.patterns = patterns
		self.highlightingRules = []
		for style in self.patterns:
			self.appendHighlightRule(style)


	def appendHighlightRule(self, style):
		rule = HighlightingRule(self.editor)
		if style.pattern:
			rule.pattern = QtCore.QRegExp(fr'{style.pattern}')
		elif style.patternStart and style.patternEnd:
			rule.patternStart = QtCore.QRegExp(fr'{style.patternStart}')
			rule.patternEnd = QtCore.QRegExp(fr'{style.patternEnd}')
		else:
			return
		rule.index = style.index
		rule.style = style
		self.highlightingRules.append(rule)


class HighlightingRule(object):
	def __init__(self, editor):
		super(HighlightingRule, self).__init__()
		self.pattern = None
		self.patternStart = None
		self.patternEnd = None
		self.style = None
		self.index = None
		self.editor = editor
