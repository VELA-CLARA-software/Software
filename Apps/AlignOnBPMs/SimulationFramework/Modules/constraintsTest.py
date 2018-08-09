from constraints import *

cons = constraintsClass()

constraintsList = {
'1':{'type': 'lessThan', 'value': 23, 'limit': 0, 'weight': 1},
'2': {'type': 'greaterThan', 'value':0,'limit':12,'weight':1}}

print cons.constraints(constraintsList)
