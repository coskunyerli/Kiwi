#!venvFlow/bin/python
# --coding: utf-8 --
import sys

from PySide import QtGui

from MainWindow import MainWindow

reload( sys )
sys.setdefaultencoding( 'utf8' )
if __name__ == "__main__":
    # setup app

    # setup Qt app for ui
    app = QtGui.QApplication( sys.argv )
    app.setApplicationName( "TodoList" )

    # setup ui
    mainWindow = MainWindow()
    mainWindow.show()


    sys.exit( app.exec_() )

"""

<key>NSPrincipalClass</key>
<string>NSApplication</string>
<key>NSHighResolutionCapable</key>
<string>True</string>

Bunu ekle plist içine

"""
