from numpy import genfromtxt
import os
import numpy as np
from math import sin, cos, pi, atan
import matplotlib.pyplot as plt


def readInFiles(folderPath,airSpeeds):
    i=0
    allData = 0.0
    for root, dirs, files in os.walk(folderPath, topdown=False):
        for name in files:
            fileName = os.path.join(root, name)
            print(fileName)
            my_data = genfromtxt(fileName, skip_header=1, delimiter=',')
            if i==0:
                allData = my_data
            else:
                allData = np.append(allData, my_data, axis=0)

            i = i+1
#TODO: if airSpeeds is not empty, append imput data

    return allData


def nonDimensionalize(propData,airDens):
    # Propeller Diameter
    diameter = 9 * .0254  # meters
    #airDens = 1.0717  # kg/m^3
    # Advance Ratio J=(advance speed)/(RPS*Diameter)
    J = (propData[:, 19]) / ((propData[:, 12]) / 60.0 * diameter)

    # Propeller Efficiency Eff=(power out)/(power in) = (thrust x velocity)/(torque*rotation(rad/s))
    standDrag = 0.0002 * (propData[:, 19])  ** 2 - 0.0005 * (propData[:, 19])  + 5E-05
    if np.sum(propData[:, 9])<0:
        propData[:, 9] = -propData[:, 9]  # Reverse Thrust

    if np.sum(propData[:, 8]) < 0:
        propData[:, 8] = -propData[:, 8]  # Reverse Torque

    propData[:, 9] = propData[:, 9] + standDrag

    Eff = ((propData[:, 9] * 9.81) * (propData[:, 19])) / ((propData[:, 8]) * (propData[:, 12] / 60.0 * 2.0 * pi))
    Eff_electric = ((propData[:, 9] * 9.81) * (propData[:, 19])) / ((propData[:, 10]) * (propData[:, 11]))
    # Coefficient of Thrust Ct=thrust/(rho*RPS^2*D^4)

    Ct = (propData[:, 9] * 9.81) / (airDens * (propData[:, 12] / 60.0) ** 2.0 * diameter ** 4)

    return J, Eff, Ct, Eff_electric


