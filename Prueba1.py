#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from Menu import *
from tkinter import messagebox



# La clase 'Aplicacion' ha crecido. En el ejemplo se incluyen
# nuevos widgets en el método constructor __init__(): Uno de
# ellos es el botón 'Info'  que cuando sea presionado llamará
# al método 'verinfo' para mostrar información en el otro
# widget, una caja de texto: un evento ejecuta una acción:

class Aplicacion():
    def __init__(self):
        # En el ejemplo se utiliza el prefijo 'self' para
        # declarar algunas variables asociadas al objeto
        # ('mi_app')  de la clase 'Aplicacion'. Su uso es
        # imprescindible para que se pueda acceder a sus
        # valores desde otros métodos:

        self.raiz = Tk()
        self.raiz.geometry('500x500')
        self.raiz.title('Analisis de Series de Tiempo')
        self.raiz.configure(background='black')




        ####################################################
        ###########    SALIR  ##############################
        ####################################################
        # Define el botón 'self.bsalir'. En este caso
        # cuando sea presionado, el método destruirá o
        # terminará la aplicación-ventana 'self.raíz' con
        # 'self.raiz.destroy'

        self.bsalir = ttk.Button(self.raiz, text='Salir',
                                 command=self.raiz.destroy)
        # Coloca el botón 'self.bsalir' a la derecha del
        # objeto anterior.

        self.bsalir.pack(side=RIGHT)

        # El foco de la aplicación se sitúa en el botón
        # 'self.binfo' resaltando su borde. Si se presiona
        # la barra espaciadora el botón que tiene el foco
        # será pulsado. El foco puede cambiar de un widget
        # a otro con la tecla tabulador [tab]

        ####################################################
        ###########    PLOTEAR #############################
        ####################################################
        # Definimos el boton que queremos que vaya a plotear
        self.plotear = ttk.Button(self.raiz, text="Grafica", command=self.graficar)
        self.plotear.pack(side=RIGHT)
        ####################################################
        ###########    Regresa MENU #######################
        ####################################################
        # Definimos el boton que queremos que vaya a plotear
        self.VolverMenu = ttk.Button(self.raiz, text="Graficar", command=self.RegresaMenu)
        self.VolverMenu.pack(side=RIGHT)

        self.raiz.mainloop()

    def graficar(self):
        import matplotlib
        matplotlib.use("TkAgg")
        import pandas as pd
        import numpy as np
        from matplotlib.animation import FuncAnimation
        import matplotlib.pyplot as plt
        df = pd.read_csv("Jenny.csv", )
        Reposo = df["reposo"].values
        plt.plot(Reposo)
        plt.show()

    def verinfo(self):
        # Borra el contenido que tenga en un momento dado
        # la caja de texto

        self.tinfo.delete("1.0", END)

        # Obtiene información de la ventana 'self.raiz':

        info1 = self.raiz.winfo_class()
        info2 = self.raiz.winfo_geometry()
        info3 = str(self.raiz.winfo_width())
        info4 = str(self.raiz.winfo_height())
        info5 = str(self.raiz.winfo_rootx())
        info6 = str(self.raiz.winfo_rooty())
        info7 = str(self.raiz.winfo_id())
        info8 = self.raiz.winfo_name()
        info9 = self.raiz.winfo_manager()

        # Construye una cadena de texto con toda la
        # información obtenida:

        texto_info = "Clase de 'raiz': " + info1 + "\n"
        texto_info += "Resolución y posición: " + info2 + "\n"
        texto_info += "Anchura ventana: " + info3 + "\n"
        texto_info += "Altura ventana: " + info4 + "\n"
        texto_info += "Pos. Ventana X: " + info5 + "\n"
        texto_info += "Pos. Ventana Y: " + info6 + "\n"
        texto_info += "Id. de 'raiz': " + info7 + "\n"
        texto_info += "Nombre objeto: " + info8 + "\n"
        texto_info += "Gestor ventanas: " + info9 + "\n"

        # Inserta la información en la caja de texto:

        self.tinfo.insert("1.0", texto_info)

    def RegresaMenu(self):
        self.raiz.destroy()
        MENU()



def main():
    mi_app = Aplicacion()
    return 0
if __name__ == '__main__':
    main()






