import laserTiming as lt
import signal
import time
import argparse

def sigint_handler(signum, frame):
    laser.turnOffLaserGating()

parser = argparse.ArgumentParser(description='Shoot laser until we reach an integrated charge measured on the WCM')
parser.add_argument('-q', '--charge', default=0, help='Burst until integrated charge is met', type=float)
parser.add_argument('-s', '--nshots', default=0, help='Burst for N shots', type=int)
parser.add_argument('-b', '--burst', help='Switch laser to burst mode', action='store_true')
parser.add_argument('-n', '--normal', help='Switch laser to normal mode', action='store_true')
parser.add_argument('-p', '--position', default=None, help='Motor Position', type=float)
parser.add_argument('-e', '--energy', default=None, help='Beam Energy', type=float)
parser.add_argument('-c', '--comment', default=None, help='Additional Comment', type=str)
args = parser.parse_args()

if args.burst or args.normal:
    laser = lt.LaserTiming(bpms=False)
elif args.charge > 0 or args.nshots > 0:
    laser = lt.LaserTiming(bpms=True)
# laser.setBurst(10)
if args.burst:
    print 'Setting BURST mode'
    laser.turnOffLaser()
elif args.normal:
    print 'Setting NORMAL LASER mode'
    laser.turnOnLaser()
elif args.charge > 0:
    print 'Running for ', args.charge, 'pC'
    laser.turnOnForIntegratedCharge(args.charge, pos=args.position, energy=args.energy, comment=args.comment)
elif args.nshots > 0:
    print 'Running for ', args.nshots, ' shots'
    laser.turnOnForNPulse(args.nshots, pos=args.position, energy=args.energy, comment=args.comment)
else:
    parser.print_help()
