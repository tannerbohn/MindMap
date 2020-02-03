import tkinter as tk
import sys
import subprocess
import math
import threading
import ColourScheme as cs
import time
import os


from header import DIR

sys.path.insert(0, DIR+'/GraphicsTools/')
import graphicsTools as g

from ColourScheme import *


addLabelGeom=[0,0,0,0,0]

def addEnter(event=[]):
	return

def addLeave(event=[], stage=0):

	#try:

	total_stages=20

	f = 1.0*stage/total_stages
	
	if stage<=total_stages:
		bgColour = g.shadeN([(1.0,1.0,1.0), cs.background], [0,1], f)
		textColour = g.shadeN([cs.darkText, cs.lightText], [0,1], f)


		fontColour = g.shadeN([bgColour, textColour], [0,1], cs.fontOpacity)

		tk_text.configure(fg=g.toHex(fontColour), bg=g.toHex(bgColour))#g.toHex(textColour))


	if stage < total_stages:
		t = threading.Timer(0.01, addLeave, [[], stage+1])
		t.daemon = True
		t.start()
	else:
		tk_text.place(x=-1, y=-1,width=0, height=0)
		tk_root.focus()

def addFile(event=[]):
	global sheets, addLabelGeom, tk_text

	pixelX=tk_root.winfo_width()
	pixelY=tk_root.winfo_height()

	num = len(tk_sheets)
	gridSide = int(math.ceil(math.sqrt(num)))

	tk_text.focus()

	fontSize = addLabelGeom[4]

	tk_text.place(x=addLabelGeom[0], y=addLabelGeom[1],
				width=addLabelGeom[2], height=addLabelGeom[3])

	fontColour = g.toHex(g.shadeN([(1,1,1), cs.darkText], [0,1], cs.fontOpacity))

	tk_text.configure(font=(g.mainFont, fontSize, "normal"), fg=fontColour, bg="white")


	tk_root.update()




def sheetClick(filename, event=[]):
	

	if filename=='+':
		filename = tk_text.get('1.0', 'end').strip().replace(' ','_').split('.')[0]
		filename = filename+'.json'
		filename = DIR+'\\Sheets\\'+filename

	print(filename)

	cmd = 'python '+DIR+'/mindmap.py '+filename

	subprocess.call(cmd+" >/dev/null 2>&1 &", shell=True)

	exit()

def sheetRightClick(sheet, event=[]):
	
	

	deleteSheet = tk.messagebox.askyesno("Deletion Confirmation",
		"Would you like to delete the page "+sheet['name']+'?')

	if deleteSheet:
		filename = sheet['filename']
		print("deleting ", filename)


		cmd = 'rm '+filename

		subprocess.call(cmd+" >/dev/null 2>&1 &", shell=True)

		# now need to redraw window
		initPages()
	

def labelEnter(sheet, event=[]):

	sheet.configure(bg="white", fg=g.toHex(g.shadeN([(1,1,1),cs.darkText],[0,1],cs.fontOpacity)))

def labelLeave(sheet, event=[]):
	#sheet.configure(bg=g.toHex(cs.background), fg="white")

	pulse(sheet, stage=0)


def pulse(sheet, stage=0):

	try:

		total_stages=20

		f = 1.0*stage/total_stages
		
		lightFontColour = g.shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity)
		darkFontColour = g.shadeN([(1,1,1), cs.darkText], [0,1], cs.fontOpacity)

		if stage<=total_stages:
			sheetColour = g.shadeN([(1,1,1), cs.background], [0,1], f)

			

			textColour = g.shadeN([darkFontColour, lightFontColour], [0,1], f)


			sheet.configure(bg=g.toHex(sheetColour), fg=g.toHex(textColour))


		if stage < total_stages:
			t = threading.Timer(0.01, pulse, [sheet, stage+1])
			t.daemon = True
			t.start()
	except:
		pass


def getFileList():
	flines = os.listdir(DIR+'\\Sheets\\')
	files = []
	for name in flines:
		sheet = DIR+'\\Sheets\\'+name
		namestr = name.replace('.json','')
		files.append({'filename':sheet, 'name':namestr})
	return files

