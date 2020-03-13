from datetime import datetime
import struct
import os
import shutil
from data.config_reader import config_reader
import numpy
import data.charge_measurement_data_base as dat
import ruamel.yaml, json
from six import string_types
import xlrd
import pandas
import openpyxl
from xlutils.copy import copy

class data_logger(object):
    my_name = 'data_logger'
    config = config_reader()
    _log_config = None
    _pil_name = None
    _llrf_name = None
    _mag_name = None
    _scan_type = None

    log_start = datetime.now()
    log_start_str = log_start.isoformat('-').replace(":", "-").split('.', 1)[0]
    pil_name = "dummy"
    llrf_name = "dummy"
    mag_name = []
    scan_type = "dummy"

    def __init__(self):
        pass

    @property
    def log_config(self):
        return data_logger._log_config

    @log_config.setter
    def log_config(self,value):
        data_logger._log_config = value
        self.log_directory = data_logger.config.log_config['LOG_DIRECTORY'] + self.log_start_str
        self.file_directory = data_logger.config.log_config['FILE_DIRECTORY']
        os.makedirs(self.log_directory)
        self.working_directory = self.log_directory + '\\'
        self.data_path = self.working_directory + 'data_log'  # MAGIC_STRING
        self.log_path = self.working_directory + 'log.txt'
        self.header(self.my_name + ' log_config')
        self.message([
            'log_directory     = ' + self.log_directory,
            'working_directory = ' + self.working_directory,
            'data_path    = ' + self.data_path,
            'log_path     = ' + self.log_path
        ])


    def header(self, text, add_to_log = False):
        str = '*' + '\n' +'*** ' + text + '***'
        print(str)
        if add_to_log:
            self.write_log(str)

    def message(self,text=[], add_to_log = False):
        if isinstance(text, string_types):
            str = text
        else:
            str = '\n'.join(text)
        print(str)
        if add_to_log:
            self.write_log(str)

    def write_log(self, str):
        #write_str = datetime.now().isoformat('-').replace(":", "-").split('.', 1)[0] + ' ' + str + '\n'
        write_str = datetime.now().isoformat(' ') + ' ' + str + '\n'
        with open(self.log_path,'a') as f:
            f.write(write_str)

    def write_list(self, data, file):
        with open(file,'w') as f:
            for item in data:
                f.write("%s\n" % item)

    def add_to_scan_log(self,x):
        towrite = " ".join(map(str, x))
        self.message('Adding to scan log =  ' + towrite, True)
        with open(self.scan_log,'a') as f:
            f.write( towrite + '\n')

    def add_to_scan_yaml(self,d):
        with open(self.scan_log, 'w') as outfile:
            ruamel.yaml.dump(d, outfile, default_flow_style=False)

    def add_to_scan_json(self,d):
        with open(self.scan_log, 'a') as outfile:
            outfile.write(json.dumps(d, indent=4, sort_keys=True))
            outfile.write('\n')
            file = outfile
        self.m, self.cross, self.qe = self.write_to_excel(d, file.name)
        shutil.copy(file.name, data_logger.config.log_config['FILE_DIRECTORY'])
        self.year = str(datetime.now().year)
        self.month = datetime.now().strftime('%m')
        self.day = datetime.now().strftime('%d')
        self.scandir = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\" + self.year + "\\" + self.month + "\\" + self.day
        if not os.path.isdir(self.scandir):
            os.makedirs(self.scandir)
        shutil.copy(file.name, self.scandir)
        return self.m, self.cross, self.qe, file.name

    def write_to_excel(self, d, filename):
        self.wcmmean = []
        self.ophirmean = []
        self.wcmstderr = []
        self.ophirstderr = []
        self.wcmmeanall = []
        self.ophirmeanall = []
        self.wcmstderrall = []
        self.ophirstderrall = []
        self.klyfwdmean = []
        self.klyfwdstderr = []
        self.vcxmean = []
        self.vcxstderr = []
        self.vcymean = []
        self.vcystderr = []
        self.vcsigxmean = []
        self.vcsigxstderr = []
        self.vcsigymean = []
        self.vcsigystderr = []
        self.bsolmean = []
        self.solmean = []
        self.offcrestmean = []
        for j in range(0,len(d["ophir_values"])-1):
            self.ophirmean.append(numpy.mean(list(d["ophir_values"].values())[j]))
            self.wcmmean.append(numpy.mean(list(d["charge_values"].values())[j]))
            self.ophirstderr.append(numpy.std(list(d["ophir_values"].values())[j]) / numpy.sqrt(len(list(d["ophir_values"].values())[j])))
            self.wcmstderr.append(numpy.std(list(d["charge_values"].values())[j]) / numpy.sqrt(len(list(d["charge_values"].values())[j])))
            self.klyfwdmean.append(numpy.mean(list(d["kly_fwd_pwr_values"].values())[j]))
            self.klyfwdstderr.append(
                numpy.std(list(d["kly_fwd_pwr_values"].values())[j]) / numpy.sqrt(len(list(d["kly_fwd_pwr_values"].values())[j])))
            self.vcxmean.append(numpy.mean(list(d["vc_x_pix_values"].values())[j]))
            self.vcymean.append(numpy.mean(list(d["vc_y_pix_values"].values())[j]))
            self.vcxstderr.append(numpy.std(list(d["vc_x_pix_values"].values())[j]) / numpy.sqrt(len(list(d["vc_x_pix_values"].values())[j])))
            self.vcystderr.append(numpy.std(list(d["vc_y_pix_values"].values())[j]) / numpy.sqrt(len(list(d["vc_y_pix_values"].values())[j])))
            self.vcsigxmean.append(numpy.mean(list(d["vc_sig_x_pix_values"].values())[j]))
            self.vcsigymean.append(numpy.mean(list(d["vc_sig_y_pix_values"].values())[j]))
            self.vcsigxstderr.append(
                numpy.std(list(d["vc_sig_x_pix_values"].values())[j]) / numpy.sqrt(len(list(d["vc_sig_x_pix_values"].values())[j])))
            self.vcsigystderr.append(
                numpy.std(list(d["vc_sig_y_pix_values"].values())[j]) / numpy.sqrt(len(list(d["vc_sig_y_pix_values"].values())[j])))
            self.bsolmean.append(numpy.mean(list(d["bsol_values"].values())[j]))
            self.solmean.append(numpy.mean(list(d["sol_values"].values())[j]))
            self.offcrestmean.append(list(d["off_crest_phase"].values())[j])
        for i, j, k, l in zip(self.wcmmean, self.ophirmean, self.wcmstderr, self.ophirstderr):
            self.wcmmeanall.append(i)
            self.ophirmeanall.append(j)
            self.wcmstderrall.append(k)
            self.ophirstderrall.append(l)
        self.klyfwdmeanall = numpy.mean(self.klyfwdmean)
        self.klyfwdstderrall = numpy.mean(self.klyfwdstderr)
        self.vcxmeanall = numpy.mean(self.vcxmean)
        self.vcxstderrall = numpy.mean(self.vcxstderr)
        self.vcymeanall = numpy.mean(self.vcymean)
        self.vcystderrall = numpy.mean(self.vcystderr)
        self.vcsigxmeanall = numpy.mean(self.vcsigxmean)
        self.vcsigxstderrall = numpy.mean(self.vcsigxstderr)
        self.vcsigymeanall = numpy.mean(self.vcsigymean)
        self.vcsigystderrall = numpy.mean(self.vcsigystderr)
        self.bsolmeanall = numpy.mean(self.bsolmean)
        self.solmeanall = numpy.mean(self.solmean)
        self.offcrestmeanall = numpy.mean(self.offcrestmean)
        self.x, self.y = self.ophirmeanall, self.wcmmeanall
        try:
            self.m, self.c = numpy.around(numpy.polyfit(self.x, self.y, 1), 2)
        except:
            self.m, self.c = 0, 0
        self.fit = self.m
        self.cross = self.c
        self.QE = numpy.around(4.66e-6 * self.m / 15.4, 6)
        self.qeall = self.QE
        self.new_row_data = ['', filename, self.cross, self.fit, self.qeall]
        d["fit"] = self.m
        d["cross"] = self.c
        d["qe"] = self.QE * 10**(5)
        d["kly_fwd_mean_all"] = self.klyfwdmeanall
        self.rb = xlrd.open_workbook(data_logger.config.log_config['SUMMARY_FILE'])
        self.df = pandas.DataFrame({'':[''],
                                    'filename': [os.path.basename(filename)],
                                    'charge_cross_zero': [self.cross],
                                    'fit': [self.fit],
                                    'qe_effective': [self.qeall],
                                    'kly_fwd_mean': [self.klyfwdmeanall],
                                    'kly_fwd_stderr': [self.klyfwdstderrall],
                                    'vc_x_pix_mean': [self.vcxmeanall],
                                    'vc_x_pix_stderr': [self.vcxstderrall],
                                    'vc_y_pix_mean': [self.vcymeanall],
                                    'vc_y_pix_stderr': [self.vcystderrall],
                                    'vc_sig_x_pix_mean': [self.vcsigxmeanall],
                                    'vc_sig_x_pix_stderr': [self.vcsigxstderrall],
                                    'vc_sig_y_pix_mean': [self.vcsigymeanall],
                                    'vc_sig_y_pix_stderr': [self.vcsigystderrall],
                                    'sol_mean': [self.solmeanall],
                                    'bsol_mean': [self.bsolmeanall],
                                    'off_crest_phase_mean': [self.offcrestmeanall]})
        self.writer = pandas.ExcelWriter(data_logger.config.log_config['SUMMARY_FILE'], engine='openpyxl')
        # try to open an existing workbook
        self.writer.book = openpyxl.load_workbook(filename=data_logger.config.log_config['SUMMARY_FILE'])
        # copy existing sheets
        self.writer.sheets = dict((ws.title, ws) for ws in self.writer.book.worksheets)
        # read existing file
        self.reader = pandas.read_excel(data_logger.config.log_config['SUMMARY_FILE'])
        self.df.to_excel(self.writer, index=False, header=False, startrow=len(self.reader) + 1)
        # write out the new sheet
        self.writer.close()
        return self.m, self.c, self.QE * 10**(5)

    def get_scan_log(self):
        self.scan_log_start = datetime.now()
        self.scan_log_start_str = self.scan_log_start.isoformat('-').replace(":", "-").split('.', 1)[0]
        self.directory = data_logger.config.log_config['LOG_DIRECTORY'] + self.pil_name
        self.scan_directory = data_logger.config.log_config['LOG_DIRECTORY'] + self.pil_name + '\\' + self.scan_type
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        if not os.path.isdir(self.scan_directory):
            os.makedirs(self.scan_directory)
        self.scan_log = self.scan_directory + '\\wcm_vs_ophir_' + self.scan_log_start_str + ".json"
        log = []
        with open(self.scan_log,"w+") as f:
            lines = list(line for line in (l.strip() for l in f) if line)
            for line in lines:
                if '#' not in line:
                    log.append([int(x) for x in line.split()])
        self.header(self.my_name + ' get_scan_log')
        self.message('read scan_log: ' + self.scan_log)
        # for i in log:
        #     self.message(map(str,i),True)
        return log

    def start_data_logging(self):
        self.header(self.my_name + ' start_data_logging')
        self.message([
            'data_path     = ' + self.data_path,
            'starting monitoring, update time = ' + str(self.log_config['DATA_LOG_TIME'])
        ])

    def write_data_log_header(self,values):
        print(self.my_name + ' writing data_log header to ' + self.data_path)
        joiner = '\t'
        names = []
        types = []
        [names.append(x) for x,y in values.items()]
        # names[names.index(dat.time_stamp)] =  dat.time_stamp +  ", (start = " + datetime.now().isoformat(' ') + ")"
        [types.append(str(type(y)))  for x,y in values.items()]
        try:
            with open(self.data_path  + '.dat', 'ab') as f:
                f.write(joiner.join(names)+ "\n")
                f.write(joiner.join(types)+ "\n")
                # f.write(struct.pack('<i', 245))
        except:
            pass

    def write_data(self,values):
        try:
            with open(self.data_path + '.dat', 'ab') as f:
                for val in values.itervalues():
                    self.write_binary(f,val)
        except:
            pass

    def write_binary(self, f, val):
        if type(val) is long:
            f.write(struct.pack('<l', val))
            #print struct.calcsize('<l')
        elif type(val) is int:
            f.write(struct.pack('<i', val))
            #print struct.calcsize('<i')
        elif type(val) is float:
            f.write(struct.pack('<f', val))
            #print struct.calcsize('<f')
        elif type(val) is RF_GUN_PROT_STATUS:
            f.write(struct.pack('<B', val))
            #print struct.calcsize('<B')
        # elif type(val) is STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
        # elif type(val) is GUN_MOD_STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
        # elif type(val) is VALVE_STATE:
        #     f.write(struct.pack('<B', val))
        #     #print struct.calcsize('<B')
        elif type(val) is bool:
            f.write(struct.pack('<?', val))
            #print struct.calcsize('<?')
        elif type(val) is numpy.float64:
            f.write(struct.pack('<f', val))
            #f.write(struct.pack('<?', val))
        elif type(val) is str:
            f.write(struct.pack('<i', -1))
        else:
            print(self.my_name + ' write_binary() error unknown type, ' + str(type(val)) )
        #print str(val) + '   ' + str(type(val))