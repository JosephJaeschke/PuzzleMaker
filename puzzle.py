class Node(object):
    def __init__(self,pos):
        self.parent=None
	self.pos=pos
	self.move=0
	self.stepcount=-1

import math
import numpy
import pygame
import sys
from random import randint
import random
import os.path
import time
import scipy
import scipy.stats
#MISC SETUP AND PRINT STUFF===========================================
print "Enter File Name: "
fobj=raw_input()
fo=None
n=0
start=None
auxillary=None
fifo=[]

def initPuz():
	global n
	global auxillary
	global start
	n=int(fo.read(1))
	start=numpy.zeros([n,n,3])
	auxillary=numpy.empty((n,n),dtype=object)
	for x in range(n):
		for y in range(n):
			char=fo.read(1)
			if char=='':
				break
			if char=='\n'  or char==" ":
				char=fo.read(1)
			auxillary[y][x]=Node((x,y))
			auxillary[y][x].move=int(char)
			auxillary[y][x].stepcount=-1
			start[y][x][0]=int(char)
	auxillary[0][0].stepcount=0

def initRand():
	global n
	global auxillary
	global start
	print "Enter Dimension: "
	n=int(raw_input())
	start=numpy.zeros([n,n,3])
	auxillary=numpy.empty((n,n),dtype=object)
	for x in range(n):
		for y in range(n):
			val=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
			auxillary[y][x]=Node((x,y))
			auxillary[y][x].move=val
			auxillary[y][x].stepcount=-1
	auxillary[0][0].stepcount=0

def reInit():
	global n
	global auxillary
	global start
	start=numpy.zeros([n,n,3])
	auxillary=numpy.empty((n,n),dtype=object)
	for x in range(n):
		for y in range(n):
			val=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
			auxillary[y][x]=Node((x,y))
			auxillary[y][x].move=val
			auxillary[y][x].stepcount=-1
	auxillary[0][0].stepcount=0


if os.path.isfile(fobj):
	fo=open(fobj,"r")
	initPuz()
else:
	initRand()
root=auxillary[0][0]
root.stepcount=0
pygame.font.init()
font2=pygame.font.SysFont("monospace",500/(n*2))
font=pygame.font.SysFont("monospace",500/(n))
pygame.init()
pygame.display.set_caption('puzzle')
window=pygame.display.set_mode((700,700)) #set window size
bgc=(0,0,0) #set background color number
window.fill(bgc)
bs=700/n
sys.setrecursionlimit(999999999)
def grid(): #draw the nxn grid and print 2d arr values for each square
	for y in range(n):
		for x in range(n):
			rect=pygame.Rect(x*bs,y*bs,bs,bs)
			pygame.draw.rect(window,((23*x)%255,(17*y)%255,(x*y)%255),rect)
			char=str(int(auxillary[x][y].move)) #print the move value for each square
			char2=str(int(auxillary[x][y].stepcount)) #To print num of moves
			text=font.render(char,1,(255,255,255))
			window.blit(text,(x*bs+2,y*bs+2))
			text=font2.render(char2,1,(255,255,0)) #to print num of moves
			window.blit(text,(x*bs,y*bs+bs/2+(500/(n*3.5))))
	rect=pygame.Rect((n-1)*bs,(n-1)*bs,bs,bs)
	pygame.draw.rect(window,(255,255,255),rect)
	pygame.display.update()
	text=font.render("G",1,(0,0,0))
	window.blit(text,((n-1)*bs+2,(n-1)*bs+2))
	char2=str(int(auxillary[x][y].stepcount))
	text=font2.render(char2,1,(5,5,255))
	window.blit(text,(x*bs,y*bs+bs/2+(500/(n*3.5))))
	pygame.display.update()
