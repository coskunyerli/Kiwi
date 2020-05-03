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


def first_(arr, func):
	for item in arr:
		if func(item):
			return item
	return None


def _binarySearch(arr, l, r, cmp):
	# Check base case
	if r >= l:
		mid = int(l + (r - l) / 2)
		res = cmp(arr[mid])
		# If element is present at the middle itself
		if res == 0:
			return mid

		# If element is smaller than mid, then it
		# can only be present in left subarray
		elif res > 0:
			return _binarySearch(arr, l, mid - 1, cmp)

		# Else the element can only be present
		# in right subarray
		else:
			return _binarySearch(arr, mid + 1, r, cmp)

	else:
		# Element is not present in the array
		return None


def binarySearch(arr, cmp):
	return _binarySearch(arr, 0, len(arr) - 1, cmp)


def cmp(a, b):    return (a > b) - (a < b)
