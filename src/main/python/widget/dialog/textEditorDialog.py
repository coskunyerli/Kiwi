import datetime
import os

import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore
import core
from enums import DataType
from model.data import FileData
from model.styleItem import StyleItem
from service.configurationService import ConfigurationService
from widget.textEditWidget import TextEditorWidget


class TextEditorDialog(QtWidgets.QDialog, ConfigurationService):
	fileSaved = QtCore.Signal(FileData)


	def __init__(self, parent = None, disableStyle = False):
		super(TextEditorDialog, self).__init__(parent)
		self.dialogLayout = QtWidgets.QHBoxLayout(self)
		self.dialogLayout.setContentsMargins(0, 0, 0, 0)
		self.textEditorWidget = TextEditorWidget(self)
		self.dialogLayout.addWidget(self.textEditorWidget)
		self.setWindowTitle('New Text File')
		self.resize(500, 600)
		self.currentTextData = None

		self.autoSaveTimer = QtCore.QTimer(self)
		self.autoSaveTimer.setSingleShot(True)
		if disableStyle is False:
			self.styleItems = list(map(lambda item: StyleItem.create(item), self.configuration().get('patterns')))
		else:
			self.styleItems = []
		self.textEditorWidget.setStyleItems(self.styleItems)
		self.initialize()
		self.initializeShortcuts()
		self.initSignalsAndSlots()


	def initializeShortcuts(self):
		self.saveShortcut = QtWidgets.QShortcut(self.textEditorWidget.editor)
		self.saveShortcut.setKey(QtGui.QKeySequence.Save)
		self.saveShortcut.activated.connect(self.save)
		self.saveShortcut.setContext(QtCore.Qt.WidgetShortcut)


	# self.escapeShortcut = QtWidgets.QShortcut(self)
	# self.escapeShortcut.setKey(QtGui.QKeySequence.Close)
	# self.escapeShortcut.activated.connect(self.close)

	def initSignalsAndSlots(self):
		self.textEditorWidget.editor.document().modificationChanged.connect(self.updateDialogTitle)
		self.textEditorWidget.editor.document().contentsChanged.connect(self.startAutoSave)
		self.autoSaveTimer.timeout.connect(self.autoSave)


	def initialize(self):
		self.textEditorWidget.editor.document().clearUndoRedoStacks()
		self.textEditorWidget.editor.document().setModified(False)


	def save(self):
		if self.isModified() is True:
			if self.currentTextData is None:
				filename, result = QtWidgets.QInputDialog.getText(self, 'Save File', 'Enter a filename to save',
																  text = 'Text')
				filenameArray = filename.split(' ')
				filename = '_'.join(filenameArray)
				now = datetime.datetime.now().timestamp()
				path = os.path.join(core.fbs.filesPath, f'{filename}_{int(now)}.json')
			else:
				filename = self.currentTextData.filename
				path = self.currentTextData.path
				result = True

			if filename and result is True:
				return self.__save(filename, path)
		return False


	def setCurrentData(self, data):
		self.currentTextData = data


	def autoSave(self):
		if self.currentTextData is not None:
			self.__save(self.currentTextData.filename, self.currentTextData.path)


	def startAutoSave(self):
		if self.currentTextData is not None:
			self.autoSaveTimer.start(500)


	def __save(self, filename, path):
		self.autoSaveTimer.stop()
		with open(path, 'w') as file:
			file.write(self.textEditorWidget.editor.toHtml())

		self.setModified(False)
		newFile = FileData(filename, path)
		newFile.setType(DataType.STYLEDATA)
		self.currentTextData = newFile
		self.fileSaved.emit(newFile)
		return True


	def open(self):
		if self.currentTextData is not None:
			with open(self.currentTextData.path) as file:
				content = file.read()
				if content == '':
					self.textEditorWidget.editor.document().blockSignals(True)
					self.textEditorWidget.editor.clear()
					self.textEditorWidget.editor.document().blockSignals(False)
				else:
					self.textEditorWidget.editor.setHtml(content)
		super(TextEditorDialog, self).open()


	def reject(self):
		if self.isModified() is True:
			ret = QtWidgets.QMessageBox.warning(self, "Application",
												"The document hasdasas been modified.\n"
												"Do you want to save your changes?",
												QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel |
												QtWidgets.QMessageBox.No)

			if ret == QtWidgets.QMessageBox.Yes:
				# save the session before quit
				if not self.save():
					# if not saved, not closed
					return

			elif ret == QtWidgets.QMessageBox.Cancel:
				return
		super(TextEditorDialog, self).reject()


	def isModified(self):
		return self.textEditorWidget.editor.document().isModified()


	def setModified(self, res):
		self.textEditorWidget.editor.document().setModified(res)


	def updateDialogTitle(self, change):
		if change and self.windowTitle().find('*') == -1:
			self.setWindowTitle('%s*' % self.windowTitle())
		elif not change and self.windowTitle().find('*') != -1:
			self.setWindowTitle('%s' % self.windowTitle()[:-1])
