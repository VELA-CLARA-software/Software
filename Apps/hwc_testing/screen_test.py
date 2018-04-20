

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
import screen_test_data

scr.init()

tester = tf.hwc_tester(sys.argv)
message = tester.message

tester.message('scr_init = scr.init()')
scr_init = scr.init()
message('scr_init.setVerbose()')



scr_init.setDebugMessage()

#vela_inj = scr_init.physical_VELA_INJ_Screen_Controller()
message('clara_ph1 = scr_init.physical_CLARA_PH1_Screen_Controller()')
clara_ph1 = scr_init.physical_CLARA_PH1_Screen_Controller()


# tester.test_docstring(clara_ph1.silence)
# tester.test_docstring(clara_ph1.isVOut)

clara_screen_names = clara_ph1.getScreenNames()

print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
print screen_test_data.funcnames[0]
//_____________________________________________________________________________
method_to_call = getattr(clara_ph1, screen_test_data.funcnames[0])
result = method_to_call()

tester.test_docstring(result)

src\VCmagnets.cpp|261|error C2664: 'magnetController::magnetController(const magnetController &)' : cannot convert argument 1 from 'bool' to 'bool *'|


# funcnames={
# "getScreenObject":    clara_ph1.getScreenObject,
# "isHOut":             clara_ph1.isHOut,
# "isVOut":             clara_ph1.isVOut,
# "is_HandV_OUT":       clara_ph1.is_HandV_OUT,
# "isHIn":              clara_ph1.isHIn,
# "isVIn":              clara_ph1.isVIn,
# "isScreenIn":         clara_ph1.isScreenIn,
# "isHMoving":          clara_ph1.isHMoving,
# "isVMoving":          clara_ph1.isVMoving,
# "isScreenMoving":     clara_ph1.isScreenMoving,
# "moveScreenTo":       clara_ph1.moveScreenTo,
# "insertYAG":          clara_ph1.insertYAG,
# "moveScreenOut":      clara_ph1.moveScreenOut,
# "setScreenSDEV":      clara_ph1.setScreenSDEV,
# "setScreenTrigger":   clara_ph1.setScreenTrigger,
# "getScreenState":     clara_ph1.getScreenState,
# "getScreenType":      clara_ph1.getScreenType,
# "isScreenInState":    clara_ph1.isScreenInState,
# "isMover":            clara_ph1.isMover,
# "isPneumatic":        clara_ph1.isPneumatic,
# "isYAGIn":            clara_ph1.isYAGIn,
# "isHEnabled":         clara_ph1.isHEnabled,
# "isVEnabled":         clara_ph1.isVEnabled,
# "isHElement":         clara_ph1.isHElement,
# "isVElement":         clara_ph1.isVElement,
# "getACTPOS":          clara_ph1.getACTPOS,
# "getJDiff":           clara_ph1.getJDiff,
# "getDevicePosition":  clara_ph1.getDevicePosition,
# "getScreenNames":     clara_ph1.getScreenNames,
# "getAvailableDevices":clara_ph1.getAvailableDevices,
# "jogScreen":          clara_ph1.jogScreen,
# "resetPosition":      clara_ph1.resetPosition,
# "setEX":              clara_ph1.setEX,
# "setPosition":        clara_ph1.setPosition,
# "debugMessagesOff":   clara_ph1.debugMessagesOff,
# "debugMessagesOn":    clara_ph1.debugMessagesOn,
# "messagesOff":        clara_ph1.messagesOff,
# "messagesOn":         clara_ph1.messagesOn,
# "silence":            clara_ph1.silence,
# "verbose":            clara_ph1.verbose}





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
	#
     #    .def("isHOut",                &screenController::isHOut, (arg("name")), isHOutString                                )
     #    .def("isVOut",                &screenController::isVOut, (arg("name")), isVOutString                                )
     #    .def("is_HandV_OUT",          &screenController::is_HandV_OUT, (arg("name")), isHandVOutString                      )
     #    .def("isHIn",                 &screenController::isHIn, (arg("name")), isHOutString                                 )
     #    .def("isVIn",                 &screenController::isVIn, (arg("name")), isVInString                                  )
     #    .def("isScreenIn",            &screenController::isScreenIn, (arg("name")), isScreenInString                        )
     #    .def("isHMoving",             &screenController::isHMoving, (arg("name")), isHMovingString                          )
     #    .def("isVMoving",             &screenController::isVMoving, (arg("name")), isVMovingString                          )
     #    .def("isScreenMoving",        &screenController::isScreenMoving, (arg("name")), isScreenMovingString                )
     #    .def("moveScreenTo",          &screenController::moveScreenTo, (arg("name"),arg("state")), moveScreenToString       )
     #    .def("insertYAG",             &screenController::insertYAG, (arg("name")), insertYAGString                          )
     #    .def("moveScreenOut",         &screenController::moveScreenOut, (arg("name")), moveScreenOutString                  )
     #    .def("setScreenSDEV",         &screenController::setScreenSDEV, (arg("name")), setScreenSDEVString                  )
     #    .def("setScreenTrigger",      &screenController::setScreenTrigger, (arg("name")), setScreenTriggerString            )
     #    .def("getScreenState",        &screenController::getScreenState, (arg("name")), getScreenStateString                )
     #    .def("getScreenType",         &screenController::getScreenType, (arg("name")), getScreenTypeString                  )
     #    .def("isScreenInState",       &screenController::isScreenInState, (arg("name"),arg("state")), isScreenInStateString )
     #    .def("isMover",               &screenController::isMover, (arg("name")), isYAGInString                              )
     #    .def("isPneumatic",           &screenController::isPneumatic, (arg("name")), isMoverString                          )
     #    .def("isYAGIn",               &screenController::isYAGIn, (arg("name")), isPneumaticString                          )
     #    .def("isHEnabled",            &screenController::isHEnabled, (arg("name")), isHEnabledString                        )
     #    .def("isVEnabled",            &screenController::isVEnabled, (arg("name")), isVEnabledString                        )
     #    .def("isHElement",            &screenController::isHElement, (arg("name")), isHElementString                        )
     #    .def("isVElement",            &screenController::isVElement, (arg("name")), isVElementString                        )
     #    .def("getACTPOS",             &screenController::getACTPOS, (arg("name")), getACTPOSString                          )
     #    .def("getJDiff",              &screenController::getJDiff, (arg("name")), getJDiffString                            )
     #    .def("getDevicePosition",     &screenController::getDevicePosition, (arg("name"),arg("state")), getDevicePosString  )
     #    .def("getScreenNames",        &screenController::getScreenNames_Py, getScreenNamesString                            )
     #    .def("getAvailableDevices",   &screenController::getAvailableDevices, (arg("name")), getAvailableDevicesString      )
     #    .def("jogScreen",             &screenController::jogScreen, (arg("name"),arg("jog (mm)")), jogScreenString          )
     #    .def("resetPosition",         &screenController::resetPosition, (arg("name")), resetPositionString                  )
     #    .def("setEX",                 &screenController::setEX, (arg("name")), setEXString                                  )
     #    .def("setPosition",           &screenController::setPosition, (arg("name"),arg("pos (mm)")), setPositionString      )
     #    .def("debugMessagesOff",      &screenController::debugMessagesOff                         )
     #    .def("debugMessagesOn",       &screenController::debugMessagesOn                          )
     #    .def("messagesOff",           &screenController::messagesOff                              )
     #    .def("messagesOn",            &screenController::messagesOn                               )
     #    .def("silence",               &screenController::silence                                  )
     #    .def("verbose",               &screenController::verbose                                  )

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


		