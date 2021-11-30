import sys, os
import HRFOv2_EPICS_data

#from HRFOv2_EPICS_data import data_functions


class utilities():

	def __init__(self):
		print('Initaited utilities()')



	def create_bespoke_folder_name(self, foldername):
		'''
		set up a folder in the same directory as savepath with a name based on date_time_from - date_time_to
		if the folder already exists - pass
		if there is a problem (haven't had one yet) then quit the script
		:return:
		'''

		self.directory = HRFOv2_EPICS_data.values[HRFOv2_EPICS_data.savepath]
		self.folder_name = foldername
		path = f'{self.directory}\\{self.folder_name}'

		print(path)

		try:
			os.makedirs(path)
			print(f'\nNew "{self.folder_name}" folder created.')
		except OSError:
			try:
				folder_test = path
				print(f'\n"{self.folder_name}" folder already exists.')
			except:
				print(f'\n...Problem with setting up "{self.folder_name}" folder....')
				sys.exit()

		return path
