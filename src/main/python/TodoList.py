#!/Users/coskunyerli/PycharmProjects/ive/venv/bin/python
# --coding: utf-8 --
import sys
import core
import logging as log

from widget.mainWindow import MainWindow
from model.fbs import TodoListApplicationContext

if __name__ == "__main__":
	# setup app
	fbs = TodoListApplicationContext()
	core.fbs = fbs
	# setup Qt app for ui
	fbs.app.setApplicationName("TodoList")

	# setup ui
	mainWindow = MainWindow()
	mainQss = fbs.qss('style.qss')
	if mainQss is not None:
		mainWindow.setStyleSheet(mainQss)
	else:
		log.warning('Main qss is not loaded successfully')

	mainWindow.show()

	sys.exit(fbs.app.exec_())

"""

<key>NSPrincipalClass</key>
<string>NSApplication</string>
<key>NSHighResolutionCapable</key>
<string>True</string>

"""
