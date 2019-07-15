#!/usr/bin/env python3
__author__ = "Miguel Villamizar"
__copyright__ = "Copyright 2017"
# Linear system for Gauss-Jordan elimination method
def variables_fill(args):
    vars = []
    for variables in args:
        for key in variables:
            if(key == "result"):
                continue
            if(key not in vars):
                vars.append(key)
    vars.sort()
    vars.append("result")
    for variables in args:
        for key in vars:
            if key not in (variables.keys()):
                variables[key] = 0.0
    NxN = (len(vars)-1) == len(args)
    return args,NxN,vars

def show_array(array,position):
	print(position)
	for equation in array:
		for i in position:
		    print(equation[i],end=" ")
		print()

def converter_of_row(array,modify,position,change,pivot_row = None):
    if(not(change)):
        if(pivot_row == None):
            return array
        multiplier = -1.00*array[position[modify]]
        for variable in position:         
            array[variable] += multiplier*pivot_row[variable]   
    else:    
        dividend = array[position[modify]]
        for variable in position:
            try:
                array[variable] /= dividend
            except ZeroDivisionError:
                array[variable] = 0         

def GaussJordan(array,position):
    count = 0
    while(count < len(position)-1):
        converter_of_row(array[count],count,position,True)
        count2 = 0
        while(count2 < len(position)-1):
            if(count2 == count):
                count2 += 1
                continue
            pivot_row = array[count]
            converter_of_row(array[count2],count,position,False,pivot_row)
            count2 += 1
        count += 1    

linearSystem = []
print("note: all unknown quantity to the left equal sign")
while(True):
    equation = input("Insert your equation (if you do not want insert more press \"$\"): ")
    if("$" in equation):
        break
    equation = equation.replace(" ","")
    i = 0
    count = 0
    dict = {}
    while(i < len(equation)):
        if(equation[i].isalpha()):
            if (i == 0):
                value = 1.0
            else:
                if(count == 0 or equation[i-1] == "-" or equation[i-1] == "+"):
                    value = float(equation[i-1]+"1")
                else:
                    value = float(equation[i-count:i])
            count = 0
            if(equation[i] in dict):
            	dict[equation[i]] += value
            else:
            	dict[equation[i]] = value
            i += 1
            continue
        if(equation[i] == "="):
            value = float(equation[i+1:])
            dict['result'] = value
        count += 1
        i += 1
    if ("result" not in list(dict.keys())):
        dict['result'] = 0.0
    linearSystem.append(dict)

linearSystem,NxN,vars = variables_fill(linearSystem)
if(NxN):
    show_array(linearSystem,vars)
    GaussJordan(linearSystem,vars)
    show_array(linearSystem,vars)
else:
    print("Error the number of variables and equations are different")