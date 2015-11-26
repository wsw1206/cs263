import math
import random
width = 800;
height = 600;
diag = 1000;

class Object:
  def __init__(self, name, x=0, y=0):
    self.name = name
    if x==0 and y==0:
			self.setrandom()
    else:
			self.x = x
			self.y = y
    #print self.x, self.y
  def setrandom(self):
    self.x = int(random.random()*width)
    self.y = int(random.random()*height)

class Shelter(Object):
  def __init__(self, name, x=0, y=0):
    Object.__init__(self, name, x, y)
    if name == 'bush':
      self.shield = ['snake', 'hawk']
    if name == 'hole':
      self.shield = ['fox', 'hawk']
    if name == 'tree':
      self.shield = ['fox', 'snake']

class Food(Object):
	def __init__(self, x, y):
		Object.__init__(self, 'food', x, y)

class Environment:
  def __init__(self):  
    #self.map = {}
    self.food = []
    self.prey = []

    self.hawk = []
    self.fox = []
    self.snake = []

    self.bush = []
    self.hole = []
    self.tree = []

    self.prey2 = []

  def add(self, type, x=0, y=0):
  	if type == 'food':
  		newfood = Food(x, y)
  		self.food.append(newfood)

        
          


  def remove(self, obj):
    if obj.name == 'food':
      #print 'remove food'
      self.food.remove(obj)
    if obj.name == 'prey':
      print 'remove prey'
      self.prey.remove(obj)
    if obj.name == 'prey2':
      print 'remove prey2'
      self.prey2.remove(obj)


    #else:
  		#print 'dont have'
  		
  def find(self, type, center, range):
    if type == 'food':
  		list = self.food
    elif type == 'prey':
      list = self.prey
    elif type == 'hawk':
      list = self.hawk
    elif type == 'bush':
      list = self.bush
    elif type == 'predator':
      list = self.hawk+self.fox+self.snake
    elif type == 'prey2':
      list = self.prey2
    
    target = None
    pos = None
    min_d = math.sqrt(width**2+height**2)
    for obj in list:
  	  x = center[0]-obj.x
  	  y = center[1]-obj.y
  	  d =  math.sqrt(x**2+y**2)
  	  if d < min_d:
  			target = obj
  			min_d = d
    if min_d>range:
  		target = None
    return target

  def findall(self, type, center, range):
    if type == 'hawk':
      list = self.hawk
    if type == 'fox':
      list = self.fox
    if type == 'snake':
      list = self.snake
    if type == 'food':
      list = self.food

    target = []
    for obj in list:
      x = center[0]-obj.x
      y = center[1]-obj.y
      d =  math.sqrt(x**2+y**2)
      if d < range:
        target.append(obj)
    return target

  def findshelter(self, type, center, predator, range):
    if type == ['hawk']:
      list = self.bush+self.hole
    elif type == ['fox']:
      list = self.hole+self.tree
    elif type == ['snake']:
      list = self.bush+self.tree
    elif 'hawk' in type and 'fox' in type:
      list = self.hole
    elif 'hawk' in type and 'snake' in type:
      list = self.bush
    elif 'snake' in type and 'fox' in type:
      list = self.tree

    target = None
    min_d = width+height
    for obj in list:
      x = center[0]-obj.x
      y = center[1]-obj.y
      d1 =  abs(x)+abs(y)
      x = predator[0]-obj.x
      y = predator[1]-obj.y
      d2 =  abs(x)+abs(y)
      if d1 < min_d and d1*8 < d2*9:
        target = obj
        min_d = d1
    return target


    #return None
  