# a class to allow the user to move the laser to a user-chosen location on the virtual cathode
import sys, math, time
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_PILaser_Control
import epics
vert_pv = 'CLA-LAS-OPT-PICO-4C-PM-4:V:MREL'
horiz_pv = 'CLA-LAS-OPT-PICO-4C-PM-4:H:MREL'

class BeamOutOfRangeException(Exception):
    pass

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
        # print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
        # print 'Size: {:.3f}, {:.3f}'.format(self.lassx, self.lassy)
        # if laser is more than 3 mm away from rf centre, quit. 
        if abs(self.lasx - rfx0) > 6 or abs(self.lasy - rfy0) > 5: 
            raise BeamOutOfRangeException('Suspect beam way off centre from RF - assume RF centre {}, {}'.format(rfx0, rfy0))

    def move_horiz(self, delta):
        """Move the laser horizontally."""
        self.pilc.setHstep(delta)
        assert self.pilc.moveH()  # returns True on success, presumably False on fail?
        time.sleep(0.1)

    def move_vert(self, delta):
        """Move the laser vertically."""
        # vertical movement is currently not working in the controller - use EPICS instead
        # self.pilc.setVstep(v_step)
        # assert self.pilc.moveV()
        epics.caput(vert_pv, -delta)  # have to reverse the sign
        time.sleep(0.1)

    def setposition(self,setx, sety, delta=5, prec=0.1):
        self.getposition()
        # how much to move at a time?
        move_amount = delta  # seems OK for a small step
        precision = prec  # as a fraction of sigma x or y
        print 'Moving to {:.3f}, {:.3f}'.format(setx, sety)
        while abs(setx - self.lasx) > self.lassx * precision or abs(sety - self.lasy) > self.lassy * precision:
            # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
            h_step = math.copysign(move_amount, -(setx - self.lasx)) if abs(setx - self.lasx) > self.lassx * precision else 0
            # Do a bigger step in y
            v_step = 3 * math.copysign(move_amount, sety - self.lasy) if abs(sety - self.lasy) > self.lassy * precision else 0
            # print 'Move amount: H {}, V {}'.format(h_step, v_step)
            self.move_horiz(h_step)
            self.move_vert(v_step)
            self.getposition()
            # print 'Position: {:.3f}, {:.3f}'.format(self.lasx, self.lasy)
            # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)
        print 'Final position {:.3f}, {:.3f}'.format(self.lasx, self.lasy)






## where do we want to put it?
#try:
#    req_x = float(sys.argv[1])  # 6.15
#    req_y = float(sys.argv[2])  # 4.75
#except IndexError:
#    print('Usage: vc_mover.py <required_x> <required_y>')
#    print('Positions in mm')
#    exit()
#print('Target position:', req_x, req_y)
#
##exit()
#
#init = VELA_CLARA_PILaser_Control.init()
#pilc = init.physical_PILaser_Controller()
#x = pilc.getX()  # h position
#y = pilc.getY()  # v position
#sx = pilc.getSigX()  # width
#sy = pilc.getSigY()  # height
#print('Start position:', x, y)
#print('Size:', sx, sy)
#
## how much to move at a time?
#move_amount = 5  # seems OK for a small step
#precision = 0.1  # as a fraction of sigma x or y
#while abs(req_x - x) > sx * precision or abs(req_y - y) > sy * precision:
#    # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
#    h_step = math.copysign(move_amount, -(req_x - x)) if abs(req_x - x) > sx * precision else 0
#    # Do a bigger step in y
#    v_step = 3 * math.copysign(move_amount, req_y - y) if abs(req_y - y) > sy * precision else 0
#    print('Move amount', h_step, v_step)
#    pilc.setHstep(h_step)
#    assert pilc.moveH()  # returns True on success, presumably False on fail?
#    time.sleep(0.1)
#    pilc.setVstep(v_step)
#    assert pilc.moveV()
#    time.sleep(0.1)
#    x = pilc.getX()  # h position
#    y = pilc.getY()  # v position
#    sx = pilc.getSigX()  # width
#    sy = pilc.getSigY()  # height
#    print('Position:', x, y)
#    # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)