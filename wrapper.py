import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import math
import threading
import ColourScheme as cs
import time
import os

import settings
from utils import toHex, shadeN
from ColourScheme import *


addLabelGeom=[0,0,0,0,0]



def addEnter(event=[]):

	return

def addLeave(event=[], stage=0):

	#try:

	total_stages=20

	f = 1.0*stage/total_stages
	
	if stage<=total_stages:
		bgColour = shadeN([(1.0,1.0,1.0), cs.background], [0,1], f)
		textColour = shadeN([cs.darkText, cs.lightText], [0,1], f)


		fontColour = shadeN([bgColour, textColour], [0,1], cs.fontOpacity)

		tk_text.configure(fg=toHex(fontColour), bg=toHex(bgColour))#toHex(textColour))


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

	fontColour = toHex(shadeN([(1,1,1), cs.darkText], [0,1], cs.fontOpacity))

	tk_text.configure(font=(settings.MAIN_FONT, fontSize, "normal"), fg=fontColour, bg="white")


	tk_root.update()




def sheetClick(filename, event=[]):
	

	if filename=='+':
		filename = tk_text.get('1.0', 'end').strip().replace(' ','_').split('.')[0]
		filename = filename+'.json'
		filename = settings.SRC_DIR+'/Sheets/'+filename

	print(filename)

	cmd = 'python3 '+settings.SRC_DIR+'/mindmap.py '+filename

	subprocess.call(cmd, shell=True)

	#init_pages() # buggy...
	exit()

def sheetRightClick(sheet, event=[]):
	
	deleteSheet = messagebox.askyesno("Deletion Confirmation",
		"Would you like to delete the page "+sheet['name']+'?')

	if deleteSheet:
		filename = sheet['filename']
		print("deleting ", filename)


		cmd = 'rm '+filename

		subprocess.call(cmd+" >/dev/null 2>&1 &", shell=True)

		# now need to redraw window
		init_pages()
	

def labelEnter(sheet, event=[]):

	sheet.configure(bg="white", fg=toHex(shadeN([(1,1,1),cs.darkText],[0,1],cs.fontOpacity)))

def labelLeave(sheet, event=[]):
	#sheet.configure(bg=toHex(cs.background), fg="white")

	pulse(sheet, stage=0)


def pulse(sheet, stage=0):

	try:

		total_stages=20

		f = 1.0*stage/total_stages
		
		lightFontColour = shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity)
		darkFontColour = shadeN([(1,1,1), cs.darkText], [0,1], cs.fontOpacity)

		if stage<=total_stages:
			sheetColour = shadeN([(1,1,1), cs.background], [0,1], f)

			

			textColour = shadeN([darkFontColour, lightFontColour], [0,1], f)


			sheet.configure(bg=toHex(sheetColour), fg=toHex(textColour))


		if stage < total_stages:
			t = threading.Timer(0.01, pulse, [sheet, stage+1])
			t.daemon = True
			t.start()
	except:
		pass


def get_sheet_list():
	flines = os.listdir(settings.SRC_DIR+'/Sheets/')
	files = []
	for name in flines:
		filename = settings.SRC_DIR+'/Sheets/'+name
		namestr = name.replace('.json','')
		files.append({'filename':filename, 'name':namestr})
	return files

def resize_layout(event=[]):
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
			tks.configure(font=(settings.MAIN_FONT, fontSize*4, "bold"))
			addLabelGeom=[loc[0], loc[1], gridWidth, gridHeight, fontSize]
		else:

			tks.configure(font=(settings.MAIN_FONT, fontSize, "bold"))
		pos +=1


def graphics_init(colour_scheme):

	tk_root.title("MindMap Wrapper")
	tk_root.geometry("{}x{}+{}+{}".format(
		settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//2,
		settings.SCREEN_SIZE[0]//4, settings.SCREEN_SIZE[1]//2))
		
	tk_root.config(bg=toHex(colour_scheme.background))


def init_pages():
	global tk_sheets

	# destroy any sheets in list so that we can update it (ex. after deletion)
	for s in tk_sheets:
		s.destroy()


	font_colour = toHex(shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity))

	

	tk_sheets=[]

	sheets_info = get_sheet_list()

	for s in sheets_info:
		s_box = tk.Label(tk_root, text=s['name'], font=settings.FONT, bg=toHex(cs.background), fg=font_colour, cursor='hand1', anchor=tk.CENTER)
		s_box.bind('<Button-1>', lambda event, filename=s['filename']: sheetClick(filename, event))
		s_box.bind('<Button-3>', lambda event, sheet=s: sheetRightClick(sheet, event))

		s_box.bind('<Enter>', lambda event, sheet=s_box: labelEnter(sheet, event))
		s_box.bind('<Leave>', lambda event, sheet=s_box: labelLeave(sheet, event))
		
		tk_sheets.append(s_box)

	s_box_plus = tk.Label(tk_root, text='+', font=settings.FONT, bg=toHex(cs.background), fg=font_colour, cursor='hand1', anchor=tk.CENTER)
	s_box_plus.bind('<Button-1>', addFile)
	s_box_plus.bind('<Enter>', lambda event, sheet=s_box_plus: labelEnter(sheet, event))
	s_box_plus.bind('<Leave>', lambda event, sheet=s_box_plus: labelLeave(sheet, event))
	
	tk_sheets.append(s_box_plus)

	resize_layout()

if __name__ == "__main__":
	
	cs = ColourScheme()

	tk_root = tk.Tk()

	graphics_init(cs)

	tk_root.bind("<Configure>", resize_layout)

	

	# create list of files on canvas
	sheets = get_sheet_list()


	tk_sheets=[]
	font_colour = toHex(shadeN([cs.background, cs.lightText], [0,1], cs.fontOpacity))
	for s in sheets:
		s_box = tk.Label(tk_root, text=s['name'], font=settings.FONT, bg=toHex(cs.background), fg=font_colour, cursor='hand1', anchor=tk.CENTER)
		s_box.bind('<Button-1>', lambda event, filename=s['filename']: sheetClick(filename, event))
		s_box.bind('<Button-3>', lambda event, sheet=s: sheetRightClick(sheet, event))

		s_box.bind('<Enter>', lambda event, sheet=s_box: labelEnter(sheet, event))
		s_box.bind('<Leave>', lambda event, sheet=s_box: labelLeave(sheet, event))
		
		tk_sheets.append(s_box)

	s_box_plus = tk.Label(tk_root, text='+', font=settings.FONT, bg=toHex(cs.background), fg=font_colour, cursor='hand1', anchor=tk.CENTER)
	s_box_plus.bind('<Button-1>', addFile)
	s_box_plus.bind('<Enter>', lambda event, sheet=s_box_plus: labelEnter(sheet, event))
	s_box_plus.bind('<Leave>', lambda event, sheet=s_box_plus: labelLeave(sheet, event))
	
	tk_sheets.append(s_box_plus)

	tk_text = tk.Text(tk_root)
	tk_text.configure(bd=0, highlightthickness=0)
	tk_text.bind('<Return>', lambda event, filename='+': sheetClick(filename, event))
	tk_text.bind('<Enter>', addEnter)
	tk_text.bind('<Leave>', addLeave)

	resize_layout()

	tk_root.mainloop()
	

	
	