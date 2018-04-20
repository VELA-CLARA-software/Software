from config_reader import Config_Reader
from data_logger import Data_Logger



class Generic_Experiment:

	logger = Data_Logger()
	config_reader =  Config_Reader("test_input.yml")
	config_reader.read_file()