import sys, os
import HRFOv2_EPICS_data

from HRFOv2_EPICS_data import data_functions


class utilities():

	def __init__(self):
		print('Initaited utilities()')

	def create_folder_named_date_time_from_to(self):
		'''
		set up a folder in the same directory as savepath with a name based on date_time_from - date_time_to
		if the folder already exists - pass
		if there is a problem (haven't had one yet) then quit the script
		:return:
		'''

		#self.savepath =
		self.directory = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
		#directory = os.path.dirname(os.path.realpath(__file__))  # directory of script
		self.folder_name = self.create_folder_name()
		path = r'{}\Analysis_Results'.format(self.directory)  # path to be created

		print('directory = {}\npath = {}'.format(self.directory, path))

		try:
			os.makedirs(path)
			print('\nNew "Analysis_Results" folder created.')
		except OSError:
			try:
				folder_test = path
				print('\n"Analysis_Results" folder already exists.')
			except:
				print('\n...Problem with setting up "Analysis_Results" folder.... call Tony!')
				sys.exit()

	def create_folder_name(self):
		'''

		:return:
		'''
		df = data_functions

		self.date_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_from]
		self.time_from = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_from]
		self.date_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.date_to]
		self.time_to = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.time_to]

		self.folder_name = df.concatenate_date_time_to_folder_format(self.date_from,
		                                                             self.time_from,
		                                                             self.date_to,
		                                                             self.time_to)


