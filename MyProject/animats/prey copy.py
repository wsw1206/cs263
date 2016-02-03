import sys
sys.path.append("..")

from environment.env import *
from QLearn import QLearn
from predator import Predator
import random

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

class Prey(Object):
	
	senserange = 80
	distinct = 10

	#actions = ['up', 'down', 'left','right', 'stroll', 'eat']
	actions = ['up', 'down', 'left', 'right', 'eat']
	def __init__(self, x=0, y=0, file='qlearn.txt'):
		Object.__init__(self, 'prey', x, y)
		self.qlearn = QLearn(Prey.actions)
		#self.origin = (self.x, self.y)
		self.dangerous = 0
		self.step = 4
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
		self.food = None
		self.fd = diag
		self.hawkxy = []
		self.hd = diag

	def tick(self, env):
		#qLearn.
		# initial reward for each step
		currentState  = self.getState(env)
		action = self.qlearn.chooseAction(currentState)
		dis = self.act(currentState, action, env)
		#print dis
		nextState = self.getState(env) #get the new state after performing actions
		reward = self.getReward(currentState, nextState, action, dis) #update energies and get the reward after performing action
		# if currentState>=7:
		# 	print currentState, action, reward, dis
		
		
		
		#print "Reward is:", reward
		if (currentState-6.5)*(nextState-6.5)>0:
			self.qlearn.learn(currentState, action, reward, nextState) #update the Q Table

	def act(self, state, action, env):
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
		if state <= 6:
			return self.fd - (abs(self.x-self.food.x) + abs(self.y-self.food.y))
		elif state <= 11:
			hd = 0
			for hawkxy in self.hawkxy:
				hd += (abs(self.x-hawkxy[0]) + abs(self.y-hawkxy[1]))
			return (self.hd - hd)
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
		if self.dangerous:
			r = Predator.senserange+Prey.distinct
			self.food = random.choice(env.food)
		else:
			r = Prey.senserange
		# r = Prey.senserange
		hawks = env.findall('hawk', (self.x, self.y), r)
		if len(hawks) != 0:
			self.hawkxy = []
			self.dangerous = 1
			if len(hawks) == 1:
				hawk = hawks[0]
				err = 0
				state = []
				if hawk.y + err <= self.y and hawk.x - err >= self.x:
					state += [7]  # 1 up right
				if hawk.y + err <= self.y and hawk.x + err <= self.x:
					state += [8]  # 2 up left
				if hawk.y - err >= self.y and hawk.x + err <= self.x:
					state += [9]  # 3 down left
				if hawk.y - err >= self.y and hawk.x - err >= self.x:
					state += [10] # 4 down right
				self.hawkxy.append((hawk.x, hawk.y))
				self.hd = abs(self.x-hawk.x) + abs(self.y-hawk.y)
				return random.choice(state)
			else:
				self.hd = 0
				for hawk in hawks:
					self.hawkxy.append((hawk.x, hawk.y))
					self.hd += (abs(self.x-hawk.x)+abs(self.y-hawk.y))
				return 11 # many hawks

		self.dangerous = 0
		food = env.find('food', (self.x, self.y), Prey.senserange)
		err = 10
		state = []
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
		self.fd = abs(self.x-self.food.x) + abs(self.y-self.food.y)
			
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

	def getReward(self, state, nstate, action, dis):
		#if state==6:
		reward = 0
		if action == 'eat':
			reward -= 25
			if state == 5:
				reward += 125
		if state<=4:   # for food 
			if dis<=0: # <=0 further
				reward -= 10
		elif state == 6:
			if dis>0:
				reward += int(random.random()*2)*10
		elif state<=11 and state>=7: # for hawk
			#reward 
			if dis<0: # <=0 further
				reward += 20
			else:
				reward -= 40

		if self.dumbed:
			reward -= 100

		if state<=6 and nstate>6:
			print state
			reward -= 300

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
			food = env.find('food', (self.x, self.y), Prey.senserange)
			env.remove(food)

#if __name__ == "__main__":
#	p = Prey()

#	print p.x