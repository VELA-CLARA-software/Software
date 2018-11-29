import laserTiming as lt
import signal
import time
import argparse

def sigint_handler(signum, frame):
    laser.turnOffLaserGating()

parser = argparse.ArgumentParser(description='Shoot laser until we reach an integrated charge measured on the WCM')
parser.add_argument('-q', '--charge', default=0, help='Burst until integrated charge is met', type=float)
parser.add_argument('-s', '--nshots', default=1, help='Burst for N shots', type=int)
parser.add_argument('-b', '--burst', help='Switch laser to burst mode', action='store_true')
parser.add_argument('-n', '--normal', help='Switch laser to normal mode', action='store_true')
args = parser.parse_args()

if args.burst or args.normal:
    laser = lt.LaserTiming(bpms=False)
else:
    laser = lt.LaserTiming(bpms=True)
# laser.setBurst(10)
if args.burst:
    laser.turnOffLaser()
elif args.normal:
    laser.turnOnLaser()
elif args.charge > 0:
    print args.charge
    laser.turnOnForIntegratedCharge(args.charge)
elif args.nshots > 0:
    print args.nshots
    laser.turnOnForNPulse(args.nshots)
