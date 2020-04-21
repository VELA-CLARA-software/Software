'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   05-06-2018
//  FileName:    main.py
//  Description: Generic template for __main__ for general High Level Application
//
//
//*/
'''

'''******** Import modules *********'''
'''
the sys module is used to add to the PATH environment variable and to enable arguments to be 
passed to the application on start-up 
'''
import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
import VELA_CLARA_PILaser_Control as pil

''' 
QApplication is the top-level class we create, 
'''
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtCore
from vc_image_auto_save_gui import Ui_VC_IMAGE_AUTO_SAVE
import time

class gui(QMainWindow, Ui_VC_IMAGE_AUTO_SAVE): # do we ''need'' to inhereit from a main windOw?
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)



class controller(object):

    pil_init = pil.init()
    pil_init .setVerbose()
    pil_controller = pil_init.physical_PILaser_Controller()
    pil_data = [pil_controller.getVCDataObjConstRef()]
    pil_daq = [pil_controller.getClaraDAQObj_VC()]

    def __init__(self,argv):
        self.gui = gui()
        #self.gui.setupUi()
        self.gui.show()


        self.seconds_between_saves = self.gui.minutes_to_next_save.value() * 60
        self.pixel_threshold = self.gui.pix_int_threshold.value()



        self.gui.checkBox.stateChanged.connect(self.set_shouldsave)
        self.gui.pix_int_threshold.valueChanged.connect(self.set_threshold)
        self.gui.minutes_to_next_save.valueChanged.connect(self.set_time_between_saves)

        self.shouldsave = False


        self.time_start = time.time()

        self.start_count = 0
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.get_image)
        self.timer.start(1000)

        self.saved_images = ["","","","","",""]


    def set_shouldsave(self):
        if self.gui.checkBox.isChecked():
            self.shouldsave = True
        else:
            self.shouldsave = False

    def set_threshold(self):
        self.pixel_threshold = self.gui.pix_int_threshold.value()

    def set_time_between_saves(self,value):
        self.seconds_between_saves  = value * 60
        print("seconds_between_saves = ", self.seconds_between_saves)

    def get_image(self):
        print("get_image ", time.time() - self.time_start)
        print("intensity = ", controller.pil_data[0].avg_pix, self.pixel_threshold )
        if self.shouldsave:
            print("shouldsave")
            if time.time() - self.time_start > self.seconds_between_saves:
                print("time up")
                self.time_start = time.time()
                if controller.pil_controller.isNotCollectingOrSaving_VC():
                    print("IS NOT COLLECTING")
                    if controller.pil_controller.isAcquiring_VC():
                        print("IS ACQUIRING")
                        if controller.pil_data[0].avg_pix > self.pixel_threshold:
                            print("PIXEL IS ABOVE")
                            controller.pil_controller.collectAndSave_VC(1)

        print(controller.pil_daq[0].latestFilename)
        if controller.pil_daq[0].latestFilename != self.saved_images[-1]:
            self.saved_images.append(controller.pil_daq[0].latestFilename)
            self.saved_images.pop(0)
            self.gui.label_1.setText( self.saved_images[0] )
            self.gui.label_2.setText( self.saved_images[1] )
            self.gui.label_3.setText( self.saved_images[2] )
            self.gui.label_4.setText( self.saved_images[3] )
            self.gui.label_5.setText( self.saved_images[4] )
            self.gui.label_6.setText( self.saved_images[5] )


        #controller.cam_controller.collectAndSave_VC(10)



class main_application(QApplication):
	'''
		Simple class to own the main controller
		Everything else is created and managed in controller
	'''
	def __init__(self, argv):
		#
		# you need this init line here to instantiate a QApplication
		QApplication.__init__(self, argv)
		#
		# Everything is handled by a controller
		self.controller = controller(argv)


if __name__ == '__main__':
	APPLICATION_NAME = "Virtual Cathode Image Autosaver"
	print('Starting ' + APPLICATION_NAME)
	''' 
		sys.argv are the parameters passed from the command line
		e.g to run this you might type python 
	'''
	app = main_application(sys.argv)
	sys.exit(app.exec_())
