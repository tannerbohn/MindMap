import header as h
import sys
import tkinter as tk
from PIL import ImageTk
import graphicsTools as g

from Sheet import Sheet


def resizeLayout(event=[]):
    global sheet

    pixelX=tk_root.winfo_width()
    pixelY=tk_root.winfo_height()

    sheet.resize()


def graphicsInit():
    tk_root.title("MindMap")
    tk_root.geometry("%dx%d%+d%+d" % (g.WIDTH/2, g.HEIGHT/2, g.WIDTH/4, g.HEIGHT/4))
    tk_root.config(bg="black")
    tk_canvas.configure(bd=0, highlightthickness=0)

    tk_root.protocol('WM_DELETE_WINDOW', exit_app)  # root is your root window


def exit_app():
    # check if saving
    # if not:
    tk_root.destroy()


if __name__ == "__main__":
    tk_root = tk.Tk()
    tk_canvas = tk.Canvas(tk_root)

    img = ImageTk.PhotoImage(file=h.DIR+'\\icons\\mindmap.png')
    tk_root.tk.call('wm', 'iconphoto', tk_root._w, img)

    graphicsInit()

    fileName=h.DIR+"\\Sheets\\tmp_thought.json"
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    print("fileName:", fileName)

    sheet = Sheet(root=tk_root, canvas=tk_canvas, fileName=fileName)

    # have to do this after creating sheet, since resizeLayout calls sheet resize functions
    tk_root.bind("<Configure>", resizeLayout)


    resizeLayout()

    tk_root.mainloop()