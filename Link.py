from header import *

class Link:

	width = 3.0

	length=0.0
	z_length=0.0


	def __init__(self, parentSheet, tA, tB, importance):
		self.root=parentSheet.root
		self.canvas=parentSheet.canvas

		self.parentSheet = parentSheet

		self.cs = self.parentSheet.cs

		self.tA = tA
		self.tB = tB

		self.importance = importance

		self._layers = []

		#self.colour = tuple([v*0.5 + 1.0*0.5 for v in self.parentSheet.colour])
		self.colour = self.cs.link # g.shadeN([self.tA.colour, self.cs.background],[0,1],0.5)  #

		if importance != 1:
			self.colour =  g.shadeN([self.colour, self.cs.background], [0,1], 0.75)

			self.width = 5

		#print "importance =", importance

		self.setZooms()

		self.initDrawing()

	def setZooms(self):

		self.z_width = self.width * self.parentSheet.curZoom

		self.z_length = self.length * self.parentSheet.curZoom

	def initDrawing(self):
		#self.canvasIndex = self.canvas.create_line(self.tA.pixLoc[0], self.tA.pixLoc[1],
		#			self.tB.pixLoc[0], self.tB.pixLoc[1],
		#			fill="white", width=5)

		x0,y0,x1,y1 = self.getCoords()

		#xb0,yb0,xb1,yb1 = self.getHeadCoords()

		self.canvasIndex = self.add_to_layer(self.importance, self.canvas.create_line, (x0,y0,x1,y1),
			fill=g.toHex(self.colour), activefill = g.toHex(self.cs.highlight2), width=int(self.z_width),
			activewidth = 5)

	
		self.canvas.tag_bind(self.canvasIndex, '<Button-3>', self.remove)
		#self.canvas.tag_bind(self.canvasIndex2, '<ButtonRelease-3>', self.endDrag)

		self.grow()

	def add_to_layer(self, layer, command, coords, **kwargs):

		layer_tag = "layer %s" % layer
		
		if layer_tag not in self._layers:
			self._layers.append(layer_tag)
		
		tags = kwargs.setdefault("tags", [])
		tags.append(layer_tag)
		item_id = command(coords, **kwargs)
		self._adjust_layers()
		return item_id

	def _adjust_layers(self, readjust=False):

		if readjust:
			# just lower the soft ones
			self.canvas.lower("layer 0")

		else:
			# lower all
			for layer in sorted(self._layers):
				self.canvas.lower(layer)
			'''
			if layer == "layer 1":
				self.canvas.lower(layer)
				print "layer 1"
			elif layer == "layer 2":
				self.canvas.lower(layer)
				self.canvas.lower(layer)
				print "layer 2"
			'''


	def updateLine(self):
		x0,y0,x1,y1 = self.getCoords()

		#xb0,yb0,xb1,yb1 = self.getHeadCoords()

		self.canvas.coords(self.canvasIndex, x0, y0, x1, y1)
		#self.canvas.coords(self.canvasIndex2, xb0, yb0, xb1, yb1)

		self.canvas.itemconfig(self.canvasIndex, width=int(self.z_width))
		#self.canvas.itemconfig(self.canvasIndex2, width=int(self.z_width*2))

	def remove(self, event=[]):
		self.parentSheet.pausePanning = True

		self.canvas.delete(self.canvasIndex)
		#self.canvas.delete(self.canvasIndex2)

		self.parentSheet.removeLink(self.tA, self.tB)


	def endDrag(self, event):

		self.parentSheet.pausePanning = False

	def grow(self, stage=0):
		

		if self.parentSheet.fastGraphics: return

		total_stages=10

		f = 1.0*stage/total_stages

		if stage<=total_stages:

			x0,y0,x1,y1 = self.getCoords()

			x1p = (1.0-f)*x0 + f*x1
			y1p = (1.0-f)*y0 + f*y1
			self.canvas.coords(self.canvasIndex, x0, y0, x1p, y1p)


			w = self.z_width*f
			self.canvas.itemconfig(self.canvasIndex, width=int(w))


		self.root.update()

		if stage < total_stages:
			t = threading.Timer(0.02, self.grow, [stage+1])
			t.daemon = True
			t.start()
			#time.sleep(0.005)
			#self.grow(max_width, stage+1)

	def getCoords(self, dFrac=0.5):
		x0,y0,x1,y1 = self.tA.pixLoc[0], self.tA.pixLoc[1], self.tB.pixLoc[0], self.tB.pixLoc[1]

		# only want line to go between white rings around thoughts
		length = dist((x0, y0), (x1, y1))

		#frac of way white ring on A is to center to A
		f0 = (1.0*length - (self.tA.z_r + self.tA.z_ringSpacing[0]))/length
		x0p = (1.0-f0)*x1 + f0*x0
		y0p = (1.0-f0)*y1 + f0*y0

		#frac of way white ring on B is to center to B
		f1 = (1.0*length - (self.tB.z_r + self.tB.z_ringSpacing[0]))/length
		x1p = (1.0-f1)*x0 + f1*x1
		y1p = (1.0-f1)*y0 + f1*y1

		self.z_length = dist((x0p, y0p), (x1p, y1p))
		self.length = self.z_length/self.parentSheet.curZoom

		return (x0p, y0p, x1p, y1p)


	def zoom(self, direction):
		self.setZooms()
		self.updateLine()

	def isImportant(self):
		return self.importance==1