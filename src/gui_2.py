from Tkinter import Tk, Listbox, END, Label, N, E, S, W, Menu, Frame, Entry, Scale, HORIZONTAL, Canvas, \
                    SINGLE, StringVar, OptionMenu, DISABLED, NORMAL, Button
from PIL import ImageTk, Image, ImageDraw, ImageFont
from os import listdir, makedirs
from os.path import isfile, join, abspath, dirname, isdir, basename
import tkFileDialog


class Gui(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.lframe = Frame()
        self.rframe = Frame()
        self.rbframe = Frame()
        self.mframe = Frame(width=802, height=700)
        self.listbox = Listbox(self.lframe, selectmode=SINGLE, height=35, bg="#333", fg="#fff")
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.imglbl = Label(self.mframe)
        self.path = abspath(".")
        self.overlaytext = ""
        self.txt = Entry(self.rframe)
        self.filename = ""
        self.tool1 = Scale(self.rframe, from_=0, to=255, orient=HORIZONTAL)
        self.tool2 = Button(self.rframe, text="Next image", command=self.nextimg, state=DISABLED)
        self.tool3 = Button(self.rframe, text="Preview", command=self.preview, state=DISABLED)
        self.tool4 = Button(self.rframe, text="Save file", command=self.savesingle, state=DISABLED)
        self.tool5 = Button(self.rframe, text="Save all", command=self.saveall, state=DISABLED)
        self.var1 = StringVar()

        self.imgidx = 0
        self.maximgidx = 0

        self.dimensions()
        self.mainframe()

    def mainframe(self):
        self.parent.title("Watermarkinator v0.8")
        self.parent.configure(background='#333')

        self.loadimage(join("howto", "intro.png"))
        self.listfiles(self.path)

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

        tool5 = Button(self.lframe, text="Resize folder", command=self.resizeall, highlightthickness=0)
        tool5.grid(row=1, column=0, padx=10, sticky=N+S+E+W)

        self.lframe.grid(row=0, column=0, padx=10, sticky=N+W)
        self.mframe.grid(row=0, column=1, padx=0, pady=15, sticky=N)
        self.rframe.grid(row=0, column=6, padx=15, pady=10, sticky=N+E)
        self.rbframe.grid(row=0, column=6, padx=0, pady=0, sticky=E+W+S)

        self.txt.grid(row=0, column=6, padx=5, pady=5)
        lbltxt = Label(self.rframe, text="Overlay Text", bg="#333", fg="white")
        lbltxt.grid(row=0, column=7, padx=1, pady=5, sticky=W+N)

        self.tool1.set(255)
        self.tool1.grid(row=1, column=6, padx=5, pady=5, sticky=N+S+E+W)
        lblt1 = Label(self.rframe, text="Opacity", bg="#333", fg="white")
        lblt1.grid(row=1, column=7, padx=1, pady=5, sticky=W+N)

        lst1 = ['Top-left', 'Top-right', 'Bottom-left', 'Bottom-right']

        self.var1.set("Bottom-right")
        drop = OptionMenu(self.rframe, self.var1, *lst1)
        drop.config(highlightthickness=0)
        drop.grid(row=2, column=6, padx=5, pady=5, sticky=W + N + E)
        lblt2 = Label(self.rframe, text="Location", bg="#333", fg="white")
        lblt2.grid(row=2, column=7, padx=1, pady=5, sticky=W + N)

        self.tool2.grid(row=4, column=6, padx=5, pady=5, sticky=N+S+E+W)
        self.tool3.grid(row=5, column=6, padx=5, pady=5, sticky=N+S+E+W)
        self.tool4.grid(row=6, column=6, padx=5, pady=5, sticky=N+S+E+W)
        self.tool5.grid(row=7, column=6, padx=5, pady=5, sticky=N+S+E+W)

    def savesingle(self):
        savename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg", initialfile="marked_" + basename(self.filename))

        if not savename:
            return

        self.imagerdy.save(savename)

    def saveall(self):
        savename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg", initialdir=dirname(self.filename))

        if not savename:
            return

    def howto(self, which):
        name = ""
        if which == "resize":
            name = join("howto", "dr2_2.png")
        elif which == "open":
            name = join("howto", "dr3_1.png")
        elif which == "preview":
            name = join("howto", "dr4_1.png")

        canvas = Canvas(bg="#333", width=260, height=339, highlightthickness=0)
        photoimage = ImageTk.PhotoImage(file=name)
        photoimage.image = photoimage
        canvas.create_image(260, 339, image=photoimage, anchor=S + E)
        canvas.place(x=1026, y=300)

    def resizeall(self):
        self.howto("resize")
        foldername = tkFileDialog.askdirectory()

        if not foldername:
            return

        onlyfiles = [f for f in listdir(foldername) if isfile(join(foldername, f))]
        images = [fi for fi in onlyfiles if fi.endswith((".jpg", ".png", ".gif"))]
        images = sorted(images)

        if not images:
            return

        foldername_re = join(foldername, "resized")

        if not isdir(foldername_re):
            makedirs(foldername_re)

        for image in images:
            orig = Image.open(join(foldername, image))
            fitted = orig.resize((800, 600), Image.ANTIALIAS)
            fitted.save(join(foldername, "resized", image))

        self.loadimage(join(foldername_re, images[0]))
        self.listfiles(foldername)
        self.tool2.configure(state=NORMAL)
        self.tool3.configure(state=NORMAL)
        self.filename = join(foldername_re, images[0])
        self.path = foldername_re
        self.listbox.bind("<<ListboxSelect>>", self.onselect)

    def preview(self):
        self.howto("preview")
        self.overlay(self.txt.get())
        self.tool4.config(state=NORMAL)
        self.tool5.config(state=NORMAL)

    def overlay(self, text):
        if not self.filename:
            return

        base = Image.open(self.filename).convert('RGBA').resize((800, 600), Image.ANTIALIAS)
        txt = Image.new('RGBA', base.size, (255, 255, 255, 00))

        font = ImageFont.truetype(join(abspath("."), "fonts", "DolceVitaBold.ttf"), 20)
        w, h = font.getsize(text)
        x, y = 0, 0
        if self.var1.get() == "Bottom-right":
            x = 800-w-15
            y = 600-h-15
        elif self.var1.get() == "Bottom-left":
            x = 15
            y = 600 - h - 15
        elif self.var1.get() == "Top-right":
            x = 800-w-15
            y = 15
        elif self.var1.get() == "Top-left":
            x = 15
            y = 15

        d = ImageDraw.Draw(txt)
        d.text((x, y), text, fill=(255, 255, 255, self.tool1.get()), font=font)
        w = txt.rotate(0)
        out = Image.alpha_composite(base, w)

        self.imagerdy = out
        self.drawimage(out)

    def nextimg(self):
        if not self.filename:
            return

        if self.imgidx+1 < self.maximgidx:
            self.listbox.selection_clear(self.imgidx)
            case1 = self.listbox.get(self.imgidx+1)
            self.imgidx += 1
            self.filename = join(self.path, case1)
            self.loadimage(join(self.path, case1))
            self.listbox.selection_set(self.imgidx)
        else:
            case2 = self.listbox.get(0)
            self.imgidx = 0
            self.filename = join(self.path, case2)
            self.loadimage(join(self.path, case2))
            self.listbox.selection_clear(self.maximgidx-1)
            self.listbox.selection_set(self.imgidx)

    def listfiles(self, imgdir):
        mypath = imgdir
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = [fi for fi in onlyfiles if fi.endswith((".jpg", ".png", ".gif"))]
        images = sorted(images)
        self.maximgidx = len(images)

        self.listbox.delete(0, END)
        for item in images:
            self.listbox.insert(END, item)
        self.listbox.grid(row=0, padx=10, pady=15, sticky=N+E)

    def drawimage(self, image):
        image = ImageTk.PhotoImage(image)

        self.imglbl.configure(image=image)
        self.imglbl.image = image
        self.imglbl.grid(row=0, column=1, sticky=N)

    def loadimage(self, filename):
        try:
            image = Image.open(filename).resize((800, 600), Image.ANTIALIAS)
        except IOError:
            print "not an image.."
            return

        self.drawimage(image)

    def getpath(self):
        ftypes = [
            ('Jpg files', '*.jpg'),
            ('Png files', '*.png'),
            ('Gif files', '*.gif'),
            ('All files', '*'),
        ]
        self.filename = tkFileDialog.askopenfilename(filetypes=ftypes)

        if not self.filename:
            return

        self.howto("open")
        self.listbox.bind("<<ListboxSelect>>", self.onselect)
        self.tool2.config(state=NORMAL)
        self.tool3.config(state=NORMAL)
        self.path = dirname(self.filename)
        self.listfiles(dirname(self.filename))
        self.loadimage(self.filename)

    def onselect(self, val):
        sender = val.widget
        idx = sender.curselection()
        self.imgidx = idx[0]
        value = sender.get(idx)
        self.loadimage(join(self.path, value))

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