#END MISC SETUP STUFF======================================================================
#g third dim is (step number,moves to get there,visited?)
def solve(current,aux): #takes a point defined by x pos and y pos
	y=current.pos[0]
	x=current.pos[1]
	if current.move==0:
		aux[x][y].stepcount=aux[x][y].parent.stepcount+1
	fifo.pop(0)
	if x-current.move in range(n) and (aux[x-current.move][y].stepcount==-1 or current.stepcount<aux[x-current.move][y].stepcount) and not (x-current.move,y)==(0,0):
        	fifo.append(aux[x-current.move][y])
        	aux[x-current.move][y].parent=current
        	aux[x-current.move][y].stepcount=current.stepcount+1
	if x+current.move in range(n) and (aux[x+current.move][y].stepcount==-1 or current.stepcount<aux[x+current.move][y].stepcount) and not (x+current.move,y)==(0,0):
        	fifo.append(aux[x+current.move][y])
        	aux[x+current.move][y].parent=current
        	aux[x+current.move][y].stepcount=current.stepcount+1
    	if y-current.move in range(n) and (aux[x][y-current.move].stepcount==-1 or current.stepcount<aux[x][y-current.move].stepcount) and not (x,y-current.move)==(0,0):
        	fifo.append(aux[x][y-current.move])
        	aux[x][y-current.move].parent=current
        	aux[x][y-current.move].stepcount=current.stepcount+1
    	if y+current.move in range(n) and (aux[x][y+current.move].stepcount==-1 or current.stepcount<aux[x][y+current.move].stepcount) and not (x,y+current.move)==(0,0):
        	fifo.append(aux[x][y+current.move])
        	aux[x][y+current.move].parent=current
        	aux[x][y+current.move].stepcount=current.stepcount+1
    	if fifo:
		solve(fifo[0],aux)

def evaluate():
	score=0
	global auxillary
	if not auxillary[n-1][n-1].stepcount==-1:
		score=auxillary[n-1][n-1].stepcount
	else:
		for y in range(n):
			for x in range(n):
				if auxillary[x][y].stepcount==-1:
					score=score+1
		score=score*-1
	return score

def getRead(node,arr):
		for i in range(n):
			for j in range(n):
				arr[i][j].stepcount=-1
		node.stepcount=0
		arr[0][0].stepcount=0
		fifo.append(arr[0][0])
		solve(arr[0][0],arr)

def hillClimb(itrNum):
	oldMove=0
	global auxillary
	getRead(auxillary[0][0],auxillary)
	grid()
	score=evaluate()
	for i in range(itrNum):
		matrixindex=int(randint(0,n*n-2))
		x=matrixindex/n
		y=matrixindex%n
		walkNum=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
		oldScore=evaluate()
		oldMove=auxillary[x][y].move
		auxillary[x][y].move=walkNum
		getRead(auxillary[0][0],auxillary)
		newScore=evaluate()
		if newScore>oldScore:
			auxillary[x][y].move=walkNum
			score=newScore
		else:
			auxillary[x][y].move=oldMove
		getRead(auxillary[0][0],auxillary)
	grid()
	return score

def hillWalk(prob,itrNum):
	oldMove=0
	global auxillary
	getRead(auxillary[0][0],auxillary)
	grid()
	score=evaluate()
	for i in range(itrNum):
		matrixindex=int(randint(0,n*n-2))
		x=matrixindex/n
		y=matrixindex%n
		walkNum=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
		oldScore=evaluate()
		oldMove=auxillary[x][y].move
		auxillary[x][y].move=walkNum
		getRead(auxillary[0][0],auxillary)
		newScore=evaluate()
		if newScore>oldScore:
			auxillary[x][y].move=walkNum
			score=newScore
		elif random.uniform(0,1)<prob:
			auxillary[x][y].move=walkNum
			score=newScore
		else:
			auxillary[x][y].move=oldMove
		getRead(auxillary[0][0],auxillary)
	grid()
	return score

def hillRestart(resNum,iterNum):
	global auxillary
	getRead(auxillary[0][0],auxillary)
	grid()
	saveState=evaluate()
	better=numpy.empty((n,n),dtype=object)
	for y in range(n):
		for x in range(n):
			better[x][y]=Node((x,y))
			better[x][y].move=auxillary[x][y].move
			better[x][y].stepcount=auxillary[x][y].stepcount
	for i in range(resNum):
		val=hillClimb(iterNum)
		if int(val)>int(saveState):
			for y in range(n):
				for x in range(n):
					better[x][y].move=auxillary[x][y].move
					better[x][y].stepcount=auxillary[x][y].stepcount
			saveState=val
		for y in range(n):
			for x in range(n):
				auxillary[x][y].move=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
				auxillary[x][y].stepcount=-1
		auxillary[0][0].stepcount=0
	for y in range(n):
		for x in range(n):
			auxillary[y][x].move=better[x][y].move
			auxillary[y][x].stepcount=better[x][y].stepcount
	grid()

