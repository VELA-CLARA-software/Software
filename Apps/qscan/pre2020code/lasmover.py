# a class to allow the user to move the laser to a user-chosen location in x, y mm on the virtual cathode
import sys, math, time
#sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")
#0#import VELA_CLARA_PILaser_Control

class lasmover:
#0#    pilcinit = VELA_CLARA_PILaser_Control.init()
#0#    pilc = pilcinit.physical_PILaser_Controller()
    lasx = 'unknown' 
    lasy = 'unknown'
    lassx = 'unknown' 
    lassy = 'unknown'

    def getposition(self):
#0#        self.lasx = self.pilc.getX()  # h position
#0#        self.lasy = self.pilc.getY()  # v position
#0#        self.lassx = self.pilc.getSigX()  # width
#0#        self.lassy = self.pilc.getSigY()  # height
#0#        # rf centre positions (rough)
        rfx0 = 6
        rfy0 = 5
#0#        print('Start position:', self.lasx, self.lasy)
#0#        print('Size:', self.lassx, self.lassy) 
#0#        # if laser is more than 3 mm away from rf centre, quit. 
#0#        if abs(self.lasx - rfx0) > 6 or abs(self.lasy - rfy0) > 5: 
#0#            print('!!! Something is wrong here, suspect beam way off centre !!!!')
#0#            print('!!! Program exiting and will not move laser any further !!!!')
#0#            exit()
    
    def setposition(self,setx, sety, delta=5, prec=0.1):
#0#        self.getposition()
#0#        # how much to move at a time?
        move_amount = delta  # seems OK for a small step
#0#        precision = prec  # as a fraction of sigma x or y
#0#        while abs(setx - self.lasx) > self.lassx * precision or abs(sety - self.lasy) > self.lassy * precision:
#0#            # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
#0#            h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(setx - self.lasx) > self.lassx * precision else 0
#0#            # Do a bigger step in y
#0#            v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(sety - self.lasy) > self.lassy * precision else 0
#0#            print('Move amount', h_step, v_step)
#0#            self.pilc.setHstep(h_step)
#0#            assert self.pilc.moveH()  # returns True on success, presumably False on fail?
#0#            time.sleep(0.1)
#0#            self.pilc.setVstep(v_step)
#0#            assert self.pilc.moveV()
#0#            time.sleep(0.1)
#0#            self.getposition()
#0#            print('Position:', self.lasx, self.lasy)
#0#            # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
      