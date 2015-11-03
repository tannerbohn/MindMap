from header import *

from Thought import *

from Link import *

from ColourScheme import *

class Sheet:

	
	cursorPos=(0,0) #need to track cursor position for dragging
	dragInit=(0,0)
	pausePanning = False

	# store indices of thoughts to link
	linkA, linkB = -1,-1
	linkImportance=-1

	# zoom factor
	zoomFac = 1.05
	curZoom= 1.0

	# turn on/off animations
	fastGraphics = False

	holding=False

	def __init__(self, root, canvas, fileName):
		self.root=root
		self.canvas=canvas

		self.cs=ColourScheme()

		self.thoughts = []
		self.links = []

		self.canvas.bind("<Double-Button-1>",self.addAtCoord)
		self.canvas.bind('<Button-1>', self.startDrag)
		self.canvas.bind('<B1-Motion>', self.onDrag)
		self.canvas.bind('<ButtonRelease-1>', self.endThoughtDrag)
		self.root.bind('<Control-Key-s>', self.saveData)

		self.canvas.bind('<4>', lambda event : self.zoom('in', event))
		self.canvas.bind('<5>', lambda event : self.zoom('out', event))

		self.canvas.configure(bg=g.toHex(self.cs.background))

		self.curIndex=0 #keep track of index most recently assigned (first thought=1)

		self.fileName=fileName

		self.imageList=[]

		self.initDrawing()

		self.root.update()
		
		self.resize()

		self.loadFile()

	def initDrawing(self):
		global DIR
		# draw the save button
		
		self.saveIcon, self.imageList = g.loadImage(fileName=DIR+"/icons/save.png", size=(20,20),
				imageList=self.imageList, root=self.root, background=g.toHex(self.cs.background))
		self.saveIcon.bind("<Button-1>", self.handleSavePress)


		return


	def startDrag(self, event):
		self.dragInit = (event.x, event.y)
		self.cursorPos = (event.x, event.y)

	def endThoughtDrag(self, event):
		self.pausePanning = False
		self.root.update()

	def onDrag(self, event):
		if not self.pausePanning:
			# shift all objects on canvas
			delta = (event.x - self.cursorPos[0], event.y - self.cursorPos[1])

			self.cursorPos = (event.x, event.y)

			for t in self.thoughts:
				t.moveByPix((delta[0],delta[1]))
			for l in self.links:
				l.updateLine()

	def zoom(self, direction="in", event=[]):
	
		if direction == "in":
			self.curZoom *= self.zoomFac
		else:
			self.curZoom /= self.zoomFac


		#print "zooming ", direction, self.curZoom

		location=(event.x, event.y)

		for t in self.thoughts:
			# change size of t
			t.zoom(direction, location)

		for l in self.links:
			l.updateLine()
			l.zoom(direction)


	def loadFile(self):
		data = jsonLoad(self.fileName)
		
		if data == {}:
			return


		self.curZoom = data['zoom']

		geom = data['root_geometry']
		#geom = geom.split('+')[0]+'+0+0'
		#self.root.geometry(geom)
		
		geomD = geom.replace('+', ' ').replace('x', ' ').split()
		geomD = [int(d) for d in geomD]
		geomD2 = [geomD[0], geomD[1], g.WIDTH/2 - geomD[0]/2, g.HEIGHT/2 - geomD[1]/2]
		geom = '%sx%s+%s+%s'%tuple(geomD2)
		self.root.geometry(geom)

		self.root.update()
		self.resize()

		for t in data['thoughts']:
			self.addThought(coords=t['pixLoc'], data=t)

		for l in data['links']:
			self.linkA = l['tA']
			self.linkB = l['tB']
			self.linkImportance = l['importance']
			self.addLink()

	def saveData(self, event=[]):
		#print "saving..."
		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		oX = self.root.winfo_rootx()
		oY = self.root.winfo_rooty()
		data = {}
		data['root_geometry'] = self.root.winfo_geometry() #[pixelX, pixelY, oX, oY]

		#"1097x499+94+212"


		data['thoughts'] = []

		data['zoom'] = self.curZoom

		for t in self.thoughts:
	
			tData={}
			#tData['index'] = t.index
			tData['pixLoc'] = t.pixLoc
			tData['radius'] = t.r
			tData['text'] = t.getText()
			tData['fontSize'] = t.fontSize

			data['thoughts'].append(tData)


		data['links'] = []
		for l in self.links:
	
			lData={}
			#need to add 1 since index assignments for thoughts starts at 1
			#   instead of 0
			lData['tA'] = self.thoughts.index(l.tA)+1
			lData['tB'] = self.thoughts.index(l.tB)+1
			lData['importance'] = l.importance


			data['links'].append(lData)

			#l.grow()

	
		jsonSave(data=data, fileName=self.fileName, indent=True, sort=False, oneLine=False)
		

		self.pulse()

		return


	def groupShift(self, node, delta, shiftType=0, level=0):
		
		'''
		if length(delta) >= 0.004:
			shiftType=1
			#print 
		else:
			shiftType=0
			#print 1
		'''
		#print length(delta)

		if shiftType == 0:
			damp=1.0
			delta2 = [v*damp for v in list(delta)]
		
			for l in self.links:
				#if not l.isImportant(): continue

				if l.isImportant() and node == l.tA and not l.tB.groupShifted:
					# then shift l.tB

					#damp=1.0 - clamp(self.nodeDist(node, l.tB)/200.0)
					#delta2 = [v*damp for v in list(delta)]

					l.tB.moveBy(delta2)
					l.tB.groupShifted=True
					#if level < 1:
					self.groupShift(l.tB, delta2, shiftType, level=level+1)
					#else:
					#	self.groupShift(l.tB, delta2, shiftType=1, level=level+1)
				
				'''
				elif l.isImportant() and node == l.tB and not l.tA.groupShifted:
					# then shift l.tA

					#damp=1.0 - clamp(self.nodeDist(node, l.tA)/200.0)
					#delta2 = [v*damp for v in list(delta)]

					l.tA.moveBy(delta2)
					l.tA.groupShifted=True
					#if level < 1:
					self.groupShift(l.tA, delta2, shiftType, level=level+1)
					#else:
					#	self.groupShift(l.tA, delta2, shiftType=1, level=level+1)
				'''

				l.updateLine()
					

		elif shiftType==1:	
			for t in self.thoughts:
		
				if not t.groupShifted:

					distance = max(self.nodeDist(node, t),0.1)

					direction = getDir(node.pixLoc, t.pixLoc)

					cs = cosSim(normalize(delta), direction)

					d2 = max(distance - (node.z_r+t.z_r)*1.25, 1.0)
					
					if cs>=0.3 and d2<5:

						t.moveBy(delta)
						t.groupShifted=True
						self.groupShift(t, delta, shiftType)

			for l in self.links:
				l.updateLine()

		elif shiftType==2:	
			for t in self.thoughts:
		
				if not t.groupShifted:

					distance = max(self.nodeDist(node, t),0.1)/self.curZoom

					direction = getDir(node.pixLoc, t.pixLoc)

					cs = cosSim(normalize(delta), direction)

					d2 = max(distance - (node.r+t.r)*1.25, 1.0)
					
					if cs>=0.3 and d2<100:

						damp=1.0 - clamp(d2/400.0)
						delta2 = [v*damp for v in list(delta)]

						t.moveBy(delta2)
						t.groupShifted=True
						self.groupShift(t, delta2, shiftType)

			for l in self.links:
				l.updateLine()
		


	def nodeDist(self, tA, tB):
		return dist(tA.pixLoc, tB.pixLoc)

	def resetGroupShift(self):
		for t in self.thoughts:
			t.groupShifted=False

	def resize(self, event=[]):
		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		canvasW = pixelX
		canvasH = pixelY-0

		self.canvas.place(x=0, y=0, width=canvasW, height=canvasH)

		self.saveIcon.place(x=0, y=pixelY-30, width=30, height=30)

	def addThought(self, coords, data={}):

		self.thoughts.append(Thought(self, coords, data))

		#self.saveData()

	def addAtCoord(self, event):
		
		if self.pausePanning: return

		#print "click:", event.x, event.y
		self.addThought((event.x, event.y))

	def removeThought(self, index):

		# remove any links connected to that thought
		

		T = self.getThought(index)

		n = len(self.links)
		for i in range(n):
			l = self.links[n - i - 1]
			if l.tA == T or l.tB == T:
				#print "removing"
				l.remove()
				#self.removeLink(l.tA, l.tB)


		self.thoughts.remove(T)

		self.root.update()


		#self.saveData()

	def removeLink(self, tA, tB):
		# remove link associated with tA and tB

		for l in self.links:
			if l.tA == tA and l.tB==tB:
				self.links.remove(l)
				
				break

	def getNewIndex(self):
		self.curIndex += 1
		return self.curIndex

	def handleSavePress(self, event):
		self.saveData()

	def addLink(self):
		tA = self.linkA
		tB = self.linkB

		if tA == -1 or tB == -1:
			print "ERROR: a link end not assigned"

		if tA != tB and not self.hasLink(tA, tB):
			self.links.append(Link(self, self.getThought(tA), self.getThought(tB), importance=self.linkImportance))

			#print "Creating a link!"

		# set circle colour back to white
		TA = self.getThought(tA)
		TA.canvas.itemconfig(TA.smallCircleIndex, fill=g.toHex(self.cs.smallCircle))

		# reset link assignments
		self.resetLinkData()

		self.lowerLinks()

	def getThought(self, index):
		for t in self.thoughts:
			if t.index == index:
				return t

	def updateNodeEdges(self, node):
		for l in self.links:
	
			if node == l.tA or node == l.tB:
			
				l.updateLine()		

	def hasLink(self, tA, tB):

		TA = self.getThought(tA)
		TB = self.getThought(tB)

		for l in self.links:

			if (l.tA == TA and l.tB==TB) or (l.tA == TB and l.tB==TA):
				return True
		return False

	def resetLinkData(self):
		self.linkA = -1
		self.linkB = -1
		self.linkImportance=-1

	def lowerLinks(self):
		# make sure all the softer links are lower than the white ones

		for l in self.links:
			l._adjust_layers(readjust=True)

		for t in self.thoughts:
			t.lowerShadows()


	def pulse(self, stage=0):
		
		#try:

		total_stages=20

		f = 1.0*stage/total_stages
		
		if stage<=total_stages:
			bkgColour = g.shadeN([self.cs.background, self.cs.backgroundPulse, self.cs.background], [0,0.5,1], f)
			
			self.canvas.configure(bg=g.toHex(bkgColour))


		if stage < total_stages:
			t = threading.Timer(0.01, self.pulse, [stage+1])
			t.daemon = True
			t.start()
		#except:
		#	pass