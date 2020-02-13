import tkinter as tk
from PIL import ImageTk, Image


WIDTH = 1366#3286#
HEIGHT = 768#1440#

# TODO: add multi-monitor support (figure out dimension of current monitor)

def init(window):
	'''
	global WIDTH, HEIGHT

	WIDTH = window.winfo_screenwidth() #1366
	HEIGHT = window.winfo_screenheight() #768

	print "VALUES:", WIDTH, HEIGHT
	'''
	return


# supply vector of n colours and their centers and linearly combine them
def shadeN(colours, centers, v):

	if len(colours) == 1:
		return colours[0]
	elif len(colours) == 0:
		return (0,0,0)

	# centers must be sorted

	if v < min(centers): v = min(centers)

	if v > max(centers): v = max(centers)

	# figure out which range v is in
	r = (0,1)
	rIndex=0
	for i in range(len(centers)-1):
		m = centers[i]
		M = centers[i+1]

		if v >= m and v <= M:
			r = (m, M)
			rIndex=i
			break

	# now just return the shade in that range
	vp = (1.0*v - 1.0*r[0])/(1.0*r[1]-1.0*r[0])
	return shade(colours[rIndex], colours[rIndex+1], vp)





def shade(cA, cB, v):
	# combine the colours cA and cB with proportions
	#   specified by v

	# v in [0, 1]
	# cA/cB given as 255RGB values

	return combineColours(Iw=v, Is=1.0, LISC=(0,0,0), HIWC=cB, LIWC=cA)

def combineColours(Iw, Is, LISC, HIWC, LIWC):

	A = [v*Iw for v in HIWC]
	B = [v*(1.0-Iw) for v in LIWC]
	ApB = [a+b for (a,b) in zip(A, B)]
	C = [v*Is for v in ApB]

	D = [v*(1.0-Is) for v in LISC]

	WC = [a+b for (a,b) in zip(C, D)]

	#WC_255 = [int(v*255) for v in WC]

	#print WC
	#return WC_255
	return WC

def toFloatfHex(colour):
	if colour[0]=='#':
		colour=colour[1:]

	r = int(colour[:2], 16)
	g = int(colour[2:4], 16)
	b = int(colour[4:], 16)

	ret = toFloatf255((r, g, b))
	#print ret
	return ret

def toHexf255(colour):
	return '#%02x%02x%02x'%tuple([int(v) for v in colour])

def toHex(colour):
	return toHexf255([int(255*v) for v in colour])

def toFloatf255(colour):
	return tuple([i/255.0 for i in colour])



BG_DARK_f = (0.1, 0.1, 0.1)
BG_DARK = toHex(BG_DARK_f)

BG_LIGHT_f= (0.2, 0.2, 0.2)
BG_LIGHT= toHex(BG_LIGHT_f)



PRIMARY_f = (0.258824, 0.521569, 0.956863)#(0.0, 0.65, 1.0)
#PRIMARY_f = (0.0, 1.0, 0.2)
PRIMARY = toHex(PRIMARY_f)

LIGHT_PRIMARY_f = tuple([v*0.4 + 0.6*1 for v in PRIMARY_f])
LIGHT_PRIMARY = toHex(LIGHT_PRIMARY_f)

DARK_PRIMARY_f = tuple([v*0.5 + 0.5*0 for v in PRIMARY_f])
DARK_PRIMARY = toHex(DARK_PRIMARY_f)

COMPLEMENT_f = tuple([1.0-v for v in PRIMARY_f])
COMPLEMENT = toHex(COMPLEMENT_f)

#LIGHT_PRIMARY = toHex((1.0, 0.85, 0.5))
#PRIMARY = toHex((1.0, 0.5, 0.0))
#DARK_PRIMARY = toHex((0.5, 0.25, 0.0))

mainFont = "Lucida Sans"
#mainFont = "Droid Sans"

SMALL_FONT = (mainFont, 8)
SMALL_BOLD_FONT = (mainFont, 8, "bold")
FONT = (mainFont, 10)
BOLD_FONT = (mainFont, 10, "bold")
MED_FONT = (mainFont, 12)
LARGE_FONT = (mainFont, 18, "bold")

'''
# ALTERNATIVE QUICKREADER COLOUR SCHEME
tk_FGC = (1.0, 1.0, 1.0) # foreground
tk_BGC = (0.0, 0.0, 0.0)
tk_FGStr = "white"
tk_BGStr = "black"
tk_LHLC = (0.1, 0.1, 0.1) # tag highlight colour on mouseover
tk_LISC = (0.0, 0.35, 0.54) # colour of low-importance sentences
tk_HIWC = (1.0, 0.6, 0.0) # colour of high-importance words
tk_LIWC = (0.85, 0.9, 1.0) # colour of low-importance words
tk_BHC = (0.0, 0.65, 1.0) # bar highlight colour (for sentence importance)
tk_BPC = tk_FGC # bar position colour
'''


def loadImage(fileName, size, imageList, root, background=BG_DARK):
	#global IMG_LIST


	tk_image=[]
	with open(fileName,"rb") as fp:
		original = Image.open(fp)
		resized = original.resize(size,Image.ANTIALIAS)
		image = ImageTk.PhotoImage(resized)
		tk_image = tk.Label(root, image=image, background=background, cursor='hand1')
		imageList.append(image)	

	return tk_image, imageList