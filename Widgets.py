import gi, sys, copy, subprocess, os, pygame
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from pygame.locals import *
from ECA import ECA

class Widgets():
	"""
	Attributes
	----------
		cellColor : tuple
			RGB values to draw cells in state 1.
		bckgColor : tuple
			RGB values to draw background and cells in state 0.
		bckgGColor : tuple
			RGB values to draw background of the damage cone.
		defectColor : tuple
			RGB values to draw cells with state change.
		screen : pygame Surface
			Surface to draw simulations. 
	"""
	mainLayout = Gtk.Box(orientation=1)
	toolbarLayout = Gtk.Box(orientation=0)
	tabViewLayout = Gtk.Box(orientation=0, spacing=30)
	tab1Layout = Gtk.Box(orientation=1, spacing=30)
	tab2Layout = Gtk.Box(orientation=1, spacing=30)
	layout11 = Gtk.Box(orientation=0)
	layout12 = Gtk.Box(orientation=0)
	layout13 = Gtk.Box(orientation=0)
	layout21 = Gtk.Box(orientation=0)
	layout22 = Gtk.Box(orientation=0)
	toolbar = Gtk.Toolbar()
	tabView = Gtk.Notebook.new()
	adjRule = Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	entryRule = Gtk.SpinButton.new(adjRule, 1, 0)
	switchRandConf = Gtk.Switch.new()
	switchStr = Gtk.Switch.new()
	entrySeed = Gtk.Entry.new()
	entrySteps = Gtk.Entry.new()
	entryCells = Gtk.Entry.new()
	entryPer = Gtk.Entry.new()
	entryDefect = Gtk.Entry.new()
	entryStrLength = Gtk.Entry.new()
	switchRandValue = 0
	switchConfValue = 0
	simulationWindow = Gtk.Window.new(0)
	spinnerLayout = Gtk.Box(orientation=0)
	spinner = Gtk.Spinner()
	eca=ECA()
	#Pygame variables
	cellColor=(0, 0, 0)
	bckgColor=(255, 255, 255)
	bckgGColor=(160, 160, 160)
	defectColor=(255, 0, 0)
	screen=pygame.Surface((0, 0))
	
	def __init__(self):
		self.createToolbar()
		self.createTabView()
		self.toolbarLayout.pack_start(self.toolbar, 0, 0, 0)
		self.tabViewLayout.pack_start(self.tabView, 0, 0, 0)
		self.mainLayout.pack_start(self.toolbarLayout, 0, 0, 0)
		self.mainLayout.pack_start(self.tabViewLayout, 0, 0, 0)

	def createToolbar(self):
		imgExit=Gtk.Image.new_from_icon_name("application-exit", 0)
		imgLoad=Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave=Gtk.Image.new_from_icon_name("document-save-as", 0)
		imgRun=Gtk.Image.new_from_icon_name("media-playback-start", 0)
		imgAnalysis=Gtk.Image.new_from_icon_name("edit-find", 0)

		exitApp=Gtk.ToolButton.new(imgExit, "Exit")
		load=Gtk.ToolButton.new(imgLoad, "Load settings")
		save=Gtk.ToolButton.new(imgSave, "Save settings")
		run=Gtk.ToolButton.new(imgRun, "Run simulation")
		analysis=Gtk.ToolButton.new(imgAnalysis, "Run analysis")

		self.toolbar.insert(exitApp, -1)
		self.toolbar.insert(load, -1)
		self.toolbar.insert(save, -1)
		self.toolbar.insert(run, -1)
		self.toolbar.insert(analysis, -1)

		run.connect("clicked", self.runSimulation)
		analysis.connect("clicked", self.runAnalysis)

	def createTab1(self):
		labelRule=Gtk.Label.new("Rule: ")
		labelRandConf=Gtk.Label.new("Random configuration: ")
		labelConf=Gtk.Label.new("Seed: ")
		labelStr0=Gtk.Label.new("0")
		labelStr1=Gtk.Label.new("1")
		labelSteps=Gtk.Label.new("Steps: ")
		labelCells=Gtk.Label.new("Cells: ")
		labelDens=Gtk.Label.new("Density (%): ")

		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.entryPer.set_sensitive(False)
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		self.entryPer.set_width_chars(5)
		
		self.layout11.set_halign(0)
		self.layout12.set_halign(0)
		self.layout11.pack_start(labelRule, 1, 0, 10)
		self.layout11.pack_start(self.entryRule, 1, 0, 10)
		self.layout11.pack_start(labelRandConf, 1, 0, 10)
		self.layout11.pack_start(self.switchRandConf, 1, 0, 10)
		self.layout12.pack_start(labelConf, 1, 0, 10)
		self.layout12.pack_start(self.entrySeed, 1, 0, 10)
		self.layout12.pack_start(labelStr0, 1, 0, 5)
		self.layout12.pack_start(self.switchStr, 1, 0, 10)
		self.layout12.pack_start(labelStr1, 1, 0, 5)
		self.layout13.pack_start(labelSteps, 1, 0, 10)
		self.layout13.pack_start(self.entrySteps, 1, 0, 10)
		self.layout13.pack_start(labelCells, 1, 0, 10)
		self.layout13.pack_start(self.entryCells, 1, 0, 10)
		self.layout13.pack_start(labelDens, 1, 0, 10)
		self.layout13.pack_start(self.entryPer, 1, 0, 10)
		self.spinnerLayout.pack_start(self.spinner, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout11, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout12, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout13, 1, 0, 0)
		self.tab1Layout.pack_start(self.spinnerLayout, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)

	def createTab2(self):
		labelDefect=Gtk.Label.new("Defect position: ")
		labelStrLength=Gtk.Label.new("String length: ")
		
		self.entryDefect.set_width_chars(5)
		self.entryStrLength.set_width_chars(5)

		self.layout21.set_halign(0)
		self.layout22.set_halign(0)
		self.layout21.pack_start(labelDefect, 1, 0, 10)
		self.layout21.pack_start(self.entryDefect, 1, 0, 10)
		self.layout22.pack_start(labelStrLength, 1, 0, 10)
		self.layout22.pack_start(self.entryStrLength, 1, 0, 10)
		self.tab2Layout.pack_start(self.layout21, 1, 0, 0)
		self.tab2Layout.pack_start(self.layout22, 1, 0, 0)
	
	def createTabView(self):
		tabLabel1=Gtk.Label.new("Simulation Settings")
		tabLabel2=Gtk.Label.new("Analysis")
		self.tabView.set_border_width(20)
		self.tab1Layout.set_border_width(20)
		self.tab2Layout.set_border_width(20)
		self.createTab1()
		self.createTab2()
		self.tabView.append_page(self.tab1Layout, tabLabel1)
		self.tabView.append_page(self.tab2Layout, tabLabel2)

	def getIntValue(self, entry):
		value=entry.get_text()
		return int(value)

	def getStringValue(self, entry):
		value=entry.get_text()
		return str(value)

	def switchRandActivate(self, switchRandConf, active):
		if(switchRandConf.get_active()):
			self.entrySeed.set_sensitive(False)
			self.switchStr.set_sensitive(False)
			self.entryPer.set_sensitive(True)
			self.switchRandValue=1
		else:
			self.entrySeed.set_sensitive(True)
			self.switchStr.set_sensitive(True)
			self.entryPer.set_sensitive(False)
			self.switchRandValue=0
		
	def switchConfActivate(self, switchStr, active):
		if (switchStr.get_active()):
			self.switchConfValue=1
		else:
			self.switchConfValue=0

	def setSimulationSettings(self):
		rule=self.entryRule.get_value_as_int()
		steps=self.getIntValue(self.entrySteps)
		cells=self.getIntValue(self.entryCells)
		self.eca=ECA(rule, steps, cells)
		print(rule)
		print(steps)
		print(cells)
		if self.switchRandValue:
			dens=self.getIntValue(self.entryPer)
			self.eca.denPer=dens
			self.eca.setRandomT0()
		else:
			seedConfig=self.getStringValue(self.entrySeed)
			self.eca.setT0(seedConfig, self.switchConfValue)
	
	def setAnalysisSettings(self):
		defectPos=self.getIntValue(self.entryDefect)
		strLen=self.getIntValue(self.entryStrLength)
		self.eca.dmgPos=defectPos
		self.eca.entStringLen=strLen
		self.eca.setDamage()

	def saveSettings(self):
		pass
		#Dlg=gtk.FileChooserDialog(title="Save", parent=None, action = gtk.FILE_CHOOSER_ACTION_SAVE,  buttons=None, backend=None)

	def runSimulation(self, button):
		print("Simulation")
		self.spinner.start()
		self.setSimulationSettings()
		self.createSimScreen(self.eca.seedConfig.length*2, self.eca.steps*2)
		for i in range(self.eca.steps):
			self.drawConfiguration(y=i, bitStr=self.eca.t0, dmgBitstr=None)
			self.eca.t0=copy.deepcopy(self.eca.evolve(self.eca.t0))

		self.saveToPNG(self.screen, "Simulation.png")
		self.openImage("Simulation.png")
		self.spinner.stop()
		
	def runAnalysis(self, button):
		print("Analysis")
		entFile=open("entFile.txt", "w")
		lyapExpFile=open("lyapExp.txt", "w")
		self.spinner.start()
		self.setSimulationSettings()
		self.setAnalysisSettings()
		self.createSimScreen(self.eca.seedConfig.length*2, self.eca.steps*2)
		hx=np.zeros(self.eca.steps, dtype=float)
		
		for i in range(self.eca.steps):
			self.drawConfiguration(y=i, bitStr=self.eca.t0, dmgBitstr=self.eca.tDam)
			self.eca.getTopEntropy()
			entFile.write(str(self.eca.hX) + "\n")
			hx[i]=self.eca.hX
			self.eca.t0=copy.deepcopy(self.eca.evolve(self.eca.t0))
			self.eca.tDam=copy.deepcopy(self.eca.evolve(self.eca.tDam))

		entFile.close()
		lyapExpFile.close()
		self.saveToPNG(self.screen, "DamageSimulation.png")
		self.openImage("DamageSimulation.png")
		self.spinner.stop()

		self.setSimulationSettings()
		self.setAnalysisSettings()
		self.createSimScreen(self.eca.seedConfig.length*2, self.eca.steps*2)
		self.screen.fill(self.bckgGColor)
		for i in range(self.eca.steps):
			self.eca.getConeRatio(self.eca.tDam, i)
			self.drawCone(self.eca.tDam, i)
			self.eca.countDefects()
			self.eca.t0=copy.deepcopy(self.eca.evolve(self.eca.t0))
			self.eca.tDam=copy.deepcopy(self.eca.evolve(self.eca.tDam))

		print(self.eca.damageFreq)

		self.saveToPNG(self.screen, "DamageCone.png")
		self.openImage("DamageCone.png")

	def createSimScreen(self, width, height):
		"""
		Initialize the surface for draw simulations.
		
		Parameters
		----------
			width : int
				Length of width in pixels.
			height : int
				Length of height in pixels.
		"""
		self.screen=pygame.Surface((width, height))
		self.screen.fill(self.bckgColor)

	def drawConfiguration(self, y, bitStr=None, dmgBitstr=None):
		"""
		Draw the next step of the evolution in the simulation screen.

		Parameters
		----------
			y : int
				Step of the evolution.
			bitStr : BitString
				Configuration to draw.
			dmgBitstr : BitString
		"""
		y *= 2
		x=0
		for i in range(bitStr.length):
			if (dmgBitstr == None):
				if bitStr.bits[i]:
					self.screen.fill(self.cellColor, (x, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x, y, 2, 2))
			else:
				if (bitStr.bits[i] ^ dmgBitstr.bits[i]):
					self.screen.fill(self.defectColor, (x, y, 2, 2))
				else:
					if dmgBitstr.bits[i]:
						self.screen.fill(self.cellColor, (x, y, 2, 2))
					else:
						self.screen.fill(self.bckgColor, (x, y, 2, 2))
			x += 2

	def drawCone(self, dmgBitstr, y):
		if (y == 0):
			if dmgBitstr.bits[self.eca.dmgPos]:
				self.screen.fill(self.cellColor, (self.eca.dmgPos * 2, 0, 2, 2))
			else:
				self.screen.fill(self.bckgColor, (self.eca.dmgPos * 2, 0, 2, 2))
		else:
			y *= 2
			x=self.eca.dmgR[0]
			for i in range(self.eca.dmgR[0], self.eca.dmgR[1] + 1):
				if dmgBitstr.bits[i]:
					self.screen.fill(self.cellColor, (x * 2, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x * 2, y, 2, 2))
				x += 1
	
	def saveToPNG(self, screen, path):
		pygame.image.save(screen, path)
		print("Simulation saved")

	def openImage(self, filePath):
		if sys.platform.startswith("darwin"):
			subprocess.call(("open", filePath))
		elif os.name == "nt":
			os.startfile(filePath)
		elif os.name == "posix":
			subprocess.call(("xdg-open", filePath))


	#0101101110010010001