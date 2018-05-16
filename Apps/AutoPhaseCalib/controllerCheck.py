import inspect
import VELA_CLARA_Charge_Control as scope

chargeInit = scope.init()
methods = inspect.getmembers(chargeInit, inspect.ismethod)
for m in methods:
    print m[0]
claraScope = chargeInit.physical_CLARA_PH1_Charge_Controller()
methods = inspect.getmembers(claraScope, inspect.ismethod)
