import sys
import tkinter as tk
from PIL import ImageTk


from Sheet import Sheet
import settings


def resize_layout(event=[]):
    global sheet

    pixelX=tk_root.winfo_width()
    pixelY=tk_root.winfo_height()

    sheet.resize()


def graphics_init():
    tk_root.title("MindMap")
    tk_root.geometry("{}x{}+{}+{}".format(
        settings.WINDOW_SIZE[0],
        settings.WINDOW_SIZE[1], 
        settings.SCREEN_SIZE[0]//2 - settings.WINDOW_SIZE[0]//2,
        settings.SCREEN_SIZE[1]//2 - settings.WINDOW_SIZE[1]//2))
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

    img = ImageTk.PhotoImage(file=settings.SRC_DIR+'/icons/mindmap.png')
    tk_root.tk.call('wm', 'iconphoto', tk_root._w, img)

    graphics_init()

    
    filename=settings.SRC_DIR+"/Sheets/tmp_thought.json"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    
    print("filename:", filename)
    
    sheet = Sheet(root=tk_root, canvas=tk_canvas, filename=filename)

    # have to do this after creating sheet, since resizeLayout calls sheet resize functions
    tk_root.bind("<Configure>", resize_layout)


    resize_layout()

    tk_root.mainloop()
    