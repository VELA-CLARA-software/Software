# a class to allow the user to move the laser to a user-chosen location in x, y mm on the virtual cathode
import sys, math, time
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_PILaser_Control

class lasmover:
    pilcinit = VELA_CLARA_PILaser_Control.init()
    pilc = pilcinit.physical_PILaser_Controller()
    lasx = 'unknown' 
    lasy = 'unknown'
    lassx = 'unknown' 
    lassy = 'unknown'

    def getposition(self):
        self.lasx = self.pilc.getX()  # h position
        self.lasy = self.pilc.getY()  # v position
        self.lassx = self.pilc.getSigX()  # width
        self.lassy = self.pilc.getSigY()  # height
        # rf centre positions (rough)
        rfx0 = 6
        rfy0 = 5
        print('Start position:', self.lasx, self.lasy)
        print('Size:', self.lassx, self.lassy) 
        # if laser is more than 3 mm away from rf centre, quit. 
        if abs(self.lasx - rfx0) > 6 or abs(self.lasy - rfy0) > 5: 
            print '!!! Something is wrong here, suspect beam way off centre !!!!'
            print '!!! Program exiting and will not move laser any further !!!!'
            exit()
    
    def setposition(self,setx, sety, delta=5, prec=0.1):
        self.getposition()
        # how much to move at a time?
        move_amount = delta  # seems OK for a small step
        precision = prec  # as a fraction of sigma x or y
        while abs(setx - self.lasx) > self.lassx * precision or abs(sety - self.lasy) > self.lassy * precision:
            # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
            h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(setx - self.lasx) > self.lassx * precision else 0
            # Do a bigger step in y
            v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(sety - self.lasy) > self.lassy * precision else 0
            print('Move amount', h_step, v_step)
            self.pilc.setHstep(h_step)
            assert self.pilc.moveH()  # returns True on success, presumably False on fail?
            time.sleep(0.1)
            self.pilc.setVstep(v_step)
            assert self.pilc.moveV()
            time.sleep(0.1)
            self.getposition()
            print('Position:', self.lasx, self.lasy)
            # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
      