import numpy as np
from math import sin, cos,pi,atan
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# this file is designed to take points and translate and rotate them according to input functions
# think propeller or wing chord twist distribution

global freq, amp  #wavelength and amplitude of the sine distribution
freq=15.5  #number sinusoidal periods across the blade radius R
amp=.0625*.25*0.  #amplitude as the fraction of the propeller max radius R

ampOVERwavelength=freq*amp
print ampOVERwavelength

def fullBladeRotate(original, Theta):
    originalM=np.matrix(original)
    originalMT=np.transpose(originalM)
    R=np.matrix([[1,0,0],[0.,cos(Theta),-sin(Theta)],[0.,sin(Theta),cos(Theta)]])
    swept=R*originalMT
    sweptT=np.transpose(swept)
    return sweptT

def transAll(original,Tx,Ty,Tz):
    temp=np.copy(original)
    tx=np.copy(Tx)
    ty=np.copy(Ty)
    x=temp[:,0]
    y=temp[:,1]
    z=temp[:,2]

    x=x+tx
    y=y+ty
    z=z+Tz
    translated=np.zeros([len(x),3])
    translated[:,0]=x
    translated[:,1]=y
    translated[:,2]=z

    return translated

def rotate(original,Theta):
    # rotate points (must do first)
    Theta=90-Theta
    temp=np.copy(original)
    theta=np.copy(Theta)
    x=temp[:,0]
    y=temp[:,1]
    theta=theta*pi/180.
    xrot = x*cos(theta) - y*sin(theta)
    yrot = y*cos(theta) + x*sin(theta)
    rotated=np.zeros([len(xrot),2])
    rotated[:,0]=xrot
    rotated[:,1]=yrot
    return rotated

#funtion to translate the airfoil in a 2d plane
def trans(original, Tx,Ty,r,R):
    temp=np.copy(original)
    tx=np.copy(Tx)
    ty=np.copy(Ty)
    x=temp[:,0]-amp*sin(r/R*2.*pi*freq)*R
    y=temp[:,1]


    x=x+tx
    y=y+ty
    translated=np.zeros([len(x),2])
    translated[:,0]=x
    translated[:,1]=y

    return translated



def scale(original, Chord,Thick):
    temp=np.copy(original)
    chord=np.copy(Chord)
    thick=np.copy(Thick)
    n=len(temp[:,0])
    for i in range(n):
        temp[i][0]=temp[i][0]*chord
        temp[i][1]=temp[i][1]*chord

    for i in range(n):
        #temp[i][0]=temp[i][0]*chord
        temp[i][1]=temp[i][1]*thick

    return temp

#chord distribution where an r/R position returns a chord/R
def chorddist(r,R):

    #chord = -40.779*(r/R)**2 + 42.168*(r/R) + 6.6981
    chord=202.67*(r/R)**4 - 513.07*(r/R)**3 + 416.98*(r/R)**2 - 126.11*(r/R) + 27.892
    chordsin=chord
    chordreal=chord/100*R #convert to actual chord
    chordsinreal=chordsin/100*R+amp*sin(r/R*2.*pi*freq)*R
    return chordreal,chordsinreal

#pitch distribution where x is r/R and y is in percent of the nominal pitch
def pitchdist(r,R,Pitch):
    pitch=np.copy(Pitch)
    pitchdist = 184.34*(r/R)**3 - 455.3*(r/R)**2 + 367.02*(r/R) + 4.3333
    pitchat_roverR=pitchdist*pitch/100.
    pitchDistPerRev=pitch/(2*pi*r)
    pitchRad=atan(pitchDistPerRev)
    pitchDeg=pitchRad*180./pi

    return pitchDeg

#thickness distribution where x is r/R and y is thickness/chord
def thickdist(r,R):


    #thickdist = 134.51*(r/R)**(-0.585)*.01
    thickdist=2658.4*(r/R)**4 - 7385.9*(r/R)**3 + 7617.6*(r/R)**2 - 3566.4*(r/R) + 825.35
    thickdist=thickdist*0.01

    return thickdist


#import airfoil data points

foil = np.zeros([121, 2])

with open('clarky.csv', 'rb') as f1:
    reader = csv.reader(f1, dialect='excel', quotechar='|')
    i = 0

    for row in reader:

        foil[i, :] = row[0:2]

        i += 1

    f1.close()

#airfoil was 1000 mm long nondimensialize it to 1
maxx=max(foil[:,0])
maxy=max(foil[:,1])
minx=min(foil[:,0])
miny=min(foil[:,1])
chord0=maxx-minx
thick0=117
foiln=scale(foil,1/chord0,1)

