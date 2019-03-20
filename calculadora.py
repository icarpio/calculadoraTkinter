from tkinter import *

def Sumar():
    resultado.set("Suma = " + str(float(vartxt1.get()) + float(vartxt2.get())))
def Restar():
    resultado.set("Resta = " + str(float(vartxt1.get()) - float(vartxt2.get())))
def Multi():
    resultado.set("Producto = " + str(float(vartxt1.get()) * float(vartxt2.get())))
def Division():
    resultado.set("Division = " + str(float(vartxt1.get()) / float(vartxt2.get())))
def Clean():
    resultado.set("")
    vartxt1.set("")
    vartxt2.set("")

ventana = Frame(height=180,width=260)
ventana.pack(padx=5,pady=5)


vartxt1 = StringVar()
txt1 = Entry(ventana,textvariable=vartxt1).place(x=0,y=0)
vartxt2 = StringVar()
txt2 = Entry(ventana,textvariable=vartxt2).place(x=130,y=0)
resultado = StringVar()
txtresultado = Entry(ventana,textvariable=resultado,width=100).place(x=0,y=145)

bsuma = Button(ventana,command=Sumar,text="Sumar",padx=43,pady=5,background="#B3FF30").place(x=0,y=25)
bres = Button(ventana,command=Restar,text="Restar",padx=43,pady=5,background="#B3FF30").place(x=130,y=25,)
bmul = Button(ventana,command=Multi,text="Producto",padx=36,pady=5,background="#B3FF30").place(x=0,y=65)
bdiv = Button(ventana,command=Division,text="Division",padx=39,pady=5,background="#B3FF30").place(x=130,y=65)
blim = Button(ventana,command=Clean,text="Clean",padx=110,pady=5,background="#EEFF5E").place(x=0,y=105)

ventana.mainloop()