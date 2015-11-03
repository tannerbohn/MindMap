import math

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