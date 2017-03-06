from Tkinter import Tk, BOTH, BooleanVar, Frame, Checkbutton


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.var = BooleanVar()

        self.initUI()

    def initUI(self):
        self.parent.title("")
        self.pack(fill=BOTH, expand=True)

        cb = Checkbutton(self, text="Show title", variable=self.var, command=self.onClick)
        cb.place(x=50, y=50)

    def onClick(self):
        if self.var.get() == True:
            self.master.title("Checkbutton")
        else:
            self.master.title("")


def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == "__main__":
    main()
