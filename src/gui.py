import tkFileDialog
from Tkinter import *
from PIL import ImageTk, Image
import os


class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.getimagePath)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exitprogram)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.imageFilePath = StringVar()
        self.labelImageFile = Label(root, textvariable=self.imageFilePath)

        root.config(menu=self.menubar)

    def create_widgets(self):
        self.viewwindow = Canvas(self, bg="white")
        self.viewwindow.configure(width=1024, height=768)
        self.viewwindow.pack(side=TOP, fill=BOTH, expand=True)

    def getimage(self, filename):
        basewidth = 500

        image = Image.open(filename)
        wpercent = (basewidth/float(image.size[0]))
        hsize = (float(image.size[1])*float(wpercent))
        preview = image.resize((basewidth, int(hsize)), Image.ANTIALIAS)
        preview = ImageTk.PhotoImage(preview)
        image = ImageTk.PhotoImage(image)
        print str(image.width()) + " " + str(image.height())

        self.viewwindow.image = preview
        self.viewwindow.create_image(Canvas.winfo_width(self.viewwindow) / 2, Canvas.winfo_height(self.viewwindow) / 2, anchor=CENTER, image=preview, tags="bg_img")

        test = Label(root, textvariable=filename)
        test.pack()

    def getimagePath(self):
        filename = tkFileDialog.askopenfilename()
        print filename
        self.imageFilePath.set(filename)
        print self.imageFilePath
        self.getimage(filename)


    def exitprogram(self):
        exit(0)


root = Tk()
root.resizable(0, 0)
root.geometry("1024x768")
root.title("Wasserzeicheninator v0.1")
root.wm_state('normal')

app = Application(root)

root.mainloop()
