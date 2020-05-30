# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/Story/ui/storyPreferencesDialog.ui'
#
# Created: Mon Feb 19 10:17:47 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
import copy
import os

import core
import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets

"""
this is preferences dialog. when clicked the prefences button, this dialog will open in story app
"""


class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Preferences")
		Dialog.resize(Dialog.parent().size())
		self.verticalMainLayout = QtWidgets.QVBoxLayout(Dialog)
		self.verticalMainLayout.setObjectName("gridLayout")
		self.verticalMainLayout.setSpacing(0)
		self.verticalMainLayout.setContentsMargins(0, 0, 0, 0)

		self.mainWidget = QtWidgets.QFrame(Dialog)
		self.mainWidget.setObjectName('mainWidget')

		self.horizontalWidgetLayout = QtWidgets.QHBoxLayout(self.mainWidget)
		self.horizontalWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalWidgetLayout.setSpacing(0)

		self.preferencesInfoWidget = QtWidgets.QWidget(self.mainWidget)
		self.preferencesInfoWidgetLayout = QtWidgets.QVBoxLayout(self.preferencesInfoWidget)
		self.preferencesInfoWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.preferencesInfoWidgetLayout.setSpacing(1)

		self.preferencesInfoLabel = QtWidgets.QLabel(self.preferencesInfoWidget)
		# self.preferencesInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.preferencesInfoLabel.setObjectName('preferencesInfoLabel')
		# self.preferencesInfoLabel.setMargin(8)
		self.preferencesWidget = QtWidgets.QFrame(self.preferencesInfoWidget)

		self.preferencesInfoWidgetLayout.addWidget(self.preferencesInfoLabel)
		self.preferencesInfoWidgetLayout.addWidget(self.preferencesWidget)

		self.preferencesWidgetLayout = QtWidgets.QHBoxLayout(self.preferencesWidget)
		self.preferencesWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.preferencesWidgetLayout.setSpacing(0)

		self.categoryListWidget = QtWidgets.QListWidget(self.mainWidget)
		self.categoryListWidget.setFixedWidth(200)
		self.categoryListWidget.setObjectName('categoryListWidget')

		self.horizontalWidgetLayout.addWidget(self.categoryListWidget)
		self.horizontalWidgetLayout.addWidget(self.preferencesInfoWidget)

		self.buttonBox = QtWidgets.QWidget(Dialog)
		self.buttonBox.setObjectName('buttonBox')
		self.buttonBoxLayout = QtWidgets.QHBoxLayout(self.buttonBox)
		self.cancelButton = QtWidgets.QPushButton(self.buttonBox)
		self.cancelButton.setText('Cancel')

		self.applyButton = QtWidgets.QPushButton(self.buttonBox)
		self.applyButton.setText('Apply')

		self.okButton = QtWidgets.QPushButton(self.buttonBox)
		self.okButton.setText('Ok')

		self.buttonBoxLayout.setContentsMargins(4, 2, 4, 2)
		self.buttonBoxLayout.setSpacing(2)
		self.buttonBoxLayout.addWidget(self.applyButton)
		self.buttonBoxLayout.addItem(
				QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.buttonBoxLayout.addWidget(self.cancelButton)
		self.buttonBoxLayout.addWidget(self.okButton)

		self.verticalMainLayout.addWidget(self.mainWidget)
		self.verticalMainLayout.addWidget(self.buttonBox)
		self.retranslateUi(Dialog)
		self.okButton.clicked.connect(Dialog.accept)
		self.cancelButton.clicked.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)


	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(
				QtWidgets.QApplication.translate("Dialog", "Preferences", None))


categoryIndex = 0


class Preferences(Ui_Dialog, QtWidgets.QDialog):

	# this class is base class for preferences the others are in this class
	def __init__(self, parent, preferencesInJson):
		super(Preferences, self).__init__(parent)
		self.setStyleSheet(core.fbs.qss('preferences.qss'))
		self.setupUi(self)

		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.setWindowFlag(QtCore.Qt.Popup, True)

		self.widgetList = dict()
		self.currentVisibleWidget = None

		# get the preferences and modes
		self.preferences = preferencesInJson
		# setStyleSheet should be assigned here. because if I assign it after line 153 in a way I don't understand why,
		# there's a problem with style of transitionWidget in Linux os.
		self.initSignalsAndSlots()
		self.initialize()


	def initialize(self):
		self.__addItemToTheCategory(['Text Editor', 'Image Viewer', 'Save', 'Font', 'Export'])
		self.categoryListWidget.setCurrentIndex(self.categoryListWidget.model().index(categoryIndex, 0))


	def __addItemToTheCategory(self, categories):
		# generate category items
		for category in categories:
			listItem = QtWidgets.QListWidgetItem()
			listItem.setText(category)
			listItem.setSizeHint(QtCore.QSize(30, 27))
			self.categoryListWidget.addItem(listItem)


	def initSignalsAndSlots(self):
		self.categoryListWidget.currentTextChanged.connect(self.changePreferencesWidget)
		self.applyButton.clicked.connect(self.__apply)


	def changePreferencesWidget(self, text):
		currentWidget = self.widgetList[text]
		if self.currentVisibleWidget is not None:
			self.currentVisibleWidget.hide()
		currentWidget.show()
		self.currentVisibleWidget = currentWidget


	def accept(self):
		self.__apply()
		super(Preferences, self).accept()


	def __apply(self):
		return
