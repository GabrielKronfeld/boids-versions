import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ArtistAnimation
from celluloid import Camera
'''
pseudo-boids built off global radius, forces decreasing linearly or 1/distance^2'''
'''using a radius of influence will save on compute tremendously'''
'''strict values is BAD! does not scale well!!!'''
#each bird has an x,y,ANGLE value
#we should have a check for birds in LOS
global tau 
tau = 2*np.pi

def makebirds(i):
    while i>0:
        bird= np.array([np.random.random()*xlen,#x position
                        np.random.random()*ylen,#y position
                        np.random.random()*tau,#angle in radians
                        1,#velocity
                        0,#boidsAdjustment x axis
                        0,#boidsAdjustment y axis
                        np.random.random()*100])#color(constant)
        birds.append(bird)
        i-=1
    return 1

def initializebirds(i):
    makebirds(i)
    return 1

def updatepoints(var):
    tmp=[]
    for bird in birds:
        tmp.append(bird[var])
    return tmp

def applyBoids(birds):
    for i in birds:
        #we should have an external loop
        #then perform boids on each bird per bird, so one boids call does ONE bird
        boids1()
        boids2(i)
        boids3(i)
        edgeDetect(i)
    for i in birds:
        applyAdjustment(i)

#something like this. 
def boids(i):
    boids1()
    boids2(i)
    boids3(i)
    return 1
def boids1():

#these take a bird(type:list)
#birds want to fly in the same direction
#this weight is even across ALL birds, since it's the total avg angle. maybe should be scaled by distance too though
    scalingFactor=1
    sumAngles=0.0
    for bird in birds:
            sumAngles+=bird[2]
    avgAngle=sumAngles/len(birds)
    #I don't know if this will permanently save the values of the bird.
    #the angle is adjusted according to the magnitudes. we should really have a heading angle vs nextpoint angle.
    #right now our values change during our operation which affects our flock motion by biasing our avg flock angle
    for i in birds:
        i[4]+=np.cos(avgAngle)*scalingFactor
        i[5]+=np.sin(avgAngle)*scalingFactor
    
def boids2(i):
    #birds want to fly together
#easily done by adding an inversely linearly weighted attractor to the center of the cluster
    scalingFactor=1#*np.sqrt(xlen**2+ylen**2)
    avgX=0.0
    avgY=0.0
    '''for each bird, find the closest birds and fly them into the center of the group
    so, we can say for each bird, all other birds give their x,y coordinates (scaled by their distance linearly, or maybe by the sqrt for even more gradual)
     then give the bird a movement adjustment to fly toward that median. 
    '''
    for bird in birds:
        if i[0]==bird[0] and i[1]==bird[1]:
            pass
    else:
        #current bird position
        x1=i[0]
        y1=i[1]
        #other bird position
        x2=bird[0]
        y2=bird[1]
        #find the distance between them
        dx=x2-x1
        dy=y2-y1
        #attractive force, scaled by inverse distance linearly. 
        if dx==0 and dy==0:
            force=0
        else:
            force=scalingFactor/np.sqrt((dx**2)+(dy**2))
        if force<1:
            force=1

        avgX+=dx*force
        avgY+=dy*force
    i[4]+=avgX
    i[5]+=avgY

def boids3(i):
    #birds don't want to fly into each other
    scalingFactor=0.3
    for bird in birds:
        if i[0]==bird[0] and i[1]==bird[1]:
            pass
    #for each bird, take inverse square ((sqrt?) NO, sqrt is 1/2, inverse square is -2) of distance to a bird, then that magnitude*angle for a new vector
    #and add it to the present one. 
        else: 
            x1=i[0]
            y1=i[1]
            x2=bird[0]
            y2=bird[1]
            dx=x2-x1
            dy=y2-y1
            #repulsive force, so negative
            force=-scalingFactor/((dx**2)+(dy**2))
            '''
             decompX=np.cos(i[2])*i[3]+dx*force
            decompY=np.sin(i[2])*i[3]+dy*force
            i[4]=np.atan((decompY-y1)/(decompX-x1))
            #got angle, need to adjust magnitude
            '''
            i[4]+=dx*force
            i[5]+=dy*force

