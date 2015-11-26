
import sys
sys.path.append("..")

from environment.env import *
from QLearn import QLearn
from predator import Predator
import random
import time

	# Possible states
	# sensed food only
	# sensed hawk
	
	# Possible actions
	# 1. up
	# 2. down
	# 3. left
	# 4. right
	# 5. stroll
	# 6. eat

	# escape
	# explore
	# eat
	# hide
	# forage
	
	#numStates = 11;
	#numActions = 8;
	
	# table = zeros((2**numStates,numActions));
	# also called "self.q" here

class Prey2(Object):

	knowsnake = 0
	
	senserange = 20
	distinct = 10

	#actions = ['up', 'down', 'left','right', 'stroll', 'eat']
	actions = ['up', 'down', 'left', 'right', 'eat', 'stay']

	def __init__(self, gen = 'AA', x=0, y=0 , file='qlearn.txt'):
		Object.__init__(self, 'prey2', x, y)
		self.qlearn = QLearn(Prey2.actions)
		#self.origin = (self.x, self.y)
		self.step = 4
		self.gen = gen
		self.dumbed = 0
		fin = open(file, 'r')
		lines = fin.readlines()
		for line in lines:
			content = line.split()
			state = int(content[0])
			action = content[1]
			value = float(content[2])
			self.qlearn.setQ(state, action, value)
			#print content
		# self.qlearn.setQ(1, 'up', 10)
		# self.qlearn.setQ(2, 'down', 10)
		# self.qlearn.setQ(3, 'left', 10)
		# self.qlearn.setQ(4, 'right', 10)
		# self.qlearn.setQ(5, 'eat', 10)
		# self.qlearn.setQ(6, 'stroll', 1000)
		self.target = None
		self.fd = diag
		self.hawkxy = []
		self.hd = diag
		self.energy = 70

		
	
	def tick(self, env):
		#qLearn.
		# initial reward for each step
		self.init()
		currentState  = self.getState(env)
		action = self.qlearn.chooseAction(currentState)
		self.act(currentState, action, env)
		#print dis
		nextState = self.getState(env) #get the new state after performing actions
		reward = self.getReward(currentState, nextState, action) #update energies and get the reward after performing action
