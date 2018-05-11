# get data from virtual cathode

import sys, math, time
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_PILaser_Control

# where do we want to put it?
try:
    req_x = float(sys.argv[1])  # 6.15
    req_y = float(sys.argv[2])  # 4.75
except IndexError:
    print('Usage: vc_mover.py <required_x> <required_y>')
    print('Positions in mm')
    exit()
print('Target position:', req_x, req_y)

init = VELA_CLARA_PILaser_Control.init()
pilc = init.physical_PILaser_Controller()
x = pilc.getX()  # h position
y = pilc.getY()  # v position
sx = pilc.getSigX()  # width
sy = pilc.getSigY()  # height
print('Start position:', x, y)
print('Size:', sx, sy)

# how much to move at a time?
move_amount = 5  # seems OK for a small step
precision = 0.1  # as a fraction of sigma x or y
while abs(req_x - x) > sx * precision or abs(req_y - y) > sy * precision:
    # Gotcha: a negative H move means the beam goes RIGHT, contrary to convention
    h_step = math.copysign(move_amount, -(req_x - x)) if abs(req_x - x) > sx * precision else 0
    # Do a bigger step in y
    v_step = 3 * math.copysign(move_amount, req_y - y) if abs(req_y - y) > sy * precision else 0
    print('Move amount', h_step, v_step)
    pilc.setHstep(h_step)
    assert pilc.moveH()  # returns True on success, presumably False on fail?
    time.sleep(0.1)
    pilc.setVstep(v_step)
    assert pilc.moveV()
    time.sleep(0.1)
    x = pilc.getX()  # h position
    y = pilc.getY()  # v position
    sx = pilc.getSigX()  # width
    sy = pilc.getSigY()  # height
    print('Position:', x, y)
    # print('How far away?', abs(req_x - x), abs(req_y - y), sx / 3, sy / 3)