def filterRPM(Data1, RPM_L, RPM_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0
    j = 0
    for i in range(Dlen):
        if Data[i, 12] <= RPM_H and Data[i, 12] >= RPM_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData


def filterPower(Data1, Pow_L, Pow_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0
    j = 0
    for i in range(Dlen):
        if Data[i, 14] <= Pow_H and Data[i, 14] >= Pow_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData


def filterWind(Data1, Wind_L, Wind_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0
    j = 0
    for i in range(Dlen):
        if Data[i, 19] <= Wind_H and Data[i, 19] >= Wind_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData


def filterPoints(Data1, Point_L, Point_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0

    j = 0
    for i in range(Dlen):
        if i <= Point_H and i >= Point_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData

def filterRE(Data1, RE_L, RE_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0
    j = 0
    for i in range(Dlen):
        w = ((Data[i, 12]*0.104719755*(.2286/2*.75))**2+(Data[i,19])**2)**.5
        RE = 1.225*w*.0254/(1.846*10**(-5.0))

        if RE <= RE_H and RE >= RE_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData

def filterAR(Data1, RE_L, RE_H):
    Dlen = len(Data1[:, 0])
    Data = np.copy(Data1)
    filteredData = 0.0
    j = 0
    for i in range(Dlen):
        # Propeller Diameter
        diameter = 9 * .0254  # meters
        # Advance Ratio J=(advance speed)/(RPS*Diameter)
        RE = (Data[i, 19]) / ((Data[i, 12]) / 60.0 * diameter)

        if RE <= RE_H and RE >= RE_L:
            if j == 0:
                filteredData = Data[i, :]
                j = 1
            else:
                filData = Data[i, :]
                filteredData = np.vstack([filteredData, filData])

    return filteredData


# File header is as follows:
# 0 Time (s)
# 1 ESC signal (us)
# 2 Servo 1 (us)
# 3 Servo 2 (us)
# 4 Servo 3 (us)
# 5 AccX (g)
# 6 AccY (g)
# 7 AccZ (g)
# 8 Torque (N-m)
# 9 Thrust (kgf) !!!!!!!!!!!!!!!!!!!!!THRUST SIGN WAS BACKWARDS
# 10 Voltage (V)
# 11 Current (A)
# 12 Motor Electrical Speed (RPM)
# 13 Motor Optical Speed (RPM)
# 14 Electrical Power (W)
# 15 Mechanical Power (W)
# 16 Motor Efficiency (%)
# 17 Propeller Mech. Efficiency (kgf/W)
# 18 Overall Efficiency (kgf/W)
# 19 Airspeed m/s
# 20 Airspeed (pa)
# 21 Electrical Forward Efficiency
# 19(22) Vibration (g)
# 20-21 (23-24) App message
# 22 Airspeed (manually added) - change

# Add airspeed
airSpeeds = []

folderPath = '/Users/kmoore/Dropbox/CodeRepos/TwoProp/TwoPropEmpiricalTesting/Dynamic/Single'
singleProp = readInFiles(folderPath, airSpeeds)
# np.savetxt('baseline.csv', Baseline, delimiter=',')

folderPath = '/Users/kmoore/Dropbox/CodeRepos/TwoProp/TwoPropEmpiricalTesting/Dynamic/RightPropCounterRo/fixedDataCounter'
counterR = readInFiles(folderPath, airSpeeds)
# np.savetxt('baseline.csv', Baseline, delimiter=',')

folderPath = '/Users/kmoore/Dropbox/CodeRepos/TwoProp/TwoPropEmpiricalTesting/Dynamic/RightPropCoRotating/fixedData'
coR = readInFiles(folderPath, airSpeeds)
# np.savetxt('baseline.csv', Baseline, delimiter=',')



# folderPath = 'C:\Users\owner\Desktop\CPAW\TestOutput\StandDrag'
# StandDrag=readInFiles(folderPath,airSpeeds)
# np.savetxt('standDrag.csv', StandDrag, delimiter=',')
#standDrag= 0.0002*airSpeeds**2 - 0.0005*airSpeeds + 5E-05 # From the test with the prop not attached, put in function


RPM_L = np.float(7000.0)
RPM_H = np.float(10000.0)

singleProp = filterRPM(singleProp, RPM_L, RPM_H)
counterR = filterRPM(counterR, RPM_L, RPM_H)
coR = filterRPM(coR, RPM_L, RPM_H)


Pow_L = np.float(-501.0)
Pow_H = np.float(500.0)

singleProp = filterPower(singleProp, Pow_L, Pow_H)
counterR = filterPower(counterR, Pow_L, Pow_H)
coR = filterPower(coR, Pow_L, Pow_H)


Wind_L = np.float(-100.0)
Wind_H = np.float(0.0)

singleProp = filterWind(singleProp, Wind_L, Wind_H)
counterR = filterWind(counterR, Wind_L, Wind_H)
coR = filterWind(coR, Wind_L, Wind_H)

#singleProp = filterPoints(singleProp, Point_L, Point_H)
#counterR = filterPoints(counterR, len(counterR[:,1])-len(counterR[:,1])+475, len(counterR[:,1])-125)
#coR = filterPoints(coR, len(coR[:,1])-len(coR[:,1]), len(coR[:,1]))

RE_L = np.float(100000.0)
RE_H = np.float(150000.0)

singleProp = filterRE(singleProp, RE_L, RE_H)
counterR = filterRE(counterR, RE_L, RE_H)
coR = filterRE(coR, RE_L, RE_H)

AR_L = np.float(0.0)
AR_H = np.float(.5)

singleProp = filterAR(singleProp, AR_L, AR_H)
counterR = filterAR(counterR, AR_L, AR_H)
coR = filterAR(coR, AR_L, AR_H)


airDens = 0.97022 # kg/m^3
J1, Eff1, Ct1, Effel1 = nonDimensionalize(singleProp,airDens)
Jcr, Effcr, Ctcr, Effelcr = nonDimensionalize(counterR,1.0235)
Jco, Effco, Ctco, Effelco = nonDimensionalize(coR,1.0235)


# Efficiency
plt.figure(1)
plt.plot(J1, np.absolute(Eff1), 'rx', label='Single Prop')
plt.plot(Jcr, np.absolute(Effcr), 'bo', label='Counter Props')
plt.plot(Jco, np.absolute(Effco), 'b+', label='Co Props')
plt.ylabel('Efficiency (thrust x airspeed)/(torque x rotation)')
plt.xlabel('Advance Ratio (J)')
plt.legend()
axes = plt.gca()
axes.set_xlim([0.0, .5])
#axes.set_ylim([0.0, 1.0])



# Thrust Coefficient

plt.figure(2)
plt.plot(J1, Ct1, 'rx', label='Single Prop')
plt.plot(Jcr, Ctcr, 'bo', label='Counter Props')
plt.plot(Jco, Ctco, 'b+', label='Co Props')
plt.ylabel('Ct')
plt.legend()
plt.xlabel('Advance Ratio (J)')
axes = plt.gca()
axes.set_xlim([0.0, .5])
#axes.set_ylim([-.005, 0.15])


# np.savetxt('single.csv', [J1,np.absolute(Eff1),Ct1], delimiter=',')
# np.savetxt('counter.csv', [Jcr,np.absolute(Effcr),Ctcr], delimiter=',')
# np.savetxt('co.csv', [Jco,np.absolute(Effco),Ctco], delimiter=',')





plt.show()
