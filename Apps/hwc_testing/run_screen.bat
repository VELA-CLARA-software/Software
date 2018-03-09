 @ECHO OFF
 SET OUTPUT=screen_test_output.txt
 @ECHO ON
 screen_test.py  %OUTPUT% > %OUTPUT% 2>&1