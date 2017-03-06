from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import os

class Application:

    def __init__(self, master):
        frame = Frame(master, width=200, height=200)
        frame.pack()

        self.canvas = Canvas(bg="white")
        self.imageFilePath = StringVar()

        path = os.path.abspath("test.jpg")

        self.imageFilePath.set(path)

        self.menubar = Menu()
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.select_image)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exitprogram)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.labelFile = Label(frame, textvariable=self.imageFilePath)

        root.config(menu=self.menubar)

    def select_image(self):
        filename = askopenfilename()
        self.imageFilePath.set(filename)
        self.show_image()

    def exitprogram(self):
        exit(0)

    def show_image(self):
        basewidth = 500

        image = Image.open(self.labelFile)
        wpercent = (basewidth / float(image.size[0]))
        hsize = (float(image.size[1]) * float(wpercent))
        preview = image.resize((basewidth, int(hsize)), Image.ANTIALIAS)
        preview = ImageTk.PhotoImage(preview)
        image = ImageTk.PhotoImage(image)
        print str(image.width()) + " " + str(image.height())

        self.canvas.image = preview
        self.canvas.create_image(Canvas.winfo_width(self.canvas) / 2, Canvas.winfo_height(self.canvas) / 2,
                                     anchor=CENTER, image=preview, tags="bg_img")


root = Tk()
root.title("wasinator v2")
root.geometry("1024x768")
app = Application(root)
root.mainloop()
