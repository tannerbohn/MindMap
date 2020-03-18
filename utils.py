import tkinter as tk
from PIL import ImageTk, Image
import datetime
import parsedatetime
import math
import json


def jsonSave(data, filename, indent=True, sort=False, oneLine=False):
	f = open(filename, 'w')


	if indent:
		f.write(json.dumps(data, indent=4, sort_keys=sort))
	else:
		f.write(json.dumps(data, sort_keys=sort))

	f.close()

def jsonLoad(filename):
	try:
		file = open(filename)
		t=file.read()
		file.close()
		return json.loads(t)
	except:
		return {}

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




def loadImage(filename, size, imageList, root, background=None):
	#global IMG_LIST

	if background == None:
		background = (0,0,0)

	tk_image=[]
	with open(filename,"rb") as fp:
		original = Image.open(fp)
		resized = original.resize(size,Image.ANTIALIAS)
		image = ImageTk.PhotoImage(resized)
		tk_image = tk.Label(root, image=image, background=background, cursor='hand1')
		imageList.append(image)	

	return tk_image, imageList






def parseTime(inStr):

	# string should be of form h:m day/month/year

	if len(inStr) <= 1:
		return getTimeVec("now")

	try:
		if ':' in inStr and '/' in inStr:
			parts = inStr.split()

			hour, minute = parts[0].split(':')
			hour, minute = int(hour), int(minute)

			if parts[1]=="today":
				today = getTimeVec("now")
				day, month, year = today['day'], today['month'], today['year']
			else:
				day, month, year = parts[1].split('/')
				day, month, year = int(day), int(month), int(year)

			return {"year":year, "month":month, "day":day, "hour":hour, "minute":minute, "second":0, "worked":True}
		else:
			# see if we can try parse natural language
			return getTimeVec(inStr)
	except:
		print("time parsing error")
		return getTimeVec("now")

def timeDiff(T1, T2=[], short=False):

	# takes output from getTimeVec()

	# [TD["year"], TD["month"],TD["day"],TD["hour"],TD["minute"],TD["second"]]

	# note: months start at 1 (not zero)

	T2p = []
	if T2 == []:
		T2 = getTimeVec("now")
	
	T2p = datetime.datetime(year = T2['year'], month=T2['month'], day=T2['day'], hour=T2['hour'], minute=T2['minute'], second=T2['second'])
	T1p = datetime.datetime(year = T1['year'], month=T1['month'], day=T1['day'], hour=T1['hour'], minute=T1['minute'], second=T1['second'])

	T1TotalSecs = (T1p-datetime.datetime(1970,1,1)).total_seconds()
	T2TotalSecs = (T2p-datetime.datetime(1970,1,1)).total_seconds()

	T1InFuture = (T1TotalSecs > T2TotalSecs)

	#print "T1:", T1

	#if T1InFuture:
	#	print "T1 in future"

	tDiff = 0
	if T1InFuture:
		tDiff = T1TotalSecs - T2TotalSecs
	else:
		tDiff = T2TotalSecs - T1TotalSecs

	daysDiff = math.floor(tDiff/(86400.0))
	tDiff = tDiff - 86400.0*daysDiff

	hoursDiff = math.floor(tDiff/(3600.0))
	tDiff = tDiff - 3600.0*hoursDiff

	minutesDiff = math.floor(tDiff/(60.0))
	tDiff = tDiff - 60.0*minutesDiff

	secondsDiff = tDiff#math.floor(tDiff/(60))
	#tDiff = tDiff - 60.0*hoursDiff

	#print daysDiff, "days"
	#print hoursDiff, "hours"
	#print minutesDiff, "minutes"
	#print secondsDiff, "seconds"

	# combine values into str

	diffStr=""

	if short:
		numStr=0
		if daysDiff != 0:
			if numStr < 2:
				diffStr += (' %s'%int(daysDiff))+"d"
				numStr += 1
		if hoursDiff != 0:
			if numStr < 2:
				diffStr += (' %s'%int(hoursDiff))+"h"
				numStr += 1
		if minutesDiff != 0:
			if numStr < 2:
				diffStr += (' %s'%int(minutesDiff))+"m"
				numStr += 1
		if secondsDiff != 0:
			if numStr < 2:
				diffStr += (' %s'%int(secondsDiff))+"s"
				numStr += 1
	else:

		if daysDiff != 0:
			if daysDiff == 1:
				diffStr += (' %s'%int(daysDiff))+" day"
			else:
				diffStr += (' %s'%int(daysDiff))+" days"
		if hoursDiff != 0:
			if hoursDiff == 1:
				diffStr += (' %s'%int(hoursDiff))+" hour"
			else:
				diffStr += (' %s'%int(hoursDiff))+" hours"
		if minutesDiff != 0:
			if minutesDiff == 1:
				diffStr += (' %s'%int(minutesDiff))+" minute"
			else:
				diffStr += (' %s'%int(minutesDiff))+" minutes"
		if secondsDiff != 0:
			if secondsDiff == 1:
				diffStr += (' %s'%int(secondsDiff))+" second"
			else:
				diffStr += (' %s'%int(secondsDiff))+" seconds"

	if T1InFuture:
		if short:
			diffStr = "-"+diffStr
		else:
			diffStr = "in"+diffStr
	else:
		if short:
			diffStr = "+"+diffStr
		else:
			diffStr = diffStr+" ago"

	#print "DIFFSTR:", diffStr.strip()

	return diffStr.strip()

