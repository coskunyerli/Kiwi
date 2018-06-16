#!venvFlow/bin/python
# --coding: utf-8 --
import os
import sys

from PySide import QtGui, QtCore

from python.MainWindow import MainWindow
from python.path import projectPath, testPath

reload( sys )
sys.setdefaultencoding( 'utf8' )

def loadConfigVar():
    pass

if __name__ == "__main__":
    # setup app

    # setup Qt app for ui
    # if not os.path.exists( projectPath ):
    #     loadConfigVar()
    app = QtGui.QApplication( sys.argv )
    # app.setWindowIcon( QtGui.QIcon( 'icon.png' ) )
    app.setApplicationName( "TodoList" )
    # app.setAttribute( QtCore.Qt.AA_)
    # app.setStyle( "plastique" )
    # setup ui
    mainWindow = MainWindow()
    mainWindow.show()
   # mainWindow.setWindowTitle()

    sys.exit( app.exec_() )

"""

<key>NSPrincipalClass</key>
<string>NSApplication</string>
<key>NSHighResolutionCapable</key>
<string>True</string>

Bunu ekle plist içine

"""
