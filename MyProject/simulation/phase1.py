#!/usr/bin/python
# import animats
import sys
sys.path.append("..")

from environment.env import *
from animats.prey import Prey
from animats.predator import Predator
import pygame
import math
import time
import csv
import random

class Simulator:
  def __init__(self):
    # initialize pygame
    self.env = Environment()
    #self.animat = []
    ########
    for i in range(40):
      self.env.prey.append(Prey())
    for i in range(10):
      self.env.prey.append(Prey('aa'))

    for i in range(1):
      self.env.hawk.append(Predator('hawk'))

    for i in range(1):
      self.env.fox.append(Predator('fox'))

    fin = open('map.csv', 'rb')
    lines = csv.reader(fin)

    for line in lines:
      if line[0]=='1':
        self.env.bush.append(Shelter('bush', int(line[1]), int(line[2])))
      if line[0]=='2':
        self.env.bush.append(Shelter('hole', int(line[1]), int(line[2])))
      if line[0]=='3':
        self.env.bush.append(Shelter('tree', int(line[1]), int(line[2])))

    fin.close()

    # self.env.add('food', 400, 307)
    # self.env.add('food', 400, 305)
    # self.env.add('food', 400, 310)
    # self.env.add('food', 395, 307)
    #for i in range(10):
    #  self.env.add('food')
    # self.env.add('food', 400, 306)
    # self.env.add('food', 400, 305)
    # self.env.add('food', 400, 304)
    # self.env.add('food', 400, 303)
    # self.env.add('food', 400, 302)
    # self.env.add('food', 400, 301)
    #self.env.add('food', 400, 302)
    #self.env.add('food')
    #self.env.add('food')
    #print len(self.objects)
    # initialize the screen

  def update(self):
    #self.env.update()
    while len(self.env.food) <= 20:
      self.env.add('food')
    for prey in self.env.prey:
      prey.tick(self.env)

    for predator in (self.env.hawk+self.env.fox+self.env.snake):
      predator.tick(self.env)

    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()



    # repaint

if __name__ == "__main__":
  # (width, height, num_animats),  picture maximum size is 800x600
  simulation = Simulator()

  # # try to add slider and button
  # master = Tk()
  # Button(master, text='Show', command=show_values).pack()
  # # w = Scale(master, from_=0, to=42)
  # # w.pack()
  # w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
  # w.pack()
  #c = pygame.time.Clock()

  fout = open('phase1.csv', 'wb')
  spamwriter = csv.writer(fout, dialect='excel')
  spamwriter.writerow(['tick', 'prey', 'energy'])
  i = 1
  k = 0
  N = 30
  while i<5000: # main loop
    simulation.update()
    n = len(simulation.env.prey)
    
    
    # n0 = 0
    # n1 = 0
    # for prey in simulation.env.prey:
    #   if prey.gen == 'AA':
    #     n0 += 1
    #   else:
    #     n1 += 1
    #     if random.random() < 0.005:
    #       k += 1
    # #print n0, n1    
    # spamwriter.writerow([str(n0), str(n1)])

    e = 0

    for prey in simulation.env.prey:
      e += prey.energy
    if e != 0:
      e /= len(simulation.env.prey)
    spamwriter.writerow([str(i), str(n), str(e)])

    # for prey in simulation.env.prey:
    #   spamwriter.writerow([str(prey.x), str(prey.y)])

    
    i += 1
    # if i == 1000:
    #   for j in range(3):
    #     simulation.env.snake.append(Predator('snake'))

    for j in range(n):
      if random.random() < 0.0022:
        k += 1
        
    while k>2:
      simulation.env.prey.append(Prey('aa'))
      print 'add', i
      k -= 2


  print 'Finished'
  fout.close()
  
  

    #pygame.time.delay(100)
  #print 12321



    #pygame.time.wait(1000)

