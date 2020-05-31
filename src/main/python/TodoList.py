#!/Users/coskunyerli/PycharmProjects/ive/venv/bin/python
# --coding: utf-8 --
import datetime
import os
import sys
import logging as log
from model.fbs import TodoListApplicationContext
import PySide2.QtWidgets as QtWidgets

if __name__ == "__main__":
	# setup app
	fbs = TodoListApplicationContext()
	try:
		logName = datetime.datetime.now().strftime("%m-%d-%Y.log")
		log.basicConfig(filename = os.path.join(fbs.get_resource('log'), logName),
						format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = log.INFO)
	except Exception as e:
		QtWidgets.QMessageBox.warning(None, 'Unexpected Error is occurred while creating log file', str(e))
	log.info('Kiwi begins...')
	try:
		import core
		from service.configurationService import ConfigurationService
		from service.dataListModelService import DataListModelFolderItemService
		from service.saveListModelService import SaveListModelFolderItemService
		from widget.mainWindow import MainWindow

		log.info('Library is imported successfully...')

		# initialize services
		saveListService = SaveListModelFolderItemService()
		dataListService = DataListModelFolderItemService()
		confService = ConfigurationService()
		log.info('Services is started successfully...')

		saveListService.saveListModelService().setPath(fbs.fileListPath)
		dataListService.dataListModelService().setPath(fbs.filePath)


		confService.configuration().setPath(fbs.conf)
		confService.configuration().read()
		log.info('Configuration is loaded successfully...')

		core.fbs = fbs
		# setup Qt app for ui
		fbs.app.setApplicationName("Kiwi")

		# setup ui
		mainWindow = MainWindow()
		log.info('Widget is created successfully...')

		mainQss = fbs.qss('style.qss')
		if mainQss is not None:
			mainWindow.setStyleSheet(mainQss)
			log.info('Styles are loaded successfully...')
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
