# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#
from ..SAMPLlab import PhysicalConstants as PhyC


class Beamline(object):
    def __init__(self, componentlist=[], tracklocal=False, precision=1e-9):
        # array of components
        self.componentlist = componentlist
        self.tracklocal = tracklocal
        self.precision = precision
        # tracking method
        self.trackingMethod = 'default'
        # self.tracker = @TrackMatlab;       % pointer to tracking function

    def find(self, lst, a):
        return [i for i, x in enumerate(lst) if x == a]

    def ComputePositions(self):
        positions = [0]
        for component in self.componentlist:
            positions.append(positions[-1] + component.length)
        return positions

    def AppendComponent(self, component):
        self.componentlist.append(component)

    def TrackMatlab(self, elements, beam):
        nmax = len(self.componentlist)
        s = elements[0]
        e = elements[-1]
        # print("range = ", s, " ", e, "maxn = ",nmax)
        # beamout = None
        for n in range(s, e + 1):
            m = n % nmax
            if m == 0:
                m = nmax
            # break

            self.componentlist[n].Track(beam)
            beam.globaltime = beam.globaltime + self.componentlist[n].length / (beam.beta * PhyC.SpeedOfLight)
            inbeam = self.find(beam.distance[1], 1)
            # beam.distance[0][inbeam]
            beam.distance[0][inbeam] = beam.distance[0][inbeam] + self.componentlist[n].length
        return beam


            # check for spin tracking
            # if(~isempty(beam.spins) && ismethod(cmpt,'TrackSpin'))
            #     beam = cmpt.TrackSpin(beam);
            # end

    #         beam.globaltime = beam.globaltime + ...
    #             cmpt.length/(beam.beta * PhysicalConstants.SpeedOfLight);
    #
    #         inbeam = find(beam.distance(2,:)==1);
    #         beam.distance(1,inbeam) = beam.distance(1,inbeam) + cmpt.length;
    #
    #         if ~isempty(cmpt.aperture)
    #             x  = beam.particles(1,:)/cmpt.aperture(1);
    #             y  = beam.particles(3,:)/cmpt.aperture(2);
    #             ix =  ( (x.*x + y.*y) >= 1 );
    #             beam.distance(2,ix) = 0;
    #         end
    #
    #     end
    #
    # end % function TrackMatlab

