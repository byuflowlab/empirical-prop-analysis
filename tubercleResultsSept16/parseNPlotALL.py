

from numpy import genfromtxt
import os
import numpy as np
from math import sin, cos, pi, atan
import matplotlib.pyplot as plt

def readInFiles(folderPath, airSpeeds):
    i=0
    for root, dirs, files in os.walk(folderPath, topdown=False):
        for name in files:
            fileName=os.path.join(root, name)
            print(fileName)
            my_data = genfromtxt(fileName,skip_header=1, delimiter=',')
            if i==0:

                standDrag= 0.0002*(airSpeeds[i]**2) - 0.0005*airSpeeds[i] + 5E-05
                my_data[:,9]=-my_data[:,9]+standDrag #reverse thrust sign, correct for test stand drag
                my_data[:,8]=-my_data[:,8] #reverse torque sign
                allData=my_data



                airSpeed = np.zeros(len(my_data[:, 0]));
                airSpeed.fill(airSpeeds[i])
                airSpeed = np.transpose([airSpeed])


                allData= np.append(allData, airSpeed, axis=1)
            else:

                 standDrag= 0.0002*(airSpeeds[i]**2) - 0.0005*airSpeeds[i] + 5E-05
                 my_data[:,9]=-my_data[:,9]+standDrag #reverse thrust sign, correct for test stand drag
                 my_data[:,8]=-my_data[:,8] #reverse torque sign

                 airSpeed = np.zeros(len(my_data[:, 0]));
                 airSpeed.fill(airSpeeds[i])
                 airSpeed = np.transpose([airSpeed])
                 my_data= np.append(my_data, airSpeed, axis=1)
                 allData= np.append(allData, my_data, axis=0)
            i=i+1
    return allData


def nonDimensionalize(propData):
    #Propeller Diameter
    diameter = 5.5 *.0254 #meters
    airDens=1.0717 #kg/m^3
    #Advance Ratio J=(advance speed)/(RPS*Diameter)
    J=(propData[:,22])/((propData[:,12])/60.0*diameter)

    #Propeller Efficiency Eff=(power out)/(power in) = (thrust x velocity)/(torque*rotation(rad/s))
    Eff=((propData[:,9]*9.81)*(propData[:,22]))/((propData[:,8])*(propData[:,12]/60.0*2.0*pi))
    Eff_electric = ((propData[:,9]*9.81)*(propData[:,22]))/((propData[:,10])*(propData[:,11]))
    #Coefficient of Thrust Ct=thrust/(rho*RPS^2*D^4

    Ct=(propData[:,9]*9.81)/(airDens*(propData[:,12]/60.0)**2.0*diameter**4)



    return J, Eff, Ct, Eff_electric

def filterRPM(Data1, RPM_L, RPM_H):
    Dlen = len(Data1[:, 0])
    Data=np.copy(Data1)
    j=0
    for i in range(Dlen):
        if Data[i,12]<=RPM_H and Data[i,12]>=RPM_L:
            if j==0:
                filteredData=Data[i,:]
                j=1
            else:
                filData=Data[i,:]
                filteredData=np.vstack([filteredData, filData])


    return filteredData


def filterPower(Data1, Pow_L, Pow_H):
    Dlen = len(Data1[:, 0])
    Data=np.copy(Data1)
    j=0
    for i in range(Dlen):
        if Data[i,14]<=Pow_H and Data[i,14]>=Pow_L:
            if j==0:
                filteredData=Data[i,:]
                j=1
            else:
                filData=Data[i,:]
                filteredData=np.vstack([filteredData, filData])


    return filteredData

def filterWind(Data1, Wind_L, Wind_H):
    Dlen = len(Data1[:, 0])
    Data=np.copy(Data1)
    j=0
    for i in range(Dlen):
        if Data[i,22]<=Wind_H and Data[i,22]>=Wind_L:
            if j==0:
                filteredData=Data[i,:]
                j=1
            else:
                filData=Data[i,:]
                filteredData=np.vstack([filteredData, filData])


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
# 19 Vibration (g)
# 20-21 App message
# 22 Airspeed (manually added)

