if __name__ == '__main__':
	import sys

	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
	from generic_experiment import Generic_Experiment


	generic_experiment = Generic_Experiment()


#
#
#
#
#
# from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper
# f=open("test_input.yml")
# data = load(f, Loader=Loader)
#
#
# import yaml
# document = """
#   a: 1
#   b:
#     c: 3
#     d: 4
# """
# print yaml.dump(yaml.load(document))