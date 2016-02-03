
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

class Prey(Object):
	
	senserange = 80
	distinct = 10

	#actions = ['up', 'down', 'left','right', 'stroll', 'eat']
	actions = ['up', 'down', 'left', 'right', 'eat', 'stay']
	def __init__(self, x=0, y=0, file='qlearn.txt'):
		Object.__init__(self, 'prey', x, y)
		self.qlearn = QLearn(Prey.actions)
		#self.origin = (self.x, self.y)
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
		self.target = None
		self.fd = diag
		self.hawkxy = []
		self.hd = diag

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
		if currentState==11:
		 	print currentState, action, reward
		# 	#time.sleep(1)
		
		
		
		#print "Reward is:", reward
		self.qlearn.learn(currentState, action, reward, nextState) #update the Q Table

	def init(self):
		self.hawk = None
		self.reward = 0
		self.pdis = 0
		self.safe = 0

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
		if self.pdis != 0:
			hawk = self.hawk
			diffx = hawk.x - self.x
			diffy = hawk.y - self.y
			dis = (abs(diffx)+abs(diffy))
			self.reward = dis - self.pdis
		else:
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
		
		hawk = env.find('hawk', (self.x, self.y), Prey.senserange)
		if hawk!=None:
			err = 10
			shelter = env.find('hawkshelter', (self.x, self.y), Prey.senserange)
			if shelter!=None and abs(shelter.y-self.y) <= err and abs(shelter.x-self.x) <= err:
				self.safe = 1
				return 11 # right shelter

			self.hawk = hawk
			state = []
			diffx = hawk.x - self.x
			diffy = hawk.y - self.y
			x = self.x-2*diffx
			y = self.y-2*diffy

			if x < 0:
				x = 0
			elif x > width:
				x = width
			if y < 0:
				y = 0
			elif y > height:
				y = height

			self.target = Food(x, y)
			#print self.target.x, self.target.y
				# 7 8 9 10  ## coordinate 1 2 3 4
			err = 5
			if diffy < -err:
				state += [7]
			if diffy > err:
				state += [8]
			if diffx < -err:
				state += [9]
			if diffx > err:
				state += [10]
			self.pdis += (abs(diffx)+abs(diffy))
			#print state
			if state==[]:
				state = [7,8,9,10]
			return random.choice(state)


		err = 10
		food = env.find('food', (self.x, self.y), diag)
		if self.target == None:
			 self.target = food
		if self.target not in env.food:
			if abs(self.target.y-self.y) <= err and abs(self.target.x-self.x) <= err:
				self.target = random.choice(env.food)

		food = env.find('food', (self.x, self.y), Prey.senserange)
		if food!=None:
			self.target = food

		food = self.target

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
			if self.target == None:
				self.target = random.choice(env.food)
			if self.target not in env.food and random.random()<0.05:
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

		if self.safe == 1:
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
			food = env.find('food', (self.x, self.y), Prey.senserange)
			if food!=None:
				env.remove(food)

#if __name__ == "__main__":
#	p = Prey()

#	print p.x