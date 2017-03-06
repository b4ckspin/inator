from Tkinter import Tk, Listbox, END, Label, N, E, S, W, Menu, Frame, Entry, Scale, HORIZONTAL, Canvas
from ttk import Button
from PIL import ImageTk, Image
from os import listdir
from os.path import isfile, join, abspath, dirname
import tkFileDialog


class Gui(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.lframe = Frame()
        self.rframe = Frame()
        self.rbframe = Frame()
        self.mframe = Frame(width=802, height=700)
        self.listbox = Listbox(self.lframe, height=35, bg="#333", fg="#fff")
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.imglbl = Label(self.mframe)
        self.path = abspath(".")

        self.imgidx = 0
        self.maximgidx = 0

        self.dimensions()
        self.mainframe()

    def mainframe(self):
        self.parent.title("GUI test 2")
        self.parent.configure(background='#333')

        self.loadimage("empty.png")

        self.lframe.configure(background="#333")
        self.mframe.configure(background='#333')
        self.rframe.configure(background='#333')
        self.rframe.columnconfigure(6, weight=1)
        self.rbframe.configure(background='#333')

        self.filemenu.add_command(label="Open", command=self.getpath)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command="")

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        self.listfiles(self.path)

        lstlbl = Label(self.lframe, text="placeholder")
        lstlbl.grid(row=11, padx=10, pady=4, columnspan=2, sticky=N+S+E+W)

        self.lframe.grid(row=0, column=0, padx=10, pady=0, sticky=N+W)
        self.mframe.grid(row=0, column=1, padx=0, pady=15, sticky=N)
        self.rframe.grid(row=0, column=6, padx=15, pady=10, sticky=N+E)
        self.rbframe.grid(row=0, column=6, padx=0, pady=0, sticky=S+E)

        txt = Entry(self.rframe)
        txt.grid(row=0, column=6, padx=5, pady=5)
        lbltxt = Label(self.rframe, text="Overlay Text", bg="#333", fg="white")
        lbltxt.grid(row=0, column=7, padx=1, pady=5, sticky=W+N)

        tool1 = Scale(self.rframe, from_=0, to=255, orient=HORIZONTAL)
        tool1.set(128)
        tool1.grid(row=1, column=6, padx=5, pady=5, sticky=N+S+E+W)
        lblt1 = Label(self.rframe, text="Opacity", bg="#333", fg="white")
        lblt1.grid(row=1, column=7, padx=1, pady=5, sticky=W+N)

        tool2 = Button(self.rframe, text="Next image", command=self.nextimg)
        tool2.grid(row=2, column=6, padx=5, pady=5, sticky=N + S + E + W)

        tool3 = Button(self.rframe, text="Preview")
        tool3.grid(row=3, column=6, padx=5, pady=5, sticky=N+S+E+W)

        tool4 = Button(self.rframe, text="Save")
        tool4.grid(row=4, column=6, padx=5, pady=5, sticky=N+S+E+W)

        canvas = Canvas(self.rbframe, bg="#333", width=125, height=150, highlightthickness=0)
        canvas.grid()
        photoimage = ImageTk.PhotoImage(file="logosmall.png")
        photoimage.image = photoimage
        canvas.create_image(60, 77, image=photoimage)

    def nextimg(self):
        if self.imgidx+1 < self.maximgidx:
            case1 = self.listbox.get(self.imgidx+1)
            self.imgidx += 1
            self.loadimage(self.path + "/" + case1)
        else:
            case2 = self.listbox.get(0)
            self.imgidx = 0
            self.loadimage(self.path + "/" + case2)

    def listfiles(self, imgdir):
        mypath = imgdir
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = [fi for fi in onlyfiles if fi.endswith((".jpg", ".png", ".gif"))]

        self.maximgidx = len(images)

        self.listbox.delete(0, END)
        for item in images:
            self.listbox.insert(END, item)
        self.listbox.bind("<<ListboxSelect>>", self.onselect)
        self.listbox.grid(row=0, padx=10, pady=15, sticky=N+E)

    def drawimage(self, image):
        basewidth = 800
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = ImageTk.PhotoImage(image.resize((basewidth, hsize), Image.ANTIALIAS))

        self.imglbl.configure(image=image)
        self.imglbl.image = image
        self.imglbl.grid(row=0, column=1, sticky=N)

    def loadimage(self, filename):
        self.drawimage(Image.open(filename))

    def getpath(self):
        filename = tkFileDialog.askopenfilename()
        self.path = dirname(filename)
        self.listfiles(dirname(filename))
        self.loadimage(filename)

    def onselect(self, val):
        sender = val.widget
        idx = sender.curselection()
        self.imgidx = idx[0]
        value = sender.get(idx)
        self.loadimage(self.path + "/" + value)

    def dimensions(self):
        w = 1300
        h = 640

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        # geometry: x,y + x on screen + y on screen
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    root.resizable(0, 0)
    app = Gui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
