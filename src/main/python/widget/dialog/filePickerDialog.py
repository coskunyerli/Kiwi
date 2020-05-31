import os
from shutil import copyfile

import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui
import core


class Data(object):
	def __init__(self, filename, name):
		self.filename = filename
		self.name = name


	def isValid(self):
		return self.filename is not None and self.name is not None


class FilePickerDialog(QtWidgets.QDialog):
	def __init__(self, parent = None):
		super(FilePickerDialog, self).__init__(parent)
		self.setFixedWidth(400)
		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.mainLayout.setContentsMargins(8, 8, 8, 8)

		# current data is invalid
		self.data = Data(None, None)

		self.fileWidget = QtWidgets.QWidget(self)
		self.fileWidgetLayout = QtWidgets.QHBoxLayout(self.fileWidget)
		self.fileWidgetLayout.setContentsMargins(0, 0, 0, 0)

		self.buttonGroupWidget = QtWidgets.QWidget(self)
		self.buttonGroupWidgetLayout = QtWidgets.QHBoxLayout(self.buttonGroupWidget)
		self.buttonGroupWidgetLayout.setContentsMargins(0, 0, 0, 0)
		self.buttonGroupWidgetLayout.setSpacing(4)

		self.filenameLabel = QtWidgets.QLabel(self.fileWidget)
		self.filenameLabel.setText('No file is selected*')
		self.filenameLabel.setStyleSheet('color:#aaa;font-size:11px')

		self.selectButton = QtWidgets.QPushButton(self.fileWidget)
		self.selectButton.setText('Select')

		self.fileWidgetLayout.addWidget(self.filenameLabel)
		self.fileWidgetLayout.addItem(
				QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.fileWidgetLayout.addWidget(self.selectButton)

		self.nameEdit = QtWidgets.QLineEdit(self)

		self.saveButton = QtWidgets.QPushButton(self.buttonGroupWidget)
		self.cancelButton = QtWidgets.QPushButton(self.buttonGroupWidget)
		self.saveButton.setDefault(True)

		self.buttonGroupWidgetLayout.addItem(
				QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.buttonGroupWidgetLayout.addWidget(self.cancelButton)
		self.buttonGroupWidgetLayout.addWidget(self.saveButton)

		self.mainLayout.addWidget(self.fileWidget)
		self.mainLayout.addWidget(self.nameEdit)
		self.mainLayout.addWidget(self.buttonGroupWidget)

		self.nameEdit.setPlaceholderText('Name')

		self.saveButton.setText('Save')
		self.cancelButton.setText('Cancel')
		self.saveButton.setDisabled(True)

		self.selectButton.clicked.connect(self.selectFile)
		self.nameEdit.textChanged.connect(self.updateName)
		self.cancelButton.clicked.connect(self.reject)
		self.saveButton.clicked.connect(self.accept)


	def selectFile(self):
		# select new filename
		filename, result = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
		# result should be true and filename is valid
		if result and filename:
			self.data.filename = filename
			self.filenameLabel.setText(filename)
		# check that current data should be valid
		if self.data.isValid():
			self.saveButton.setEnabled(True)
		else:
			self.saveButton.setDisabled(True)


	def updateName(self):
		# check that current data should be valid
		self.data.name = self.nameEdit.text()

		if self.data.isValid():
			self.saveButton.setEnabled(True)
		else:
			self.saveButton.setDisabled(True)


	def accept(self):
		basename = os.path.basename(self.data.filename)
		_, extension = os.path.splitext(self.data.filename)
		# check that extension can be ['.jpg', '.png', '.jpeg', .pdf .txt]. Others are not permitted
		if extension in ['.jpg', '.png', '.jpeg']:
			# create image reader and check that data can read or not
			imageReader = QtGui.QImageReader(self.data.filename)
			if imageReader.canRead():
				# copy file into local path and create data object
				writePath = os.path.join(core.fbs.filesPath, basename)
				copyfile(self.data.filename, writePath)
				self.data.filename = writePath

		elif extension == '.pdf' or extension == '.txt':
			writePath = os.path.join(core.fbs.filesPath, basename)
			copyfile(self.data.filename, writePath)
			self.data.filename = writePath
		else:
			# other extensions are not valid for now
			self.data = Data(None, None)

		super(FilePickerDialog, self).accept()
