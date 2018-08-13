from ComponentBase import ComponentBase
import numpy

class Marker(ComponentBase):
    def __init__(self, name=""):
        ComponentBase.__init__(self, length=0, name, aperture=[])
        self.dummy = 0

    def Track(self, beam):
        # save
        self.lastTrackedBeam = beam
