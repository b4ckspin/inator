from Tkinter import Tk, Listbox, END, Label, N, E, S, W, Menu, Frame, Entry, Scale, HORIZONTAL, Canvas, \
                    SINGLE, StringVar, OptionMenu, DISABLED, NORMAL, Button, Checkbutton, IntVar, Toplevel, Message
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
        self.iscolor = "white"
        self.isbadge = False

        self.txtlocation = StringVar()
        self.badgelocation = StringVar()
        self.whichcolor = IntVar()

        self.tool1 = Scale(self.rframe, from_=0, to=255, orient=HORIZONTAL)
        self.tool2 = Button(self.rframe, text="Next image", command=self.nextimg, state=DISABLED)
        self.tool3 = Button(self.rframe, text="Preview", command=self.preview, state=DISABLED)
        self.tool4 = Button(self.rframe, text="Save file", command=self.savesingle, state=DISABLED)
        self.tool5 = Checkbutton(self.rframe, text=self.iscolor, command=self.color, variable=self.whichcolor)
        self.tool6 = Checkbutton(self.rframe, command=self.badge, state=DISABLED)

        self.imgidx = 0
        self.maximgidx = 0

        self.dimensions()
        self.mainframe()

    def mainframe(self):
        self.parent.title("Watermarkinator")
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
        self.filemenu.add_command(label="Info", command=self.getinfo)
        self.filemenu.add_command(label="Exit", command=self.exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        tool5 = Button(self.lframe, text="Resize folder", command=self.resizeall, highlightthickness=0)
        tool5.grid(row=2, column=0, padx=10, sticky=N+S+E+W)
        tool7 = Button(self.lframe, text="Open image", command=self.getpath, highlightthickness=0)
        tool7.grid(row=1, column=0, padx=10, pady=2, sticky=N+S+E+W)

        self.lframe.grid(row=0, column=0, padx=10, sticky=N+W)
        self.mframe.grid(row=0, column=1, padx=0, pady=15, sticky=N)
        self.rframe.grid(row=0, column=6, padx=15, pady=10, sticky=N+E)
        self.rbframe.grid(row=0, column=6, padx=0, pady=0, sticky=E+W+S)

        # text
        self.txt.grid(row=0, column=6, padx=5, pady=5)
        lbltxt = Label(self.rframe, text="Overlay Text", bg="#333", fg="white")
        lbltxt.grid(row=0, column=7, padx=1, pady=5, sticky=W+N)

        # text location
        lst1 = ['Top-left', 'Top-right', 'Bottom-left', 'Bottom-right']
        self.txtlocation.set("Bottom-right")
        drop = OptionMenu(self.rframe, self.txtlocation, *lst1)
        drop.config(highlightthickness=0)
        drop.grid(row=2, column=6, padx=5, pady=5, sticky=W + N + E)
        lblt2 = Label(self.rframe, text="Location", bg="#333", fg="white")
        lblt2.grid(row=2, column=7, padx=1, pady=5, sticky=W + N)

        # text opacity
        self.tool1.set(255)
        self.tool1.grid(row=3, column=6, padx=5, pady=5, sticky=N+S+E+W)
        lblt1 = Label(self.rframe, text="Opacity", bg="#333", fg="white")
        lblt1.grid(row=3, column=7, padx=1, pady=5, sticky=W+N)

        # text color
        self.tool5.grid(row=4, column=6, padx=5, pady=5, sticky=N+E+W)
        lblt3 = Label(self.rframe, text="Color", bg="#333", fg="white")
        lblt3.grid(row=4, column=7, padx=1, pady=5, sticky=W+N)

        # badge
        self.tool6.grid(row=5, column=6, padx=5, pady=5, sticky=N+S+E+W)
        lblt4 = Label(self.rframe, text="Badge", bg="#333", fg="white")
        lblt4.grid(row=5, column=7, padx=1, pady=5, sticky=W+N)

        # badge location
        lst2 = ['Top-left', 'Top-right', 'Bottom-left', 'Bottom-right']
        self.badgelocation.set("Bottom-right")
        drop2 = OptionMenu(self.rframe, self.badgelocation, *lst2)
        drop2.config(highlightthickness=0)
        drop2.grid(row=6, column=6, padx=5, pady=5, sticky=W + N + E)
        lblt3 = Label(self.rframe, text="Location", bg="#333", fg="white")
        lblt3.grid(row=6, column=7, padx=1, pady=5, sticky=W + N)


        # preview
        self.tool3.grid(row=7, column=6, padx=5, pady=5, sticky=N+S+E+W)
        # save
        self.tool4.grid(row=8, column=6, padx=5, pady=5, sticky=N+S+E+W)
        # next image
        self.tool2.grid(row=9, column=6, padx=5, pady=5, sticky=N+S+E+W)

    @staticmethod
    def getinfo():
        about = """
        The Watermarkinator is developed by Dave.

        All images are property of their respective owners.


        If you like the software or have trouble, send me an email:
        david@fixx-it.at
        """
        top = Toplevel()
        top.title("Watermarkinator v1.0")

        msg = Message(top, text=about, width=400)
        msg.grid(row=0, column=0, padx=30, pady=0, sticky=E)

        button = Button(top, text="Ok", command=top.destroy)
        button.grid(row=1, column=0, padx=10, pady=10, sticky=S)

        top.focus()

    def color(self):
        if self.whichcolor.get() == 0:
            self.tool5.config(text="white")
        else:
            self.tool5.config(text="black")

    def savesingle(self):
        if not self.path or not self.filename:
            return

        self.imagerdy.save(join(self.path, "done_" + basename(self.filename)))

    @staticmethod
    def howto(which):
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
        canvas.place(x=1026, y=330)

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
            imgname = join(foldername, image)
            orig = Image.open(open(imgname, 'rb'))
            fitted = orig.resize((800, 600), Image.ANTIALIAS)
            fitted.save(join(foldername, "resized", image))

        self.loadimage(join(foldername_re, images[0]))
        self.listfiles(foldername)
        self.tool2.configure(state=NORMAL)
        self.tool3.configure(state=NORMAL)
        self.tool6.configure(state=NORMAL)
        self.filename = join(foldername_re, images[0])
        self.path = foldername_re
        self.listbox.bind("<<ListboxSelect>>", self.onselect)

    def preview(self):
        self.howto("preview")
        self.overlay(self.txt.get())
        self.tool4.config(state=NORMAL)

    def overlay(self, text):
        if not self.filename:
            return

        base = Image.open(open(self.filename, 'rb')).convert('RGBA').resize((800, 600), Image.ANTIALIAS)
        txt = Image.new('RGBA', base.size, (255, 255, 255, 00))


        #if badge is true do this, else text only
        if self.isbadge:
            badgepath = abspath(".") + "/howto/badge.png"
            badge = Image.open(badgepath, 'r')
            badge = badge.resize((120, 120), Image.ANTIALIAS)

            bw, bh = badge.size
            x, y = 0, 0
            if self.badgelocation.get() == "Bottom-right":
                x = 800 - bw - 15
                y = 600 - bh - 15
            elif self.badgelocation.get() == "Bottom-left":
                x = 15
                y = 600 - bh - 15
            elif self.badgelocation.get() == "Top-right":
                x = 800 - bw - 15
                y = 15
            elif self.badgelocation.get() == "Top-left":
                x = 15
                y = 15


            badgelocation = (x,y)
            base.paste(badge, badgelocation, badge)



        font = ImageFont.truetype(join(abspath("."), "fonts", "DolceVitaBold.ttf"), 20)
        w, h = font.getsize(text)
        x, y = 0, 0
        if self.txtlocation.get() == "Bottom-right":
            x = 800-w-15
            y = 600-h-15
        elif self.txtlocation.get() == "Bottom-left":
            x = 15
            y = 600 - h - 15
        elif self.txtlocation.get() == "Top-right":
            x = 800-w-15
            y = 15
        elif self.txtlocation.get() == "Top-left":
            x = 15
            y = 15

        r, g, b = 255, 255, 255
        if self.whichcolor.get() == 0:
            r, g, b = 255, 255, 255
        elif self.whichcolor.get() == 1:
            r, g, b = 0, 0, 0

        d = ImageDraw.Draw(txt)
        d.text((x, y), text, fill=(r, g, b, self.tool1.get()), font=font)
        w = txt.rotate(0)
        out = Image.alpha_composite(base, w)

        self.imagerdy = out
        self.drawimage(out)

    def badge(self):
        if not self.isbadge:
            self.isbadge = True
        else:
            self.isbadge = False

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
            image = Image.open(open(filename, 'rb')).resize((800, 600), Image.ANTIALIAS)
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
        self.tool6.config(state=NORMAL)
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
        h = 670

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        # geometry: x,y + x on screen + y on screen
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    @staticmethod
    def exit():
        exit(0)


def main():
    root = Tk()
    root.resizable(0, 0)
    Gui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
