from Tkinter import Tk, Frame, BOTH, Listbox, END, StringVar, Label


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.initUI()

    def initUI(self):
        self.parent.title("Listbox")
        self.pack(fill=BOTH, expand=1)

        acts = ['pic_1', 'pic_2', 'pic_3']

        lb = Listbox(self)
        for i in acts:
            lb.insert(END, i)

        lb.bind("<<ListboxSelect>>", self.onSelect)
        lb.pack(pady=15)

        self.label.pack()

    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)

def main():
    root = Tk()
    app = Example(root)
    root.geometry("1024x768+300+300")
    root.mainloop()

if __name__ == "__main__":
    main()