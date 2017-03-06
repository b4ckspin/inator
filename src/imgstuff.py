import Tkinter as tk
import Image
import ImageTk
import numpy as np
import tkFileDialog

class DIP(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("DIP Algorithms- Simple Photo Editor")
        self.pack(fill = tk.BOTH, expand = 1)

        menubar = tk.Menu(self.parent)
        self.parent.config(menu = menubar)

        self.label1 = tk.Label(self, border = 25)
        self.label2 = tk.Label(self, border = 25)
        self.label1.grid(row = 1, column = 1)
        self.label2.grid(row = 1, column = 2)

        #Open Image Menu
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label = "Open", command = self.onOpen)
        menubar.add_cascade(label = "File", menu = fileMenu)

        #menu for image ngative
        basicMenu = tk.Menu(menubar)
        basicMenu.add_command(label = "Negative", command = self.onNeg)
        menubar.add_cascade(label = "Basic", menu = basicMenu)

    def onNeg(self):
        #Image Negative Menu callback
        I2 = 255-self.I;
        im = Image.fromarray(np.uint8(I2))
        photo2 = ImageTk.PhotoImage(im)
        self.label2.image = photo2 # keep a reference!

    def setImage(self):
        self.img = Image.open(self.fn)
        self.I = np.asarray(self.img)
        l, h = self.img.size
        text = str(2*l+100)+"x"+str(h+50)+"+0+0"
        self.parent.geometry(text)
        photo = ImageTk.PhotoImage(self.img)
        self.label1.configure(image = photo)
        self.label1.image = photo # keep a reference!

    def onOpen(self):
        #Open Callback
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        filename = dlg.show()
        self.fn = filename
        #print self.fn #prints filename with path here
        self.setImage()

    #def onError(self):
        #box.showerror("Error", "Could not open file")

def main():

    root = tk.Tk()
    DIP(root)
    root.geometry("320x240")
    root.mainloop()


if __name__ == '__main__':
    main()