# classdef Beamline < handle
#     % Beamline class
#     %
#     % Properties:
#     %   componentlist
#     %   tracklocal
#     %
#     % Methods:
#     %   AppendComponent
#     %   ComputePositions
#     %   Track
#     %   SetTrackingMethod
#     %   GetTrackingMethod
#
# % =========================================================================
#
#     properties
#         componentlist = {};
#         tracklocal    = false;
#     end % properties
#
# % =========================================================================
#
#     properties (Access=private)
#         trackingMethod = 'default';   % tracking method
#         tracker = @TrackMatlab;       % pointer to tracking function
#     end
#
# % =========================================================================
#
#     properties (SetAccess=private)
#         precision = 1e-9;             % numerical precision for closed orbit and transfer matrix calculations
#     end
#
# % =========================================================================
#
#     methods
#
# % -------------------------------------------------------------------------
#
#         function SetPrecision(beamline,precision)
#             % Sets the numerical precision for closed orbit and transfer
#             % matrix calculations
#
#             beamline.precision = precision;
#
#         end % function SetPrecision
#
# % -------------------------------------------------------------------------
#
#         function AppendComponent(beamline,component)
#             % Appends a component to the beamline
#
#             beamline.componentlist{numel(beamline.componentlist)+1} = component;
#
#         end % function AppendComponent
#
# % -------------------------------------------------------------------------
#
#         function positions = ComputePositions(beamline)
#             % Returns a vector of the start and end position of each component in the beamline.
#
#             positions = zeros(1,length(beamline.componentlist)+1);
#             for n = 1:length(beamline.componentlist)
#                 positions(n+1) = positions(n) + beamline.componentlist{n}.length;
#             end
#
#         end % function ComputePositions
#
# % -------------------------------------------------------------------------
#
#         function beam = Track(beamline,range,beam)
#             % beam2 = Beamline.Track([n1 n2],beam1)
#             % Tracks a beam of particles from entrance of component n1
#             % to exit of component n2.
#
#             beam = beamline.tracker(beamline,range,beam);
#
#         end % function Track
#
# % -------------------------------------------------------------------------
#
#         function SetTrackingMethod(beamline,method)
#             % Beamline.SetTrackingMethod(method)
#             % Sets the routines to use for tracking.
#             % method = 'default': use track methods built into component classes
#             % method = 'library': use track methods in library.dll
#
#             if ~strcmp(beamline.trackingMethod,method)
#                 if libisloaded(beamline.trackingMethod)
#                     unloadlibrary(beamline.trackingMethod);
#                 end
#             end
#
#             switch lower(method)
#
#                 case {'default','matlab',''}
#                     beamline.tracker = @TrackMatlab;
#                     beamline.trackingMethod = 'default';
#                     disp('Particle tracking in Matlab')
#                     beamline.precision = 1e-9;
#
#                 otherwise
#
#                     if ~libisloaded(method)
#                         loadlibrary(method,[method '.h']);
#                     end
#
#                     initparams.version = 'Tracking method';
#                     initparams.valid   = 0;
#                     structPtr = libpointer([method '_InitialisationParameters'],initparams);
#                     calllib(method,'ParticleTracking',structPtr);
#                     initparams = structPtr.value;
#
#                     if initparams.valid
#                         disp(initparams.version);
#                         beamline.tracker = @TrackLibrary;
#                         beamline.trackingMethod = method;
#
#                         beamline.precision = calllib(beamline.trackingMethod,'Precision');
#                         if beamline.precision>1e-8
#                             disp('Warning: tracking uses single precision.')
#                             disp('         Some calculations may not be accurate.')
#                         end
#                     else
#                         disp(['Failed to load tracking library ' method])
#                         clear structPtr;
#                         unloadlibrary(method);
#                         beamline.tracker = @TrackMatlab;
#                         beamline.trackingMethod = 'default';
#                         disp('Particle tracking in Matlab')
#                         beamline.precision = 1e-9;
#                     end
#             end
#
#         end % function SetTrackingMethod
#
# % -------------------------------------------------------------------------
#
#         function trackingMethod = GetTrackingMethod(beamline)
#
#             trackingMethod = beamline.trackingMethod;
#
#         end % function GetTrackingMethod
#
# % -------------------------------------------------------------------------
#
#         function CopyBeamline(beamline,range)
#
#             nmax = length(beamline.componentlist);
#             for n = range(1):range(2)
#                 m = mod(n,nmax);
#                 if(m==0)
#                     m = nmax;
#                 end
#                 beamline.componentlist{m}.TrackLibrary(beamline.trackingMethod,'Copy');
#             end
#
#         end % function CopyBeamline
#
# % -------------------------------------------------------------------------
#
#         function DeleteBeamlineCopy(beamline)
#
#             calllib(beamline.trackingMethod,'DeleteBeamlineCopy');
#
#         end % function DeleteBeamlineCopy
#
# % -------------------------------------------------------------------------
#     end % methods
#
# % =========================================================================
#
#     methods (Access=private)
#
# % -------------------------------------------------------------------------
#
#         function beam = TrackMatlab(beamline,range,beam)
#
#             nmax = length(beamline.componentlist);
#             for n = range(1):range(2)
#
#                 m = mod(n,nmax);
#                 if(m==0)
#                     m = nmax;
#                 end
#                 cmpt = beamline.componentlist{m};
#
#                 beam = cmpt.Track(beam);
#
#                 if(~isempty(beam.spins) && ismethod(cmpt,'TrackSpin'))
#                     beam = cmpt.TrackSpin(beam);
#                 end
#
#                 beam.globaltime = beam.globaltime + ...
#                     cmpt.length/(beam.beta * PhysicalConstants.SpeedOfLight);
#
#                 inbeam = find(beam.distance(2,:)==1);
#                 beam.distance(1,inbeam) = beam.distance(1,inbeam) + cmpt.length;
#
#                 if ~isempty(cmpt.aperture)
#                     x  = beam.particles(1,:)/cmpt.aperture(1);
#                     y  = beam.particles(3,:)/cmpt.aperture(2);
#                     ix =  ( (x.*x + y.*y) >= 1 );
#                     beam.distance(2,ix) = 0;
#                 end
#
#             end
#
#         end % function TrackMatlab
#
# % -------------------------------------------------------------------------
#
#         function beam = TrackLibrary(beamline,range,beam)
#
#             species = beam.species;
#
#             beam1.nparticles = size(beam.particles,2);
#             beam1.rigidity   = beam.rigidity;
#             beam1.charge     = species.charge;
#             beam1.mass       = species.mass;
#             if~isempty(beam.spins)
#                 beam1.g = species.g;
#             else
#                 beam1.g = 0;
#             end
#             beam1.globaltime = beam.globaltime;
#             bmPtr = libpointer([beamline.trackingMethod '_BeamParameters'],beam1);
#             psPtr = libpointer('doublePtr',beam.particles);
#             spPtr = libpointer('doublePtr',beam.spins);
#             dsPtr = libpointer('doublePtr',beam.distance);
#
#             calllib(beamline.trackingMethod,'InitialiseTracking',bmPtr,psPtr,spPtr,dsPtr);
#
#             if beamline.tracklocal
#
#                 calllib(beamline.trackingMethod,'TrackBeamline',range(1),range(2));
#
#             else
#
#                 nmax = length(beamline.componentlist);
#                 for n = range(1):range(2)
#                     m = mod(n,nmax);
#                     if(m==0)
#                         m = nmax;
#                     end
#                     beamline.componentlist{m}.TrackLibrary(beamline.trackingMethod,'Track');
#                 end
#
#             end
#
#             calllib(beamline.trackingMethod,'FinishTracking');
#
#             beam1           = bmPtr.Value;
#             beam.rigidity   = beam1.rigidity;
#             beam.globaltime = beam1.globaltime;
#             beam.particles  = psPtr.value;
#             if~isempty(beam.spins)
#                 beam.spins = spPtr.value;
#             end
#             beam.distance   = dsPtr.value;
#
#         end % function TrackLibrary
#
# % -------------------------------------------------------------------------
#
#     end % methods
#
# % =========================================================================
#
# end % classdef Beamline
