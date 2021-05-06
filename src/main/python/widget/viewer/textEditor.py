import datetime
import os
import logging as log
import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore
import core
from enums import DataType
from model.data import FileData
from model.styleItem import StyleItem
from service.configurationService import ConfigurationService
from widget.tagAction import TagAction
from widget.textEditWidget import TextEditorWidget
from widget.toast import Toast
from widget.viewer.baseViewerInterface import BaseViewerInterface


class TextEditor(QtWidgets.QWidget, BaseViewerInterface, ConfigurationService):
	fileSaved = QtCore.Signal(FileData)


	def __init__(self, parent = None, disableStyle = False):
		super(TextEditor, self).__init__(parent)
		self.dialogLayout = QtWidgets.QHBoxLayout(self)
		self.dialogLayout.setContentsMargins(0, 0, 0, 0)
		self.textEditorWidget = TextEditorWidget(self)
		self.dialogLayout.addWidget(self.textEditorWidget)
		self.__currentTextData = None
		self.__filename = None

		self.autoSaveTimer = QtCore.QTimer(self)
		self.autoSaveTimer.setSingleShot(True)
		# add pattern if disable style is not none
		if disableStyle is False:
			self.styleItems = self.createStyleItem(self.configuration().get('patterns', []))
		else:
			self.styleItems = []
		self.textEditorWidget.setStyleItems(self.styleItems)
		self.initialize()
		self.initializeShortcuts()
		self.initSignalsAndSlots()
		self.setupEditor()


	def isExternalWidget(self):
		return False


	def fileSavedSignal(self):
		return self.fileSaved


	def setupEditor(self):
		font = QtGui.QFont()
		font.setFamily('Menlo')
		font.setFixedPitch(True)
		font.setPointSize(12)
		self.textEditorWidget.editor.setFont(font)
		self.textEditorWidget.editor.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


	def initializeShortcuts(self):
		self.saveShortcut = QtWidgets.QShortcut(self.textEditorWidget.editor)
		self.saveShortcut.setKey(QtGui.QKeySequence.Save)
		self.saveShortcut.activated.connect(self.save)
		self.saveShortcut.setContext(QtCore.Qt.WidgetShortcut)


	def initSignalsAndSlots(self):
		self.textEditorWidget.editor.document().modificationChanged.connect(self.updateDialogTitle)
		self.textEditorWidget.editor.document().contentsChanged.connect(self.startAutoSave)
		self.autoSaveTimer.timeout.connect(self.autoSave)


	def initialize(self):
		self.textEditorWidget.editor.customContextMenuRequested.connect(self.__showContextMenu)
		self.textEditorWidget.editor.document().clearUndoRedoStacks()
		self.textEditorWidget.editor.document().setModified(False)


	def save(self):
		if self.isModified() is True:
			if self.__filename is None:
				filename, result = QtWidgets.QInputDialog.getText(self, 'Save File', 'Enter a filename to save',
																  text = 'Text')
				filenameArray = filename.split(' ')
				now = datetime.datetime.now().timestamp()
				path = os.path.join(core.fbs.filesPath, f'{"_".join(filenameArray)}_{int(now)}.json')
			else:
				filename = self.__filename
				if self.currentData() is not None:
					path = self.currentData().path
				else:
					filenameArray = filename.split(' ')
					now = datetime.datetime.now().timestamp()
					path = os.path.join(core.fbs.filesPath, f'{"_".join(filenameArray)}_{int(now)}.json')
				result = True

			if filename and result is True:
				return self.__save(filename, path)
		return False


	def setCurrentData(self, data):
		if data is not None:
			self.__filename = data.name()
		self.__currentTextData = data
		self.__setCurrentData()


	def currentData(self):
		return self.__currentTextData


	def autoSave(self):
		if self.currentData() is not None:
			self.__save(self.currentData().filename, self.currentData().path)


	def startAutoSave(self):
		if self.currentData() is not None:
			self.autoSaveTimer.start(500)


	def __save(self, filename, path):
		self.autoSaveTimer.stop()
		try:
			with open(path, 'w') as file:
				file.write(self.textEditorWidget.editor.toHtml())
		except Exception as e:
			Toast.error('Text Save Error', 'Text is not saved successfully.')
			log.error(f'Text file is not saved successfully. Path is {path}. Exception is {e}')
			return False

		self.setModified(False)
		if self.currentData() is None:
			newFile = FileData(filename, path)
			newFile.setType(DataType.STYLEDATA)
			self.__currentTextData = newFile
			self.__filename = filename
		self.fileSavedSignal().emit(self.currentData())

		return True


	def __setCurrentData(self):
		if self.currentData() is not None:
			try:
				with open(self.currentData().path) as file:
					content = file.read()
					if content == '':
						self.textEditorWidget.editor.document().blockSignals(True)
						self.textEditorWidget.editor.clear()
						self.textEditorWidget.editor.document().blockSignals(False)
					else:
						self.textEditorWidget.editor.setHtml(content)

			except FileNotFoundError as e:
				Toast.error('Text Dialog Error', 'Text Editor is not opened successfully. File is not found')
				log.error(f'File does not exists in text editor viewer. Path is {self.currentData().path}.')
			except Exception as e:
				Toast.error('Text Dialog Error', 'Text Editor is not opened successfully.')
				log.error(
					f'Error occurred while open data in text editor viewer. Path is {self.currentData().path}. '
					f'Exception is {e}')


	def accept(self):
		if self.isModified() is True:
			# do not show warning message if current data is valid
			if self.currentData() is None:
				ret = QtWidgets.QMessageBox.warning(self, "Application",
													"The document hasdasas been modified.\n"
													"Do you want to save your changes?",
													QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel |
													QtWidgets.QMessageBox.No)
			else:
				ret = QtWidgets.QMessageBox.Yes

			if ret == QtWidgets.QMessageBox.Yes:
				# save the session before quit
				if self.save() is False:
					# if not saved, not closed
					return False

			elif ret == QtWidgets.QMessageBox.Cancel:
				return False

		return True


	def isModified(self):
		return self.textEditorWidget.editor.document().isModified()


	def setModified(self, res):
		self.textEditorWidget.editor.document().setModified(res)


	def updateDialogTitle(self, change):
		# update window title
		if change and self.windowTitle().find('*') == -1:
			self.setWindowTitle('%s*' % self.windowTitle())
		elif not change and self.windowTitle().find('*') != -1:
			self.setWindowTitle('%s' % self.windowTitle()[:-1])


	def createStyleItem(self, patterns):
		# create style item
		patternList = []
		for styleItemInDict in patterns:
			try:
				styleItem = StyleItem.create(styleItemInDict)
				patternList.append(styleItem)
			except ValueError as e:
				log.warning(e)
		return patternList


	def __showContextMenu(self, pos):
		defaultBackgroundColors = self.configuration().get('backgroundColor', [])

		cursor = self.textEditorWidget.editor.textCursor()
		if not cursor.hasSelection():
			cursor = self.textEditorWidget.editor.cursorForPosition(pos)

		globalPos = self.textEditorWidget.editor.mapToGlobal(pos)
		menu = QtWidgets.QMenu()

		colorActions = []
		backgroundMenu = menu.addMenu('Background Color')
		none = backgroundMenu.addAction("None")
		for color in defaultBackgroundColors:
			colorAction = QtWidgets.QWidgetAction(menu)
			colorAction.setDefaultWidget(TagAction(color, menu))
			colorAction.setProperty('color', color)
			backgroundMenu.addAction(colorAction)
			colorActions.append(colorAction)

		action = menu.exec_(globalPos)
		if action in colorActions:

			cursor.beginEditBlock()
			color = action.property('color')
			blockFormat = cursor.blockFormat()
			blockFormat.setBackground(QtGui.QBrush(QtGui.QColor(color)))
			cursor.setBlockFormat(blockFormat)
			cursor.endEditBlock()
		elif action == none:
			cursor.beginEditBlock()
			blockFormat = cursor.blockFormat()
			blockFormat.setBackground(QtGui.QBrush())
			cursor.setBlockFormat(blockFormat)
			cursor.endEditBlock()


	def id(self):
		if self.currentData() is not None:
			return self.currentData().id()
		else:
			return None
