

# sometimes 9?) missing channel when starting scr_init.physical_CLARA_PH1_Screen_Controller()
# check all chids/etc if there are channels that fail to connect
# get all screen names function 
# config files should be in AP CLARA 1 why do i see the following line??
# **** Attempting to Read \\fed.cclrc.ac.uk\org\NLab\ASTeC\Projects\VELA\Software\VELA_CLARA_PYDs\Config\claraPH1Screens.config ****
# function argument names
 
import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
import VELA_CLARA_Screen_Control as scr
import test_functions as tf

tester = tf.hwc_tester(sys.argv)
message = tester.message

tester.message('scr_init = scr.init()')
scr_init = scr.init()
message('scr_init.setVerbose()')
scr_init.setVerbose()

#vela_inj = scr_init.physical_VELA_INJ_Screen_Controller()
message('clara_ph1 = scr_init.physical_CLARA_PH1_Screen_Controller()')
clara_ph1 = scr_init.physical_CLARA_PH1_Screen_Controller()





# tester.test_docstring(clara_ph1.silence)
# tester.test_docstring(clara_ph1.isVOut)

clara_screen_names = ['S01-SCR-01','S02-SCR-01','S03-SCR-01']

funcnames={"getScreenObject" : getScreenObject}



tester.test_docstring(clara_ph1.funcnames("getScreenObject"))



# import inspect
# frame = inspect.currentframe()
# sig = inspect.getargvalues(clara_ph1.isHOut)
# print sig
# print sig
# print sig
# print sig


# for name in clara_screen_names:
# 	tester.test_function_1_arg(name,clara_ph1.isHOut,name)
	# tester.test_function_1_arg(name,clara_ph1.isVOut,name)
	# tester.test_function_1_arg(name,clara_ph1.is_HandV_OUT,name)
	# tester.test_function_1_arg(name,clara_ph1.isVIn,name)
	# tester.test_function_1_arg(name,clara_ph1.isScreenIn,name)
	# tester.test_function_1_arg(name,clara_ph1.isHMoving,name)
	# tester.test_function_1_arg(name,clara_ph1.isVMoving,name)
	# tester.test_function_1_arg(name,clara_ph1.isScreenMoving,name)
	# tester.test_function_1_arg(name,clara_ph1.isHIn,name)

        # .def("isHOut",                &screenController::isHOut, isHOutString                     )
        # .def("isVOut",                &screenController::isVOut, isVOutString                     )
        # .def("is_HandV_OUT",          &screenController::is_HandV_OUT, isHandVOutString           )
        # .def("isHIn",                 &screenController::isHIn, isHOutString                      )
        # .def("isVIn",                 &screenController::isVIn, isVInString                       )
        # .def("isScreenIn",            &screenController::isScreenIn, isScreenInString             )
        # .def("isHMoving",             &screenController::isHMoving, isHMovingString               )
        # .def("isVMoving",             &screenController::isVMoving, isVMovingString               )
        # .def("isScreenMoving",        &screenController::isScreenMoving, isScreenMovingString     )
        # .def("moveScreenTo",          &screenController::moveScreenTo, moveScreenToString         )
        # .def("insertYAG",             &screenController::insertYAG, insertYAGString               )
        # .def("moveScreenOut",         &screenController::moveScreenOut, moveScreenOutString       )
        # .def("setScreenSDEV",         &screenController::setScreenSDEV, setScreenSDEVString       )
        # .def("setScreenTrigger",      &screenController::setScreenTrigger, setScreenTriggerString )
        # .def("getScreenState",        &screenController::getScreenState, getScreenStateString     )
        # .def("isScreenInState",       &screenController::isScreenInState, isScreenInStateString   )
        # .def("isYAGIn",               &screenController::isYAGIn, isYAGInString                   )
        # .def("isHEnabled",            &screenController::isHEnabled, isHEnabledString             )
        # .def("isVEnabled",            &screenController::isVEnabled, isVEnabledString             )
        # .def("isHElement",            &screenController::isHElement, isHElementString             )
        # .def("isVElement",            &screenController::isVElement, isVElementString             )
        # .def("getACTPOS",             &screenController::getACTPOS, getACTPOSString               )
        # .def("getJDiff",              &screenController::getACTPOS, getJDiffString                )
        # .def("getDevicePosition",     &screenController::getDevicePosition, getDevicePosString    )
        # .def("jogScreen",             &screenController::jogScreen, jogScreenString               )
        # .def("resetPosition",         &screenController::resetPosition, resetPositionString       )
        # .def("setEX",                 &screenController::setEX, setEXString                       )
        # .def("setPosition",           &screenController::setPosition, setPositionString           )
        # .def("debugMessagesOff",      &screenController::debugMessagesOff                         )
        # .def("debugMessagesOn",       &screenController::debugMessagesOn                          )
        # .def("messagesOff",           &screenController::messagesOff                              )
        # .def("messagesOn",            &screenController::messagesOn                               )
		

# "getILockStates",
# "isHOut",
# "isVOut",
# "is_HandV_OUT",
# "isHIn",
# "isVIn",
# "isScreenIn",
# "isHMoving",
# "isVMoving",
# "isScreenMoving",
# "moveScreenTo",
# "insertYAG",
# "moveScreenOut",
# "setScreenSDEV",
# "setScreenTrigger",
# "getScreenState",
# "getScreenType",
# "isScreenInState",
# "isMover",
# "isPneumatic",
# "isYAGIn",
# "isHEnabled",
# "isVEnabled",
# "isHElement",
# "isVElement",
# "getACTPOS",
# "getJDiff",
# "getDevicePosition",
# "getDevicePosition",
# "jogScreen",
# "resetPosition",
# "setEX",
# "setPosition",
# "debugMessagesOff",
# "debugMessagesOn",
# "messagesOff",
# "messagesOn",
# "silence",
# "verbose")


		