# unit_testing_functions
# djs starting unit test scripts March 2018
import sys
import argparse
import pydoc


class hwc_tester(object):
	stdout_default = sys.stdout
	log_file = 'log_file.txt'
	test_docstring_count = 0
	no_docstring_count = 0
	no_docstring = []
	bad_arg_count = 0
	bad_arg = []
	def __init__(self, argv):
		self.message('Number of arguments = '+ str(len(argv)))
		self.message('Argument List:' + str(sys.argv))
		if len( argv) < 2:
			pass
		else:
			hwc_tester.log_file = argv[1]
		self.message('Output  File  ' + hwc_tester.log_file )

	def message(self,message):
		sys.stdout = open(hwc_tester.log_file, 'a')
		print message
		# # always leave end stdout printing  to screen
		sys.stdout = hwc_tester.stdout_default
		print message
	
	def get_docstring(self,function):
		return pydoc.render_doc(function, "Help on %s")

	def has_docstring(self,s):
		return s != ''
	
	def good_argument_names(self,s):
		# string manipulation, meh, mostly cancer ...
		open1 = s.find("(")
		close1 = s.rfind(")")
		scut = s[open1+1: close1].split(',')
		args = [item[item.rfind(")")+1:] for item in scut]
		arg_count = 0
		for i in args:
			if 'arg' in i:
				arg_count += 1
		if arg_count > 1:
			return False, ', '.join(args[1:])
		else:
			return True, ', '.join(args[1:])

	def test_docstring(self,function):
		hwc_tester.test_docstring_count += 1
		ds = self.get_docstring(function).split('\n')
		if self.has_docstring(ds[-1]):
			self.message(function.__name__ + ' Has a docstring = ' + ds[-1])
		else:
			self.message(function.__name__ + ' cant find docstring, ' + ds[-1])
			hwc_tester.no_docstring_count += 1
			hwc_tester.no_docstring.append(function.__name__)
		has_good_args,args = self.good_argument_names(ds[3])
		if has_good_args:
			self.message(function.__name__ + ' Has Good Argument names, ' + args)
		else:
			self.message(function.__name__ + ' Has BAD  Argument names, ' + args)
			hwc_tester.no_docstring.append(function.__name__)
		return len(args)

	def test_function_0_arg(self, name, function):
		result = function()
		output = "%s, function = %s, return = %s , return type  = %s" % (name, function.__name__, result, type(result))
		self.message(output)

	def test_function_1_arg(self, name, function, arg):
		result = function(arg)
		output = "%s, function = %s, arg = %s,  return = %s , return type  = %s" % (name, function.__name__, arg, result, type(result))
		self.message(output)
