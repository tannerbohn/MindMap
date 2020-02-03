import graphicsTools as g
import tkinter as tk
import calculations as calc
import math
import subprocess
import time
import timeOperations as timeOps
import threading
import tkinter as tk

class Thought:

	root=[]
	canvas=[]

	std_r = 50 # "standard" radius
	r = 50 # default radius
	fontSize = 12

	cursorPos=(0,0) #need to track cursor position for dragging
	dragInit=(0,0)
	dragFontInit=10

	# the thickness of the rings (not currently used)
	ringWidths = [3.0, 2.0, 2.0, 2.0, 2.0]
	ringSpacing= [8, 8,8,8,8]

	# radius of small circle
	smallRad = 8.0

	pulsePause = False


	curZoom = 1.0

	groupShifted=False

	# determine whether resizing the font will automatically resize the circle
	#  and if typing will automatically resize the circle
	autoTextSize=False

	# height of the circle above the canvas (for shadows)
	height = 10.0

	# label font size
	labelFontSize=8
	hasTime=False

	def __init__(self, parentSheet, coords, data={}):
		self.root=parentSheet.root
		self.canvas=parentSheet.canvas

		self.parentSheet = parentSheet
		self.index=parentSheet.getNewIndex() #index of thought on sheet (in case we want to delete later)
		
		self.cs = parentSheet.cs
		self.textColour=self.cs.lightText # will soon make set to optimal value

		# colour of the main circle (match background)
		self.colour = self.cs.def_thought


		self.ringWidths = [v*self.cs.ringWidthMult for v in self.ringWidths]
			


		self.loc=(1.0*coords[0]/self.root.winfo_width(), 1.0*coords[1]/self.root.winfo_height())
		self.pixLoc=(coords[0], coords[1])

		self.text = ""
		if data != {}:
			self.text = data['text']
			self.r = data['radius']
			self.fontSize = data['fontSize']

		
		self.prevDrawTime = time.time()

		self.initDrawing()

		self.prevPulseTime = time.time()-5.0

		
		

	def setZooms(self):
		self.curZoom = self.parentSheet.curZoom

		cz = self.curZoom
		self.z_r = self.r*cz
		self.z_fontSize=self.fontSize*cz
		self.z_ringSpacing = [v*cz for v in self.ringSpacing]
		self.z_ringWidths = [math.ceil(v*cz*self.cs.ringWidthMult) for v in self.ringWidths]

		self.z_height = self.height*cz

		self.z_labelFontSize = self.labelFontSize*cz

		# don't scale the small circle as fast
		self.z_smallRad = self.smallRad*(cz*0.5+0.5)	
	
	def initDrawing(self):
		
		self.setZooms()
		self.pulsePause = True

		self.reDraw(init=True)
		self.setBinds()
		
		

		self.tk_text.focus()

		self.handleHashTags()

		self.updateFont()

		#self.grow(max_r=self.z_r, stage=0)

		self.pulsePause = False

		self.handleTime()

	def reDraw(self, init=False, r=-1, pixChange=False, fromZoom=False):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		# r : radius of main circle
		if init:
			r = self.z_r
		else:
			if r == -1:
				r = self.z_r

			# prevent bubbles from moving when screen resized
			if pixChange:
				self.loc = (1.0*self.pixLoc[0]/canvasW, 1.0*self.pixLoc[1]/canvasH)
		r=int(r)
		
		# center of circle
		x = 1.0*canvasW*self.loc[0]
		y = 1.0*canvasH*self.loc[1]
		self.pixLoc=(x,y)

		'''
		curTime = time.time()
		draw = (curTime - self.prevDrawTime)>1./60
		if draw or init:
			self.prevDrawTime = curTime
		else:
			return
		'''

		''' 
		draw filled circle for pulse animation
		'''

		offset = 0#10*self.curZoom
		rFrac=0.5#1.1
		x0p, y0p = (x+offset)-r*rFrac, (y+offset)-r*rFrac #x-r/2, y-r/2
		x1p, y1p = (x+offset)+r*rFrac, (y+offset)+r*rFrac #x+r/2, y+r/2

		if init:
			fill = g.toHex(self.cs.lightGrey)
			self.pulseCircleIndex = self.canvas.create_oval(x0p, y0p, x1p, y1p,
				fill=fill, width=0, activewidth=0, tags="pulseCircle")

			#self.canvas.tag_lower(self.pulseCircleIndex, "all")
		else:
			self.canvas.coords(self.pulseCircleIndex, x0p, y0p, x1p, y1p)

		''' 
		draw main filled circle
		'''
		x0p, y0p = x-r, y-r
		x1p, y1p = x+r, y+r

		if init:
			fill, outline = g.toHex(self.colour), g.toHex(self.cs.highlight2)
			self.mainCircleIndex = self.canvas.create_oval(x0p, y0p, x1p, y1p, fill=fill,
					outline=fill, activeoutline=outline, width=2, activewidth=2, tags="mainCircle")
			
			#self.canvas.itemconfigure("mainCircle", cursor="hand1")
		else:
			self.canvas.coords(self.mainCircleIndex, x0p, y0p, x1p, y1p)

		


		'''
		now create and draw text box
		'''
		if init:
			self.tk_text = tk.Text(self.root, bd=0, highlightthickness=0, wrap="word",
					font=(g.mainFont, int(self.z_labelFontSize), "normal"),
					bg=g.toHex(self.colour), fg=g.toHex(self.cs.lightText))

			self.tk_text.insert(tk.END, self.text) # set initial text
			self.tk_text.tag_configure("center", justify='center')
			self.tk_text.tag_add("center", 1.0, "end")

		tr = (r*0.7)
		tx = x
		ty = y
		tx0p, ty0p = tx-tr, ty-tr
		self.tk_text.place(x=tx0p, y=ty0p, width=2*tr, height=2*tr)
		if fromZoom:
			self.updateFont(fromZoom=True)




		'''
		draw ring around main filled circle
		'''
		ring1_r = r+int(self.z_ringSpacing[0])
		x0p, y0p = x-ring1_r, y-ring1_r
		x1p, y1p = x+ring1_r, y+ring1_r
		if init:
			outline = g.toHex(self.cs.ring1)
			self.mainRingIndex = self.canvas.create_oval(x0p, y0p, x1p, y1p, fill='',
					outline=outline, activeoutline=g.toHex(self.cs.highlight2),
					width=self.z_ringWidths[0], activewidth = self.z_ringWidths[0]*2)
		else:
			self.canvas.coords(self.mainRingIndex, x0p, y0p, x1p, y1p)
			if fromZoom:
				self.canvas.itemconfig(self.mainRingIndex, width=self.z_ringWidths[0], activewidth = self.z_ringWidths[0]*2)



		''' draw text for times above ring '''
		tx = x
		ty = y-r-int(self.z_ringSpacing[0]) - 10*self.curZoom
		if init:
			self.labelIndex = self.canvas.create_text(tx, ty,
				text="", font=(g.mainFont, int(self.z_fontSize), "normal"),
				fill=g.toHex(g.shadeN([self.cs.background, self.cs.lightText], [0,1], 0.54)))

		self.canvas.coords(self.labelIndex, tx, ty)
		#if fromZoom:
		#	self.updateFont(fromZoom=True)	

		'''
		draw small circle on outer ring
		'''
		pRad=r+int(self.z_ringSpacing[0])
		pa = pRad#*1.0/math.sqrt(2.0)
		pb = math.sqrt(pRad*pRad - pa*pa)
		s_x, s_y = x-pa, y+pb
		s_r = int(self.z_smallRad)
		x0p, y0p = s_x-s_r, s_y-s_r
		x1p, y1p = s_x+s_r, s_y+s_r
		if init:
			outline, fill = g.toHex(self.cs.ring1), g.toHex(self.cs.smallCircle)
			self.smallCircleIndex = self.canvas.create_oval(x0p, y0p, x1p, y1p, fill=fill,
					outline=outline, width=0, activefill=g.toHex(self.cs.highlight2))
		else:
			self.canvas.coords(self.smallCircleIndex, x0p, y0p, x1p, y1p)


		''' draw circles under main circle for shadow '''
		
		if init:
			self.shadowCircleIndex=[]
		
			self.numShadow = 10
	
		ns = 1.0*self.numShadow
		
		#reDraw = (time.time() - self.prevDrawTime)>0.1
		for i in range(0,self.numShadow):
		
			x_offset = 0
			y_offset = self.z_height

			rFrac=1.0 + (1.0 +0.01*self.z_height)*(0.02*i)*(self.std_r/self.r)
			x0p, y0p = (x+x_offset)-r*rFrac, (y+y_offset)-r*rFrac
			x1p, y1p = (x+x_offset)+r*rFrac, (y+y_offset)+r*rFrac
			if init:
				fill = g.shadeN([self.cs.shadow, self.cs.background], [0,1.0], 1.0*math.sqrt(i/ns))
				shadowIndex = self.canvas.create_oval(x0p, y0p, x1p, y1p, fill=g.toHex(fill), width=0)
				self.shadowCircleIndex.append(shadowIndex)
				self.canvas.tag_lower(shadowIndex, "all")
			else:
				#if reDraw:
				self.canvas.coords(self.shadowCircleIndex[i], x0p, y0p, x1p, y1p)
					#self.prevDrawTime=time.time()

				

	def lowerShadows(self):
		for i in range(0,self.numShadow):
			self.canvas.tag_lower(self.shadowCircleIndex[i], "all")

	def resizeCircleForText(self):
		return

		text = self.getText()

		if '#s' in text: return

		textLines = text.splitlines()
		nLines = len(textLines)
		

		fs = self.z_fontSize


		

		nLinesP = 0
		lenTextP=0

		for l in textLines:
			if '##' not in l:
				nLinesP += 1
				lenTextP += len(l)
			else:
				nLinesP += 0.5
				lenTextP += 0.5*len(l)

		widthPerLayer = 2.5 * fs * math.sqrt(1.0*lenTextP)

		rad = 0.7 * (widthPerLayer + nLinesP*fs*1.5)/2.0
		rad = max(rad, 50*self.curZoom)

		self.z_r = rad
		self.r = rad/self.curZoom

		'''
		# current text box width
		curW = 2.0*math.floor(self.z_r*0.7)
		# want to calculate size of textbox to fit text
		layers=0
		#width=0
		for l in textLines:
			#layers += 1 # increase height needed for every line
			#print fs*math.sqrt(len(l))
			f_layers = math.ceil(2.0 * fs*math.sqrt(len(l))/curW)
			layers += max(1, f_layers-1)
	
		rad = (7.0/2.0)*layers*fs*self.curZoom*0.7/2.0
		rad = max(rad, 10*self.curZoom)

		self.z_r = rad
		self.r = rad/self.curZoom
		'''

		'''
		rad = 0.5*layers/2.0
		rad = rad * fs/0.7
		rad = max(rad, 10)

		rad = fs * (len(textLines)) + 10
		print rad

		self.z_r = rad
		self.r = self.z_r/self.curZoom

		self.reDraw()

		self.parentSheet.updateNodeEdges(self)
		'''

		self.reDraw()

		self.parentSheet.updateNodeEdges(self)

	def setBinds(self):
		# bind to release instea of press so that we can look
		# at the most recently typed text
		self.tk_text.bind('<KeyRelease>', self.typing)

		# drag main circle to move
		self.canvas.tag_bind(self.mainCircleIndex, '<Button-1>', self.startDrag)
		self.canvas.tag_bind(self.mainCircleIndex, '<ButtonRelease-1>', self.endDrag)
		self.canvas.tag_bind(self.mainCircleIndex, '<B1-Motion>', self.onLeftDrag)


		# double click to run command
		self.canvas.tag_bind(self.mainCircleIndex, '<Control-Button-1>', self.tryCommand)
		# dragging main circle
		self.canvas.tag_bind(self.mainCircleIndex, '<Button-3>', self.startDrag)
		self.canvas.tag_bind(self.mainCircleIndex, '<ButtonRelease-3>', self.endDrag)
		self.canvas.tag_bind(self.mainCircleIndex, '<B3-Motion>', self.onRightDrag)
		# pulse when mouse over

	
		self.canvas.tag_bind(self.mainCircleIndex, '<Enter>',
				(lambda event, widget="mainCircle": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.mainCircleIndex, '<Leave>',
				(lambda event, widget="mainCircle": self.widgetLeave(event, widget)))

		

		# drag outer (left click) ring to resize
		self.canvas.tag_bind(self.mainRingIndex, '<Button-1>', self.startDrag)
		self.canvas.tag_bind(self.mainRingIndex, '<ButtonRelease-1>', self.endDrag)
		self.canvas.tag_bind(self.mainRingIndex, '<B1-Motion>', self.onRingLeftDrag)

		self.canvas.tag_bind(self.mainRingIndex, '<Button-3>', self.startDrag)
		self.canvas.tag_bind(self.mainRingIndex, '<ButtonRelease-3>', self.endDrag)
		self.canvas.tag_bind(self.mainRingIndex, '<B3-Motion>', self.onRingRightDrag)

		self.canvas.tag_bind(self.mainRingIndex, '<Enter>',
				(lambda event, widget="mainRing": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.mainRingIndex, '<Leave>',
				(lambda event, widget="mainRing": self.widgetLeave(event, widget)))

		# click small circle to create link
		self.canvas.tag_bind(self.smallCircleIndex, '<Button-1>',
				(lambda event, importance=1: self.linkAdd(importance)))

		self.canvas.tag_bind(self.smallCircleIndex, '<Button-3>',
				(lambda event, importance=0: self.linkAdd(importance)))

		self.canvas.tag_bind(self.smallCircleIndex, '<Enter>',
				(lambda event, widget="smallCircle": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.smallCircleIndex, '<Leave>',
				(lambda event, widget="smallCircle": self.widgetLeave(event, widget)))

	def widgetEnter(self, event=[], widget=""):
		if widget=="mainCircle":
			self.canvas.config(cursor="hand1")

			self.pulse()

		elif widget == "mainRing":
			self.canvas.config(cursor="hand1")#sizing")
		elif widget == "smallCircle":
			self.canvas.config(cursor="hand1")

	def widgetLeave(self, event=[], widget=""):

		self.canvas.config(cursor="arrow")


	def startDrag(self, event):
		self.pulsePause=True

		#self.holding = True
		#self.parentSheet.holding = True

		canvasW=1.0*self.root.winfo_width()
		canvasH=1.0*self.root.winfo_height()
		self.loc = (self.pixLoc[0]/canvasW, self.pixLoc[1]/canvasH)

		self.dragInit = (event.x, event.y)
		self.cursorPos = (event.x, event.y)
		self.dragFontInit = self.fontSize

		self.height *= 1.5
		self.z_height *= 1.5


		self.parentSheet.pausePanning = True

	def endDrag(self, event):
		self.pulsePause = False
		self.parentSheet.pausePanning = False


		#self.holding = False
		#self.parentSheet.holding = False

		
		self.height /= 1.5
		self.z_height /= 1.5
		self.reDraw()
		
		
		self.lowerShadows()

		self.root.update()

	def onRightDrag(self, event):
		delta = (event.x - self.cursorPos[0], event.y - self.cursorPos[1])

		self.cursorPos = (event.x, event.y)
		#print "drag:", event.x, event.y
		#self.moveTo((1.0*event.x/self.root.winfo_width(), 1.0*event.y/self.root.winfo_height()))

		moveDelta = (1.0*delta[0]/self.root.winfo_width(), 1.0*delta[1]/self.root.winfo_height())
		self.moveBy(moveDelta)

		# also move node's connections
		self.groupShifted=True
		self.parentSheet.groupShift(self, moveDelta)
		self.parentSheet.resetGroupShift()

	def onLeftDrag(self, event):

		delta = (event.x - self.cursorPos[0], event.y - self.cursorPos[1])

		self.cursorPos = (event.x, event.y)
		#print "drag:", event.x, event.y
		#self.moveTo((1.0*event.x/self.root.winfo_width(), 1.0*event.y/self.root.winfo_height()))
		self.moveBy((1.0*delta[0]/self.root.winfo_width(), 1.0*delta[1]/self.root.winfo_height()))

		self.parentSheet.updateNodeEdges(self)
		return

	def onRingLeftDrag(self, event):
		cz = self.curZoom

		#print "drag:", event.x, event.y
	
		# calculate new radius
		center = self.pixLoc

		cur = (event.x, event.y)

		# calculate dist form center to cur
		d = dist(center, cur)/cz

		if d <= 10:
			self.remove()
			return

		self.r = d-self.ringSpacing[0]
		self.z_r = cz*self.r

		self.reDraw()

		self.parentSheet.updateNodeEdges(self)

	def onRingRightDrag(self, event):


		self.cursorPos = (event.x, event.y)

		initDistance = calc.dist(self.dragInit, self.pixLoc)

		curDistance = calc.dist(self.cursorPos, self.pixLoc)

		deltaDist = 1.0*curDistance / initDistance

		#print "dist:", deltaDist

		fontSize = int(self.dragFontInit*deltaDist) #max(min(int(deltaDist), 4), 40)
		self.fontSize = fontSize
		self.z_fontSize = self.fontSize*self.curZoom
		#self.tk_text.config(font=(g.mainFont, int(self.z_fontSize), "normal"))
		self.updateFont()

		self.resizeCircleForText()

	def tryCommand(self, event):
		#print "trying command!"
		
		text = self.getText().strip()

		if len(text) < 1: return

		text = text.splitlines()

		#print text

		cmdLines=[]
		for l in text:
			l = l.strip()
			if l.rfind('##') == 0:
				l = l[2:].strip()

			if len(l)<=4: continue
			if l[0:2]=='[[' and l[len(l)-2:]==']]':
				cmdLines.append(l[2:len(l)-2].strip())
			else:
				continue

		for cmd in cmdLines:

			cmdStr = cmd+" > /dev/null 2>&1 &"

			#+" > /dev/null 2>&1 &"
			try:
				output = str(subprocess.call(cmdStr, shell=True))

				output = output.strip()
				if output != "" and output != '0':
					newLoc = self.pixLoc
					newLoc = (newLoc[0]+self.z_r, newLoc[1]+self.z_r)

					# need text, radius, fontSize
					data = {'text': output, 'radius':max(self.z_r*0.5, 15), 'fontSize':self.z_fontSize}
					self.parentSheet.addThought(coords=newLoc, data=data)
			except:
				print("Command failed: ", cmdStr)
				pass

	def linkAdd(self, importance=1):

		# see which link end is free to assign

		if importance == 0:
			#print "double click!"
			self.parentSheet.resetLinkData()
		#else:
		#	print "single click"

		if self.parentSheet.linkA == -1:
			self.parentSheet.linkA = self.index
			self.parentSheet.linkImportance = importance #random.randint(1,2)

			# hold circle colour
			holdColour = g.shadeN([(1,1,1), self.cs.highlight2], [0,3], importance+2)
			if importance==1:
				self.canvas.itemconfig(self.smallCircleIndex, fill=g.toHex(holdColour))
			else:
				self.canvas.itemconfig(self.smallCircleIndex, fill=g.toHex(holdColour))
		elif self.parentSheet.linkB == -1:
			self.parentSheet.linkB = self.index

			self.parentSheet.addLink()


	def moveByPix(self, x):

		newX, newY = self.pixLoc[0] + x[0], self.pixLoc[1]+x[1]

		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		self.loc = (1.0*newX/pixelX, 1.0*newY/pixelY)

		self.reDraw()

		self.parentSheet.updateNodeEdges(self)

	def moveBy(self, x):
		newX = self.loc[0]+x[0] #max(min(self.loc[0]+x, 1), 0)
		newY = self.loc[1]+x[1] #max(min(self.loc[1]+y, 1), 0)
		
		self.loc = (newX, newY)

		self.reDraw()

	def moveTo(self, x):
		# must provide normalized coords (0-1)
		self.moveBy((x[0] - self.loc[0], x[1] - self.loc[1]))

	def remove(self, event=[]):
		

		for i in self.shadowCircleIndex:
			self.canvas.delete(i)
		self.canvas.delete(self.mainCircleIndex)
		self.canvas.delete(self.mainRingIndex)
		self.canvas.delete(self.smallCircleIndex)
		self.canvas.delete(self.labelIndex)

		self.hasTime = False

		self.canvas.delete(self.pulseCircleIndex)

		self.widgetEnter()

		#self.canvas.delete("all")

		self.tk_text.destroy()
		#self.tk_text.grid(row = 1, column = 0)
		#self.tk_text.grid_remove()

		#self.parentSheet.pausePanning=False
		self.parentSheet.removeThought(self.index)


	def getText(self):
		text = self.tk_text.get("0.0",tk.END)
		text = text.strip()
		return text

	def typing(self, event):
		#self.tk_text.tag_configure("center", 1.0, "end")
		self.tk_text.tag_add("center", 1.0, "end")

		self.handleTime()

		self.handleHashTags()

		self.resizeCircleForText()

	def handleHashTags(self, event=[]):
		# check for hashtags
		text = self.getText()+'  '

		if len(text) <3 : return

		LIC = self.parentSheet.cs.background # low importance colour
		
		max_shades = 5

		HIC=(0,0,0)

		
		shadeChar='1'
		foundTag=True
		if '#b' in text:
			shadeChar = text[text.rfind('#b')+2]
			HIC = self.cs.blue
		elif '#r' in text:
			shadeChar = text[text.rfind('#r')+2]
			HIC = self.cs.red
		elif '#g' in text:
			shadeChar = text[text.rfind('#g')+2]
			HIC = self.cs.green
		elif '#y' in text:
			shadeChar = text[text.rfind('#y')+2]
			HIC = self.cs.yellow
		elif '#o' in text:
			shadeChar = text[text.rfind('#o')+2]
			HIC = self.cs.orange
		elif '#p' in text:
			shadeChar = text[text.rfind('#p')+2]
			HIC = self.cs.purple
		elif '#w' in text:
			shadeChar = text[text.rfind('#w')+2]
			HIC = self.cs.white
		elif '#k' in text:
			shadeChar = text[text.rfind('#k')+2]
			HIC = self.cs.black
		elif '#h' in text:
			shadeChar = text[text.rfind('#h')+2]
			HIC = self.cs.highlight
		else:
			self.colour = self.parentSheet.cs.def_thought#background
			self.recolour()
			foundTag=False


		if foundTag and not shadeChar.isdigit():
			shadeChar = '1'

		# shades for for 1, 2, 3, 4, 5
		if foundTag and shadeChar.isdigit():
			self.colour = g.shadeN([HIC, self.parentSheet.cs.background], [1, max_shades+1], int(shadeChar))


		self.recolour()

		self.updateFont()

	def updateFont(self, fromZoom=False):

		# dynamically optimize text colour
		textColour=self.textColour
		lum = calc.luminance(self.colour)
		if lum >= 0.5:
			#print "light background"

			# 87% opacity for important black text on coloured background
			textColour=g.shadeN([self.colour, self.cs.darkText], [0, 1], self.cs.fontOpacity)
		else:
			#print "dark background"
			#textColour=self.cs.lightText

			textColour=g.shadeN([self.colour, self.cs.lightText], [0, 1], self.cs.fontOpacity)
		
		#if textColour != self.textColour:
		self.textColour=textColour
	
		insertbg=[v*0.5+w*0.5 for v,w in zip(self.textColour, self.cs.def_thought)]

		if not fromZoom:
			self.tk_text.configure(fg=g.toHex(textColour), insertbackground=g.toHex(insertbg))


		if not fromZoom:
			tags = list(self.tk_text.tag_names(index=None))
			tags.remove("sel")
			tags.remove("center")
			for t in tags:
				self.tk_text.tag_delete(t)


		text = self.getText()

		# check for bolding
		fontThickness="normal"
		if '#B' in text:
			fontThickness = "bold"
		elif '#I' in text:
			fontThickness = "italic"
		
		self.tk_text.configure(font=(g.mainFont, int(self.z_fontSize//1), fontThickness))
		self.canvas.itemconfig(self.labelIndex, font=(g.mainFont, max(1,int(self.z_labelFontSize//1)), "normal"))
		
		if '#' not in text and '*' not in text:
			return

		pos=1

		LINES = text.splitlines()

		for l in range(len(LINES)):
			
			line = LINES[l]

			#print "line: ", line

			if line.strip() == "" or ('#' not in line and '*' not in line):
				pos += 1
				continue

			fontSize = self.z_fontSize
			if len(line)>=2:
				#if line[0:2] == '##':
				if '##' in line:
					fontSize = fontSize/2
			

			locLS = 0
			locRS = len(line)-1

			# also colour each word by its importance
			words = split2(line)
			for W in words:
				
				word = W[0]
				wStart = W[1]
				wEnd = W[2]

				
				
				if W[0][0]=='#':
					tagName='%s.%s'%(pos,wStart)+'WF'
					self.tk_text.tag_add(tagName, '%s.%s'%(pos,wStart), '%s.%s'%(pos, wStart+len(word)))
					
					self.tk_text.tag_config(tagName, font=(g.mainFont, int(self.z_fontSize//2), fontThickness))
				elif W[0][0]=='*' and W[0][len(W[0])-1]=='*':
					tagName='%s.%s'%(pos,wStart)+'BF'
					self.tk_text.tag_add(tagName, '%s.%s'%(pos,wStart), '%s.%s'%(pos, wStart+len(word)))
			
					self.tk_text.tag_config(tagName, font=(g.mainFont, int(fontSize//1), "bold"))
				else:
					tagName='%s.%s'%(pos,wStart)+'norm'
					self.tk_text.tag_add(tagName, '%s.%s'%(pos,wStart), '%s.%s'%(pos, wStart+len(word)))
			
					self.tk_text.tag_config(tagName, font=(g.mainFont, int(fontSize//1), fontThickness))

			pos += 1
	
	def handleTime(self):
		text = self.getText()

		start = text.find('<<')
		end = text.find('>>')

		# make sure the order is << then >>
		hasTime=True
		if start == -1 or end == -1 or end-start <= 3:
			hasTime=False

		if hasTime:

			timeStr = text[start+2:end].strip()

			parsedTime = timeOps.parseTime(timeStr)

			self.parsedTime = parsedTime
			# calculate time diff
			diffStr = timeOps.timeDiff(parsedTime, short=True)
			#print diffStr

			if not self.hasTime:
				self.hasTime = True
				#print "starting thread"
				self.watchTime()
		

			#self.canvas.itemconfig(self.labelIndex, text=diffStr)
		else:
			self.hasTime = False
			self.canvas.itemconfig(self.labelIndex, text="")


	def watchTime(self):

		if not self.hasTime:
			return

		diffStr = timeOps.timeDiff(self.parsedTime, short=True)
		#print "watch: ", diffStr
		self.canvas.itemconfig(self.labelIndex, text=diffStr)

		t = threading.Timer(5, self.watchTime)#, [[], stage+1, height])
		t.daemon = True
		t.start()

	def recolour(self, event=[]):

		self.canvas.itemconfig(self.mainCircleIndex, fill = g.toHex(self.colour), outline=g.toHex(self.colour))
		self.tk_text.configure(bg=g.toHex(self.colour))



	def grow(self, max_r=50, stage=0):
		if self.parentSheet.fastGraphics: return

		total_stages=10#max_r/3

		if stage<=total_stages:
			self.reDraw(r=1.0*max_r*stage / total_stages)


		self.root.update()

		if stage < total_stages:
			#t = threading.Timer(0.01, self.grow, [max_r, stage+1])
			#t.daemon = True
			#t.start()
			time.sleep(0.005)
			self.grow(max_r, stage+1)

	def pulse(self, event=[], stage=0, height=6):

		#print "pulse"

		if self.pulsePause and stage==0: return

		#if self.parentSheet.holding and not self.holding: return
		

		if stage==0:
			

				
			if time.time()-self.prevPulseTime <= 1:
				return

			self.pulsePause=True




		total_stages=9
		# fraction of way through pulse
		f1 = 1.0*stage/total_stages
	

		if stage <= total_stages:

			pixMove=2*1.0*height/total_stages
	
			# make the jumping smoother
			dt = -1.0*math.atan(2*(2*f1-1.0))
			self.z_height += dt*pixMove
			self.moveByPix((0,-1.0*pixMove*dt))

			t = threading.Timer(0.03, self.pulse, [[], stage+1, height])
			t.daemon = True
			t.start()

		else:
			self.reDraw()
			self.pulsePause=False

			self.prevPulseTime = time.time()


	def pulse2(self, event=[], stage=0):
		if self.pulsePause and stage==0: return

		if stage==0:
			
			if time.time()-self.prevPulseTime <= 1:
				return

		if self.colour == self.cs.def_thought: return

		#if self.parentSheet.fastGraphics: return
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		if stage==0:
			self.canvas.tag_lower(self.pulseCircleIndex, "all")
			#for i in range(self.numShadow):
			#	self.canvas.tag_raise(self.pulseCircleIndex, self.shadowCircleIndex[i])

		total_stages=10

		f = 1.0*stage/total_stages

		r = self.z_r
		
		# center of circle
		x = 1.0*canvasW*self.loc[0]
		y = 1.0*canvasH*self.loc[1]

		#print "here"

		if stage <= total_stages:
			self.pulsePause = True

			pRad = 40*self.curZoom

			curRad = r+f*pRad

			x0p, y0p = x-curRad, y-curRad
			x1p, y1p = x+curRad, y+curRad

			fill = g.shadeN([self.colour, self.cs.def_thought], [0,1], f)

			self.canvas.coords(self.pulseCircleIndex, x0p, y0p, x1p, y1p)
			self.canvas.itemconfig(self.pulseCircleIndex, fill = g.toHex(fill))



			t = threading.Timer(0.04, self.pulse, [[], stage+1])
			t.daemon = True
			t.start()
		else:
			offset = 0 #10*self.curZoom
			rFrac=0.5 #1.1
			x0p, y0p = (x+offset)-r*rFrac, (y+offset)-r*rFrac #x-r/2, y-r/2
			x1p, y1p = (x+offset)+r*rFrac, (y+offset)+r*rFrac #x+r/2, y+r/2
			self.canvas.coords(self.pulseCircleIndex, x0p, y0p, x1p, y1p)
			#self.canvas.itemconfig(self.pulseCircleIndex, fill = g.toHex(self.cs.lightGrey))

			self.pulsePause=False

			self.prevPulseTime = time.time()
		
		
	def zoom(self, direction, location):
		cz = self.parentSheet.curZoom
		
		self.setZooms()

		pX, pY = self.root.winfo_width(), self.root.winfo_height()


		f=1.0
		if direction == "in":
			f = self.parentSheet.zoomFac
		else:
			f = 1.0/self.parentSheet.zoomFac

		#delta = getDir((pX/2, pY/2), self.pixLoc)
		delta = calc.getDir(location, self.pixLoc)

		delta2 = (delta[0]*f, delta[1]*f)

		diff = (delta2[0]-delta[0], delta2[1]-delta[1])

		self.pixLoc = (self.pixLoc[0]+diff[0], self.pixLoc[1]+diff[1])

		self.reDraw(pixChange=True, fromZoom=True)


def split2(string):

	# return list of words with start and end indices of each
	words = []

	inWord=False
	start = 0
	end = 0
	for i in range(len(string)):

		if not inWord and string[i] != ' ':
			inWord = True
			start = i
			end = 0
		elif inWord and not string[i] != ' ':
			inWord = False
			end = i
			words.append([string[start:end], start, end])
		elif inWord and i == len(string)-1:
			end = i+1
			words.append([string[start:end], start, end])

	return words