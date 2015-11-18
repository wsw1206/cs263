from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
 
from pybrain.tools.shortcuts import buildNetwork
import pickle
 
#Define network structure
class FFN():
	def __init__(self):
		#self.network = FeedForwardNetwork(name="Predator")
		fileObject = open('ffn.txt','r')
		self.network = pickle.load(fileObject)
		inputLayer = LinearLayer(6, name="Input")
		hiddenLayer = SigmoidLayer(6, name="Hidden")
		outputLayer = LinearLayer(5, name="Output")
	 
	# 	self.network.addInputModule(inputLayer)
	# 	self.network.addModule(hiddenLayer)
	# 	self.network.addOutputModule(outputLayer)
	 
	# 	c1 = FullConnection(inputLayer, hiddenLayer, name="Input_to_Hidden")
	# 	c2 = FullConnection(hiddenLayer, outputLayer, name="Hidden_to_Output")
	# #c3 = FullConnection(hiddenLayer, hiddenLayer, name="Recurrent_Connection")
	 
	# 	self.network.addConnection(c1)
	# #network.addRecurrentConnection(c3)
	# 	self.network.addConnection(c2)
	# 	self.network.sortModules()
	 
	#Add a data set
		ds = SupervisedDataSet(6,5)
	 
	#Up/Right
		ds.addSample([1,0,0,1,0,0],[1,0,0,0,0])
		ds.addSample([1,0,0,1,0,0],[0,0,0,1,0])
	#Up/Left
		ds.addSample([1,0,1,0,0,0],[1,0,0,0,0])
		ds.addSample([1,0,1,0,0,0],[0,0,1,0,0])
	#Down/Left
		ds.addSample([0,1,1,0,0,0],[0,1,0,0,0])
		ds.addSample([0,1,1,0,0,0],[0,0,1,0,0])
	#Down/Right
		ds.addSample([0,1,0,1,0,0],[0,1,0,0,0])
		ds.addSample([0,1,0,1,0,0],[0,0,0,1,0])
	#Eat
		ds.addSample([0,0,0,0,1,0],[0,0,0,0,1])
	#Stroll
		ds.addSample([0,0,0,0,0,1],[1,0,0,0,0])
		ds.addSample([0,0,0,0,0,1],[0,1,0,0,0])
		ds.addSample([0,0,0,0,0,1],[0,0,1,0,0])
		ds.addSample([0,0,0,0,0,1],[0,0,0,1,0])
	 
	#Train the network
		trainer = BackpropTrainer(self.network, ds, momentum=0.99)
	 
		#print self.network
	 
		#print "\nInitial weights: ", self.network.params
	 
		max_error = 1e-7
		error, count = 1, 1000
		#Train
		# while abs(error) >= max_error and count > 0:
		# 	error = trainer.train()
		# 	count = count - 1
	 
		# print "Final weights: ", self.network.params
		# print "Error: ", error
	 
	#Test data
		#print '\nUp/Right:',self.network.activate([1,0,0,1,0,0])
		#print 'Up/Left:',self.network.activate([1,0,1,0,0,0])
		#print 'Down/Left:',self.network.activate([0,1,1,0,0,0])
		#print 'Down/Right:',self.network.activate([0,1,0,1,0,0])
		#print 'Eat:',self.network.activate([0,0,0,0,1,0])
		#print 'Stroll:',self.network.activate([0,0,0,0,0,1])

		fileObject = open('ffn.txt', 'w')
		pickle.dump(self.network, fileObject)
		fileObject.close()

	def act(self, params):
		return self.network.activate(params)

if __name__ == '__main__':
	a = FFN()
	result = a.act([1,0,0,1,0,0])
	result.sort()
	print result
	print len(result)
	#print result[0]


