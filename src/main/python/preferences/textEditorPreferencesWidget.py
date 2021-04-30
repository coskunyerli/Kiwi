# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/preferencesDialogue.ui'
#
# Created: Sun Jun 17 21:53:40 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

import re
from PySide2 import QtGui, QtCore, QtWidgets
from model.styleItem import StyleItem
from service.configurationService import ConfigurationService
from service.preferencesService import PreferencesService
from widget.buttonWithRightClick import ButtonWithRightClick


class Ui_Form(object):
	def setupUi(self, Form):
		self.formLayout = QtWidgets.QVBoxLayout(Form)
		# self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setSpacing(0)
		self.modeGroupBoxWidget = QtWidgets.QGroupBox('Mode', Form)
		self.modeGroupBoxWidgetLayout = QtWidgets.QVBoxLayout(self.modeGroupBoxWidget)
		self.modeCombobox = QtWidgets.QComboBox(Form)
		self.modeCombobox.setObjectName("modeCombobox")
		self.modeGroupBoxWidgetLayout.addWidget(self.modeCombobox)

		self.formLayout.addWidget(self.modeGroupBoxWidget)

		self.nameGroupBoxWidget = QtWidgets.QGroupBox('Name', Form)
		self.nameGroupBoxWidgetLayout = QtWidgets.QGridLayout(self.nameGroupBoxWidget)

		self.nameLabel = QtWidgets.QLabel(self.nameGroupBoxWidget)
		self.nameLineEdit = QtWidgets.QLineEdit(self.nameGroupBoxWidget)
		self.nameLineEdit.setObjectName('nameLineEdit')

		self.patternLabel = QtWidgets.QLabel(self.nameGroupBoxWidget)
		self.patternLineEdit = QtWidgets.QLineEdit(self.nameGroupBoxWidget)
		self.patternLineEdit.setObjectName('patternLineEdit')
		self.patternLineEdit.setFixedHeight(50)

		self.nameGroupBoxWidgetLayout.addWidget(self.nameLabel, 0, 0)
		self.nameGroupBoxWidgetLayout.addWidget(self.nameLineEdit, 0, 1)
		self.nameGroupBoxWidgetLayout.addWidget(self.patternLabel, 1, 0)
		self.nameGroupBoxWidgetLayout.addWidget(self.patternLineEdit, 1, 1)

		self.formLayout.addWidget(self.nameGroupBoxWidget)

		self.checkBoxGroupBoxWidget = QtWidgets.QGroupBox('Style', Form)
		self.checkBoxGroupBoxWidget.setObjectName("checkBoxFrame")
		self.checkBoxGroupBoxWidgetLayout = QtWidgets.QVBoxLayout(self.checkBoxGroupBoxWidget)

		self.strikeCheckbox = QtWidgets.QCheckBox(self.checkBoxGroupBoxWidget)
		self.strikeCheckbox.setObjectName("strikeCheckbox")
		self.checkBoxGroupBoxWidgetLayout.addWidget(self.strikeCheckbox)
		self.italicCheckBox = QtWidgets.QCheckBox(self.checkBoxGroupBoxWidget)
		self.italicCheckBox.setObjectName("italicCheckBox")
		self.checkBoxGroupBoxWidgetLayout.addWidget(self.italicCheckBox)
		self.boldCheckBox = QtWidgets.QCheckBox(self.checkBoxGroupBoxWidget)
		self.boldCheckBox.setObjectName("boldCheckBox")
		self.checkBoxGroupBoxWidgetLayout.addWidget(self.boldCheckBox)

		self.formLayout.addWidget(self.checkBoxGroupBoxWidget)

		self.fontGroupBox = QtWidgets.QGroupBox('Font', Form)
		self.fontGroupBoxLayout = QtWidgets.QGridLayout(self.fontGroupBox)

		self.fontLabel = QtWidgets.QLabel(self.fontGroupBox)
		self.fontLabel.setObjectName("fontLabel")
		self.fontGroupBoxLayout.addWidget(self.fontLabel, 0, 0)
		self.fontComboBox = QtWidgets.QFontComboBox(self.fontGroupBox)
		self.fontComboBox.setObjectName("fontComboBox")
		self.fontGroupBoxLayout.addWidget(self.fontComboBox, 0, 1)

		self.fontSizeLabel = QtWidgets.QLabel(self.fontGroupBox)
		self.fontSizeLabel.setObjectName("fontSizeLabel")
		self.fontGroupBoxLayout.addWidget(self.fontSizeLabel, 1, 0)
		self.fontSizeCombo = QtWidgets.QComboBox(self.fontGroupBox)
		self.fontSizeCombo.setObjectName("fontSizeCombo")
		self.fontGroupBoxLayout.addWidget(self.fontSizeCombo, 1, 1)
		self.fontGroupBoxLayout.setColumnStretch(1, 1)
		self.formLayout.addWidget(self.fontGroupBox)

		self.colorGroupBox = QtWidgets.QGroupBox('Color', Form)
		self.colorGroupBoxLayout = QtWidgets.QGridLayout(self.colorGroupBox)

		self.colorLabel = QtWidgets.QLabel(self.colorGroupBox)
		self.colorLabel.setObjectName("colorLabel")
		self.colorGroupBoxLayout.addWidget(self.colorLabel, 0, 0)
		self.colorButton = QtWidgets.QPushButton(self.colorGroupBox)
		self.colorButton.setFixedHeight(24)
		self.colorButton.setText("")
		self.colorButton.setObjectName("colorButton")
		self.colorGroupBoxLayout.addWidget(self.colorButton, 0, 1)

		self.backColorLabel = QtWidgets.QLabel(self.colorGroupBox)
		self.backColorLabel.setObjectName("backColorLabel")
		self.backColorButton = ButtonWithRightClick(self.colorGroupBox)
		self.backColorButton.setFixedHeight(24)
		self.backColorButton.setText("")
		self.backColorButton.setObjectName("backColorButton")
		self.colorGroupBoxLayout.addWidget(self.backColorLabel, 1, 0)
		self.colorGroupBoxLayout.addWidget(self.backColorButton, 1, 1)

		self.colorGroupBoxLayout.setColumnStretch(1, 1)

		self.formLayout.addWidget(self.colorGroupBox)
		self.previewDisplayWidget = QtWidgets.QWidget(Form)
		self.previewDisplayWidget.setObjectName("frame")
		self.previewDisplayWidgetLayout = QtWidgets.QVBoxLayout(self.previewDisplayWidget)
		self.previewDisplayWidgetLayout.setSpacing(8)
		self.previewDisplayWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.previewDisplayWidgetLayout.setObjectName("verticalLayout_2")
		self.previewWidgetLabel = QtWidgets.QLabel(self.previewDisplayWidget)
		self.previewDisplayWidgetLayout.addWidget(self.previewWidgetLabel)
		self.previewDisplay = QtWidgets.QLineEdit(self.previewDisplayWidget)
		self.previewDisplay.setFixedHeight(100)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.previewDisplay.sizePolicy().hasHeightForWidth())
		self.previewDisplay.setSizePolicy(sizePolicy)
		self.previewDisplay.setSizeIncrement(QtCore.QSize(0, 0))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setStrikeOut(False)
		self.previewDisplay.setFont(font)
		self.previewDisplay.setCursor(QtCore.Qt.IBeamCursor)
		self.previewDisplay.setEchoMode(QtWidgets.QLineEdit.Normal)
		self.previewDisplay.setCursorPosition(17)
		self.previewDisplay.setAlignment(QtCore.Qt.AlignCenter)
		self.previewDisplay.setDragEnabled(False)
		self.previewDisplay.setReadOnly(True)
		self.previewDisplay.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
		self.previewDisplay.setObjectName("previewDisplay")
		self.previewDisplayWidgetLayout.addWidget(self.previewDisplay)
		self.formLayout.addWidget(self.previewDisplayWidget)
		self.formLayout.addItem(
			QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

		self.resetWidget = QtWidgets.QWidget(Form)
		self.resetLayout = QtWidgets.QHBoxLayout(self.resetWidget)
		self.resetLayout.setObjectName('resetLayout')
		self.resetLayout.setContentsMargins(0, 0, 0, 0)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.newButton = QtWidgets.QPushButton(self.resetWidget)
		self.deleteButton = QtWidgets.QPushButton(self.resetWidget)
		self.resetButton = QtWidgets.QPushButton(self.resetWidget)

		self.resetLayout.addWidget(self.resetButton)
		self.resetLayout.addItem(spacerItem)
		self.resetLayout.addWidget(self.newButton)
		self.resetLayout.addWidget(self.deleteButton)

		self.formLayout.addWidget(self.resetWidget)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)


	def retranslateUi(self, Form):
		Form.setWindowTitle("Preferences")
		self.strikeCheckbox.setText("Strike Out")
		self.italicCheckBox.setText("Italic")
		self.boldCheckBox.setText("Bold")
		self.fontLabel.setText("Font")
		self.fontSizeLabel.setText("Font Size")
		self.colorLabel.setText("Color")
		self.backColorLabel.setText("Background")
		self.previewWidgetLabel.setText("Preview")
		self.previewDisplay.setText("this is test text")
		self.deleteButton.setText("Delete")
		self.newButton.setText("New")
		self.nameLabel.setText("Name")
		self.resetButton.setText('Reset')
		self.patternLabel.setText("Pattern")
		self.nameLineEdit.setPlaceholderText('Enter a Name')
		self.patternLineEdit.setPlaceholderText('Example : \\[\\+\\].*')


