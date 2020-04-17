from python.static import increment_str


class BaseEnumeration(object):
	def __init__(self):
		self.name = self.__class__.__name__


	def setName(self, name):
		self.name = name


	def inc(self, text):
		return text


	def split(self, text):
		return text


	def stop(self, text):
		return (self.displayFormat() % self.split(text)) != text


	def next(self, text):
		final = self.displayFormat() % self.inc(self.split(text))
		if self.stop(text):
			return final
		else:
			return None


	def displayFormat(self):
		return '%s'


	def __str__(self):
		return self.name


	@classmethod
	def create(cls):
		return cls()


class NumberEnumeration(BaseEnumeration):
	def __init__(self):
		super(NumberEnumeration, self).__init__()


	def inc(self, text):
		try:
			return str(int(text) + 1)
		except ValueError, e:
			print str(e)
			return str(-1)


	def split(self, text):
		return text.split('.')[0]


	def displayFormat(self):
		return '%s.'


class NumberEnumeration1(NumberEnumeration):
	def displayFormat(self):
		return '%s.)'


class NumberEnumeration2(NumberEnumeration):
	def displayFormat(self):
		return '(%s)'


	def split(self, text):
		return text.split(')')[0][1:]


class NumberEnumeration3(NumberEnumeration):
	def displayFormat(self):
		return '%s)'


	def split(self, text):
		return text.split(')')[0]


class AlphabetEnumeration(BaseEnumeration):
	def __init__(self):
		super(AlphabetEnumeration, self).__init__()


	def inc(self, text):
		try:
			return increment_str(text)
		except ValueError, e:
			print str(e)
			return ''


	def displayFormat(self):
		return '%s)'


	def split(self, text):
		return text.split(')')[0]


class AlphabetEnumeration2(AlphabetEnumeration):
	def split(self, text):
		return super(AlphabetEnumeration2, self).split(text).upper()


class AlphabetEnumeration3(AlphabetEnumeration):
	def displayFormat(self):
		return '%s.)'


	def split(self, text):
		return text.split('.')[0]


class AlphabetEnumeration4(AlphabetEnumeration):
	def displayFormat(self):
		return '(%s)'


	def split(self, text):
		return text.split(')')[0][1:].upper()


class ListEnumeration(BaseEnumeration):
	def split(self, text):
		return '-'


	def displayFormat(self):
		return '%s '


class TodoEnumeration(BaseEnumeration):
	def split(self, text):
		return '[]'


	def displayFormat(self):
		return '%s '


if __name__ == '__main__':
	print NumberEnumeration2.create().next('(1) Ahmet bir salaktir')
	print globals().get('AlphabetEnumeration4').__name__
