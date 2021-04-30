import datetime
import sys, inspect, math


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


def passedTime(time, suffix = None):
	if suffix is None:
		suffix = ['just', ' secs', ' mins', ' hrs', ' days', ' months', ' year']

	timeInMili = time.timestamp() * 1000
	nowInMili = datetime.datetime.now().timestamp() * 1000

	diffInMiliSecond = nowInMili - timeInMili
	second = diffInMiliSecond / 1000
	if second <= 0:
		return suffix[0]

	minutes = second / 60
	if minutes < 1:
		return f'{math.floor(diffInMiliSecond / 1000)}{suffix[1]}'

	hour = minutes / 60
	if hour < 1:
		return f'{math.floor(second / 60)}{suffix[2]}'

	day = hour / 24
	if day < 1:
		return f'{math.floor(minutes / 60)}{suffix[3]}'
	month = day / 30
	if month < 1:
		return f'{math.floor(hour / 24)}{suffix[4]}'

	year = month / 12
	if year < 1:
		return f'{math.floor(day / 30)}{suffix[5]}'
	else:
		f'{math.floor(year)}{suffix[6]}'


def getValueFromDict(value, typeArray, error):
	for type_ in typeArray:
		if isinstance(value, type_) is True:
			return value
	raise ValueError(f'{error}. Value should be {typeArray} class. Current is {type(value)}')
