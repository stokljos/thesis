import pandas as pd
import numpy as np
from scipy import io
import sys
import math
import os

def process_results(inputArgs):
    
    list_of_files = os.listdir()
    for ii in list_of_files:
        if ii[-17:] == 'referenceFile.txt':
            refFile = ii
        if ii == 'onset.txt':
            onFile = ii
            
    with open(onFile, 'rt') as h:
        data = [line.split() for line in h]
        exonset = float(data[0][0])

    with open(refFile, 'rt') as h:
        data = [line.split() for line in h]
        nodes = int(data[0][0])
        peaks = data[4]
        
    for ii in range(len(peaks)):
        peaks[ii] = float(peaks[ii])
       
    maxDisp = peaks[-2]
    
    with open('topDispxcyc.txt', 'rt') as h:
        data = [line.split() for line in h]
        disp = []
        i = 0
        loc = 0
        for line in range(len(data)):
            if len(data[i])<nodes or data[i][-1] == '-':
                break

            else:
                for ii in range(0,nodes):
                        loc += float(data[i][ii])

                loc = loc/nodes
                disp.append(loc)
                loc = 0
                i += 1

    with open('baseReactxcyc.txt', 'rt') as h:
        data = [line.split() for line in h]
        force = []
        i = 0
        loc = 0
        for line in range(len(data)):
            if len(data[i])<nodes or data[i][-1] == '-':
                break
            else:
                for ii in range(0,nodes):
                    loc += float(data[i][ii])


                loc = -loc
                force.append(loc)
                loc = 0
                i += 1               
    h.close

    maxStrength = max(force)
    maxStrengthI = force.index(maxStrength)  
    
    if disp[maxStrengthI]>maxDisp:
        for ii in range(len(disp)):
            if math.isclose(maxDisp,disp[ii],abs_tol = 0.01):
                lim = ii
                break
        maxStrength = max(force[:lim])
        maxStrengthI = force.index(maxStrength)          
        
    onsetD = 0
    for ii in range(1,len(force)):
        if (force[ii-1]-force[ii])/max(force) > 0.1 and force[ii]> 0 and ii > maxStrengthI:
            onsetD = disp[ii-1]
            onsetF = force[ii-1]
            break
    
    if onsetD == 0:
        onsetD = disp[-1]
        onsetF = force[-1]
        
    if onsetD < 0:
        onsetD = max(disp)
        onsetF = force[disp.index(onsetD)]
       
    value = abs((onsetD-exonset)/exonset)
    with open('results.out','w') as outFile:
        outFile.write(str(value))

    
    
if __name__ == "__main__":
    n = len(sys.argv)
    responses = []
    for i in range(1,n):
        responses.append(sys.argv[i])

    process_results(responses)

    
       
        