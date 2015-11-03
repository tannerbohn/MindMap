import datetime
import parsedatetime
import math

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
		print "time parsing error"
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