#!/Users/coskunyerli/PycharmProjects/ive/venv/bin/python
# --coding: utf-8 --
import sys
from PySide2 import QtWidgets
from python.mainWindow import MainWindow

reload( sys )
sys.setdefaultencoding( 'utf8' )
if __name__ == "__main__":
    # setup app

    # setup Qt app for ui
    app = QtWidgets.QApplication( sys.argv )
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

"""