#input propeller parameters set inputs to 1 to create non-dimensionalized blade
R=5.5/2. #Radius in inches
pitchNom=4. #Pitch in inches

#we want x number of bumps (this is hard coded into the chord dist curve)
#initialize radius array with enough elements to define the bumps
numSections=300
numSec=300.

#of hub top and bottom locations
upper=.07*R #this is actually the bottom, make it smaller to decrease it's distance
lower=-.11*R #this is actually the top, make it more negative to make it higher
#these control the point density in the hub, keep them equal
tuneFactor=10.
tuneF=10

r=np.arange(0.08*R, R, R/numSec)

#create point cloud of airfoils
#Initialize point cloud

m=len(r)
chord,chordsin=chorddist(r[0],R)
chordsave=chord

thick=thickdist(r[0],R)
theta=pitchdist(r[0],R,pitchNom)
thetasave=theta
#scale airfoil
foilcloud=scale(foiln,chordsin,thick)
foilcloud=trans(foilcloud,(-chord/4.),0,r[0],R)
foilcloud=rotate(foilcloud,theta)
Zr=np.zeros(len(foilcloud[:,0])); Zr.fill(r[0])
Zr=np.transpose([Zr])
foilcloud=np.append(foilcloud,Zr,axis=1)

chordz=np.arange(.001*chordsin, chordsin, chordsin/(numSections/2))


# #Fill in root
# for i in range(numSections/2):
#     #now r[i] will give us the position
#     #get chord and thickness and scale
#
#     chordnew=chordz[i]
#
#
#     foil1=scale(foiln,chordnew,thick)
#     foil1=rotate(foil1,theta)
#     #foil1=rotate(foil1,theta)
#     Zr=np.zeros(len(foil1[:,0])); Zr.fill(r[0])
#     Zr=np.transpose([Zr])
#     foil1=np.append(foil1,Zr,axis=1)
#     a=foil1.shape
#     b=foilcloud.shape
#     foilcloud=np.append(foilcloud,foil1,axis=0)
#     #print foil1



#fill in point cloud
for i in range(m-1):
    #now r[i] will give us the position
    #get chord and thickness and scale
    chord,chordsin=chorddist(r[i+1],R)
    chordsave=np.append(chordsave,chord)

    thick=thickdist(r[i+1],R)
    theta=pitchdist(r[i+1],R,pitchNom)
    thetasave=np.append(thetasave,theta)
    #scale airfoil
    foil1=scale(foiln,chordsin,thick)
    foil1=trans(foil1,(-chord/4.),0,r[i+1],R)
    foil1=rotate(foil1,theta)
    #foil1=rotate(foil1,theta)
    Zr=np.zeros(len(foil1[:,0])); Zr.fill(r[i+1])
    Zr=np.transpose([Zr])
    foil1=np.append(foil1,Zr,axis=1)
    a=foil1.shape
    b=foilcloud.shape
    foilcloud=np.append(foilcloud,foil1,axis=0)
    savez=r[i+1]
    savei=i
    #print foil1

chordz=np.arange(.001*chordsin, chordsin, chordsin/(numSections/2))

#Fill in Tip
for i in range(numSections/2):
    #now r[i] will give us the position
    #get chord and thickness and scale

    chordnew=chordz[i]


    foil1=scale(foiln,chordnew,thick)
    foil1=trans(foil1,(-chord/4.),0,r[savei+1],R)
    foil1=rotate(foil1,theta)
    #foil1=rotate(foil1,theta)
    Zr=np.zeros(len(foil1[:,0])); Zr.fill(savez)
    Zr=np.transpose([Zr])
    foil1=np.append(foil1,Zr,axis=1)
    a=foil1.shape
    b=foilcloud.shape
    foilcloud=np.append(foilcloud,foil1,axis=0)
    #print foil1


r=r*.0254
chordsave=chordsave*.0254

# print 'r'
# print r
# print 'chordsave'
# print chordsave
# print 'theta'
# print thetasave

#Center Blade
Tx=0.
Ty=-.05*R
Tz=0.
cloudTranslated=transAll(foilcloud,Tx,Ty,Tz)

#Make other half of the blade
angle=pi #180 degrees
cloudRotated=fullBladeRotate(cloudTranslated,angle)
#cloudRotated=fullBladeRotate(foilcloud,angle)
foilcloud=np.append(foilcloud,cloudRotated,axis=0)



