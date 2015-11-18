import sys
sys.path.append("..")

from environment.env import *
from QLearn import QLearn
from predator import Predator
import random

	# Possible states
	# 1 food, up
	# 2 food, down
	# 3 food, left
	# 4 food, right
	# 5 food, on
	# 6 nothing
	
	# Possible actions
	# 1. up
	# 2. down
	# 3. left
	# 4. right
	# 5. stroll
	# 6. eat
	
	#numStates = 11;
	#numActions = 8;
	
	# table = zeros((2**numStates,numActions));
	# also called "self.q" here

class Prey(Object):
	
	senserange = 100
	distinct = 10

	#actions = ['up', 'down', 'left','right', 'stroll', 'eat']
	actions = ['up', 'down', 'left','right', 'stay', 'eat']
	def __init__(self, x=0, y=0, file='qlearn.txt'):
		Object.__init__(self, 'prey', x, y)
		self.qlearn = QLearn(Prey.actions)
		#self.origin = (self.x, self.y)
		self.dangerous = 0
		self.step = 4
		self.dumbed = 0
		self.lastact = None
		self.foodeaten = 0

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
		self.food = None
		self.fd = diag
		self.hawk = None
		self.hd = diag
		self.bush = None
		self.bd = diag
		self.hunger = 0

	def tick(self, env):
		#qLearn.
		# initial reward for each step
		currentState  = self.getState(env)
		action = self.qlearn.chooseAction(currentState)
		self.act(currentState, action, env)
		#print dis
		reward = self.getReward(currentState, action) #update energies and get the reward after performing action
		
		nextState = self.getState(env) #get the new state after performing actions
		print currentState, action, reward #self.hunger, (self.food.x, self.food.y)
		#if currentState>=7:
		#	print currentState, action, reward
		
		#print "Reward is:", reward
		self.qlearn.learn(currentState, action, reward, nextState) #update the Q Table

	def act(self, state, action, env):
		self.hunger += 1

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
			if self.food not in env.food:
				self.food = random.choice(env.food)
			food = self.food
			print food.x, food.y

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
		# if state <= 6:
		# 	return self.fd - (abs(self.x-self.food.x) + abs(self.y-self.food.y))
		# elif state <= 11:
		# 	hd = 0
		# 	for hawkxy in self.hawkxy:
		# 		hd += (abs(self.x-hawkxy[0]) + abs(self.y-hawkxy[1]))
		# 	return (self.hd - hd)
		#print self.x, self.y
		#print action

	def adjustxy(self):
		self.dumbed = 1
		if self.x < 0:
			self.x = 0
		elif self.x > width:
			self.x = width
		elif self.y < 0:
			self.y = 0
		elif self.y > height:
			self.y = height
		else:
			self.dumbed = 0

	def getState(self, env):
		self.bush = env.find('bush', (self.x, self.y), Prey.senserange)
		self.origin = (self.x, self.y)

		err = 0
		state = []

		hawk = env.find('hawk', (self.x, self.y), Prey.senserange)
		if hawk != None:
			xdiff = hawk.x - self.x
			ydiff = hawk.y - self.y

			if abs(xdiff)>=abs(ydiff):
				if xdiff > 0:
					return 10 # hawk on the right
				elif xdiff < 0:
					return 9 # on the left
				else:
					return random.choice([7,8,9,10])
			else:
				if ydiff > 0:
					return 8 # down
				else:
					return 7 # up

			# if hawk.y + err < self.y:
			# 	state += [7] * (100/(abs(hawk.y - self.y))) # up
			# if hawk.y - err > self.y:
			# 	state += [8] * (100/(abs(hawk.y - self.y))) # down
			# if hawk.x + err < self.x:
			# 	state += [9] * (100/(abs(hawk.x - self.x)))# left
			# if hawk.x - err > self.x:
			# 	state += [10] * (100/(abs(hawk.x - self.x)))# right
			# self.hawk = hawk
			# if len(state)==0:
			# 	state = [7,8,9,10]
			# return random.choice(state)

		err = 10
		self.dangerous = 0
		food = env.find('food', (self.x, self.y), diag)
		if food != None:
			if food.y + err < self.y:
				state += [1] * (abs(food.y - self.y) * int(10*random.random()+1)) # up
			if food.y - err > self.y:
				state += [2] * (abs(food.y - self.y) * int(10*random.random()+1)) # down
			if food.x + err < self.x:
				state += [3] * (abs(food.x - self.x) * int(10*random.random()+1))# left
			if food.x - err > self.x:
				state += [4] * (abs(food.x - self.x) * int(10*random.random()+1))# right
			if abs(food.y-self.y) <= err and abs(food.x-self.x) <= err:
				state.append(5) # on
			self.food = food
		else:
			state.append(6) # nothing
			if self.food not in env.food:
				self.food = random.choice(env.food)
			
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

	def getReward(self, state, action):
		#if state==6:
		reward = 0
		# energy consumption
		if action == 'eat':
			reward -= 10
		#elif action != 'stay':
		#	reward -= 1

		# getting hungry
		reward -= 5

		# food eaten
		if self.foodeaten == 1:
			reward += 110

		# food dis	
		if self.food != None:
			dis = abs(self.x-self.food.x)+abs(self.y-self.food.y)
			dis -= (abs(self.origin[0]-self.food.x)+abs(self.origin[1]-self.food.y))
			if state <= 6:
				if dis < 0:
					reward += 10

		if self.hawk == None and action == 'stay':
			reward -= 50
			
		# hawk dis
		if self.hawk != None:
			dis = max(abs(self.x-self.hawk.x), abs(self.y-self.hawk.y))
			dis -= max(abs(self.origin[0]-self.hawk.x), abs(self.origin[1]-self.hawk.y))
			if dis > 0:
				reward += 20
			else:
				dis = min(abs(self.x-self.hawk.x), abs(self.y-self.hawk.y))
				dis -= min(abs(self.origin[0]-self.hawk.x), abs(self.origin[1]-self.hawk.y))
				if dis > 0:
					reward += 10
				else:
					reward -= 50

		if self.dumbed:
			reward -= 200

		#if state<=6 and nstate>6:
		#	reward -= 1000

		# init for next tick
		self.foodeaten = 0
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
			self.foodeaten = 1
			# print 'eating'
			food = env.find('food', (self.x, self.y), Prey.senserange)
			env.remove(food)
			self.hunger -= 50
			self.hunger = max(0, self.hunger)

#if __name__ == "__main__":
#	p = Prey()

#	print p.x