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

class Simulator:
  def __init__(self):
    # initialize pygame
    pygame.init()
    ###################
    self.env = Environment()
    #self.animat = []
    ########
    for i in range(10):
      self.env.prey.append(Prey())

    for i in range(20):
      self.env.snake.append(Predator('snake'))
    # for i in range(3):
    #   self.env.hawk.append(Predator('hawk'))
    # for i in range(3):
    #   self.env.fox.append(Predator('fox'))

    # fin = open('map.csv', 'rb')
    # lines = csv.reader(fin)
    # fout = open('map.csv', 'wb')
    # spamwriter = csv.writer(fout, dialect='excel')

    # for line in lines:
    #   if line[0]=='1':
    #     self.env.bush.append(Shelter('bush', int(line[1]), int(line[2])))
    #   if line[0]=='2':
    #     self.env.bush.append(Shelter('hole', int(line[1]), int(line[2])))
    #   if line[0]=='3':
    #     self.env.bush.append(Shelter('tree', int(line[1]), int(line[2])))
    # for i in range(15):
    #   self.env.bush.append(Shelter('bush'))
    #   #spamwriter.writerow(['1', str(self.env.bush[-1].x), str(self.env.bush[-1].y)])

    # for i in range(15):
    #   self.env.hole.append(Shelter('hole'))
    #   #spamwriter.writerow(['2', str(self.env.hole[-1].x), str(self.env.hole[-1].y)])

    # for i in range(15):
    #   self.env.tree.append(Shelter('tree'))
      #spamwriter.writerow(['3', str(self.env.tree[-1].x), str(self.env.tree[-1].y)])

    # fout.close()
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
    frame = 20 # side length
    self.size = width+frame, height+frame
    self.screen = pygame.display.set_mode(self.size)
    self.screenWidth = width+frame
    self.screenHeight = height+frame

    # set the name of display windows
    pygame.display.set_caption('CS263C project')

    #initialize sprites
    self.bg = pygame.image.load("../resources/bg.jpg")
    
    # pictures resources for Yao-Jen
    self.prey = pygame.image.load("../resources/prey.png")

    # self.hawk = pygame.image.load("../resources/hawk.gif")
    # self.fox  = pygame.image.load("../resources/fox.png")
    self.snake = pygame.image.load("../resources/snake.png")

    # self.bush =  pygame.image.load("../resources/bush.png")
    # self.hole =  pygame.image.load("../resources/hole.png")
    # self.tree =  pygame.image.load("../resources/tree.png")

    self.food = pygame.image.load("../resources/nut.png")


    # modify pictures to appropriate sizes
    self.prey          = pygame.transform.scale(self.prey, (28,28))
    # self.hawk          = pygame.transform.scale(self.hawk, (40,40))
    # self.fox           = pygame.transform.scale(self.fox, (40,40))
    self.snake         = pygame.transform.scale(self.snake, (40,40))

    # self.bush          = pygame.transform.scale(self.bush, (55,55))
    # self.hole          = pygame.transform.scale(self.hole, (30,20))
    # self.tree          = pygame.transform.scale(self.tree, (55,55))

    self.bg            = pygame.transform.scale(self.bg, (self.screenWidth, self.screenHeight))
    self.food          = pygame.transform.scale(self.food, (20,20))


    # initialize the model
    # self.env = animats.Environment(num_animats, width, height)
  def draw(self, obj):
    if obj.name == 'prey':
      #print obj.x, obj.y
      #self.screen.blit(pygame.transform.rotate(self.prey, obj.direct), (obj.x,obj.y))
      self.screen.blit(self.prey, (obj.x-14,obj.y-14))
      pygame.draw.circle(self.screen, (0,255,255), [obj.x, obj.y], Prey.senserange, 1)

      pygame.draw.circle(self.screen, (0,0,0), [obj.target.x, obj.target.y], 10, 4)

    # if obj.name == 'hawk':
    #   self.screen.blit(self.hawk, (obj.x,obj.y))
    #   pygame.draw.circle(self.screen, (255,0,0), [obj.x+20, obj.y+20], obj.senserange, 1)
    # if obj.name == 'fox':
    #   self.screen.blit(self.fox, (obj.x,obj.y))
    #   pygame.draw.circle(self.screen, (255,0,0), [obj.x+20, obj.y+20], obj.senserange, 1)
    if obj.name == 'snake':
      self.screen.blit(self.snake, (obj.x,obj.y))
      pygame.draw.circle(self.screen, (255,0,0), [obj.x+20, obj.y+20], obj.senserange, 1)


    # if obj.name == 'bush':
    #   self.screen.blit(self.bush, (obj.x-27,obj.y-27))
    # if obj.name == 'hole':
    #   self.screen.blit(self.hole, (obj.x-15,obj.y-10))
    # if obj.name == 'tree':
    #   self.screen.blit(self.tree, (obj.x-27,obj.y-27))
      #pygame.draw.circle(self.screen, (255,0,0), [obj.x, obj.y], 5, 1)

    if obj.name == 'food':
      self.screen.blit(self.food, (obj.x,obj.y))

  def update(self):
    #self.env.update()
    while len(self.env.food) <= 60:
      self.env.add('food')

    while len(self.env.prey) <= 10:
      self.env.prey.append(Prey())


    for prey in self.env.prey:
      prey.tick(self.env)
      

    for predator in (self.env.hawk+self.env.fox+self.env.snake):
      predator.tick(self.env)

    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()
    self.screen.blit(self.bg, (0,0))

    for prey in self.env.prey:
      self.draw(prey)
    for food in self.env.food:
      self.draw(food)
   
    for predator in (self.env.hawk+self.env.fox+self.env.snake):
      self.draw(predator)

    for shelter in (self.env.bush+self.env.hole+self.env.tree):
      self.draw(shelter)

    # repaint
    
    pygame.display.flip()

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

  while 1: # main loop
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT:
        if len(simulation.env.prey)>0:
          fout = open('qlearn.txt', 'w')
          dict = simulation.env.prey[0].qlearn.q
          num = 0
          for i in range(1,12):
            for (k,v) in  dict.items():
              if k[0]==i:
                fout.write(str(k[0]))
                fout.write(' ')
                fout.write(str(k[1]))
                fout.write(' ')
                fout.write(str(v))
                fout.write('\n')
                num += 1
            #fout.writ('12312')
          fout.close()
          print num
        pygame.quit()
        sys.exit()
    simulation.update()
    #pygame.time.delay(100)
  #print 12321



    #pygame.time.wait(1000)

