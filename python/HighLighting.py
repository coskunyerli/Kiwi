import re
import Enumeration

from PySide2 import QtGui

from staticMethods import get_classes


class Highlighter( QtGui.QSyntaxHighlighter ):
	def __init__( self, editor, patterns ):
		super( Highlighter, self ).__init__( editor.document() )
		self.editor = editor
		self.updateHighlighterRules( patterns )
		self.editor.document().blockCountChanged.connect( self.setEnumaration )
		self.enumClasses = get_classes( Enumeration.__name__ )


	def highlightBlock( self, text ):
		for rule in self.highlightingRules:
			matches = rule.search( text )
			for match in matches:
				self.setFormat( match.start(), match.end() - match.start(), rule.style.charFormat )


	def setEnumaration( self ):
		block = self.editor.textCursor().block().previous()
		if block.isValid() and block.next().text() == '':
			text = block.text()
			for rule in self.highlightingRules:
				matches = rule.search( text )
				for _ in matches:
					if rule.style.enumarationClass is not None:
						klass = self.enumClasses.get( rule.style.enumarationClass )
						if klass:
							cursor = QtGui.QTextCursor( block.next() )
							enum = klass.create()
							t = enum.next( block.text() )
							if t is not None:
								cursor.insertText( t )
							else:
								self.editor.document().blockCountChanged.disconnect( self.setEnumaration )
								cursor.setPosition( block.position(), QtGui.QTextCursor.KeepAnchor )
								cursor.removeSelectedText()
								self.editor.document().blockCountChanged.connect( self.setEnumaration )
							del enum


	def updateHighlighterRules( self, patterns ):
		self.patterns = patterns
		self.highlightingRules = []
		for style in self.patterns:
			rule = HighlightingRule( self.editor )
			rule.pattern = re.compile( style.pattern )
			rule.style = style
			self.highlightingRules.append( rule )


class HighlightingRule( object ):
	def __init__( self, editor ):
		super( HighlightingRule, self ).__init__()
		self.pattern = None
		self.style = None
		self.editor = editor


	def search( self, text ):
		if self.pattern:
			matches = re.finditer( self.pattern, text )
			if matches:
				return matches
			else:
				return []
		return []
