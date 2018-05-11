# get data from virtual cathode

import sys, math, time
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_PILaser_Control
init = VELA_CLARA_PILaser_Control.init()
pilc = init.physical_PILaser_Controller()
x = pilc.getX()  # h position
y = pilc.getY()  # v position
sx = pilc.getSigX()  # width
sy = pilc.getSigY()  # height

# where do we want to put it?
req_x = 6.15
req_y = 4.75

# how much to move at a time?
move_amount = 100  # seems OK for a small step

while abs(req_x - x) < sx / 2 and abs(req_y - y) < sy / 2:
    # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
    h_step = math.copysign(-(req_x - x), move_amount)
    v_step = math.copysign(req_y - y, move_amount)
    pilc.setHstep(h_step)
    pilc.setVstep(v_step)
    assert pilc.moveH()
    # assert pilc.moveV()
    time.sleep(0.2)
    x = pilc.getX()  # h position
    y = pilc.getY()  # v position
    sx = pilc.getSigX()  # width
    sy = pilc.getSigY()  # height
    print('Position:', x, y)