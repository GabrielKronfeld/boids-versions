import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ArtistAnimation
from celluloid import Camera

xpoints=[]
ypoints=[]
colors=[]
birds=[]
xlen=10
ylen=10
avoidfactor=0.01
matchingfactor=0.01
centeringfactor=0.0001
protectedRange=0.2
visibleRange=3
turnfactor=0.2
maxspeed=0.3
minspeed=0.2


class boid():
    def __init__(self, x, y,vx,vy,color):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.color=color


def nextFrame():
    xpoints=[]
    ypoints=[]
    colors=[]
    for bird in birds:
        xpoints.append(bird.x)
        ypoints.append(bird.y)
        colors.append(bird.color)
    x=np.array(xpoints)
    y=np.array(ypoints)
    framePlot= plt.scatter(x,y,s=6,c=colors)
    applyBoids(birds)
    return framePlot


def makebirds(i):
    #we get a list of i boid objects.
    while i>0:
        
        birds.append(
            boid(   np.random.random()*xlen,#x position
                    np.random.random()*ylen,#y position
                    np.random.random()*xlen,#vx 
                    np.random.random()*ylen,#vy
                    np.random.random()*100#color
                ))
        i-=1
    return 1

def initializebirds(i):
    makebirds(i)
    return 1



def applyBoids(birds):
    for i in birds:
        #we should have an external loop
        #then perform boids on each bird per bird, so one boids call does ONE bird
        boids(i)
    for i in birds:
        applyAdjustment(i)

#something like this. 
def boids(i):
    #for birds in your radius, apply the boids algorithms
    #if in protected or visual range, apply different actions
    visibleboids=[]
    squishedboids=[]
    for otherboids in birds:
        if(otherboids==i):#same boid
            pass#do nothing
        else:
        #get radius apart, and then apply these points
            if getDist(i,otherboids)<protectedRange:
                squishedboids.append(otherboids)
                #not including birds that are too close into the visible range effects
            elif getDist(i,otherboids)<visibleRange:
                visibleboids.append(otherboids)
    separation(i,squishedboids)
    alignment(i,visibleboids)
    cohesion(i,visibleboids)
    screenedges(i)
    
def separation(boid,otherboids):
    close_dX=0
    close_dY=0
    for otherboid in otherboids:
        close_dX+=boid.x-otherboid.x
        close_dY+=boid.y-otherboid.y
    boid.vx+=close_dX*avoidfactor
    boid.vy+=close_dY*avoidfactor

def alignment(boid,otherboids):
    xv_avg=0
    yv_avg=0
    for otherboid in otherboids:
        xv_avg+=otherboid.vx
        yv_avg+=otherboid.vy
    if len(otherboids)!=0:
        xv_avg=xv_avg/len(otherboids)
        yv_avg=yv_avg/len(otherboids)
        boid.vx+=(xv_avg-boid.vx)*matchingfactor
        boid.vy+=(yv_avg-boid.vy)*matchingfactor
    
def cohesion(boid,otherboids):
    xavg=0
    yavg=0
    for otherboid in otherboids:
        xavg+=otherboid.x
        yavg+=otherboid.y
    if len(otherboids)!=0:
        xavg=xavg/len(otherboids)
        yavg=yavg/len(otherboids)
        boid.vx+=(xavg-boid.x)*centeringfactor
        boid.vy+=(yavg-boid.y)*centeringfactor
    
def screenedges(boid):
    leftmargin=xlen*0.2
    rightmargin=xlen*0.8
    topmargin=ylen*0.8
    bottommargin=ylen*0.2

    if boid.x < leftmargin:
        boid.vx = boid.vx + turnfactor
    if boid.x > rightmargin:
        boid.vx = boid.vx - turnfactor
    if boid.y > bottommargin:
        boid.vy = boid.vy - turnfactor
    if boid.y < topmargin:
        boid.vy = boid.vy + turnfactor

def speedlimit(boid):
    speed=np.sqrt((boid.vx**2)+(boid.vy**2))/3
    if speed>maxspeed:
        boid.vx=(boid.vx/speed)*maxspeed
    if speed<minspeed:
        boid.vx=(boid.vx/speed)*minspeed

def getDist(i,j):
    return np.sqrt(((i.x-j.x)**2)+((i.y-j.y)**2))
    

def applyAdjustment(i):
    #add the movement vector to position, make sure they stay in the grid by looping around
    speedlimit(i)
    i.x+=i.vx
    i.y+=i.vy


initializebirds(100)
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
