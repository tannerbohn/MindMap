from header import *

class Sidebar:

	def __init__(self, root):
		self.root=root

		self.canvas = Canvas(self.root)

		self.initSidebar()

		


	def initSidebar(self):
		# position

		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		canvasW = 100
		canvasH = pixelY-0

		self.canvas.place(x=0, y=0, width=canvasW, height=canvasH)

	def resize(self):

		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		canvasW = pixelX
		canvasH = pixelY-0

		self.canvas.place(x=0, y=0, width=100, height=canvasH)
