import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')

#import module
import VELA_CLARA_Camera_Control as cam
import time

#initialize
h = cam.init()
h.setVerbose()
cam_controller = h.physical_NEW_VELA_Camera_Controller()
print('Continue...')
raw_input()

allcams = ["BA1-SCR-01", "BA1-SCR-02", "BA1-SCR-03", "BA1-COFF-01", "BA1-COFF-02", "BA1-COFF-03",
           "BA1-COFF-04", ]

for cam in allcams:
    if cam_controller.startAcquiring(cam):
        print(cam, ' sent acquiring success')
    else:
        print(cam, ' sent acquiring failure')
    time.sleep(0.5)

    sent_save = False
    if cam_controller.isAcquiring():
        if cam_controller.collectAndSave(cam, 5):
            sent_save = True
            print(cam, " saving images yay")
        else:
            print(cam, ' saving images nay')

    if sent_save:
        # this ia surprisingly SLOW!!!
        while cam_controller.isCollectingOrSaving(cam):
            print(cam, ' iscollecting and saving')
        print(cam, ' collecting and saved to ', cam_controller.getLatestFilename(cam))
    else:
        print('ERROR ', cam, ' could not save image')

raw_input()


raw_input()




# mycam = 'SO1-CAM-01'
# cam_controller.startAcquiring(mycam)

# raw_input()


# if cam_controller.isAcquiring(mycam):
# cam_controller.collectAndSave(10)
# else:
# print("NOT ACQUIRING")

# raw_input()


# cam_controller.collectAndSave_VC(10)


# raw_input()
# raw_input()


# if cam_controller.velaLEDOn():
# print 'Sent ON to VELA LED'
# else:
# print 'FAILED Sent ON to VELA LED'

# if cam_controller.claraLEDOn():
# print 'Sent ON to CLARA LED'
# else:
# print 'FAILED Sent ON to CLARA LED'


# raw_input()

# if cam_controller.isVelaLEDOn():
# print 'VELA LED ON'
# else:
# print 'VELA LED OFF'

# if cam_controller.isClaraLEDOn():
# print 'CLARA LED ON'
# else:
# print 'CLARA  LED OFF'

# raw_input()

# cam_controller.velaLEDOff()
# cam_controller.claraLEDOff()

# raw_input()

# if cam_controller.isVelaLEDOn():
# print 'VELA LED ON'
# else:
# print 'VELA LED OFF'

# if cam_controller.isClaraLEDOn():
# print 'CLARA LED ON'
# else:
# print 'CLARA  LED OFF'

# raw_input()


# import VELA_CLARA_Camera_IA_Control as ia
# import time

# h = ia.init()
# h.setVerbose()
# cameras = h.physical_CLARA_Camera_IA_Controller()

# raw_input()
