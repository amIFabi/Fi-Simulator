import numpy as np, matplotlib.pyplot as plt, copy, math
from Bitstring import *
from Simulation import *

class Analysis:

	eca = ECA()
	dfctPos = 0
	strLength = 16
	dens = np.zeros(8, dtype=np.uint)
	dmgRad = np.zeros(2, dtype=np.uint)
	ttrow = [1]
	lyapExp = np.zeros(8, dtype=np.double)
	strProb = np.zeros((2 ** strLength), dtype=float)

	def __init__(self, dfctPos=0, strLength=16, eca=ECA()):
		self.dfctPos = dfctPos
		self.strLength = strLength
		self.eca = copy.deepcopy(eca)
		self.dens = np.zeros(eca.x.length, dtype=np.uint)
		self.lyapExp = np.zeros(eca.x.length, dtype=np.double)

	def simAnalysis(self, sim1=Simulation(), sim2=Simulation()):
		totalStr = sim1.xn.length - self.strLength
		entropy = np.zeros(sim1.steps, dtype=np.double)
		
		for i in range(sim1.steps):
			self.ttrow = copy.deepcopy(self.getTrinomialRow(self.ttrow))
			self.countDefects(sim1.xn, sim2.xn)
			entropy[i] = self.getEntropy(totalStr, sim1.xn)
			sim2.stepForward(i, sim1.xn)
			sim1.stepForward(i)
		
		sim1.saveToPNG(fileName="SimAnalysis.png")
		sim2.saveToPNG(fileName="SimDefects.png")
		self.getLyapunovExp(sim2.steps)

		plt.figure("Density")
		plt.plot(self.dens, "m,-")
		plt.savefig("../sim/SimDensity.png")
		plt.clf()
		plt.figure("Lyapunov exponents")
		plt.plot(self.ttrow, "m,-")
		plt.savefig("../sim/LyapunovExp.png")
		plt.clf()
		plt.figure("Entropy")
		plt.plot(entropy, "m,-")
		plt.savefig("../sim/Entropy.png")
		plt.clf()

	def ruleAnalysis(self):
		pass

	def setDefect(self):
		x = copy.deepcopy(self.eca.x)
		x.bits[self.dfctPos] = not(self.eca.x.bits[self.dfctPos])
		
		return x

	def getConeRadius(self, y, t, tp):
		self.dmgRad[0] = self.dfctPos
		self.dmgRad[1] = self.dfctPos
		if(y > 0):
			i = 0
			while(i < self.dfctPos):
				if(t.bits[i] ^ tp.bits[i]):
					self.dmgRad[0] = i
					break
				else:
					i += 1
			i = t.length - 1
			while(i > self.dfctPos):
				if(t.bits[i] ^ tp.bits[i]):
					self.dmgRad[1] = i
					break
				else:
					i -= 1
			if((self.dmgRad[1] - self.dmgRad[0]) > (2 * y)):
				self.dmgRad[0] = self.dfctPos

	def getDensity(self, xn):
		n = 0
		for i in range(xn.length):
			if(xn.bits[i]):
				n += 1
		
		return n

	def countDefects(self, t, tp):
		if (self.dmgRad[0] == self.dmgRad[1]):
			self.lyapExp[self.dfctPos] += 1.0
		else:
			for x in range(self.dmgRad[0], int(self.dmgRad[1] + 1)):
				if(t.bits[x] ^ tp.bits[x]):
					self.lyapExp[x] += 1.0

	def getEntropy(self, totalStr, xn):
		string = Bitstring(self.strLength)
		theta = 0.0
		entropy = 0.0
		for i in range(totalStr):
			k = i
			for j in range(self.strLength):
				string.bits[j] = xn.bits[k]
				k += 1
			n = string.binToInt()
			self.strProb[n] += 1.0
		
		for i in range(len(self.strProb)):
			if(self.strProb[i]):
				theta += 1.0
			
		if(theta):
			entropy=((1.0 / self.strLength) * math.log(theta, 2))
		
		return entropy

	#def getTrinomialRow(self, kn, prev=np.ones(1, dtype=np.uint)):
		#if(len(prev) == 1):
		#	return np.ones(3, dtype=np.uint)
		#else:
		#	current = np.ones((len(prev) + 2), dtype=np.uint)
		#	currentmid = len(current) // 2
		#	prevmid=len(prev) // 2
		#	for i in range(kn):
		#		pointer1 = prevmid - i
		#		pointer2 = prevmid + i
		#		if(pointer1 == pointer2):
		#			current[currentmid] = prev[prevmid - 1] + prev[prevmid] + prev[prevmid + 1]
		#		else:
		#			if((pointer1 - 1) >= 0):
		#				current[currentmid - i] = prev[prevmid - i - 1] + prev[prevmid - i] + prev[prevmid - i + 1]
		#				current[currentmid + i] = current[currentmid - i]
		#			else:
		#				current[currentmid - i] = prev[prevmid - i] + prev[prevmid - i + 1]
		#				current[currentmid + i] = current[currentmid - i]
		#	return current

	def getTrinomialRow(self, n):
		if(len(n) == 1):
			n.append(1)
			
			return n
		else:
			nt = []
			nt.append((n[0] +  (n[1] * 2)))
			for i in range(1, (len(n))):
				if(i != (len(n) - 1)):
					k = n[i - 1] + n[i] + n[i + 1]
				else:
					k = n[i - 1] + n[i]	
				nt.append(k)
			nt.append(1)

			return nt

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.lyapExp[i] > 0):
				self.lyapExp[i] = (1 / t) * (math.log(self.lyapExp[i]))

"""
a = Analysis()
n = [1]
for i in range(256):
	print(n)
	n = copy.deepcopy(a.getTrinomialRow(n))
"""