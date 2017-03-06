from Tkinter import Tk, Frame, Canvas
import ImageTk

t = Tk()
t.title("Transparency")


frame2 = Frame()
frame2.grid()

canvas = Canvas(frame2, bg="#333", width=500, height=500)
canvas.grid()

photoimage = ImageTk.PhotoImage(file="logosmall.png")
canvas.create_image(150, 100, image=photoimage)

t.mainloop()