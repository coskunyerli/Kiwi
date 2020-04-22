# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/preferencesDialogue.ui'
#
# Created: Sun Jun 17 21:53:40 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import os
import re

from PySide2 import QtGui, QtCore, QtWidgets
from widget.buttonWithRightClick import ButtonWithRightClick


class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.modeCombobox = QtWidgets.QComboBox(Form)
		self.modeCombobox.setObjectName("modeCombobox")
		self.verticalLayout_3.addWidget(self.modeCombobox)
		self.checkBoxFrame = QtWidgets.QWidget(Form)
		self.checkBoxFrame.setObjectName("checkBoxFrame")
		self.gridLayout = QtWidgets.QHBoxLayout(self.checkBoxFrame)
		self.gridLayout.setSpacing(0)
		self.gridLayout.setContentsMargins(9, 0, 9, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.strikeCheckbox = QtWidgets.QCheckBox(self.checkBoxFrame)
		self.strikeCheckbox.setObjectName("strikeCheckbox")
		self.gridLayout.addWidget(self.strikeCheckbox)
		self.italicCheckBox = QtWidgets.QCheckBox(self.checkBoxFrame)
		self.italicCheckBox.setObjectName("italicCheckBox")
		self.gridLayout.addWidget(self.italicCheckBox)
		self.boldCheckBox = QtWidgets.QCheckBox(self.checkBoxFrame)
		self.boldCheckBox.setObjectName("boldCheckBox")
		self.gridLayout.addWidget(self.boldCheckBox)

		self.nameFrame = QtWidgets.QWidget(Form)
		self.nameFrame.setObjectName("nameFrame")
		self.nameLayout = QtWidgets.QHBoxLayout(self.nameFrame)
		self.nameLabel = QtWidgets.QLabel(self.nameFrame)
		self.nameLineEdit = QtWidgets.QLineEdit(self.nameFrame)
		self.nameLayout.addWidget(self.nameLabel)
		self.nameLayout.addWidget(self.nameLineEdit)

		self.patternFrame = QtWidgets.QWidget(Form)
		self.patternFrame.setObjectName("patternFrame")
		self.patternLayout = QtWidgets.QHBoxLayout(self.patternFrame)
		self.patternLabel = QtWidgets.QLabel(self.patternFrame)
		self.patternLineEdit = QtWidgets.QLineEdit(self.patternFrame)
		self.patternLineEdit.setObjectName('patternLineEdit')
		self.patternLayout.addWidget(self.patternLabel)
		self.patternLayout.addWidget(self.patternLineEdit)
		self.verticalLayout_3.addWidget(self.nameFrame)
		self.verticalLayout_3.addWidget(self.patternFrame)
		self.verticalLayout_3.addWidget(self.checkBoxFrame)

		self.fontFrame = QtWidgets.QWidget(Form)
		self.fontFrame.setObjectName("fontFrame")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.fontFrame)
		self.horizontalLayout.setContentsMargins(9, 9, -1, 9)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.fontFamiliyWidget = QtWidgets.QWidget(self.fontFrame)
		self.fontFamiliyWidget.setObjectName("fontFamiliyWidget")
		self.verticalLayout_5 = QtWidgets.QHBoxLayout(self.fontFamiliyWidget)
		self.verticalLayout_5.setContentsMargins(-1, 9, -1, 9)
		self.verticalLayout_5.setObjectName("verticalLayout_5")
		self.fontLabel = QtWidgets.QLabel(self.fontFamiliyWidget)
		self.fontLabel.setObjectName("fontLabel")
		self.verticalLayout_5.addWidget(self.fontLabel)
		self.fontComboBox = QtWidgets.QFontComboBox(self.fontFamiliyWidget)
		self.fontComboBox.setObjectName("fontComboBox")
		self.verticalLayout_5.addWidget(self.fontComboBox)
		self.horizontalLayout.addWidget(self.fontFamiliyWidget)
		self.fontStyleWidget = QtWidgets.QWidget(self.fontFrame)
		self.fontStyleWidget.setObjectName("fontStyleWidget")
		self.horizontalLayout.addWidget(self.fontStyleWidget)
		self.pixedWidget = QtWidgets.QWidget(self.fontFrame)
		self.pixedWidget.setObjectName("pixedWidget")
		self.verticalLayout_4 = QtWidgets.QHBoxLayout(self.pixedWidget)
		self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.pixelLabel = QtWidgets.QLabel(self.pixedWidget)
		self.pixelLabel.setObjectName("pixelLabel")
		self.verticalLayout_4.addWidget(self.pixelLabel)
		self.fontSizeCombo = QtWidgets.QComboBox(self.pixedWidget)
		self.fontSizeCombo.setObjectName("fontSizeCombo")
		self.verticalLayout_4.addWidget(self.fontSizeCombo)
		self.horizontalLayout.addWidget(self.pixedWidget)
		self.verticalLayout_3.addWidget(self.fontFrame)
		self.colorFrame = QtWidgets.QWidget(Form)
		self.colorFrame.setObjectName("colorFrame")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.colorFrame)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.colorLabel = QtWidgets.QLabel(self.colorFrame)
		self.colorLabel.setObjectName("colorLabel")
		self.horizontalLayout_2.addWidget(self.colorLabel)
		self.colorButton = QtWidgets.QToolButton(self.colorFrame)
		self.colorButton.setText("")
		self.colorButton.setObjectName("colorButton")
		self.horizontalLayout_2.addWidget(self.colorButton)

		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem)

		self.backColorLabel = QtWidgets.QLabel(self.colorFrame)
		self.backColorLabel.setObjectName("backColorLabel")
		self.horizontalLayout_2.addWidget(self.backColorLabel)
		self.backColorButton = ButtonWithRightClick(self.colorFrame)
		self.backColorButton.setText("")
		self.backColorButton.setObjectName("backColorButton")
		self.horizontalLayout_2.addWidget(self.backColorButton)

		self.verticalLayout_3.addWidget(self.colorFrame)
		self.frame = QtWidgets.QWidget(Form)
		self.frame.setObjectName("frame")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
		self.verticalLayout_2.setSpacing(20)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.label = QtWidgets.QLabel(self.frame)
		self.label.setObjectName("label")
		self.verticalLayout_2.addWidget(self.label)
		self.previewDisplay = QtWidgets.QLineEdit(self.frame)
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
		self.verticalLayout_2.addWidget(self.previewDisplay)
		self.verticalLayout_3.addWidget(self.frame)
		spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(spacerItem1)

		self.resetWidget = QtWidgets.QWidget(Form)
		self.resetLayout = QtWidgets.QHBoxLayout(self.resetWidget)
		self.resetLayout.setObjectName('resetLayout')
		self.okButton = QtWidgets.QPushButton(self.resetWidget)
		self.cancelButton = QtWidgets.QPushButton(self.resetWidget)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.newButton = QtWidgets.QPushButton(self.resetWidget)
		self.deleteButton = QtWidgets.QPushButton(self.resetWidget)
		self.resetLayout.addWidget(self.newButton)
		self.resetLayout.addWidget(self.deleteButton)
		self.resetLayout.addItem(spacerItem)
		self.resetLayout.addWidget(self.cancelButton)
		self.resetLayout.addWidget(self.okButton)

		self.verticalLayout_3.addWidget(self.resetWidget)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)


	def retranslateUi(self, Form):
		Form.setWindowTitle("Preferences")
		self.strikeCheckbox.setText("Strike Out")
		self.italicCheckBox.setText("Italic")
		self.boldCheckBox.setText("Bold")
		self.fontLabel.setText("Font")
		self.pixelLabel.setText("Px")
		self.colorLabel.setText("Color")
		self.backColorLabel.setText("Background")
		self.label.setText("Preview")
		self.previewDisplay.setText("this is test text")
		self.okButton.setText("OK")
		self.cancelButton.setText("Cancel")
		self.deleteButton.setText("Delete")
		self.newButton.setText("New")
		self.nameLabel.setText("Name")
		self.patternLabel.setText("Pattern")
		self.nameLineEdit.setPlaceholderText('Enter a Name')
		self.patternLineEdit.setPlaceholderText('Example : \\[\\+\\].*')