def simulatedAnnealing(temp,decayRate,itrNum):
	oldMove=0
	temp=float(temp)
	global auxillary
	getRead(auxillary[0][0],auxillary)
	score=evaluate()
	grid()
	for i in range(itrNum):
		matrixindex=int(randint(0,n*n-2))
		x=matrixindex/n
		y=matrixindex%n
		walkNum=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
		oldScore=evaluate()
		oldMove=auxillary[x][y].move
		auxillary[x][y].move=walkNum
		getRead(auxillary[0][0],auxillary)
		newScore=evaluate()
		if newScore>oldScore:
			auxillary[x][y].move=walkNum
			score=newScore
		elif random.uniform(0,1)<math.exp((newScore-oldScore)/temp):
			auxillary[x][y].move=walkNum
			score=newScore
		else:
			auxillary[x][y].move=oldMove
		temp=temp*decayRate
		getRead(auxillary[0][0],auxillary)
	grid()
	return score

def genetic(popSize,generations):
    global auxillary
    population=numpy.empty((popSize),dtype=object)
    scores=numpy.zeros(popSize)
    avgScore=0
    for i in range(popSize): #initial population
        arr=numpy.empty((n,n),dtype=object)
        for x in range(n):
            for y in range(n):
                val=int(randint(1,max([n-x-1,x-1,n-y-1,y-1])))
                arr[y][x]=Node((x,y))
                arr[y][x].move=val
                arr[y][x].stepcount=-1
        arr[0][0].stepcount=0
        population[i]=arr
        getRead(arr[0][0],arr)
        scores[i]=population[i][n-1][n-1].stepcount
        bestVal=0
        bestIndex=0
    for k in range(generations):
        tempscores=[]
        selected=[]
        for i in range(popSize):
            tempscores.append(scores[i])
        for i in range(popSize):
            if scipy.stats.percentileofscore(tempscores,scores[i])>80:
                selected.append(population[i])
            elif random.uniform(0,100)<scipy.stats.percentileofscore(tempscores,scores[i]):
                selected.append(population[i])
        for x in range(popSize):
            if len(selected)==0:
		    selected.append(random.choice(population))
		    selected.append(random.choice(population))
            switch=random.uniform(0,n*n)
            puz1=random.choice(selected)
	    if random.uniform(0,1)>0.5:
		puz2=puz1
	    else:
		puz2=random.choice(selected)
            arr=numpy.empty((n,n),dtype=object)
            for i in range(n):
                for j in range(n):
                    arr[j][i]=Node((i,j))
                    population[x]=arr
            for i in range(n):
                for j in range(n):
                    population[x][i][j].move=puz1[i][j].move
                    population[x][i][j].pos=puz1[i][j].pos
                    population[x][i][j].stepcount=-1
                    if i*n+j>switch:
                        population[x][i][j].move=puz2[i][j].move
                        population[x][i][j].pos=puz2[i][j].pos
                        population[x][i][j].stepcount=-1
        for x in range(popSize-1): #mutate
            for i in range(n):
                for j in range(n):
                    if random.uniform(0,1)<0.02:
			    population[x][j][i].move=int(randint(1,max([n-i-1,i-1,n-j-1,j-1])))
			    population[x][j][i].stepcount=-1
        avgScore=0
        for i in range(popSize):
            getRead(population[i][0][0],population[i])
            scores[i]=population[i][n-1][n-1].stepcount
        for i in range(popSize):
            if scores[i]>bestVal:
                bestVal=scores[i]
                bestIndex=i
                getRead(population[bestIndex][0][0],population[bestIndex])
                auxillary=population[bestIndex]
    grid()



print "1)Print 2)Hill Climbing 3) Hill Climbing RR 4)Hill Climbing RW 5)Simulated Annealing 6)Genetic"
choice=int(raw_input())
if choice == 1:
	getRead(auxillary[0][0],auxillary)
	grid()
elif choice == 2:
	print "Enter iteration number:"
	it=int(raw_input())
	hillClimb(it)
elif choice == 3:
	print "Enter iteration number:"
	it=int(raw_input())
	print "Enter restart number:"
	rs=int(raw_input())
	hillRestart(rs,it)
elif choice == 4:
	print "Enter iteration number:"
	it=int(raw_input())
	print "Enter probability:"
	pr=float(raw_input())
	hillWalk(pr,it)
elif choice == 5:
	print "Enter iteration number:"
	it=int(raw_input())
	print "Enter temperature:"
	tp=int(raw_input())
	print "Enter tempreature decay rate:"
	dc=float(raw_input())
	simulatedAnnealing(tp,dc,it)
elif choice == 6:
	print "Enter iteration number:"
	it=int(raw_input())
	print "Enter population size:"
	sz=int(raw_input())
	genetic(sz,it)
else:
	print "Invalid option"
print("FINISHED");

while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