#		print currentState, action, reward
		# 	#time.sleep(1)
		
		
		
		#print "Reward is:", reward
		self.qlearn.learn(currentState, action, reward, nextState) #update the Q Table

	def init(self):
		self.hawk = None
		self.reward = 0
		self.pdis = 0
		self.safe = []
		self.escape = 0

	def act(self, state, action, env):
		self.energy -= 1

		if self.energy >= 70:
			env.prey2.append(Prey2())
			

		if self.energy <= 0:
			env.prey2.remove(self)
			print 'die from food'
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
		if action == 'stroll':		
			if self.target not in env.food:
				self.target = random.choice(env.food)
			food = self.target

			self.x += 2 * (step * (random.random()-0.5))
			self.y += 2 * (step * (random.random()-0.5))
			
			x = abs(self.x - food.x)
			y = abs(self.y - food.y)
			t = max(x,y)
			self.x = int((t*self.x + 2*food.x) / (t+2.0))
			self.y = int((t*self.y + 2*food.y) / (t+2.0))
			
			# print 'stroll', food.x, food.y
		self.adjustxy()
		if action == 'eat':
			self.eat(state, env)
		#print self.x, self.y
		#print action
	
		dis = abs(self.x-self.target.x) + abs(self.y-self.target.y)
		self.reward = self.fdis - dis

	def adjustxy(self):
		self.dumbed = 0
		if self.x < 0:
			self.x = 0
			self.dumbed = 1
		elif self.x > width:
			self.x = width
			self.dumbed = 1
		if self.y < 0:
			self.y = 0
			self.dumbed = 1
		elif self.y > height:
			self.y = height
			self.dumbed = 1

	def getState(self, env):
		err = self.step-1
		# check existence of predator 
		hawks = env.findall('hawk', (self.x, self.y), Prey2.senserange)
		foxes = env.findall('fox', (self.x, self.y), Prey2.senserange)
		snakes = env.findall('snake', (self.x, self.y), Prey2.senserange)

		predators = hawks+foxes
		type = ['hawk']*min(1,len(hawks)) + ['fox']*min(1,len(foxes))

		if Prey2.knowsnake > random.random():
			predators += snakes
			type += ['snake']*min(1,len(snakes))

		if snakes != []:
			Prey2.knowsnake += 0.001
			Prey2.knowsnake = min(1.5, Prey2.knowsnake)
		
		if predators != []:
			self.escape = 1
			x = 0
			y = 0
			for predator in predators:
				x += predator.x
				y += predator.y
			x /= len(predators)
			y /= len(predators)
			nearest = env.find('predator', (self.x, self.y), Prey2.senserange)
			shelter = env.findshelter(type, (self.x, self.y), (x,y), Prey2.senserange)
			if shelter!=None:
				self.target = shelter
	
			else:
				# diffx = x - self.x
				# diffy = y - self.y
				x = 3*self.x-2*x
				y = 3*self.y-2*y

				if x < 0:
					if y < 0:
						x, y = -y, -x
					elif y > height:
						x, y = y-height, height+x
					elif y <= height/2:
						x, y = 0, y+Prey2.senserange
					else:
						x, y = 0, y-Prey2.senserange
				elif x > width:
					if y < 0:
						x, y = -y, x-width
					elif y > height:
						x, y = width+height-y, width+height-x
					elif y <= height/2:
						x, y = width, y+Prey2.senserange
					else:
						x, y = width, y-Prey2.senserange
				elif x < width/2:
					if y < 0:
						x, y = x+Prey2.senserange, 0
					elif y > height:
						x, y = x+Prey2.senserange, height
				else:
					if y < 0:
						x, y = x-Prey2.senserange, 0
					elif y > height:
						x, y = x-Prey2.senserange, height
				
				self.target = Object(x, y)

		else:
			food = env.findall('food', (self.x, self.y), Prey2.senserange)
			if len(food)==0:
				food = None
			elif self.target not in food:
				food = random.choice(food)
			else:
				food = self.target

			if food!=None:
				self.target = food
			if self.escape == 0 and self.target!=None:
		 		if abs(self.target.y-self.y) <= err and abs(self.target.x-self.x) <= err:
		 			self.target = food

		# food = env.find('food', (self.x, self.y), Prey.senserange)
		# if food!=None:
		# 	self.target = food

		target = self.target

		state = []
		if target != None:
			if target.y + err < self.y:
				state += [1] * (abs(target.y - self.y) * int(10*random.random()+1)) # up
			if target.y - err > self.y:
				state += [2] * (abs(target.y - self.y) * int(10*random.random()+1)) # down
			if target.x + err < self.x:
				state += [3] * (abs(target.x - self.x) * int(10*random.random()+1))# left
			if target.x - err > self.x:
				state += [4] * (abs(target.x - self.x) * int(10*random.random()+1))# right
			if abs(target.y-self.y) <= err and abs(target.x-self.x) <= err:
				if target in (env.bush+env.hole+env.tree):
					state.append(6) # on
					self.safe = target.shield
				else:
					state.append(5) # on
			# food = env.find('food', (self.x, self.y), Prey.senserange)
			# if food!=None:
			# 	self.target = food
			# else:
			# 	if self.target == None:
			# 		self.target = random.choice(env.food)
			# 	if self.target not in env.food and random.random()<0.05:
			# 		self.target = random.choice(env.food)
		else:
			state.append(6) # nothing	
			if (self.target == None or self.target not in env.food):
				self.target = random.choice(env.food)

			 	

		self.fdis = abs(self.x-self.target.x) + abs(self.y-self.target.y)
			
		# 	if abs(food.x-self.x)<=err and abs(food.y-self.y)<=err:
		# 		state = 5
		# 	else:
		# 		if food.y <= self.y and food.x >= self.x:
		# 			state = 1 # quadrant 1
		# 		elif food.y <= self.y and food.x <= self.x:
		# 			state = 2 # quadrant 2
		# 		elif food.x < self.x and food.y > self.y:
		# 			state = 3 # quadrant 3
		# 		#elif food.x > self.x and food.y > self.y:
		# 		else:
		# 			state = 4 # quadrant 4
		# 			print state
		# else:
		# 	state = 6 # nothing
			#print state
		#print state
		#print state
		#food = env.find('food', (self.x, self.y), diag)
		return random.choice(state)

	def getReward(self, state, nstate, action):
		#if state==6:

		reward = self.reward

		if self.safe != [] and self.escape == 1:
			reward += 100

		if action == 'eat':
			reward -= 25
			if state == 5:
				reward += 125
		# if state<=4:   # for food 
		# 	if dis<=0: # <=0 further
		# 		reward -= 10
		# elif state == 6:
		# 	if dis>0:
		# 		reward += int(random.random()*2)*10
		# elif state<=11 and state>=7: # for hawk
		# 	#reward 
		# 	if dis<0: # <=0 further
		# 		reward += 20
		# 	else:
		# 		reward -= 40

		if self.dumbed:
			reward -= 100

		# if state<=6 and nstate>6:
		# 	print state
		# 	reward -= 300

		return reward
		# if action == 'eat':
		# 	if state == 5:
		# 		return 100
		# 	else:
		# 		return -100
		# else:
		# 	return 0
	#	if state==6 and nextstate != 6:
	#		self.reward += 0
		#self.reward -= 1;
		# else:
		# 	return -10

	def eat(self, state, env):
		if state==5:
			# print 'eating'
			food = env.find('food', (self.x, self.y), Prey2.senserange)
			if food!=None:
				self.energy += 15
				self.energy = min(self.energy, 100)
				env.remove(food)

#if __name__ == "__main__":
#	p = Prey()

#	print p.x