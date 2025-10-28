from tkinter import *

root = Tk()

root.title("Pat Machine")
root.geometry("600x400")

gen = Button(root, text="Generate", width=10, font=("", 15))
gen.place(anchor=SE, relx=0.9, rely=0.9)

root.mainloop()
