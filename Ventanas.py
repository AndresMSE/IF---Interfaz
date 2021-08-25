import tkinter as tk
from tkinter import messagebox


def validar():
    if entrada1.get()=="lili":
        abrirventana2()
    else:
        messagebox.showwarning("cuidado!","pass incrrecto")

def abrirventana2():
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('380x300+500+100')
    win.configure(background='dark turquoise')
    win.title("ventana2")
    e3=tk.Label(win,text="Bienvnidos a la segunda ventana",bg="pink",fg="white")
    e3.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    boton2=tk.Button(win,text='Ok close',command=win.destroy)
    boton2.pack(side=tk.TOP)

def cerrarventana():
    ventana.destroy()


ventana=tk.Tk()
ventana.title("ventana 1")
ventana.geometry('400x400')
ventana.configure(background='yellow')

e1=tk.Label(ventana,text="password:", bg="blue", fg="white")
e1.pack(padx=5,pady=5,ipadx=5,ipady=5)
entrada1=tk.Entry(ventana)
entrada1.pack(fill=tk.X, padx=5,pady=5,ipadx=5,ipady=5)

boton=tk.Button(ventana,text="nueva ventana",fg="red",command=abrirventana2)
boton.pack(side=tk.TOP)
boton3=tk.Button(ventana,text="Vaiidar Pass", fg="Green",command=validar)
boton3.pack(side=tk.TOP)
ventana.mainloop()