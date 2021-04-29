import json
import logging as log


class __PreferencesService__(object):
	def __init__(self):
		self.__data = {}


	def data(self):
		return self.__data


	def get(self, key, default = None):
		data = self.__data.get(key)
		if data is None:
			return default
		else:
			return data


	def read(self, setting):
		preferencesInJson = setting.value('preferences', {})
		try:
			preferencesInDict = json.loads(preferencesInJson)
			if len(preferencesInDict) == 0:
				log.warning(f'Preferences is empty')
			self.__data = preferencesInDict
		except Exception as e:
			log.error(f'Preferences is not loaded successfully. Exception is {e}')


	def write(self, setting):
		try:
			preferencesInJson = json.dumps(self.data())
			setting.setValue('preferences', preferencesInJson)
		except Exception as e:
			log.error(f'Preferences is not wrote successfully. Exception is {e}')


__preferences__ = __PreferencesService__()


class PreferencesService(object):
	def preferences(self):
		return __preferences__
