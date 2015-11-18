#!/usr/bin/env python
import sys
sys.path.append("..")

from environment.env import width, height
import random

class Object:
	def __init__(self, name, x=0, y=0):
		self.name = name
		if x==0 and y==0:
			self.x = int(random.random()*width);
			self.y = int(random.random()*height);
		else:
			self.x = x
			self.y = y
		print self.x, self.y