def toDict(T):
	# [TD["year"], TD["month"],TD["day"],TD["hour"],TD["minute"],TD["second"]]


	TD = {"year":T[0], "month":T[1], "day":T[2], "hour":T[3], "minute":T[4], "second":T[5]}


	return TD

def secondsDiff(T1, T2):
	T2p = datetime.datetime(year = T2['year'], month=T2['month'], day=T2['day'], hour=T2['hour'], minute=T2['minute'], second=T2['second'])
	T1p = datetime.datetime(year = T1['year'], month=T1['month'], day=T1['day'], hour=T1['hour'], minute=T1['minute'], second=T1['second'])

	T1TotalSecs = (T1p-datetime.datetime(1970,1,1)).total_seconds()
	T2TotalSecs = (T2p-datetime.datetime(1970,1,1)).total_seconds()

	return T1TotalSecs - T2TotalSecs

def fixStr(inStr):
	inStr = inStr.lower()

	if "from now" not in inStr and "in " in inStr:
		inStr = inStr.replace("in ", " ")
		inStr = inStr+" from now"

	inStr = inStr.replace("by ", " ")
	inStr = inStr.replace("a little while", "10 minutes")
	inStr = inStr.replace("a while", "30 minutes")
	inStr = inStr.replace("a couple", "2")
	inStr = inStr.replace("a few", "3")
	inStr = inStr.replace("some time", "2 hours")
	inStr = inStr.replace("several", "6")
	inStr = inStr.replace("midnight", "11:59 pm")
	inStr = inStr.replace("soon", "30 minutes from now")

	inStr = inStr.replace("half hour", "30 minutes")
	inStr = inStr.replace("half an hour", "30 minutes")
	inStr = inStr.replace("half a day", "12 hours")

	return inStr

def getTimeVec(inStr):
	cal = parsedatetime.Calendar()
	[T, worked] = cal.parse(fixStr(inStr))

	T  = [item for item in T]

	#if worked == 0:
	#	print "PARSE FAILED"

	#time.struct_time(tm_year=2015, tm_mon=7, tm_mday=3, tm_hour=4, tm_min=6, tm_sec=36, tm_wday=4, tm_yday=184, tm_isdst=-1)

	Year = T[0]
	Month = T[1]
	DayOfMonth = T[2]
	Hour24 = T[3]
	Minute = T[4]
	Second = T[5]
	Weekday = T[6]
	DayOfYear = T[7]

	#NOW = cal.parse("now")

	return {"year":Year, "month":Month, "day":DayOfMonth, "hour":Hour24, "minute":Minute, "second":Second, "worked":worked!=0}






def dist(p1, p2):
	v = (p1[0]-p2[0], p1[1]-p2[1])

	l = math.sqrt(sum([a*a for a in v]))
	return l


def length(v):
	return dist((0,0,0), v)


def normalize(v, thresold=0.0001):
	# normalize vector v

	l = math.sqrt(sum([a*a for a in v]))

	if l <= thresold:
		return (0,0)

	v = tuple([a/l for a in v])

	return v


def getDir(p1, p2):

	v = (p2[0]-p1[0], p2[1]-p1[1])

	return v


def luminance(c):
	luminance = 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
	return luminance


def clamp(x, bounds=[0,1]):
	return max(min(x, bounds[1]), bounds[0])


def dot(v1, v2):
	return sum([a*b for a, b in zip(v1, v2)])


def cosSim(v1, v2):
	N = dot(v1, v2)
	D = dist((0,0), v1)*dist((0,0), v2)

	if D <= 0.01: D = 0.01

	return N/D