class TextEditorPreferencesWidget(Ui_Form, QtWidgets.QFrame, ConfigurationService, PreferencesService):
	fontChanged = QtCore.Signal()
	acceptPreferences = QtCore.Signal(list)


	def __init__(self, parent = None):
		super(TextEditorPreferencesWidget, self).__init__(parent)
		patternListInDefault = self.configuration().get('patterns', [])
		patternInPreferences = self.preferences().get('pattern', {})
		if len(patternInPreferences) == 0:
			self.patternArray = list(map(lambda patternInDict: StyleItem.create(patternInDict), patternListInDefault))
		else:
			self.patternArray = list(map(lambda patternInDict: StyleItem.create(patternInDict), patternInPreferences))
		self.default = []
		self.__isChanged = False

		self.currentPattern = None
		self.colorDialog = QtWidgets.QColorDialog(self)
		self.setupUi(self)

		self.modeCombobox.addItems(list(map(lambda item: item.name, self.patternArray)))
		self.fontSizeCombo.addItems(list(map(lambda x: str(x), QtGui.QFontDatabase().standardSizes())))

		self.previewDisplay.setAlignment(QtCore.Qt.AlignLeft)
		self.initSignalandSlots()
		self.initialize(0)
		self.dynamicInitSignalandSlots()


	def initialize(self, index):
		self.patternLineEdit.setProperty('error', False)
		self.modeCombobox.setCurrentIndex(index)
		self.setWindowOpacity(1.0)
		self.currentPattern = self.patternArray[index]
		charFormat = self.currentPattern.charFormat
		font = charFormat.font()
		self.patternLineEdit.setText(self.currentPattern.pattern)
		self.nameLineEdit.setText(self.currentPattern.name)
		self.fontComboBox.setCurrentIndex(self.fontComboBox.findText(QtGui.QFontInfo(font).family()))
		self.fontSizeCombo.setCurrentIndex(self.fontSizeCombo.findText(str(font.pointSize())))
		self.italicCheckBox.setChecked(bool(int(font.italic())))
		self.strikeCheckbox.setChecked(bool(int(font.strikeOut())))
		self.boldCheckBox.setChecked(True if font.weight() == QtGui.QFont.Bold else False)
		self.fontComboBox.setCurrentIndex(self.fontComboBox.findText(QtGui.QFontInfo(font).family()))
		self.fontSizeCombo.setCurrentIndex(self.fontSizeCombo.findText(str(font.pointSize())))
		qss = "background-color: %s;border-radius:8px;" % charFormat.foreground().color().name()
		self.colorButton.setStyleSheet(qss)
		qss = "background-color: %s;border-radius:8px;" % charFormat.background().color().name()
		if charFormat.background().isOpaque():
			self.backColorButton.setStyleSheet(qss)
		else:
			self.setBackgroundNone()
		self.updatePreview()


	def dynamicInitSignalandSlots(self):
		self.italicCheckBox.stateChanged.connect(
			lambda value: self.checkBoxChanged(self.currentPattern.charFormat.setFontItalic, bool(value)))
		self.strikeCheckbox.stateChanged.connect(
			lambda value: self.checkBoxChanged(self.currentPattern.charFormat.setFontStrikeOut, bool(value)))
		self.boldCheckBox.stateChanged.connect(
			lambda value: self.checkBoxChanged(self.currentPattern.charFormat.setFontWeight,
											   QtGui.QFont.Bold if bool(value) else QtGui.QFont.Normal))
		self.nameLineEdit.textChanged.connect(self.nameChange)


	def initSignalandSlots(self):
		self.fontChanged.connect(self.__fontChanged)
		self.modeCombobox.currentIndexChanged.connect(self.modeChanged)
		self.colorButton.clicked.connect(
			lambda: self._setColorIntoDialog(self.currentPattern.charFormat.foreground().color(), 'foreground'))
		self.backColorButton.clicked.connect(
			lambda: self._setColorIntoDialog(self.currentPattern.charFormat.background().color(), 'backgorund'))
		self.colorDialog.accepted.connect(self.openColorPicker)
		self.fontSizeCombo.currentIndexChanged.connect(self.fontChangedSlot)
		self.fontComboBox.currentIndexChanged.connect(self.fontChangedSlot)
		self.patternLineEdit.textChanged.connect(self.patternChange)

		self.newButton.clicked.connect(self.newConfItem)
		self.deleteButton.clicked.connect(self.deleteConfItem)
		self.resetButton.clicked.connect(self.reset)
		self.backColorButton.rightClicked.connect(self.setBackgroundNone)


	def modeChanged(self, index):
		self.initialize(index)


	@QtCore.Slot()
	def checkBoxChanged(self, method, value):
		method(value)
		self.fontChanged.emit()


	def setBackgroundNone(self):
		self.currentPattern.charFormat.setBackground(QtGui.QBrush())
		self.backColorButton.setStyleSheet("QPushButton{border:2px solid red;border-radius:8px;}")
		self.fontChanged.emit()


	@QtCore.Slot()
	def setMargin(self, method, value):
		method(value)
		self.fontChanged.emit()


	def _setColorIntoDialog(self, color, type):
		self.colorDialog.setProperty('object', type)
		self.colorDialog.setCurrentColor(color)
		self.colorDialog.show()


	@QtCore.Slot()
	def openColorPicker(self):
		color = self.colorDialog.currentColor()
		if color.isValid():
			hexColor = color.name()
			qss = "background-color: %s;border-radius:8px" % hexColor
			if self.colorDialog.property('object') == 'foreground':
				self.colorButton.setStyleSheet(qss)
				self.currentPattern.charFormat.setForeground(color)
			else:
				self.backColorButton.setStyleSheet(qss)
				self.currentPattern.charFormat.setBackground(color)
				self.backColorButton.setIcon(QtGui.QIcon())
			self.fontChanged.emit()


	@QtCore.Slot()
	def fontChangedSlot(self, *args):
		px = self.fontSizeCombo.currentText()
		family = self.fontComboBox.currentText()
		self.currentPattern.charFormat.setFontFamily(family)
		self.currentPattern.charFormat.setFontPointSize(int(px))
		self.fontChanged.emit()


	def nameChange(self, value):
		self.currentPattern.name = value


	def patternChange(self, value):
		try:
			if value:
				re.compile(value)
				self.currentPattern.pattern = value
				self.patternLineEdit.setStyleSheet('background-color: #3f5c3d;')
				self.newButton.setEnabled(True)
				self.deleteButton.setEnabled(True)
				self.modeCombobox.setEnabled(True)
			else:
				raise Exception('Pattern value is empty')

		except:
			self.patternLineEdit.setStyleSheet('background-color: #5c3e3d;')
			self.newButton.setEnabled(False)
			self.deleteButton.setEnabled(False)
			self.modeCombobox.setEnabled(False)


	def updatePreview(self):
		self.previewDisplay.setFont(self.currentPattern.charFormat.font())
		backgroundColor = self.currentPattern.charFormat.background()
		if backgroundColor.isOpaque():
			background = backgroundColor.color().name()
		else:
			background = '#2B2B2B'
		qss = "color: %s;background-color : %s" % (
			self.currentPattern.charFormat.foreground().color().name(), background)
		self.previewDisplay.setStyleSheet(qss)


	def newConfItem(self):
		item = self.currentPattern.copy()
		item.name = 'New Item'
		item.pattern = 'New Pattern'
		self.patternArray.append(item)
		self.modeCombobox.addItem(item.name)
		self.modeCombobox.setCurrentIndex(len(self.patternArray) - 1)


	def reset(self):
		pass


	def deleteConfItem(self):
		index = self.patternArray.index(self.currentPattern)
		self.patternArray.remove(self.currentPattern)
		self.modeCombobox.removeItem(index)
		self.initialize(0)


	def accept(self):
		self.acceptPreferences.emit(self.patternArray)
		super(TextEditorPreferencesWidget, self).accept()


	def name(self):
		return 'Text Editor'


	def changed(self):
		return self.__isChanged


	def __fontChanged(self):
		self.__isChanged = True
		self.updatePreview()
