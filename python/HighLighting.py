import re
from PySide import QtGui, QtCore

class Highlighter( QtGui.QSyntaxHighlighter ):
    def __init__( self, editor, patterns ):
        super( Highlighter, self ).__init__( editor.document() )
        self.editor = editor
        self.updateHighlighterRules( patterns )


    def highlightBlock( self, text ):
        for rule in self.highlightingRules:
            matches = rule.search( text )
            for match in matches:
                self.setFormat( match.start(), match.end() - match.start(), rule.format )


    def updateHighlighterRules( self, patterns ):
        self.patterns = patterns
        self.highlightingRules = []
        for pattern in self.patterns:
            self.format = pattern.charFormat
            rule = HighlightingRule( self.editor )
            rule.pattern = re.compile( pattern.pattern )
            rule.format = self.format
            self.highlightingRules.append( rule )

class HighlightingRule( object ):
    def __init__( self, editor ):
        super( HighlightingRule, self ).__init__()
        self.pattern = None
        self.format = None
        self.editor = editor


    def search( self, text ):
        if self.pattern:
            matches = re.finditer( self.pattern, text )
            if matches:
                return matches
            else:
                return []
        return []