#Add airspeed
airSpeeds=[0.,
           2.64379456,
           5.91970368,
           9.1956128,
           12.47152192,
           15.74743104,
           19.02334016,
           22.29924928,
           25.5751584,
           28.85106752]



folderPath = './Baseline2'
Baseline2=readInFiles(folderPath,airSpeeds)
# np.savetxt('baseline.csv', Baseline, delimiter=',')

folderPath = './Baseline3'
Baseline3=readInFiles(folderPath,airSpeeds)
# np.savetxt('baseline.csv', Baseline, delimiter=',')

folderPath = './One'
one=readInFiles(folderPath,airSpeeds)
#np.savetxt('MM.csv', MM, delimiter=',')

folderPath = './Two'
two=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Three'
three=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Four'
four=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Five'
five=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Six'
six=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Seven'
seven=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Eight'
eight=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

folderPath = './Nine'
nine=readInFiles(folderPath,airSpeeds)
# np.savetxt('val6x4.csv', val6x4, delimiter=',')

# folderPath = 'C:\Users\owner\Desktop\CPAW\TestOutput\StandDrag'
# StandDrag=readInFiles(folderPath,airSpeeds)
# np.savetxt('standDrag.csv', StandDrag, delimiter=',')

#standDrag= 0.0002*airSpeeds**2 - 0.0005*airSpeeds + 5E-05 # From the test with the prop not attached, put in function


RPM_L=np.float(9000.0)
RPM_H=np.float(22500.0)

Baseline2=filterRPM(Baseline2,RPM_L,RPM_H)
Baseline3=filterRPM(Baseline3,RPM_L,RPM_H)
one=filterRPM(one,RPM_L,RPM_H)
two=filterRPM(two,RPM_L,RPM_H)
three=filterRPM(three,RPM_L,RPM_H)
four=filterRPM(four,RPM_L,RPM_H)
five=filterRPM(five,RPM_L,RPM_H)
six=filterRPM(six,RPM_L,RPM_H)
seven=filterRPM(seven,RPM_L,RPM_H)
eight=filterRPM(eight,RPM_L,RPM_H)
nine=filterRPM(nine,RPM_L,RPM_H)

Pow_L=np.float(8.0)
Pow_H=np.float(200.0)

Baseline2=filterPower(Baseline2,Pow_L,Pow_H)
Baseline3=filterPower(Baseline3,Pow_L,Pow_H)
one=filterPower(one,Pow_L,Pow_H)
two=filterPower(two,Pow_L,Pow_H)
three=filterPower(three,Pow_L,Pow_H)
four=filterPower(four,Pow_L,Pow_H)
five=filterPower(five,Pow_L,Pow_H)
six=filterPower(six,Pow_L,Pow_H)
seven=filterPower(seven,Pow_L,Pow_H)
eight=filterPower(eight,Pow_L,Pow_H)
nine=filterPower(nine,Pow_L,Pow_H)

Wind_L=np.float(0.0)
Wind_H=np.float(100.0)

Baseline2=filterWind(Baseline2,Wind_L,Wind_H)
Baseline3=filterWind(Baseline3,Wind_L,Wind_H)
one=filterWind(one,Wind_L,Wind_H)
two=filterWind(two,Wind_L,Wind_H)
three=filterWind(three,Wind_L,Wind_H)
four=filterWind(four,Wind_L,Wind_H)
five=filterWind(five,Wind_L,Wind_H)
six=filterWind(six,Wind_L,Wind_H)
seven=filterWind(seven,Wind_L,Wind_H)
eight=filterWind(eight,Wind_L,Wind_H)
nine=filterWind(nine,Wind_L,Wind_H)


