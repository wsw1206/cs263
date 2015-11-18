import sys
sys.path.append("..")

from environment.env import *
from ffn import FFN
import random

class Predator(Object):

	senserange = 80

	def __init__(self, type, x=0, y=0):
		Object.__init__(self, type, x, y)
		self.brain = FFN()
		self.step = 4
		#print self.x, self.y
		self.stroll = [random.choice(['up', 'down', 'left', 'right'])]

	def tick(self, env):
		params = self.sense(env)
		result = self.brain.act(params)
		if params[5] == 1:
			if len(self.stroll)>=2:
				self.act(self.stroll[-1], env)
				self.stroll.pop()
			else:
				action = ['up', 'down', 'left', 'right']
				re = ['down', 'up', 'right', 'left']
				del action[re.index(self.stroll[0])]
				self.stroll = [action[random.randrange(0,3)]]*random.randrange(50,100)
			return
		action = self.choseaction(result, env)
		#if action == 'eat':
			#print params, result, action
		self.act(action, env)

	def sense(self, env):
		prey = env.find('prey', (self.x, self.y), Predator.senserange)
		err = 2
		result = [0, 0, 0, 0, 0, 0]
		if prey != None and self.name not in prey.safe:
			if abs(prey.y-self.y) <= err and abs(prey.x-self.x) <= err:
				result[4] += 1 # on
			else:
				if prey.y + err < self.y:
					result[0] += 1 # up
				if prey.y - err > self.y:
					result[1] += 1 # down
				if prey.x + err < self.x:
					result[2] += 1 # left
				if prey.x - err > self.x:
					result[3] += 1 # right
		else:
			result[5] += 1 # nothing	
		return result

	def choseaction(self, result, env):
		actions = ['up', 'down', 'left', 'right', 'eat']
		maxr = max(result)
		list = []
		for i in range(len(result)):
			if result[i] > (maxr*0.8):
				list.append(i)
		if len(list)==4:
			#list = list * 2
			prey = env.find('prey', (self.x, self.y), diag)
			if prey != None and self.name not in prey.safe:
				if prey.y  < self.y:
					list += [0]*5
				if prey.y  > self.y:
					list += [1]*5
				if prey.x  < self.x:
					list += [2]*5
				if prey.x  > self.x:
					list += [3]*5
		return actions[random.choice(list)]

	def act(self, action, env):
		step = self.step
		#if state == 6:
		#	step = Prey.foodrange
		if action == 'up':
			self.y = self.y-step
		if action == 'down':
			self.y = self.y+step
		if action == 'left':
			self.x = self.x-step
		if action == 'right':
			self.x = self.x+step
		self.adjustxy()
		if action == 'eat':
			self.eat(env)
		#print self.x, self.y
		#print action

	def adjustxy(self):
		constrain = 0
		if self.x < constrain:
			self.x = constrain
			self.stroll = ['right']*2
		if self.x > width-constrain:
			self.x = width-constrain
			self.stroll = ['left']*2
		if self.y < constrain:
			self.y = constrain
			self.stroll = ['down']*2
		if self.y > height-constrain:
			self.y = height-constrain
			self.stroll = ['up']*2

	def eat(self, env):
		prey = env.find('prey', (self.x, self.y), Predator.senserange)
		if prey!=None:
			if self.name != 'snake':
				env.prey.remove(prey)
			elif random.random()>0.5:
				env.prey.remove(prey)
			else:
				print 'half escape'
			# env.remove(prey)
			
			# learning
		#else :
			#print 'Eat False'





