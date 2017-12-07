
# this class monitors the LLRF and is used to get values
# it will be used to set the masks etc?
# we will create a LLRF control class to set pulse widths and amplitudes


class LLRF_monitor:

	num_buffer_traces = 30

	def __init__(self,llrf, KFPow = 'KLYSTRON_FORWARD_POWER',
							CRPow = 'CAVITY_REVERSE_POWER',
							CRPha = 'CAVITY_REVERSE_PHASE'):
		self.KFPow = KFPow
		self.CRPow = CRPow
		self.CRPha = CRPha
		self.traces_to_monitor = [KFPow, CRPow, CRPha]
		self.tracedata = {}
		#self.latestTraceIndex = {}
		self.llrf = llrf
		self.llrfObj = [self.llrf.getLLRFObjConstRef() ]
		for trace in self.traces_to_monitor:
			self.setupTraces(trace)
		self.evid = self.getEVID()

	def setupTraces(self,trace_name):
		# Start individual traces as required
		# the channels for these names are defined in the config file
		self.llrf.startTraceMonitoring(trace_name)
		self.llrf.setNumBufferTraces(trace_name,self.num_buffer_traces)
		# dictionary (keyed by trace type) of trace data objects (should dynamically update)
		self.tracedata[trace_name] = self.llrfObj[0].trace_data[trace_name]
		# dictionary (keyed by trace type) of latest trace data index (should dynamically update)
		#self.latestTraceIndex[trace_name] = self.llrfObj[0].trace_data[trace_name].latest_trace_index

	def get_num_break_downs(self):
		self.llrf.getNumOutsideMaskTraces()

	def getEVID(self):
		# it shouldn't matter which trace EVID we look at
		# (they should all update together)
		return self.tracedata[self.CRPow].EVID

	# set the cavity reverse power trace HI mask to mask
	def set_cavity_rev_power_mask_HI(self, mask):
		return self.llrf.setCavRevPwrHMask(mask)

	# set the cavity reverse power trace LO mask to mask
	def set_cavity_rev_power_mask_LO(self, mask):
		return self.llrf.setCavRevPwrLoMask(mask)

	#
	def enable_check_masks(self):
		return self.llrf.setShouldCheckMask(self.CRPow)

	# sets the indices of the Klystron Forward Power trace mean calculation
	def set_klystron_forward_power_trace_mean_range(self,start_index ,stop_index):
		a = self.llrf.setMeanStartIndex(self.KFPow,start_index)
		if not a:
			print('Error Setting ', self.KFPow, ' mean power start index to ', start_index)
		a = self.llrf.setMeanStopIndex(self.KFPow,stop_index)
		if not a:
			print('Error Setting ', self.KFPow, ' mean power stop index to ', stop_index)

	# this returns the mean klystron forward power in the ranges defined by set_klystron_forward_power_trace_mean_range
	def get_mean_klystron_foward_power(self):
		return self.tracedata[self.KFPow].traces[ self.llrfObj[0].trace_data[self.KFPow].latest_trace_index ].mean

	# get the number of elements in the trace time data less than t
	def get_trace_index_at_time(self,t):
		return sum(i < t for i in self.llrfObj[0].time_vector.values)


