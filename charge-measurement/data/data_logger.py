from datetime import datetime
import struct
import os
import shutil
from data.config_reader import config_reader
import numpy
import ruamel.yaml, json
from six import string_types
import xlrd
import pandas
import openpyxl

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
        self.write_to_excel(d, file.name)
        shutil.copy(file.name, data_logger.config.log_config['FILE_DIRECTORY'])
        self.year = str(datetime.now().year)
        self.month = datetime.now().strftime('%m')
        self.day = datetime.now().strftime('%d')
        self.scandir = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\" + self.year + "\\" + self.month + "\\" + self.day
        if not os.path.isdir(self.scandir):
            os.makedirs(self.scandir)
        shutil.copy(file.name, self.scandir)
        return file.name

    def write_to_excel(self, d, filename):
        self.wcmmean = numpy.mean(list(d['charge_mean'].values()))
        self.ophirmean = numpy.mean(list(d['ophir_mean'].values()))
        self.wcmstderr = numpy.mean(list(d['charge_stderr'].values()))
        self.ophirstderr = numpy.mean(list(d['ophir_stderr'].values()))
        self.klyfwdmean = numpy.mean(list(d['kly_fwd_pwr_mean'].values()))
        self.klyfwdstderr = numpy.mean(list(d['kly_fwd_pwr_stderr'].values()))
        self.gunfwdmean = numpy.mean(list(d['gun_fwd_pwr_mean'].values()))
        self.gunfwdstderr = numpy.mean(list(d['gun_fwd_pwr_stderr'].values()))
        self.gunphaspmean = numpy.mean(list(d['gun_pha_sp_mean'].values()))
        self.gunphaspstderr = numpy.mean(list(d['gun_pha_sp_stderr'].values()))
        self.gunphaffmean = numpy.mean(list(d['gun_pha_ff_mean'].values()))
        self.gunphaffstderr = numpy.mean(list(d['gun_pha_ff_stderr'].values()))
        self.vcintensitymean = numpy.mean(list(d['vc_intensity_mean'].values()))
        self.vcintensitystderr = numpy.mean(list(d['vc_intensity_stderr'].values()))
        self.vcxmean = numpy.mean(list(d['vc_x_pix_mean'].values()))
        self.vcxstderr = numpy.mean(list(d['vc_x_pix_stderr'].values()))
        self.vcymean = numpy.mean(list(d['vc_y_pix_mean'].values()))
        self.vcystderr = numpy.mean(list(d['vc_y_pix_stderr'].values()))
        self.vcsigxmean = numpy.mean(list(d['vc_sig_x_pix_mean'].values()))
        self.vcsigxstderr = numpy.mean(list(d['vc_sig_x_pix_stderr'].values()))
        self.vcsigymean = numpy.mean(list(d['vc_sig_y_pix_mean'].values()))
        self.vcsigystderr = numpy.mean(list(d['vc_sig_y_pix_stderr'].values()))
        self.bsolmean = numpy.mean(list(d['bsol_values'].values()))
        self.solmean = numpy.mean(list(d['sol_values'].values()))
        self.offcrestmean = numpy.mean(list(d['off_crest_phase_dict'].values()))
        self.fit = d['fit']
        self.cross = d['cross']
        self.qe = d['qe']
        self.new_row_data = ['', filename, self.cross, self.fit, self.qe]
        # d["kly_fwd_mean_all"] = self.klyfwdmeanall
        self.rb = xlrd.open_workbook(data_logger.config.log_config['SUMMARY_FILE'])
        self.df = pandas.DataFrame({'':[''],
                                    'filename': [os.path.basename(filename)],
                                    'charge_cross_zero': [self.cross],
                                    'fit': [self.fit],
                                    'qe_effective': [self.qe],
                                    'kly_fwd_mean': [self.klyfwdmean],
                                    'kly_fwd_stderr': [self.klyfwdstderr],
                                    'gun_fwd_mean': [self.gunfwdmean],
                                    'gun_fwd_stderr': [self.gunfwdstderr],
                                    'gun_pha_sp_mean': [self.gunphaspmean],
                                    'gun_pha_sp_stderr': [self.gunphaspstderr],
                                    'gun_pha_ff_mean': [self.gunphaffmean],
                                    'gun_pha_ff_stderr': [self.gunphaffstderr],
                                    'vc_x_pix_mean': [self.vcxmean],
                                    'vc_x_pix_stderr': [self.vcxstderr],
                                    'vc_y_pix_mean': [self.vcymean],
                                    'vc_y_pix_stderr': [self.vcystderr],
                                    'vc_sig_x_pix_mean': [self.vcsigxmean],
                                    'vc_sig_x_pix_stderr': [self.vcsigxstderr],
                                    'vc_sig_y_pix_mean': [self.vcsigymean],
                                    'vc_sig_y_pix_stderr': [self.vcsigystderr],
                                    'sol_mean': [self.solmean],
                                    'bsol_mean': [self.bsolmean],
                                    'off_crest_phase_mean': [self.offcrestmean]})
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
        return filename

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