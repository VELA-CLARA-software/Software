from state_monitor import state_monitor
from VELA_CLARA_LLRF_Control import LLRF_TYPE
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class rf_protection_monitor(state_monitor):
    # whoami
    my_name = 'rf_protection_monitor'
    def __init__(self,
                 llrf_type=LLRF_TYPE.UNKNOWN_TYPE,
                 controller=None,
                 data_dict=None,
                 data_dict_key='',
                 update_time = 1000
        ):
        state_monitor.__init__(self,
                               llrf_type=llrf_type,
                               controller=controller,
                               data_dict=data_dict,
                               data_dict_key=data_dict_key,
                               update_time=update_time
        )
        self.prot_object = [self.localcontrol.getRFProtObjConstRef(self.llrf_type_string())]
        self.start()
        self.set_success = True


    def check(self):
        #print('Checking rf protection state')
        self.dict[self.key] = self.prot_object[0].status