def edgeDetect(i):
    #if bird is within the last 20% of the border, add heavy repulsive pressure
      #birds don't want to fly into each other
      #find nearest wall point, use that as a repulsive force?
    scalingFactor=1.0
    for bird in birds:
        if i[0]==bird[0] and i[1]==bird[1]:
            pass
    #for each bird, take inverse square ((sqrt?) NO, sqrt is 1/2, inverse square is -2) of distance to a bird, then that magnitude*angle for a new vector
    #and add it to the present one. 
    #double check math for turning force.
        else: 
            x1=i[0]
            y1=i[1]
            if x1>xlen*0.7:
                i[4]+=i[0]/((xlen-x1/xlen)**2)
            if x1<xlen*0.3:
                i[4]+=i[0]/(x1**2)
            if y1>ylen*0.7:
                i[5]+=-i[1]/((ylen-y1/ylen)**2)
            if y1<ylen*0.3:
                i[5]+=i[1]/(y1**2)
                

            #repulsive force, so negative
            '''
             decompX=np.cos(i[2])*i[3]+dx*force
            decompY=np.sin(i[2])*i[3]+dy*force
            i[4]=np.atan((decompY-y1)/(decompX-x1))
            #got angle, need to adjust magnitude
            '''

def applyAdjustment(i):
    #add the movement vector to position, make sure they stay in the grid by looping around
    scalingFactor=i[3]#velocity
    nextX=(i[0]+i[4])
    nextY=(i[1]+i[5])
    dx=nextX-i[0]#just i[4]
    dy=nextY-i[1]#just i[5]

    i[2]=np.atan(dx/dy)

    normalizedNextX=nextX/np.sqrt(nextX**2+nextY**2)
    normalizedNextY=nextY/np.sqrt(nextX**2+nextY**2)

    i[0]=(i[0]+normalizedNextX*scalingFactor)%xlen
    i[1]=(i[1]+normalizedNextY*scalingFactor)%ylen
    i[2]=np.atan(dx/dy)
#   i[3]=i[3], no updates
    i[4]=0.0
    i[5]=0.0
#   i[6]=i[6] color is constant too
    return 1

xpoints=[]
ypoints=[]
colors=[]
birds=[]
xlen=10
ylen=10

initializebirds(100)

def nextFrame():
        xpoints=updatepoints(0)
        ypoints=updatepoints(1)
        colors=updatepoints(6)
        x=np.array(xpoints)
        y=np.array(ypoints)
        tmp= plt.scatter(x,y,s=6,c=colors)
        applyBoids(birds)
        return tmp




# initializing a figure in  
# which the graph will be plotted 
fig= plt.figure()
camera=Camera(fig)
plt.axis([0,xlen,0,ylen])
artists=[]
for i in range(0, 1000):
    nextFrame()
    camera.snap()
animation=camera.animate()
plt.show()
'''
# marking the x-axis and y-axis 
axis = plt.axes(xlim =(0, 4),  
                ylim =(-2, 2))  
  
# initializing a line variable 
line, = axis.plot([], [], lw = 3)  
   
# data which the line will  
# contain (x, y) 
def init():  
    line.set_data([], []) 
    return line, 
   
def animate(i): 
    x = np.linspace(0, 4, 1000) 
   
    # plots a sine graph 
    y = np.sin(2 * np.pi * (x - 0.01 * i)) 
    line.set_data(x, y) 
      
    return line, 
   
anim = FuncAnimation(fig, animate, init_func = init, 
                     frames = 200, interval = 20, blit = True) 
  
   
anim.save('continuousSineWave.mp4',  
          writer = 'ffmpeg', fps = 30)
'''
'''
np.random.seed(19680801)  # seed the random number generator.
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100
#figsize is size of plot physically, x and y length, NOT values or axis
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
#a,b x y data positions, c is color of point, s is size of point, data is data 
ax.scatter('a', 'b', c='c', s='d', data=data)
ax.set_xlabel('entry a')
ax.set_ylabel('entry b')
'''