def resizeLayout(event=[]):
	global tk_sheets, addLabelGeom

	pixelX=tk_root.winfo_width()
	pixelY=tk_root.winfo_height()

	#tk_canvas.place(x=0, y=0, width=pixelX, height=pixelY)

	pos=0
	num = len(tk_sheets)
	gridSide = int(math.ceil(math.sqrt(num)))

	gridWidth = pixelX/gridSide
	gridHeight = pixelY/gridSide
	#print gridSide

	fontSize = int(50.0*min(pixelX, pixelY)/(500.0*gridSide))

	for tks in tk_sheets:
		loc = ((pos%gridSide)*gridWidth, math.floor(pos/gridSide)*gridHeight)
		
		tks.place(x=loc[0], y=loc[1], width=gridWidth, height=gridHeight)
		if tks.cget('text')=='+':
			tks.configure(font=(g.mainFont, fontSize*4, "bold"))
			addLabelGeom=[loc[0], loc[1], gridWidth, gridHeight, fontSize]
		else:

			tks.configure(font=(g.mainFont, fontSize, "bold"))
		pos +=1


def graphicsInit():
	global cs

	tk_root.title("MindMap Wrapper")
	tk_root.geometry("%dx%d%+d%+d" % (g.WIDTH/2, g.HEIGHT/2, g.WIDTH/4, g.HEIGHT/4))
	

	
	tk_root.config(bg=g.toHex(cs.background))

	#tk_canvas.config(bg="black")


def initPages():
	global tk_sheets


	fontColour = g.toHex(g.shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity))

	for s in tk_sheets:
		s.destroy()

	tk_sheets=[]

	sheets = getFileList()

	for s in sheets:
		s_box = tk.Label(tk_root, text=s['name'], font=g.FONT, bg=g.toHex(cs.background), fg=fontColour, cursor='hand1', anchor=CENTER)
		s_box.bind('<Button-1>', lambda event, filename=s['filename']: sheetClick(filename, event))
		s_box.bind('<Button-3>', lambda event, sheet=s: sheetRightClick(sheet, event))

		s_box.bind('<Enter>', lambda event, sheet=s_box: labelEnter(sheet, event))
		s_box.bind('<Leave>', lambda event, sheet=s_box: labelLeave(sheet, event))
		
		tk_sheets.append(s_box)

	s_box_plus = tk.Label(tk_root, text='+', font=g.FONT, bg=g.toHex(cs.background), fg=fontColour, cursor='hand1', anchor=CENTER)
	s_box_plus.bind('<Button-1>', addFile)
	s_box_plus.bind('<Enter>', lambda event, sheet=s_box_plus: labelEnter(sheet, event))
	s_box_plus.bind('<Leave>', lambda event, sheet=s_box_plus: labelLeave(sheet, event))
	
	tk_sheets.append(s_box_plus)

	resizeLayout()

if __name__ == "__main__":
	
	cs = ColourScheme()

	tk_root = tk.Tk()
	#tk_canvas = Canvas(tk_root)

	graphicsInit()

	tk_root.bind("<Configure>", resizeLayout)

	
	


	# create list of files on canvas
	sheets = getFileList()

	#sheets.append({'filename':'', 'name':'+', 'special':True})

	tk_sheets=[]
	fontColour = g.toHex(g.shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity))
	for s in sheets:
		s_box = tk.Label(tk_root, text=s['name'], font=g.FONT, bg=g.toHex(cs.background), fg=fontColour, cursor='hand1', anchor=tk.CENTER)
		s_box.bind('<Button-1>', lambda event, filename=s['filename']: sheetClick(filename, event))
		s_box.bind('<Button-3>', lambda event, sheet=s: sheetRightClick(sheet, event))

		s_box.bind('<Enter>', lambda event, sheet=s_box: labelEnter(sheet, event))
		s_box.bind('<Leave>', lambda event, sheet=s_box: labelLeave(sheet, event))
		
		tk_sheets.append(s_box)

	s_box_plus = tk.Label(tk_root, text='+', font=g.FONT, bg=g.toHex(cs.background), fg=fontColour, cursor='hand1', anchor=tk.CENTER)
	s_box_plus.bind('<Button-1>', addFile)
	s_box_plus.bind('<Enter>', lambda event, sheet=s_box_plus: labelEnter(sheet, event))
	s_box_plus.bind('<Leave>', lambda event, sheet=s_box_plus: labelLeave(sheet, event))
	
	tk_sheets.append(s_box_plus)

	tk_text = tk.Text(tk_root)
	tk_text.configure(bd=0, highlightthickness=0)
	tk_text.bind('<Return>', lambda event, filename='+': sheetClick(filename, event))
	tk_text.bind('<Enter>', addEnter)
	tk_text.bind('<Leave>', addLeave)

	resizeLayout()

	tk_root.mainloop()
	

	
	