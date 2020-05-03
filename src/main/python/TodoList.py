#!/Users/coskunyerli/PycharmProjects/ive/venv/bin/python
# --coding: utf-8 --
import sys
import logging as log
from model.fbs import TodoListApplicationContext
import PySide2.QtWidgets as QtWidgets

if __name__ == "__main__":
	# setup app
	fbs = TodoListApplicationContext()
	try:
		import core
		from service.configurationService import ConfigurationService
		from service.dataListModelService import DataListModelFolderItemService
		from service.saveListModelService import SaveListModelFolderItemService
		from widget.mainWindow import MainWindow

		# initialize services
		saveListService = SaveListModelFolderItemService()
		saveListService.saveListModelService().setPath(fbs.fileListPath)
		dataListService = DataListModelFolderItemService()
		dataListService.dataListModelService().setPath(fbs.filePath)

		confService = ConfigurationService()
		confService.configuration().setPath(fbs.conf)
		confService.configuration().read()

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
	except Exception as e:
		QtWidgets.QMessageBox.warning(None, 'Unexpected Error is occurred', str(e))
		exit(-1)
	try:
		sys.exit(fbs.app.exec_())
	except Exception as e:
		QtWidgets.QMessageBox.warning(None, 'Unexpected runtime Error is occurred', str(e))
		exit(-1)
