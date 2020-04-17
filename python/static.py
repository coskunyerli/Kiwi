import sys, inspect


def increment_char(c):
	return chr(ord(c) + 1) if c != 'z' else 'a'


def increment_str(s):
	if s == '':
		return 'a'
	lpart = s.rstrip('z')
	num_replacements = len(s) - len(lpart)
	new_s = lpart[:-1] + increment_char(lpart[-1]) if lpart else 'a'
	new_s += 'a' * num_replacements
	return new_s


def get_classes(name):
	klasses = {}
	for name, obj in inspect.getmembers(sys.modules[name]):
		if inspect.isclass(obj):
			klasses[obj.__name__] = obj
	return klasses
