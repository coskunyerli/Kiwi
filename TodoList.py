#!/Users/coskunyerli/PycharmProjects/ive/venv/bin/python
# --coding: utf-8 --
import sys
import PySide2.QtWidgets as QtWidgets, PySide2.QtCore as QtCore, PySide2.QtWebEngineWidgets as QtWebEngineWidgets, \
	PySide2.QtWebEngine as QtWebEngine

if __name__ == "__main__":
	# setup app

	# setup Qt app for ui
	app = QtWidgets.QApplication(sys.argv)
	app.setApplicationName("TodoList")
	view = QtWebEngineWidgets.QWebEngineView()
	QtWebEngineWidgets.QWebEngineSettings.defaultSettings().setAttribute(
		QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
	QtWebEngineWidgets.QWebEngineSettings.defaultSettings().setAttribute(
			QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)
	view.load(QtCore.QUrl.fromLocalFile('/Users/coskunyerli/.todolist/files/Coskun_Yerli_CV.pdf'))
	view.show()
	sys.exit(app.exec_())
# /Users/coskunyerli/Downloads/modularity.pdf
"""

<key>NSPrincipalClass</key>
<string>NSApplication</string>
<key>NSHighResolutionCapable</key>
<string>True</string>

"""
