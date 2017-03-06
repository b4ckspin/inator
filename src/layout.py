from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH, RIGHT, RAISED
from ttk import Frame, Style, Button


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
        w = 2000
        h = 1000

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        # geometry: x,y + x on screen + y on screen
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):

        self.parent.title("Tutorial")
        self.pack(fill=BOTH, expand=1)

        # Style setting
        Style().configure("TFrame", background='#333')

        # Button Frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        closeButton = Button(self, text="Close")
        closeButton.pack(side=RIGHT, padx=5, pady=5)

        # absolute image positioning
        img1 = Image.open("ybNzUYG.jpg")
        img1pi = ImageTk.PhotoImage(img1)
        label1 = Label(self, image=img1pi)
        label1.image = img1pi
        label1.place(x=20, y=20)

        img2 = Image.open("QMYxaux.jpg")
        img2pi = ImageTk.PhotoImage(img2)
        label2 = Label(self, image=img2pi)
        label2.image = img2pi
        x = img1pi.width() + 40
        label2.place(x=x, y=20)

        img3 = Image.open("test.jpg")
        img3pi = ImageTk.PhotoImage(img3)
        label3 = Label(self, image=img3pi)
        label3.image = img3pi
        x = x + img2pi.width() + 20
        label3.place(x=x, y=20)


def main():
    root = Tk()
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
