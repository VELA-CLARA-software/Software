import os, math, h5py
import numpy as np
from scipy import interpolate
import scipy.integrate as integrate
import scipy.constants as constants
if os.name == 'nt':
    try:
        import sdds
    except:
        pass
import read_gdf_file as rgf

class twiss(dict):

    E0 = constants.m_e * constants.speed_of_light**2
    E0_eV = E0 / constants.elementary_charge
    q_over_c = (constants.e / constants.speed_of_light)

    def find_nearest(self, array, value):
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return idx-1
        else:
            return idx

    def reset_dicts(self):
        self.clear()
        self['z'] = []
        self['t'] = []
        self['kinetic_energy'] = []
        self['gamma'] = []
        self['cp'] = []
        self['p'] = []
        self['enx'] = []
        self['ex'] = []
        self['eny'] = []
        self['ey'] = []
        self['enz'] = []
        self['ez'] = []
        self['beta_x'] = []
        self['gamma_x'] = []
        self['alpha_x'] = []
        self['beta_y'] = []
        self['gamma_y'] = []
        self['alpha_y'] = []
        self['beta_z'] = []
        self['gamma_z'] = []
        self['alpha_z'] = []
        self['sigma_x'] = []
        self['sigma_y'] = []
        self['sigma_z'] = []
        self['sigma_p'] = []
        self['sigma_cp'] = []

    def read_sdds_file(self, fileName, charge=None):
        self.reset_dicts()
        self.sdds = sdds.SDDS(0)
        self.sdds.load(fileName)
        for col in range(len(self.sdds.columnName)):
            if len(self.sdds.columnData[col]) == 1:
                self[self.sdds.columnName[col]] = np.array(self.sdds.columnData[col][0])
            else:
                self[self.sdds.columnName[col]] = np.array(self.sdds.columnData[col])
        self.SDDSparameterNames = list()
        for param in self.sdds.columnName:
            if isinstance(self.beam[param][0], (float, long)):
                self.SDDSparameterNames.append(param)

    def read_astra_emit_files(self, filename, reset=True):
        if reset:
            self.reset_dicts()
        if isinstance(filename, (list, tuple)):
            for f in filename:
                self.read_astra_emit_files(f, reset=False)
        else:
            if 'xemit' not in filename.lower():
                filename = filename.replace('Yemit','Xemit').replace('Zemit','Xemit')
            xemit = np.loadtxt(filename, unpack=False)
            if 'yemit' not in filename.lower():
                filename = filename.replace('Xemit','Yemit').replace('Zemit','Yemit')
            yemit = np.loadtxt(filename, unpack=False)
            if 'zemit' not in filename.lower():
                filename = filename.replace('Xemit','Zemit').replace('Yemit','Zemit')
            zemit = np.loadtxt(filename, unpack=False)
            self.interpret_astra_data(xemit, yemit, zemit)

    def read_hdf_summary(self, filename, reset=True):
        if reset:
            self.reset_dicts()
        f = h5py.File(filename, "r")
        xemit = f.get('Xemit')
        yemit = f.get('Yemit')
        zemit = f.get('Zemit')
        for item, params in sorted(xemit.items()):
            self.interpret_astra_data(np.array(xemit.get(item)), np.array(yemit.get(item)), np.array(zemit.get(item)))

    def interpret_astra_data(self, xemit, yemit, zemit):
            z, t, mean_x, rms_x, rms_xp, exn, mean_xxp = np.transpose(xemit)
            z, t, mean_y, rms_y, rms_yp, eyn, mean_yyp = np.transpose(yemit)
            z, t, e_kin, rms_z, rms_e, ezn, mean_zep = np.transpose(zemit)
            e_kin = 1e6 * e_kin
            t = 1e-9 * t
            exn = 1e-6*exn
            eyn = 1e-6*eyn
            rms_x, rms_xp, rms_y, rms_yp, rms_z, rms_e = 1e-3*np.array([rms_x, rms_xp, rms_y, rms_yp, rms_z, rms_e])
            self['z'] = np.concatenate([self['z'],z])
            self['t'] = np.concatenate([self['t'],t])
            self['kinetic_energy'] = np.concatenate([self['kinetic_energy'], e_kin])
            gamma = 1 + (e_kin / self.E0_eV)
            self['gamma'] = np.concatenate([self['gamma'], gamma])
            cp = np.sqrt(e_kin * (2 * self.E0_eV + e_kin))
            self['cp'] = np.concatenate([self['cp'], cp])
            p = cp * self.q_over_c
            self['p'] = np.concatenate([self['p'], p])
            self['enx'] = np.concatenate([self['enx'], exn])
            ex = exn / gamma
            self['ex'] = np.concatenate([self['ex'], ex])
            self['eny'] = np.concatenate([self['eny'], eyn])
            ey = eyn / gamma
            self['ey'] = np.concatenate([self['ey'], ey])
            self['enz'] = np.concatenate([self['enz'], ezn])
            ez = ezn / gamma
            self['ez'] = np.concatenate([self['ez'], ez])
            self['beta_x'] = np.concatenate([self['beta_x'], rms_x**2 / ex])
            self['gamma_x'] = np.concatenate([self['gamma_x'], rms_xp**2 / ex])
            self['alpha_x'] = np.concatenate([self['alpha_x'], (-1 * np.sign(mean_xxp) * rms_x * rms_xp) / ex])
            # self['alpha_x'] = np.concatenate([self['alpha_x'], (-1 * mean_xxp * rms_x) / ex])
            self['beta_y'] = np.concatenate([self['beta_y'], rms_y**2 / ey])
            self['gamma_y'] = np.concatenate([self['gamma_y'], rms_yp**2 / ey])
            self['alpha_y'] = np.concatenate([self['alpha_y'], (-1 * np.sign(mean_yyp) * rms_y * rms_yp) / ey])
            self['beta_z'] = np.concatenate([self['beta_z'], rms_z**2 / ez])
            self['gamma_z'] = np.concatenate([self['gamma_z'], rms_e**2 / ez])
            self['alpha_z'] = np.concatenate([self['alpha_z'], (-1 * np.sign(mean_zep) * rms_z * rms_e) / ez])
            self['sigma_x'] = np.concatenate([self['sigma_x'], rms_x])
            self['sigma_y'] = np.concatenate([self['sigma_y'], rms_y])
            self['sigma_z'] = np.concatenate([self['sigma_z'], rms_z])
            self['sigma_p'] = np.concatenate([self['sigma_p'], (rms_e / e_kin)])
            self['sigma_cp'] = np.concatenate([self['sigma_cp'], (rms_e / e_kin) * p])
            self['mux'] = integrate.cumtrapz(x=self['z'], y=1/self['beta_x'], initial=0)
            self['muy'] = integrate.cumtrapz(x=self['z'], y=1/self['beta_y'], initial=0)

    def interpolate(self, z=None, value='z'):
        f = interpolate.interp1d(self['z'], self[value], kind='linear')
        if z is None:
            return f
        else:
            if z > max(self['z']):
                return 10**6
            else:
                return float(f(z))

    def extract_values(self, array, start, end):
        startidx = self.find_nearest(self['z'], start)
        endidx = self.find_nearest(self['z'], end) + 1
        return self[array][startidx:endidx]

    def covariance(self, u, up):
        u2 = u - np.mean(u)
        up2 = up - np.mean(up)
        return np.mean(u2*up2) - np.mean(u2)*np.mean(up2)
