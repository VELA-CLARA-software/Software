from PyQt4 import QtCore
import copy
import sys
import numpy as np
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_Camera_IA_Control as ia
class GenericThread(QtCore.QThread):
    def __init__(self, model, view):
        QtCore.QThread.__init__(self)
        self.model = model
        self.view = view

    def __del__(self):
        self.wait()

    def run(self):
        self.view.pushButton_analyse.setText('Analysing ...')

        if self.view.checkBox_useBackground.isChecked() is True:
            self.model.offlineAnalysis.useBackground(True)

            bk = np.transpose(np.flip(self.backgroundData.imageData, 1))
            bk = bk.flatten().tolist()
            b = ia.std_vector_double()
            b.extend(bk)
            self.model.offlineAnalysis.loadBackgroundImage(b)
        else:
            self.model.offlineAnalysis.useBackground(False)
        # This is where we will house expert settings
        self.model.offlineAnalysis.useESMask(True)
        if self.view.checkBox_useCustomMask.isChecked() is True:
            self.model.offlineAnalysis.setESMask(int(self.customMaskROI.pos()[0]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.pos()[1]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[1]/2))
        else:
            # make mask span full width of image
            x = int(self.model.imageWidth / 2)
            y = int(self.model.imageHeight / 2)
            self.model.offlineAnalysis.setESMask(x, y, x, y)

        if self.view.checkBox_rollingAverage.isChecked() is True:
            self.model.offlineAnalysis.useESFilter(True)
            self.model.offlineAnalysis.setESFilter(int(self.view.lineEdit_rollingAverage.text()))
        else:
            self.model.offlineAnalysis.useESFilter(False)

        if self.view.checkBox_rSquared.isChecked() is True:
            self.model.offlineAnalysis.useESRRThreshold(True)
            self.model.offlineAnalysis.setESRRThreshold(float(self.view.lineEdit_rSquared.text()))
        else:
            self.model.offlineAnalysis.useESRRThreshold(False)

        if self.view.checkBox_lowestPixValue.isChecked() is True:
            self.model.offlineAnalysis.useESDirectCut(True)
            self.model.offlineAnalysis.setESDirectCut(float(self.view.lineEdit_lowestPixelValue.text()))
        else:
            self.model.offlineAnalysis.useESDirectCut(False)

        self.model.start()
        #while self.model.isRunning():
            #time.sleep(1)
        # Set Results Labels in GUI
        self.view.label_xMLE.setText(str(self.model.offlineAnalysis.CoIA.xMLE))
        self.view.label_yMLE.setText(str(self.model.offlineAnalysis.CoIA.yMLE))
        self.view.label_sxMLE.setText(str(self.model.offlineAnalysis.CoIA.sxMLE))
        self.view.label_syMLE.setText(str(self.model.offlineAnalysis.CoIA.syMLE))
        self.view.label_cxyMLE.setText(str(self.model.offlineAnalysis.CoIA.cxyMLE))
        self.view.label_xBVN.setText(str(self.model.offlineAnalysis.CoIA.xBVN))
        self.view.label_yBVN.setText(str(self.model.offlineAnalysis.CoIA.yBVN))
        self.view.label_sxBVN.setText(str(self.model.offlineAnalysis.CoIA.sxBVN))
        self.view.label_syBVN.setText(str(self.model.offlineAnalysis.CoIA.syBVN))
        self.view.label_cxyBVN.setText(str(self.model.offlineAnalysis.CoIA.cxyBVN))

        # Set crosshairs
        x = float(self.model.offlineAnalysis.CoIA.xMLE)
        y = float(self.model.offlineAnalysis.CoIA.yMLE)
        v1 = (float(self.model.offlineAnalysis.CoIA.yMLE) -
              float(self.model.offlineAnalysis.CoIA.syMLE))
        v2 = (float(self.model.offlineAnalysis.CoIA.yMLE) +
              float(self.model.offlineAnalysis.CoIA.syMLE))
        h1 = (float(self.model.offlineAnalysis.CoIA.xMLE) -
              float(self.model.offlineAnalysis.CoIA.sxMLE))
        h2 = (float(self.model.offlineAnalysis.CoIA.xMLE) +
              float(self.model.offlineAnalysis.CoIA.sxMLE))
        self.vLineMLE.setData(x=[x, x], y=[v1, v2])
        self.hLineMLE.setData(x=[h1, h2], y=[y, y])

        x = float(self.model.offlineAnalysis.CoIA.xBVN)
        y = float(self.model.offlineAnalysis.CoIA.yBVN)
        v1 = (float(self.model.offlineAnalysis.CoIA.yBVN) -
              float(self.model.offlineAnalysis.CoIA.syBVN))
        v2 = (float(self.model.offlineAnalysis.CoIA.yBVN) +
              float(self.model.offlineAnalysis.CoIA.syBVN))
        h1 = (float(self.model.offlineAnalysis.CoIA.xBVN) -
              float(self.model.offlineAnalysis.CoIA.sxBVN))
        h2 = (float(self.model.offlineAnalysis.CoIA.xBVN) +
              float(self.model.offlineAnalysis.CoIA.sxBVN))
        self.vLineBVN.setData(x=[x, x], y=[v1, v2])
        self.hLineBVN.setData(x=[h1, h2], y=[y, y])
        self.view.pushButton_analyse.setText('Analyse')