J_B2, Eff_B2, Ct_B2, Eff_el_B2 = nonDimensionalize(Baseline2)
J_B3, Eff_B3, Ct_B3, Eff_el_B3 = nonDimensionalize(Baseline3)
J1, Eff1, Ct1, Effel1 = nonDimensionalize(one)
J2, Eff2, Ct2, Effel1 = nonDimensionalize(two)
J3, Eff3, Ct3, Effel1 = nonDimensionalize(three)
J4, Eff4, Ct4, Effel1 = nonDimensionalize(four)
J5, Eff5, Ct5, Effel1 = nonDimensionalize(five)
J6, Eff6, Ct6, Effel1 = nonDimensionalize(six)
J7, Eff7, Ct7, Effel1 = nonDimensionalize(seven)
J8, Eff8, Ct8, Effel1 = nonDimensionalize(eight)
J9, Eff9, Ct9, Effel1 = nonDimensionalize(nine)


# Tubercle Efficiency
plt.figure(1)
#plt.plot(J_B2, Eff_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Eff_B3,'k.',label='Baseline 2')
plt.plot(J1, Eff1,'rx',label='S Spacing S Bumps')
plt.plot(J2, Eff2,'gx',label='S Spacing M Bumps')
plt.plot(J3, Eff3,'bx',label='S Spacing L Bumps')
plt.ylabel('Efficiency (thrust x airspeed)/(torque x rotation)')
plt.xlabel('Advance Ratio (J)')
plt.legend()
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([0.0,1.0])

plt.figure(2)
#plt.plot(J_B2, Eff_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Eff_B3,'k.',label='Baseline 2')
plt.plot(J4, Eff4,'rx',label='M Spacing S Bumps')
plt.plot(J5, Eff5,'gx',label='M Spacing M Bumps')
plt.plot(J6, Eff6,'bx',label='M Spacing L Bumps')
plt.ylabel('Efficiency (thrust x airspeed)/(torque x rotation)')
plt.xlabel('Advance Ratio (J)')
plt.legend()
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([0.0,1.0])

plt.figure(3)
#plt.plot(J_B2, Eff_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Eff_B3,'k.',label='Baseline 2')
plt.plot(J7, Eff7,'rx',label='L Spacing S Bumps')
plt.plot(J8, Eff8,'gx',label='L Spacing M Bumps')
plt.plot(J9, Eff9,'bx',label='L Spacing L Bumps')
plt.ylabel('Efficiency (thrust x airspeed)/(torque x rotation)')
plt.xlabel('Advance Ratio (J)')
plt.legend()
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([0.0,1.0])


# Tubercle Thrust Coefficient

plt.figure(4)
#plt.plot(J_B2, Ct_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Ct_B3,'k.',label='Baseline 2')
plt.plot(J1, Ct1,'rx',label='S Spacing S Bumps')
plt.plot(J2, Ct2,'gx',label='S Spacing M Bumps')
plt.plot(J3, Ct3,'bx',label='S Spacing L Bumps')
plt.ylabel('Ct')
plt.legend()
plt.xlabel('Advance Ratio (J)')
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([-.005,0.15])

plt.figure(5)
#plt.plot(J_B2, Ct_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Ct_B3,'k.',label='Baseline 2')
plt.plot(J4, Ct4,'rx',label='M Spacing S Bumps')
plt.plot(J5, Ct5,'gx',label='M Spacing M Bumps')
plt.plot(J6, Ct6,'bx',label='M Spacing L Bumps')
plt.ylabel('Ct')
plt.legend()
plt.xlabel('Advance Ratio (J)')
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([-.005,0.15])

plt.figure(6)
#plt.plot(J_B2, Ct_B2,'ko',label='Baseline 1')
plt.plot(J_B3, Ct_B3,'k.',label='Baseline 2')
plt.plot(J7, Ct7,'rx',label='L Spacing S Bumps')
plt.plot(J8, Ct8,'gx',label='L Spacing M Bumps')
plt.plot(J9, Ct9,'bx',label='L Spacing L Bumps')
plt.ylabel('Ct')
plt.legend()
plt.xlabel('Advance Ratio (J)')
axes = plt.gca()
axes.set_xlim([0.0,1.0])
axes.set_ylim([-.005,0.15])



plt.show()