class Preferences(Ui_Form, QtWidgets.QDialog):
	fontChanged = QtCore.Signal()
	acceptPreferences = QtCore.Signal(list)


	def __init__(self, parent = None, **kwargs):
		super(Preferences, self).__init__(parent)
		self.confFileList = kwargs.get('preferences')
		self.fontArray = list(map(lambda item: item.copy(), self.confFileList))
		self.default = []

		self.currentFont = None
		self.colorDialog = QtWidgets.QColorDialog(self)
		self.setupUi(self)

		self.modeCombobox.addItems(list(map(lambda item: item.name, self.fontArray)))
		self.fontSizeCombo.addItems(list(map(lambda x: str(x), QtGui.QFontDatabase().standardSizes())))

		self.previewDisplay.setAlignment(QtCore.Qt.AlignLeft)
		self.initSignalandSlots()
		self.initialize(0)
		self.dynamicInitSignalandSlots()


	def initialize(self, index):
		self.patternLineEdit.setProperty('error', False)
		self.modeCombobox.setCurrentIndex(index)
		self.okButton.setDefault(True)
		self.setWindowOpacity(1.0)
		self.currentFont = self.fontArray[index]
		charFormat = self.currentFont.charFormat
		font = charFormat.font()
		self.patternLineEdit.setText(self.currentFont.pattern)
		self.nameLineEdit.setText(self.currentFont.name)
		self.fontComboBox.setCurrentIndex(self.fontComboBox.findText(QtGui.QFontInfo(font).family()))
		self.fontSizeCombo.setCurrentIndex(self.fontSizeCombo.findText(str(font.pointSize())))
		self.italicCheckBox.setChecked(bool(int(font.italic())))
		self.strikeCheckbox.setChecked(bool(int(font.strikeOut())))
		self.boldCheckBox.setChecked(True if font.weight() == QtGui.QFont.Bold else False)
		self.fontComboBox.setCurrentIndex(self.fontComboBox.findText(QtGui.QFontInfo(font).family()))
		self.fontSizeCombo.setCurrentIndex(self.fontSizeCombo.findText(str(font.pointSize())))
		qss = "background-color: %s" % charFormat.foreground().color().name()
		self.colorButton.setStyleSheet(qss)
		qss = "background-color: %s" % charFormat.background().color().name()
		if charFormat.background().isOpaque():
			self.backColorButton.setStyleSheet(qss)
		else:
			self.setBackgroundNone()
		self.fontChanged.emit()


	def dynamicInitSignalandSlots(self):
		self.italicCheckBox.stateChanged.connect(
				lambda value: self.checkBoxChanged(self.currentFont.charFormat.setFontItalic, bool(value)))
		self.strikeCheckbox.stateChanged.connect(
				lambda value: self.checkBoxChanged(self.currentFont.charFormat.setFontStrikeOut, bool(value)))
		self.boldCheckBox.stateChanged.connect(
				lambda value: self.checkBoxChanged(self.currentFont.charFormat.setFontWeight,
												   QtGui.QFont.Bold if bool(value) else QtGui.QFont.Normal))
		self.nameLineEdit.textChanged.connect(self.nameChange)
		self.patternLineEdit.textChanged.connect(self.patternChange)


	def initSignalandSlots(self):
		self.fontChanged.connect(self.updatePreview)
		self.modeCombobox.currentIndexChanged.connect(self.modeChanged)
		self.colorButton.clicked.connect(
				lambda: self._setColorIntoDialog(self.currentFont.charFormat.foreground().color(), 'foreground'))
		self.backColorButton.clicked.connect(
				lambda: self._setColorIntoDialog(self.currentFont.charFormat.background().color(), 'backgorund'))
		self.colorDialog.accepted.connect(self.openColorPicker)
		self.fontSizeCombo.currentIndexChanged.connect(self.fontChangedSlot)
		self.fontComboBox.currentIndexChanged.connect(self.fontChangedSlot)

		self.cancelButton.clicked.connect(self.reject)
		self.okButton.clicked.connect(self.accept)
		self.newButton.clicked.connect(self.newConfItem)
		self.deleteButton.clicked.connect(self.deleteConfItem)
		self.backColorButton.rightClicked.connect(self.setBackgroundNone)


	def modeChanged(self, index):
		self.initialize(index)


	@QtCore.Slot()
	def checkBoxChanged(self, method, value):
		method(value)
		self.fontChanged.emit()


	def setBackgroundNone(self):
		self.currentFont.charFormat.setBackground(QtGui.QBrush())
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(core.fbs.icons('transparent.png')))
		self.backColorButton.setStyleSheet("QPushButton{text-align:left}")
		self.backColorButton.setIconSize(QtCore.QSize(30, 30))
		self.backColorButton.setIcon(icon)
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
			qss = "background-color: %s" % hexColor
			if self.colorDialog.property('object') == 'foreground':
				self.colorButton.setStyleSheet(qss)
				self.currentFont.charFormat.setForeground(color)
			else:
				self.backColorButton.setStyleSheet(qss)
				self.currentFont.charFormat.setBackground(color)
				self.backColorButton.setIcon(QtGui.QIcon())
			self.fontChanged.emit()


	@QtCore.Slot()
	def fontChangedSlot(self, *args):
		px = self.fontSizeCombo.currentText()
		family = self.fontComboBox.currentText()
		self.currentFont.charFormat.setFontFamily(family)
		self.currentFont.charFormat.setFontPointSize(int(px))
		self.fontChanged.emit()


	def nameChange(self, value):
		self.currentFont.name = value


	def patternChange(self, value):
		try:
			if value:
				re.compile(value)
				self.currentFont.pattern = value
				self.patternLineEdit.setStyleSheet('background-color: white;')
				self.okButton.setEnabled(True)
				self.newButton.setEnabled(True)
				self.deleteButton.setEnabled(True)
				self.modeCombobox.setEnabled(True)
			else:
				raise Exception('Pattern value is empty')

		except:
			self.patternLineEdit.setStyleSheet('background-color: #FFC5C4;')
			self.okButton.setEnabled(False)
			self.newButton.setEnabled(False)
			self.deleteButton.setEnabled(False)
			self.modeCombobox.setEnabled(False)


	def updatePreview(self):
		self.previewDisplay.setFont(self.currentFont.charFormat.font())
		backgroundColor = self.currentFont.charFormat.background()
		if backgroundColor.isOpaque():
			background = backgroundColor.color().name()
		else:
			background = '#2B2B2B'
		qss = "color: %s;background-color : %s" % (self.currentFont.charFormat.foreground().color().name(), background)
		self.previewDisplay.setStyleSheet(qss)


	def newConfItem(self):
		item = self.currentFont.copy()
		item.name = 'New Item'
		item.pattern = 'New Pattern'
		self.fontArray.append(item)
		self.modeCombobox.addItem(item.name)
		self.modeCombobox.setCurrentIndex(len(self.fontArray) - 1)


	def deleteConfItem(self):
		index = self.fontArray.index(self.currentFont)
		self.fontArray.remove(self.currentFont)
		self.modeCombobox.removeItem(index)
		self.initialize(0)


	def accept(self):
		self.acceptPreferences.emit(self.fontArray)
		super(Preferences, self).accept()
