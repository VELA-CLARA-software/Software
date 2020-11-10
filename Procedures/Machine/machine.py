import sys,os, time
import random as r
import numpy as np
import inspect
sys.path.append("../../")
from Software.Widgets.generic.pv import *

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class Machine(object):

    bpmDataObjects = {}
    screenDataObjects = {}

    def __init__(self, machineType, lineType, gunType, controllers=['magnets', 'bpms', 'gunllrf', 'linac1llrf', 'charge', 'general']):
        super(Machine, self).__init__()
        self.machineType = machineType
        self.lineType = lineType
        self.gunType = gunType
        self.controllers = controllers
        self.pvids = {}
        self.setUpCtrls()
        if self.machineType == 'Virtual':
            self.virtualSetUp()
        self.corrSI = {}
        self.solSI = {}
        self.quadSI = {}
        self.parameters = {}
        if self.machineType == 'None':
            self.linac1PhiSp = 0
            self.gunPhiSp = 0
            self.linac1AmpSp = 35000
            self.gunAmpSp = 71000
        print('SELF.MACHINETYPE = ', self.machineType)

    # LINAC PID PVs
    #setpoint CLA-L01-LRF-CTRL-01:PHAA:PID.VAL
    #integral CLA-L01-LRF-CTRL-01:PHAA:PID.KI
    # Scan Passive CLA-L01-LRF-CTRL-01:PHAA:PID.SCAN  0=passive, 9=.1second
    #input value = CLA-L01-LRF-CTRL-01:PHAA:PID:IP.OVAL.OVAL

    def addPV(self, pv):
        if not pv in self.pvids:
            self.pvids[pv] = PVObject(pv)
            setattr(self.pvids[pv], 'writeAccess', True)
        return self.pvids[pv]

    def getPVValue(self, pv):
        pvid = self.addPV(pv)
        return pvid.value

    def setPVValue(self, pv, value):
        pvid = self.addPV(pv)
        pvid.value = value

    def initialise_parameters(self):
        if self.lineType=='VELA':
            self.velaMethod()
        elif self.lineType=='CLARA':
            self.claraMethod()
        return self.parameters

    def claraMethod(self):
        print('clara Method')
        self.parameters['magnets']=['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04',
                            'S01-HCOR1', 'S01-VCOR1', 'S01-HCOR2', 'S01-VCOR2',
                            'S02-HCOR1', 'S02-VCOR1', 'S02-HCOR2', 'S02-VCOR2',
                            'LRG-SOL', 'LRG-BSOL', 'DIP01']
        self.parameters['gun_dispersive_bpm'] = 'C2V-BPM01'
        self.parameters['gun_dispersive_screen'] = 'C2V-CAM-01'
        self.parameters['linac_dispersive_bpm'] = {1: 'C2V-BPM01'}
        self.parameters['linac_dispersive_screen'] = {1: 'C2V-CAM-01'}
        self.parameters['linac_rough_bpm'] = {1: 'S02-BPM01'}
        self.parameters['scope'] = 'WCM'
        self.parameters['dipole'] = 'S02-DIP01'

    def velaMethod(self):
        print('vela Method')
        self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
                            'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
                            'SOL', 'BSOL', 'DIP01']
        self.parameters['bpm'] = 'C2V-BPM01'
        self.parameters['scope'] = 'WCM'

    def setUpCtrls(self):
        if self.machineType == 'None':
            print('No controllers!')
            '''This is the place to get contollers'''
            # sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
            # sys.path.append(r"\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\stage\Python3_x64")
            self.magnets = None
            self.bpms = None
            self.gunllrf = None
            self.linac1llrf = None
            self.cameras = None
            self.screens = None
            self.generalPV = None
            sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
        else:
            '''This is the place to get contollers'''
            sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
            # sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\')
            # sys.path.append('C:\\Python38\\Python3_x64\\')
            # os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
            if 'magnets' in self.controllers:
                print('#### CREATING MAGNET CONTROLLER ###')
                import VELA_CLARA_Magnet_Control as mag
                from VELA_CLARA_Magnet_Control import MAG_PSU_STATE
                self.magInit = mag.init()
                self.magInit.setQuiet()
                self.magPSUState = MAG_PSU_STATE()
            if 'bpms' in self.controllers:
                import VELA_CLARA_BPM_Control as bpm
                from VELA_CLARA_BPM_Control import BPM_STATUS# as bpmstatus
                self.bpmstatus = BPM_STATUS
                self.bpmInit = bpm.init()
                self.bpmInit.setQuiet()
            if 'gunllrf' in self.controllers or 'linac1llrf' in self.controllers:
                import VELA_CLARA_LLRF_Control as llrf
                self.llrfInit = llrf.init()
                self.llrfInit.setQuiet()
            if 'charge' in self.controllers:
                import VELA_CLARA_Charge_Control as scope
                self.scopeInit = scope.init()
                self.scopeInit.setQuiet()
            if 'cameras' in self.controllers:
                import VELA_CLARA_Camera_Control as camIA
                self.camInit = camIA.init()
                self.camInit.setQuiet()
            if 'screens' in self.controllers:
                import VELA_CLARA_Screen_Control as screenIA
                self.screenInit = screenIA.init()
                self.screenInit.setQuiet()
            if self.machineType == 'Virtual':
                os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
                os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
                os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
                os.environ["EPICS_CA_SERVER_PORT"]="6000"
                sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
                if self.lineType == 'VELA':
                    if 'magnets' in self.controllers:
                        self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
                    if 'charge' in self.controllers:
                        self.scope = self.scopeInit.virtual_VELA_INJ_Charge_Controller()
                    if 'bpms' in self.controllers:
                        self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
                    if 'gunllrf' in self.controllers:
                        self.gunllrf = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
                    self.linac1llrf = None
                    if 'cameras' in self.controllers:
                        self.cameras = self.camInit.virtual_VELA_Camera_Controller()
                    if 'screens' in self.controllers:
                        self.screens = self.screenInit.virtual_VELA_INJ_Screen_Controller()
                else:
                    if 'magnets' in self.controllers:
                        self.magnets = self.magInit.virtual_C2B_Magnet_Controller()
                    if 'charge' in self.controllers:
                        self.scope = self.scopeInit.virtual_CLARA_PH1_Charge_Controller()
                    if 'bpms' in self.controllers:
                        self.bpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
                    if 'gunllrf' in self.controllers:
                        self.gunllrf = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
                    if 'linac1llrf' in self.controllers:
                        self.linac1llrf = self.llrfInit.virtual_L01_LLRF_Controller()
                    if 'cameras' in self.controllers:
                        self.cameras = self.camInit.virtual_CLARA_Camera_Controller()
                    if 'screens' in self.controllers:
                        self.screens = self.screenInit.virtual_CLARA_PH1_Screen_Controller()
            elif self.machineType == 'Physical':
                print('PHYSICAL CONTROLLERS!')
                if self.lineType == 'VELA':
                    if 'magnets' in self.controllers:
                        self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
                    if 'charge' in self.controllers:
                        self.scope = self.scopeInit.physical_VELA_INJ_Charge_Controller()
                    if 'bpms' in self.controllers:
                        self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
                    if 'gunllrf' in self.controllers:
                        self.gunllrf = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
                    self.linac1llrf = None
                    if 'cameras' in self.controllers:
                        self.cameras = self.camInit.physical_VELA_Camera_Controller()
                    if 'screens' in self.controllers:
                        self.screens = self.screenInit.physical_VELA_INJ_Screen_Controller()
                else:
                    if 'magnets' in self.controllers:
                        self.magnets = self.magInit.physical_C2B_Magnet_Controller()
                    if 'charge' in self.controllers:
                        self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
                    if 'bpms' in self.controllers:
                        self.bpms = self.bpmInit.physical_C2B_BPM_Controller()
                    if 'gunllrf' in self.controllers:
                        self.gunllrf = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
                    if 'linac1llrf' in self.controllers:
                        self.linac1llrf = self.llrfInit.physical_L01_LLRF_Controller()
                    if 'cameras' in self.controllers:
                        self.cameras = self.camInit.physical_CLARA_Camera_Controller()
                    if 'screens' in self.controllers:
                        self.screens = self.screenInit.physical_CLARA_PH1_Screen_Controller()

    def virtualSetUp(self):
        pass
        # sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
        # import SAMPL.v2_developing.sampl as sampl
        # self.magnets.switchONpsu('DIP01')
        # self.gunllrf.setAmpMVM(100)
        # self.gunllrf.setPhiDEG(0)
        # self.linac1llrf.setAmpMVM(0)
        # self.linac1llrf.setPhiDEG(-9)
        # self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
        #                     C_S01_MAG_Ctrl=self.magnets,
        #                     C_S02_MAG_Ctrl=self.magnets,
        #                     C2V_MAG_Ctrl=self.magnets,
        #                     LRRG_RF_Ctrl=None,
        #                     HRRG_RF_Ctrl=self.gunllrf,
        #                     L01_RF_Ctrl=self.linac1llrf,
        #                     messages=True)
        #
        # self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
        # self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
        # self.SAMPL.initDistribFile = '4k-250pC.ini'

    def setAmplitude(self, cavity, value):
        if cavity == 'Gun':
            self.setGunAmplitude(value)
        elif cavity == 'Linac1':
            self.setLinac1Amplitude(value)
        return True

    def getAmplitude(self, cavity):
        if cavity == 'Gun':
            return self.getGunAmplitude()
        elif cavity == 'Linac1':
            return self.getLinac1Amplitude()

    def setPhase(self, cavity, value):
        if cavity == 'Gun':
            self.setGunPhase(value)
        elif cavity == 'Linac1':
            self.setLinac1Phase(value)
        elif cavity == 'Linac1PID':
            self.setLinac1PhasePID(value)
        return True

    def getPhase(self, cavity):
        if cavity == 'Gun':
            return self.getGunPhase()
        elif cavity == 'Linac1':
            return self.getLinac1Phase()
        elif cavity == 'Linac1PID':
            return self.getLinac1PhasePID()

    def getKlystronForwardPower(self, cavity):
        if cavity == 'Gun':
            return self.getGunKlystronForwardPower()
        elif cavity == 'Linac1':
            return self.getLinac1KlystronForwardPower()

    def setGunPhase(self, phase):
        if self.machineType == 'None':
            self.gunPhiSp = phase
        else:
            self.gunllrf.setPhiSP(np.mod(180+phase,360)-180)
        return True

    def getGunPhase(self):
        if self.machineType == 'None':
            return self.gunPhiSp if hasattr(self, 'gunPhiSp') else 0
        else:
            return self.gunllrf.getPhiSP()

    def setGunAmplitude(self, amp):
        if self.machineType == 'None':
            self.gunAmpSp = amp
        else:
            self.gunllrf.setAmpSP(amp)
        return True

    def getGunAmplitude(self):
        if self.machineType == 'None':
            return self.gunAmpSp if hasattr(self, 'gunAmpSp') else 0
        else:
            return self.gunllrf.getAmpSP()

    def getGunKlystronForwardPower(self):
        return self.gunllrf.getKlyFwdPower()

    def getLinac1KlystronForwardPower(self):
        return self.linac1llrf.getKlyFwdPower()

    def setLinac1Phase(self, phase):
        print('setting L01 phase = ', np.mod(180+phase,360)-180)
        if self.machineType == 'None':
            self.linac1PhiSp = phase
        else:
            self.linac1llrf.setPhiSP(np.mod(180+phase,360)-180)
        return True

    def getLinac1Phase(self):
        if self.machineType == 'None':
            return self.linac1PhiSp if hasattr(self, 'linac1PhiSp') else 0
        else:
            return self.linac1llrf.getPhiSP()

    def setLinac1PhasePID(self, phase):
        print('setting L01 PID phase = ', np.mod(180+phase,360)-180)
        if self.machineType == 'None':
            self.linac1PhiSpPID = phase
        else:
            self.setPVValue('CLA-L01-LRF-CTRL-01:PHAA:PID.VAL',np.mod(180+phase,360)-180)
        return True

    def getLinac1PhasePID(self):
        if self.machineType == 'None':
            return self.linac1PhiSp if hasattr(self, 'linac1PhiSp') else 0
        else:
            return self.getPVValue('CLA-L01-LRF-CTRL-01:PHAA:PID.VAL')

    def setLinac1Amplitude(self, amp):
        if self.machineType == 'None':
            self.linac1AmpSp = amp
        else:
            # print 'setting L01 LLRF to ', amp
            self.linac1llrf.setAmpFF(amp)
        return True

    def getLinac1Amplitude(self):
        if self.machineType == 'None':
            # print('linac1amplitude thinks we have NONE')
            return self.linac1AmpSp if hasattr(self, 'linac1AmpSp') else (35000 + 200*np.random.random_sample())
        else:
            # print('linac1amplitude retuns ', self.linac1llrf.getAmpSP())
            return self.linac1llrf.getAmpSP()

    def getBPMDataObject(self, bpm):
        if bpm not in self.bpmDataObjects:
            self.bpmDataObjects[bpm] = self.bpms.getBPMDataObject(bpm)
        return self.bpmDataObjects[bpm]

    # def getBPMBuffer(self, bpm, buffer=10, plane='X'):
    #     if self.machineType == 'None':
    #         value = [20*np.random.random_sample() - 10 for i in range(buffer)]
    #         return value
    #     else:
    #         obj = self.getBPMDataObject(bpm)
    #         obj.setBufferSize(buffer)
    #         if plane == 'Y':
    #             while not obj.isYBufferFull():
    #                 time.sleep(0.001)
    #             return zip(obj.yBuffer, obj.statusBuffer)
    #         else:
    #             return obj.x
    #         else:
    #             return float('nan')

    def getBPMPosition(self, bpm, plane='X', ignoreNonLinear=True):
        if self.machineType == 'None':
            if bpm == 'C2V':
                value = ((30.0 * (self.getLinac1Amplitude() / 35000.0)*np.cos(2*np.pi*self.linac1PhiSp/360.0) + 5.5)/35.5 - 1.0) * 0.368 * 1e3 + (np.random.normal(0, 0.25))
            else:
                value = 20*np.random.random_sample() - 10
            return value
        else:
            obj = self.getBPMDataObject(bpm)
            # print obj.x, obj.y, obj.status
            if obj.status == self.bpmstatus.GOOD or (ignoreNonLinear is True and obj.status == self.bpmstatus.NONLINEAR):
                if plane == 'Y':
                    return obj.y
                else:
                    return obj.x
            else:
                # print 'bad! = ', obj.x, obj.y
                return float('nan')

    def getBPMPositionStatus(self, bpm, plane='X'):
        if self.machineType == 'None':
            value = 20*np.random.random_sample() - 10
            return value, self.bpmstatus.GOOD
        else:
            obj = self.getBPMDataObject(bpm)
            if plane == 'Y':
                return obj.y, obj.status
            else:
                return obj.x, obj.status

    def getScreenDataObject(self, screen):
        if screen not in self.screenDataObjects:
            self.screenDataObjects[screen] = self.cameras.getAnalysisObj(screen)
        return self.screenDataObjects[screen]

    def getScreenPosition(self, screen, plane='X', intensitycutoff=103):
        if self.machineType == 'None':
            value = 20*np.random.random_sample() - 10
            return value
        else:
            obj = self.getScreenDataObject(screen)
            intensity = obj.avg_pix
            if intensity > intensitycutoff:
                if plane == 'Y':
                    yval = obj.y
                    print('yval = ', yval)
                    return yval
                else:
                    xval =obj.x
                    print('xval = ', xval)
                    return xval
            else:
                return float('nan')

    def setCorr(self, corr, I, tol=0.05):
        # print 'setting dip01 = ', I
        if self.machineType == 'None':
            self.corrSI[corr] = I
        else:
            # print 'setting ', corr, ' = ', I
            # print(self.magnets.setSI(corr, I))
            i = 0
            while abs(self.getCorr(corr) - I) > tol:
                time.sleep(0.1)
        return True

    def getCorr(self, corr):
        if self.machineType == 'None':
            return self.corrSI[corr] if hasattr(self, 'corrSI') and corr in self.corrSI else 0
        else:
            return self.magnets.getRI(corr)

    def setSol(self, sol, I, tol=0.2):
        # print 'setting dip01 = ', I
        if self.machineType == 'None':
            self.solSI[sol] = I
        elif self.machineType == 'Physical':
            self.magnets.setSI(sol, I)
            time.sleep(0.1)
            while abs(self.getSol(sol) - I) > tol:
                # print self.getSol(sol), I, abs(self.getSol(sol) - I)
                time.sleep(0.1)
        return True

    def getSol(self, sol):
        if self.machineType == 'None':
            return self.solSI[sol] if hasattr(self, 'solSI') and sol in self.solSI else 0
        else:
            return self.magnets.getRI(sol)

    def find_nearest(self, array, value, index=None):
        subarray = np.asarray(array)
        if index is not None:
            subarray = subarray[:,index]
        idx = (np.abs(subarray - value)).argmin()
        return array[idx]

    def getWCMCharge(self, scope):
        if self.machineType == 'None':
            wcm_data = [[-180., 28.6424], [-175., 2.46292], [-170., 2.20253], [-165., \
                        2.24572], [-160., 2.01522], [-155., 2.07588], [-150., 2.44336], \
                        [-145., 2.13366], [-140., 2.11193], [-135., 2.73996], [-130., \
                        2.36129], [-125., 2.17099], [-120., 2.00984], [-115., 2.38705], \
                        [-110., 2.26005], [-105., 2.27442], [-100., 2.58211], [-95., \
                        2.09984], [-90., 2.53373], [-85., 2.80215], [-80., 2.24464], [-75., \
                        2.61765], [-70., 2.0823], [-65., 2.37115], [-60., 2.30828], [-55., \
                        2.33715], [-50., 1.96732], [-45., 2.15005], [-40., 16.9568], [-35., \
                        17.6342], [-30., 9.06696], [-25., 16.265], [-20., 32.2283], [-15., \
                        55.3548], [-10., 86.4586], [-5., 88.9817], \
                        [0., 95.6413], [5., 97.305], [10., 88.4177], [15., 95.8377], [20., \
                        88.8731], [25., 89.314], [30., 86.6351], [35., 81.5596], [40., \
                        90.3007], [45., 83.7862], [50., 75.3683], [55., 72.0417], [60., \
                        67.2645], [65., 56.998], [70., 53.0433], [75., 42.0769], [80., \
                        12.8871], [85., 5.48364], [90., 2.31569], [95., 2.3861], [100., \
                        2.07611], [105., 2.31879], [110., 1.93854], [115., 3.23816], [120., \
                        2.53554], [125., 2.37526], [130., 2.14535], [135., 2.57182], [140., \
                        2.57941], [145., 2.50883], [150., 2.14922], [155., 2.75157], [160., \
                        2.32648], [165., 2.25095], [170., 2.46884], [175., 1.95332], [180., \
                        2.24331]]
            value = self.find_nearest(wcm_data, self.gunPhiSp, 0)[1]
            # value = 100
            return  np.random.normal(0, 5) + value
        else:
            return self.scope.getCharge(scope)

    def getCTRSignal(self):
        if self.machineType == 'aNone':
            value = 700 - (1 + (300 * np.sqrt(np.abs(self.linac1PhiSp + 12)))**0.5)
            return (value + np.random.normal(0,2)) * 1e-3
        else:
            return self.getPVValue('EBT-BA1-DIA-BCM-01:PK-PK')
            # return self.scope.getCTRSignal()

    def setDip(self, I):
        # print 'setting dip01 = ', I
        if self.machineType == 'None':
            self.dipoleSI = I
        elif self.machineType == 'Virtual':
            self.magnets.setSI(self.parameters['dipole'], -1*I)
        elif self.machineType == 'Physical':
            self.magnets.setSI(self.parameters['dipole'], I)
            i = 0
            while not self.magnets.isRIequalSI(self.parameters['dipole']):
                time.sleep(0.1)
                # print self.magnets.isRIequalSI(self.parameters['dipole']), self.getDip()
        return True

    def getDip(self):
        if self.machineType == 'None':
            return self.dipoleSI if hasattr(self, 'dipoleSI') else 0
        else:
            return self.magnets.getSI(self.parameters['dipole'])

    def setDegaussMagnet(self, name, degaussToZero=True):
        if not self.machineType == 'None':
            if isinstance(name, (list, tuple)):
                self.magnets.degauss(name, degaussToZero)
            else:
                self.magnets.degauss([name], degaussToZero)
        return True

    def isMagnetDegaussing(self, name):
        if not self.machineType == 'None':
            if isinstance(name, (list, tuple)):
                return all([self.magnets.isDegaussing(m) for m in name])
            else:
                return self.magnets.isDegaussing(name)
        else:
            return False

    def setDegaussDIP(self):
        self.setDegaussMagnet(self.parameters['dipole'])
        return True

    def isDIPDegaussing(self):
        return self.isMagnetDegaussing(self.parameters['dipole'])

    def setQuad(self, name, I):
        if self.machineType == 'None':
            self.quadSI[name] = I
        elif self.machineType == 'Virtual':
            self.magnets.setSI(name, I)
        elif self.machineType == 'Physical':
            self.magnets.setSI(name, I)
            i = 0
            while not self.magnets.isRIequalSI(name):
                time.sleep(0.1)
                # print self.magnets.isRIequalSI(name), self.getQuad(name)
        return True

    def getQuad(self, name):
        if self.machineType == 'None':
            return self.quadSI[name] if hasattr(self, 'quadSI') and name in self.quadSI else 0
        else:
            return self.magnets.getSI(name)

    def set_rf_cage_in_and_wait(self, screen, timeout = 90):
        # message('rf_cage_in_and_wait: Passed ' + screen)
        self.screens.moveScreenTo(screen, scr.SCREEN_STATE.V_RF)
        waittime = time.time() + timeout
        while 1:
            if self.screens.isScreenInState(screen, scr.SCREEN_STATE.V_RF):
                return True
            if time.time() > waittime:
                message('!!!ERROR!!! rf_cage_in_and_wait timed out', header=true)
                return False

    def screens_in(self, screens):
        # message('screens_in: Passed ' + ",".join(screens))
        for screen in screens:
            if self.screens.isScreenIn(screen):
                #message('screens_in: ' + str(screen) + ' is already in.')
                pass
            else:
                #message('screens_in: move ' + str(screen) + ' in')
                self.screens.insertYAG(screen)

    def set_wait_for_screens_in(self, screens, timeout = 90):
        # message('wait_for_screen_in: Passed ' + ",".join(screens))
        # global scr_control
        waittime = time.time() + timeout
        while 1:
            all_screens_in = True
            for screen in screens:
                if self.screens.isScreenIn(screen):
                    pass
                else:
                    all_screens_in = False
                    break
            if all_screens_in:
                break
            if time.time() > waittime:
                message('!!!ERROR!!! wait_for_screen_in timed out', header=true)
                all_screens_in = False
                break
            time.sleep(2)
        return all_screens_in

    def applyDBURT(self, dburt):
        return self.magnets.applyDBURT(dburt)

    def getLLRFTrace(self, controller, trace):
        controller.startTraceMonitoring(trace)
        time.sleep(0.1)
        controller.stopTraceMonitoring(trace)
        return controller.getTraceValues(trace)

    def getKlystronForwardPowerTrace(self, cavity='Gun'):
        if cavity == 'Gun':
            return self.getLLRFTrace(self.gunllrf,'KLYSTRON_FORWARD_POWER')
        elif cavity == 'Linac1':
            return self.getLLRFTrace(self.linac1llrf,'KLYSTRON_FORWARD_POWER')

    def getKlystronReversePowerTrace(self, cavity='Gun'):
        if cavity == 'Gun':
            return self.getLLRFTrace(self.gunllrf,'KLYSTRON_REVERSE_POWER')
        elif cavity == 'Linac1':
            return self.getLLRFTrace(self.linac1llrf,'KLYSTRON_REVERSE_POWER')

    def getCavityForwardPowerTrace(self, cavity='Gun'):
        if cavity == 'Gun':
            return self.getLLRFTrace(self.gunllrf,'LRRG_CAVITY_FORWARD_POWER')
        elif cavity == 'Linac1':
            return self.getLLRFTrace(self.linac1llrf,'L01_CAVITY_FORWARD_POWER')

    def getCavityReversePowerTrace(self, cavity='Gun'):
        if cavity == 'Gun':
            return self.getLLRFTrace(self.gunllrf,'LRRG_CAVITY_REVERSE_POWER')
        elif cavity == 'Linac1':
            return self.getLLRFTrace(self.linac1llrf,'L01_CAVITY_REVERSE_POWER')

    def getGunRFTraces(self, dict=False):
        rftraces = ['LRRG_CAVITY_FORWARD_POWER', 'LRRG_CAVITY_REVERSE_POWER', 'LRRG_CAVITY_FORWARD_PHASE', 'KLYSTRON_FORWARD_POWER', 'KLYSTRON_REVERSE_POWER', 'KLYSTRON_FORWARD_PHASE']
        controller = self.gunllrf
        # controller.startTraceMonitoring()
        # time.sleep(0.25)
        # controller.stopTraceMonitoring()
        data = {t: np.array(controller.getTraceValues(t)) for t in rftraces}
        if dict:
            return data
        else:
            return [data[t] for t in rftraces]

    def getLinac1RFTraces(self, dict=False):
        rftraces = ['L01_CAVITY_FORWARD_POWER', 'L01_CAVITY_REVERSE_POWER', 'L01_CAVITY_FORWARD_PHASE', 'KLYSTRON_FORWARD_POWER', 'KLYSTRON_REVERSE_POWER', 'KLYSTRON_FORWARD_PHASE']
        controller = self.linac1llrf
        # controller.startTraceMonitoring()
        # time.sleep(0.25)
        # controller.stopTraceMonitoring()
        data = {t: np.array(controller.getTraceValues(t)) for t in rftraces}
        if dict:
            return data
        else:
            return [data[t] for t in rftraces]
