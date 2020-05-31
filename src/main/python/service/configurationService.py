import json


class __ConfigurationService__(object):
	def __init__(self):
		self.path = None
		self.data = {}


	def get(self, key, default = None):
		data = self.data.get(key)
		if data is None:
			return default
		else:
			return data


	def setPath(self, path):
		self.path = path


	def read(self):
		try:
			with open(self.path, 'r') as confFile:
				configInString = confFile.read()
				config = json.loads(configInString)
				self.data = config
		except FileNotFoundError as e:
			raise FileNotFoundError('No such file or directory for configuration file')


__configuration__ = __ConfigurationService__()


class ConfigurationService(object):
	def configuration(self):
		return __configuration__
