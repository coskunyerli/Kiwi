import json


class __ConfigurationService__(object):
	def __init__(self):
		self.path = None
		self.data = {}


	def get(self, key):
		return self.data.get(key)


	def setPath(self, path):
		self.path = path


	def read(self):
		with open(self.path, 'r') as confFile:
			configInString = confFile.read()
			config = json.loads(configInString)
			self.data = config


__configuration__ = __ConfigurationService__()


class ConfigurationService(object):
	def configuration(self):
		return __configuration__
