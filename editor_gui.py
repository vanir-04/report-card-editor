from tkinter import *
window=Tk()

#Separation
canvas1=Canvas()
canvas1.config(width='1280', height='720')
line1=canvas1.create_line(290,60,290,720,fill='black',width=2, dash = (2,5))
line2 = canvas1.create_line(0,60,1280,60, fill = 'black', width = 3)
canvas1.pack()

#Adding Widgets
window.title('Hello Python')
window.geometry("1280x720")
window.tk_setPalette(background="white")
Topic = Label(window, text="Student Marksheet", fg = "green", font = ("Times New Roman", 30))
Topic.place(x=500,y=10)

Nam_lbl = Label(window, text="Student Name", fg = "black", font = ("Times New Roman", 10))
Nam_lbl.place(x = 0, y = 130) 
Nam_txt = Entry(window, bd = 5)
Nam_txt.place(x = 100, y = 130)

Phy_lbl = Label(window, text ="Marks scored in Physics", fg = "black", font = ("Times New Roman",10))
Phy_lbl.place(x=360,y=200)
Che_lbl = Label(window, text ="Marks scored in Chemistry", fg = "black", font = ("Times New Roman",10))
Che_lbl.place(x=360,y=250)
Mat_lbl = Label(window, text ="Marks scored in Maths", fg = "black", font = ("Times New Roman",10))
Mat_lbl.place(x=360,y=300)
Cs_lbl =  Label(window, text ="Marks scored in CS", fg = "black", font = ("Times New Roman",10))
Cs_lbl.place(x=360,y=350)
Eng_lbl = Label(window, text ="Marks scored in English", fg = "black", font = ("Times New Roman",10))
Eng_lbl.place(x=360,y=400)

Phy_txt = Entry(window, bd = 5)
Phy_txt.place(x=510, y = 200)
Che_txt = Entry(window, bd = 5)
Che_txt.place(x=510, y = 250)
Mat_txt = Entry(window, bd = 5)
Mat_txt.place(x=510, y = 300)
Cs_txt = Entry(window, bd = 5)
Cs_txt.place(x=510, y = 350)
Eng_txt = Entry(window, bd = 5)
Eng_txt.place(x=510, y = 400)


window.mainloop()