#Create the hub
#create the ring
increment=1./numSec
hubAngle=np.arange(0.,2*pi,(2.*pi/numSec))
#print hubAngle
hubRingx=[]
hubRingy=[]
for i in range(numSections):
    arcPointx=.1154*R*sin(hubAngle[i])  #this makes a ring .1154*R in radius
    arcPointy=.1154*R*cos(hubAngle[i])
    hubRingx=np.append(hubRingx,arcPointx)
    hubRingy=np.append(hubRingy,arcPointy)

#create the outer tube surface
tubex=[]
tubey=[]
tubez=[]

increment2=(upper-lower)/numSec*tuneFactor
zpoints=np.arange(lower,upper,increment2)
for i in range(numSections/tuneF):
    tubeRingx=np.copy(hubRingx)
    tubeRingy=np.copy(hubRingy)
    tubex=np.append(tubex,tubeRingx)
    tubey=np.append(tubey,tubeRingy)

    for j in range(len(tubeRingx)):
        zi=zpoints[i]
        tubez=np.append(tubez,zi)


tube=np.zeros([len(tubex),3])
tube[:,2]=tubex
tube[:,1]=tubey
tube[:,0]=tubez

#Rotate the tube 90 degrees
angle=90.*pi/180.
tube=fullBladeRotate(tube,angle)
#Move it into position
Tx=.2
Ty=.07
Tz=0.
tube=transAll(tube,Tx,Ty,Tz)

#create the inner tube surface
tubeix=[]
tubeiy=[]
tubeiz=[]

hubHoleFraction=0.311

increment2=(upper-lower)/numSec*tuneFactor
zpointsi=np.arange(lower,upper,increment2)
for i in range(numSections/tuneF):
    tubeRingix=np.copy(hubRingx)
    tubeRingiy=np.copy(hubRingy)
    tubeRingix=tubeRingix*hubHoleFraction
    tubeRingiy=tubeRingiy*hubHoleFraction
    tubeix=np.append(tubeix,tubeRingix)
    tubeiy=np.append(tubeiy,tubeRingiy)

    for j in range(len(tubeRingix)):
        zii=zpointsi[i]
        tubeiz=np.append(tubeiz,zii)


tubei=np.zeros([len(tubeix),3])
tubei[:,2]=tubeix
tubei[:,1]=tubeiy
tubei[:,0]=tubeiz

#Rotate the inner surface tube 90 degrees
angle=90.*pi/180.
tubei=fullBladeRotate(tubei,angle)
#Move it into position
Tx=.2
Ty=.07
Tz=0.
tubei=transAll(tubei,Tx,Ty,Tz)

#create a disk
hubHoleFraction=0.311
increment3=(1-hubHoleFraction)/numSec*tuneFactor
diskScale=np.arange(hubHoleFraction,1.,increment3)
diskx=[]
disky=[]
for i in range(numSections/tuneF):
    innerRingx=np.copy(hubRingx)
    innerRingy=np.copy(hubRingy)

    innerRingx=innerRingx*diskScale[i]
    innerRingy=innerRingy*diskScale[i]
    diskx=np.append(diskx,innerRingx)
    disky=np.append(disky,innerRingy)

#Combine x and y into disk
disk=np.zeros([len(diskx),3])
disk[:,2]=diskx
disk[:,1]=disky

#add z value for top
diskzTop=np.full((1,len(diskx)),upper)
topDisk=np.copy(disk)
topDisk[:,0]=diskzTop

#add z value for bottom
diskzBot=np.full((1,len(diskx)),lower)
botDisk=np.copy(disk)
botDisk[:,0]=diskzBot
#combine disks
disks=np.append(topDisk,botDisk,axis=0)
#Rotate and place disks
#Rotate the disks 90 degrees
angle=90.*pi/180.
disks=fullBladeRotate(disks,angle)
#Move it into position
Tx=.2
Ty=.07
Tz=0.
disks=transAll(disks,Tx,Ty,Tz)

#combine top, bottom, and tubes to foilcloud

foilcloud=np.append(foilcloud,tube,axis=0)
foilcloud=np.append(foilcloud,tubei,axis=0)
foilcloud=np.append(foilcloud,disks,axis=0)


print len(foilcloud[:,1])

x=foilcloud[:,0]
y=foilcloud[:,1]
z=foilcloud[:,2]

np.savetxt('control.xyz', np.c_[x,y,z],delimiter=' ')




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, zdir='z', c= 'red')
plt.title("Generated Point Cloud")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.xlim([-max(z),max(z)])
plt.ylim([-max(z),max(z)])
#
#
# #plt.savefig("demo.png")
plt.show()