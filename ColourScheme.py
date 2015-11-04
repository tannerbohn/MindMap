import sys

from header import DIR
sys.path.insert(0, DIR+'/GraphicsTools/')
import graphicsTools as g

class ColourScheme:
	fontOpacity = 0.87

	def __init__(self, cs_name=6):


		self.darkGrey=(0.2,0.2,0.2)
		self.lightGrey=(0.8,0.8,0.8)

		if cs_name==1:
			# canvas background colour
			# based on http://aprilzero.com/
			self.background = tuple([i/255.0 for i in [22, 28, 36]])
			self.backgroundPulse = (1,1,1)


			# white links
			self.link = (1,1,1)



			self.ring1 = (1,1,1)


			self.blue = (0,0.47,0.8)#(0.258824, 0.521569, 0.956863) #tuple([i/255.0 for i in [19, 183, 242]])
			self.red = tuple([i/255.0 for i in [226,60,29]])#tuple([i/255.0 for i in [217, 92, 81]])
			self.orange =  (1,0.6,0.27)#tuple([i/255.0 for i in [245, 185, 76]])
			self.yellow=tuple([i/255.0 for i in [255,237,121]])
			self.green=tuple([i/255.0 for i in [26, 162, 14]])
			self.purple=tuple([i/255.0 for i in [112, 83, 145]])
			self.white=(1,1,1)
			self.black=(0,0,0)


			self.lightText=(1,1,1)
			self.darkText=(0,0,0)




			# ring/edge colour when you hover over it
			self.highlight = tuple([i*0.5 + 0.5 for i in self.blue]) #self.blue

			# main blue colour
			self.highlight2 = self.red

			self.smallCircle = self.highlight

			self.ringWidthMult = 1.0

			self.shadow = (0,0,0)

			# default colour for thoughts
			self.def_thought = self.background
		elif cs_name==2:
			# canvas background colour
		
			self.background = tuple([i/255.0 for i in [220,220,220]])
			self.backgroundPulse = (0.1,0.1,0.1)


			# white links
			self.link = tuple([i/255.0 for i in [30,30,30]])



			self.ring1 = tuple([i/255.0 for i in [30,30,30]])


			self.blue = tuple([i/255.0 for i in [0,180,204]])
			self.red = tuple([i/255.0 for i in [226,60,29]])#tuple([i/255.0 for i in [217, 92, 81]])
			self.orange =  (1,0.6,0.27)#tuple([i/255.0 for i in [245, 185, 76]])
			self.yellow=tuple([i/255.0 for i in [255,237,121]])
			self.green=tuple([i/255.0 for i in [26, 162, 14]])
			self.purple=tuple([i/255.0 for i in [112, 83, 145]])
			self.white=(1,1,1)
			self.black=(0,0,0)

			self.lightText=(1,1,1)
			self.darkText=(0,0,0)


			# ring/edge colour when you hover over it
			self.highlight = (0.3,0.3,0.3)

			# main blue colour
			self.highlight2 = tuple([i*0.75 for i in self.blue])

			self.ringWidthMult = 1.0

			self.shadow = self.darkGrey
		elif cs_name==3:
			'''
				BLACK AND WHITE FOR PRINTING
			'''

			# canvas background colour
		
			self.background = (1,1,1)
			self.backgroundPulse = tuple([i/255.0 for i in [0,180,204]])


			# black links
			self.link = (0,0,0)



			self.ring1 = tuple([i/255.0 for i in [30,30,30]])


			self.blue = tuple([i/255.0 for i in [0,180,204]])
			self.red = tuple([i/255.0 for i in [226,60,29]])#tuple([i/255.0 for i in [217, 92, 81]])
			self.orange =  (1,0.6,0.27)#tuple([i/255.0 for i in [245, 185, 76]])
			self.yellow=tuple([i/255.0 for i in [255,237,121]])
			self.green=tuple([i/255.0 for i in [26, 162, 14]])
			self.purple=tuple([i/255.0 for i in [112, 83, 145]])
			self.white=(1,1,1)
			self.black=(0,0,0)

			self.lightText=(1,1,1)
			self.darkText=(0,0,0)


			# ring/edge colour when you hover over it
			self.highlight = (0.3,0.3,0.3)

			# main blue colour
			self.highlight2 = tuple([i*0.75 for i in self.blue])

			self.ringWidthMult = 1.0

			self.shadow = self.darkGrey

		elif cs_name==4:
			'''
				Dark Grey and blue highlights
			'''


			self.blue = tuple([i/255.0 for i in [0,180,204]])
			self.red = tuple([i/255.0 for i in [226,60,29]])#tuple([i/255.0 for i in [217, 92, 81]])
			self.orange =  (1,0.6,0.27)#tuple([i/255.0 for i in [245, 185, 76]])
			self.yellow=tuple([i/255.0 for i in [255,237,121]])
			self.green=tuple([i/255.0 for i in [26, 162, 14]])
			self.purple=tuple([i/255.0 for i in [112, 83, 145]])
			self.white=(1,1,1)
			self.black=(0,0,0)

			# canvas background colour
		
			self.background = (0,0,0)
			self.backgroundPulse = self.darkGrey

			self.lightText=self.lightGrey
			self.darkText=self.black


			self.link = self.blue

			self.ring1 = self.darkGrey

			# ring/edge colour when you hover over it
			self.highlight = self.blue

			# main blue colour
			self.highlight2 = tuple([i*0.75 for i in self.blue])

			self.ringWidthMult = 1.5

			self.shadow = (0,0,0)
		elif cs_name==5:
			'''
				very light grey and red highlights
			'''

			
			# www.google.com/design/spec/style/color.html#

			self.blue = g.toFloatfHex('#2196F3')
			self.red = g.toFloatfHex('#F44336')
			self.orange = g.toFloatfHex('#FF9800')
			self.yellow = g.toFloatfHex('#FFEB3B')
			self.green= g.toFloatfHex('#4CAF50')
			self.purple=g.toFloatfHex('#673AB7')
			self.white=(1,1,1)
			self.black=(0,0,0)

			self.blue_grey = g.toFloatfHex('#263238')

			# canvas background colour
		
			self.background = (0.95,0.95,0.95)
			self.backgroundPulse = self.red

			self.lightText=self.white
			self.darkText=self.black


			self.link = self.red

			self.ring1 = self.darkGrey

			# only used by #h
			self.highlight = self.background

			# colour of rings and links when you hover over them
			self.highlight2 = tuple([i*0.75 + 0.25*v for i, v in zip(self.red, self.background)])

			self.smallCircle = self.red

			self.ringWidthMult = 1.0

			self.shadow = self.darkGrey

			self.def_thought = self.background #tuple([i*0.2 + 0.8*v for i, v in zip(self.blue_grey, self.background)])
		elif cs_name==6:
			'''
				based on dark theme www.google.com/design/spec/style/color.html#color-themes
			'''

			self.grey1 = g.toFloatfHex('#000000')
			self.grey2 = g.toFloatfHex('#212121')
			self.grey3 = g.toFloatfHex('#303030')
			self.grey4 = g.toFloatfHex('#424242')

			
			# www.google.com/design/spec/style/color.html#

			self.blue = g.toFloatfHex('#2196F3')
			self.red = g.toFloatfHex('#F44336')
			self.orange = g.toFloatfHex('#FF9800')
			self.yellow = g.toFloatfHex('#FFEB3B')
			self.green= g.toFloatfHex('#4CAF50')
			self.purple=g.toFloatfHex('#673AB7')
			self.white=(1,1,1)
			self.black=(0,0,0)

			self.lightblue = g.toFloatfHex('#03A9F4')

			# canvas background colour
		
			self.background = self.grey2
			self.backgroundPulse = self.grey3

			self.lightText=self.white
			self.darkText=self.black




			self.link = self.grey4

			# colour of main ring
			self.ring1 = self.grey4

			# colour of small circle
			self.smallCircle = self.grey3

			# never really used (except for #h)
			self.highlight = self.background
			
			# colour of rings and links when you hover over them
			self.highlight2 = g.toFloatfHex('#607D8B')

			self.ringWidthMult = 1.0

			self.shadow = self.black

			# default colour for thoughts
			self.def_thought = self.grey4