#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5 import uic, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
import numpy as np
import os
from pandas import ExcelWriter
matplotlib.use("TkAgg")
import seaborn as sns
import csv
import CWT as wv
import SSA as ssa


# Cargamos los datod tipo Ui para poder representar el programa en interfaz
qtCreatorFile = "Menus.ui"  # Nombre del archivo aquí.
Acceso = "Acceso.ui"
Mensajes = "Mensajes.ui"
MenuFile="MenuFile.ui"
MenuFunciones="Funciones.ui"
MenuGraficas="MenuGraficar.ui"
MenuExportar="Exportar.ui"
MenuVerArchivos="VerArchivos.ui"
MenuAnalizar="AnalizarMenu.ui"
MetodoFourier="MetodoFourier.ui"
MenuWB="MenuWB.ui"
Analizar_SSA = 'SSA.ui'
EstadisticasDescriptivas = 'EstadisticasDescriptivas.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
Ui_Acceso, BaseAcceso = uic.loadUiType(Acceso)
Ui_Mensaje, BaseMensaje = uic.loadUiType(Mensajes)
Ui_MenuFile, BaseMenuFile = uic.loadUiType(MenuFile)
Ui_Funciones, BaseFunciones = uic.loadUiType(MenuFunciones)
Ui_MenuGraficas,BaseGraficas=uic.loadUiType(MenuGraficas)
Ui_MenuExportar,BaseExportar=uic.loadUiType(MenuExportar)
Ui_MenuVerArchivos,BaseVerArchivos=uic.loadUiType(MenuVerArchivos)
Ui_MenuAnalizar,BaseMenuAnalizar=uic.loadUiType(MenuAnalizar)
Ui_MetodoFourier,BaseMetodFourier=uic.loadUiType(MetodoFourier)
Ui_MenuWB,BaseMenuWB=uic.loadUiType(MenuWB)
Ui_MenuSSA,BaseAnalizar_SSA=uic.loadUiType(Analizar_SSA)
Ui_EstadisticasDescriptivas, BaseEstadisticasDescriptivas= uic.loadUiType(EstadisticasDescriptivas)

# In[3]:


#Definiremos el estado #No autaorizado, si se dio acceso al usuario cambiara a #Autorizado
Estado = "No autorizado"
Archivo = 0
SerieMetodo= "Vacio"
SerieGraficar=""
SerieGraficar1=""

# Ventana principal del programa
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QtBaseClass, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Boton.clicked.connect(self.AbrirAcceso)
        self.Boton.clicked.connect(self.close)
    def AbrirAcceso(self):
        # self.destroy()
       self.Funciones = Funciones()
       self.Funciones.show()

# Ventana de Acceso
class Acceso(QtWidgets.QDialog, Ui_Acceso):

    def __init__(self):
        super(BaseAcceso, self).__init__()
        self.setupUi(self)
        self.BotonIngresar.clicked.connect(self.Entrar)
        self.BotonCancelar.clicked.connect(self.close)
    def Entrar(self):
        Usuario = self.Usuario.text()
        Contrasena = self.Contrasena.text()
        # Eventos relacionados para confirmar las identificaciones del usuario

        if Usuario == "Diego" and Contrasena == "123":
            global Estado
            Estado = "Autorizado"
            # Cerramos el Formulario
            self.close()
        self.Mensajes = Aviso()
        self.Mensajes.show()

        if Estado=="Autorizado":
         self.Mensajes.close()
         self.Funciones = Funciones()
         self.Funciones.show()
         #self.close()
class Aviso(QtWidgets.QDialog, Ui_Mensaje):
    def __init__(self):
        super(BaseMensaje, self).__init__()
        self.setupUi(self)
        self.NotificarAcceso()

    def NotificarAcceso(self):
        global Estado
        if Estado == "Autorizado":
            self.Mensaje.setText("Acceso Permitido")

            #Estado="No Autorizado"

        else:
            self.Mensaje.setText("Acceso Denegado")
#Menu de Funciones
class Funciones(QtWidgets.QMainWindow, Ui_Funciones):
    def __init__(self):
        super(BaseFunciones, self).__init__()
        self.setupUi(self)
        ################# Botones #########################
        # Importar Datos
        self.SubirArchivo.clicked.connect(self.ImportarDatos)
        # Menu de GRaficas
        self.Graficar.clicked.connect(self.MenuGraficas)
        self.ExportarArchivos.clicked.connect(self.MenuExportar)
        self.VerArchivos.clicked.connect(self.MenuVerDatos)
        self.Analizar.clicked.connect(self.MenuAnalisis)

    def ImportarDatos(self):
        # Al presionar el boton de SubirArchivo desplegamos un objeto de la clase lector csv
         self.close()
         self.Menu = LectorCsv()
         self.Menu.show()
    def MenuGraficas(self):
        self.close()
        self.Menu=MGraficas()
        self.Menu.show()
    def MenuExportar(self):
        self.close()
        self.Menu=MenuExportarDatos()
        self.Menu.show()
    def MenuVerDatos(self):
        self.close()
        self.VDatos=MenuVerDato()
        self.VDatos.show()

    def MenuAnalisis(self):
            self.close()
            self.CrearAnalisis = Analisis()
            self.CrearAnalisis.show()
#Menu lector de csv
class LectorCsv(QtWidgets.QMainWindow, Ui_MenuFile):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Importar1.clicked.connect(self.getCSV)
        self.Guardar.clicked.connect(self.CargarDatos)
        self.Cancelar.clicked.connect(self.VolverMenu)

    def getCSV(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if filePath != "":
            print("Dirección", filePath)  # Opcional imprimir la dirección del archivo
            self.df = pd.read_csv(str(filePath))
            self.Direccion.setText(str(filePath))
            self.ComboHoja.clear()
            self.ComboHoja.addItems(list(self.df.columns.values))
            global Archivo
            Archivo = pd.read_csv(str(filePath))
            print(Archivo.columns)
            
    def VolverMenu(self):
        self.VolverMenu = Funciones()
        self.close()
        self.VolverMenu.show()

    def CargarDatos(self):

        Base = pd.read_csv("Base.csv")
            #Tranformamos la lista a un dataframe de la
        Base = pd.DataFrame(Base)
        global Archivo
        aux=pd.DataFrame(Archivo)
        Nombres=aux.columns
        Indice=len(Base.columns)
        for x in Nombres:
         Base.insert(Indice,x,aux[x],True)
         Indice=Indice+1
        Base.to_csv('Base.csv',header=True,index=False)
#Menu Exportar
class MenuExportarDatos(QtWidgets.QMainWindow, Ui_MenuExportar):

    def __init__(self):
        super(BaseExportar, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Cancelar.clicked.connect(self.RegresaMenu)
        self.TipoArchivo.addItems(list(['csv','xml']))
        self.Exportar.clicked.connect(self.Exportare)


        Ittems=self.df.columns.values
        for x in Ittems:
         self.ListaExportar.addItem(x)

    def RegresaMenu(self):
        self.close()
        self.Menu = Funciones()
        self.Menu.show()


    def Exportare(self):
        # print("sss")
        data=self.ListaExportar.selectedItems()
        df=pd.read_csv("Base.csv")
        selected=[]
        for x in range(len(data)):
            selected.append(self.ListaExportar.selectedItems()[x].text())
        Exportable=pd.DataFrame([])
        contador=0
        for i in selected:
            Exportable.insert(contador,str(i),df[i],True)
            contador=contador+1
        Exportable=pd.DataFrame(Exportable)
        Nombre=self.NombreArchivo.text()
        Tipo=str(self.TipoArchivo.currentText())
        if Tipo =='csv':
         Exportable.to_csv(str(Nombre)+".csv",index=False,header=True)
        else:
            writer = ExcelWriter(str(os.getcwd())+'\\'+str(Nombre)+'.xlsx')
            Exportable.to_excel(writer, 'Datos Exportados', index=False)
            writer.save()
#Menu Ver Datos
class MenuVerDato(QtWidgets.QMainWindow, Ui_MenuVerArchivos):

    def __init__(self):
        super(BaseVerArchivos, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Cancelar.clicked.connect(self.RegresaMenu)
        self.Eliminar.clicked.connect(self.Eliminare)

        Ittems=self.df.columns.values
        for x in Ittems:
         self.ListaExportar.addItem(x)

    def RegresaMenu(self):
        self.close()
        self.Menu = Funciones()
        self.Menu.show()


    def Eliminare(self):
        # print("sss")
        data=self.ListaExportar.selectedItems()
        df=pd.read_csv("Base.csv")
        Nuevabase=pd.DataFrame(df)
        selected=[]
        for x in range(len(data)):
            selected.append(self.ListaExportar.selectedItems()[x].text())
        Exportable=pd.DataFrame([])

        for i in selected:
         Nuevabase=Nuevabase.drop([i],axis=1)

        Nuevabase.to_csv("Base.csv",index=False,header=True)
# Menu de Graficas
class MGraficas(QtWidgets.QMainWindow,Ui_MenuGraficas):
     def __init__(self):
        super(BaseGraficas, self).__init__()
        self.df = pd.read_csv("Base.csv")
        self.setupUi(self)
        self.Cancelar.clicked.connect(self.RegresaMenu)
        self.SerieTiempo.addItems(list(self.df.columns.values))
        self.SerieTiempo_2.addItems(list(self.df.columns.values))
        self.Graficar.clicked.connect(self.Graficas)
        self.ColorGrafico.addItems(list(['Rojo','Azul','Cyan','Amarillo']))
        self.ColorGrafico_2.addItems(list(['Rojo', 'Azul', 'Cyan', 'Amarillo']))
        self.TipoDeGraficoComboBox.addItems(list(['Animacion', 'Boxplot', 'Linea', 'Correlograma']))
        self.TipoDeGraficoComboBox_2.addItems(list(['Animacion', 'Boxplot', 'Linea', 'Correlograma']))
        self.Anadir.clicked.connect(self.Aneade)
        self.Anadir_2.clicked.connect(self.Aneade1)


     def RegresaMenu(self):
         self.close()
         self.Menu=Funciones()
         self.Menu.show()

     def Graficas(self):
         self.datos=self.df[str(self.SerieTiempo.currentText())]
         self.datos1=self.df[str(self.SerieTiempo_2.currentText())]

         velocidad=int(self.velocidadLineEdit.text())
         x = np.arange(0, 1500, 3 / 1500)
         y=self.datos
         z=self.datos1
         fig, (ax1, ax2) = plt.subplots(2, 1, facecolor='k', edgecolor='k')
         plt.xticks(color='white')
         plt.yticks(color='white')
         plt.grid(color='white')



         data_skip = 5
         #plt.set_facecolor("black")

         def init_func():
             # ax.clear()
             plt.xlabel('Tiempo',color='white')
             plt.ylabel('voltaje',color='white')
             ax1.set_title(str(self.SerieTiempo.currentText()))
             ax2.set_title(str(self.SerieTiempo_2.currentText()))
             ax1.set_facecolor('k')
             ax2.set_facecolor('k')
             ax1.grid()


             plt.figure(figsize=(20, 20), facecolor='k', edgecolor='k')
         fig.tight_layout()
         def Selecionarcolor(text):

             if text == "Rojo":
                 colore = "red"
             if text == "Azul":
                 colore = "blue"
             if text == "Cyan":
                 colore = "cyan"
             if text == "Amarillo":
                 colore = "yellow"

             return colore

         def update_plot(i):

             Color = str(self.ColorGrafico.currentText())
             Color1 = str(self.ColorGrafico_2.currentText())
             a = Selecionarcolor(Color)
             b = Selecionarcolor(Color1)

             ax1.plot(x[i:i + data_skip], y[i:i + data_skip], color=a)
             ax2.plot(x[i:i + data_skip], z[i:i + data_skip], color=b)

         anim = FuncAnimation(fig,
                              update_plot,
                              frames=np.arange(0, len(y), data_skip),
                              init_func=init_func,
                              interval=velocidad)
         ax = plt.gca()
         ax.set_facecolor('k')
         plt.show(block=True)
     def Aneade(self):

         def Selecionarcolor1(text):

             if text == "Rojo":
                 colore = "red"
             if text == "Azul":
                 colore = "blue"
             if text == "Cyan":
                 colore = "cyan"
             if text == "Amarillo":
                 colore = "yellow"

             return colore
         # Tipo de Grafico primer serie
         TipoGrafico = str(self.TipoDeGraficoComboBox.currentText())

         global SerieGraficar
         SerieGraficar = str(self.SerieTiempo.currentText())

         if TipoGrafico =='Boxplot':
             plt.figure(figsize=(20, 5))
             Color = str(self.ColorGrafico.currentText())
             Color=Selecionarcolor1(Color)
             ax = sns.boxplot(data=self.df[str(self.SerieTiempo.currentText())], orient="h", color=Color)
             self.estadisticas = Estadisticas()
             self.estadisticas.show()
             plt.show(block=True)

         if TipoGrafico == 'Linea':
             plt.figure(figsize=(20, 5),facecolor='k',edgecolor='k')
             Color = str(self.ColorGrafico.currentText())
             Color=Selecionarcolor1(Color)
            # global SerieGraficar
            # SerieGraficar = str(self.SerieTiempo.currentText())
             Tiempo_de_medicion = 0.002
             x1 = Tiempo_de_medicion * np.arange(0, len(self.df[str(self.SerieTiempo.currentText())]))
             ax = plt.plot(x1,self.df[str(self.SerieTiempo.currentText())],color=Color)
             plt.xticks(color='white')
             plt.yticks(color='white')
             plt.grid(color='white')

             plt.xlabel('tiempo (s)',
                        fontdict={'color': 'white',
                                  'weight': 'bold',
                                  'size': 16})
             plt.ylabel('Amplitud (mV)',
                        fontdict={'color': 'white',
                                  'weight': 'bold',
                                  'size': 16})


             #ax.spines['bottom'].set_color('red')
             #ax.spines['top'].set_color('red')
             #ax.xaxis.label.set_color('red')

             self.estadisticas = Estadisticas()
             self.estadisticas.show()
             ax = plt.gca()
             ax.set_facecolor('k')

             plt.show(block=True)


         if TipoGrafico =='Correlograma':
             plt.figure(figsize=(20, 5))
             #global SerieGraficar
             #SerieGraficar = str(self.SerieTiempo.currentText())
             df=pd.read_csv("Base.csv")
             df=pd.DataFrame(df)
             # Default heatmap
             p1 = sns.heatmap(df)
             self.estadisticas = Estadisticas()
             self.estadisticas.show()
             plt.show(block=True)

         #Aneade 2
     def Aneade1(self):

             def Selecionarcolor1(text):

                 if text == "Rojo":
                     colore = "red"
                 if text == "Azul":
                     colore = "blue"
                 if text == "Cyan":
                     colore = "cyan"
                 if text == "Amarillo":
                     colore = "yellow"

                 return colore

             # Tipo de Grafico primer serie
             TipoGrafico = str(self.TipoDeGraficoComboBox_2.currentText())
             global SerieGraficar
             SerieGraficar = str(self.SerieTiempo_2.currentText())

             if TipoGrafico == 'Boxplot':
                 plt.figure(figsize=(20, 5))
                 Color = str(self.ColorGrafico_2.currentText())
                 Color = Selecionarcolor1(Color)
                 ax = sns.boxplot(data=self.df[str(self.SerieTiempo_2.currentText())], orient="h", color=Color)
                 self.estadisticas = Estadisticas()
                 self.estadisticas.show()
                 plt.show(block=True)

             if TipoGrafico == 'Linea':
                 plt.figure(figsize=(20, 5))
                 Color = str(self.ColorGrafico_2.currentText())
                 Color = Selecionarcolor1(Color)
                 ax = plt.plot(self.df[str(self.SerieTiempo_2.currentText())], color=Color)
                 self.estadisticas = Estadisticas()
                 self.estadisticas.show()
                 plt.show(block=True)


             if TipoGrafico == 'Correlograma':
                 df = pd.read_csv("Base.csv")
                 df = pd.DataFrame(df)
                 # Default heatmap
                 plt.figure(figsize=(20, 5))
                 p1 = sns.heatmap(df)
                 self.estadisticas = Estadisticas()
                 self.estadisticas.show()
                 plt.show(block=True)
# Menu de Estadisticas
class Estadisticas(QtWidgets.QMainWindow, Ui_EstadisticasDescriptivas):
    def __init__(self):
        super(BaseEstadisticasDescriptivas, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.NMuestras.setText(str(len(self.df[str(SerieGraficar)])))
        self.Media.setText(str(round(self.df[str(SerieGraficar)].mean(),3)))
        self.Varianza.setText(str(round(self.df[str(SerieGraficar)].var(ddof=0),3)))
        self.Desviacion.setText(str(round(self.df[str(SerieGraficar)].std(),3)))
        self.Minimo.setText(str(self.df[str(SerieGraficar)].min()))
        self.Maximo.setText(str( self.df[str(SerieGraficar)].max()))
#Menu Analisis
class Analisis(QtWidgets.QMainWindow, Ui_MenuAnalizar):
    def __init__(self):
        super(BaseMenuAnalizar, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Series.addItems(list(self.df.columns.values))
        self.Metodo.addItems(list(['Fourier','Transformada Contínua Wavelet','Singular Spectrum Analysis']))
        self.Siguiente.clicked.connect(self.AbrirOpcionesMetodo)
        self.Cancelar.clicked.connect(self.Cancel)

    def AbrirOpcionesMetodo(self):
        Metodo = self.Metodo.currentText()
        global SerieMetodo
        SerieMetodo=self.Series.currentText()
        print(Metodo)
        if Metodo == "Fourier":
            df = pd.read_csv("Base.csv")
            A1 = df[str(SerieMetodo)]
            # Construir el eje Y (amplitud)
            N2 = len(A1)
            F2 = np.fft.fft(A1)  # Calcula la transformada de Fourier de los datos que tenemos en f
            Tiempo_de_medicion = 0.002
            F_medicion = 1 / Tiempo_de_medicion
            frequency_fourier2 = np.fft.fftfreq(N2, F_medicion)[:N2 // 2]
            plt.figure(figsize=(20, 5),facecolor='k',edgecolor='k')
            # construir el eje X (frecuencias)
            import math
            Frecuencia2 = (F_medicion / 2) * np.arange(0, math.floor(N2 / 2)) / math.floor(N2 / 2)

            # plt.plot(frequency_fourier2,np.abs(F2[0:N2//2]), c='cyan')
            plt.plot(Frecuencia2, np.abs(F2[0:N2 // 2]), c='red')

            plt.title('Análisis espectral',
                                fontdict={'family': 'serif',
                                          'color': 'black',
                                          'weight': 'bold',
                                          'size': 20},
                                loc='center',color='white')
            plt.xlabel('Frequency (Hz)',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16},color='white')
            plt.ylabel('Potencia',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16},color='white')
            plt.yscale('log')
            plt.xticks(color='white')
            plt.yticks(color='white')
            plt.grid(color='white')
            ax = plt.gca()
            ax.set_facecolor('k')
            self.close()
            self.MetFourier = MetFou()
            self.MetFourier.show()
            plt.show(block=True)


        elif Metodo == 'Transformada Contínua Wavelet':
            self.close()
            self.MetCWT = MenuWeb()
            self.MetCWT.show()
        elif Metodo == 'Singular Spectrum Analysis':
            self.close()
            self.MetSSA = MenuSSA()
            self.MetSSA.show()
    def Cancel(self):
            self.close()
            self.Menu = Funciones()
            self.Menu.show()
#Metodo Fourirer
class MetFou(QtWidgets.QMainWindow, Ui_MetodoFourier):
    def __init__(self):
        super(BaseMetodFourier, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Aceptar.clicked.connect(self.Analizare)
        self.Atras.clicked.connect(self.Cancel)
    def Analizare(self):
        Metodo ="Fourier"
        Serie= SerieMetodo
        print(Serie)
        if Metodo == "Fourier":
            Umbral1=self.Umbral.text()
            umbral_ruido = int(Umbral1)
            Tiempo_de_medicion = 0.002
            x1 = Tiempo_de_medicion * np.arange(0, 1500)
            F_medicion = 1 / Tiempo_de_medicion
            df = pd.read_csv("Base.csv")
            A1=df[str(Serie)]
            N2 = len(A1)
            F2 = np.fft.fft(A1)
            import math
            Frecuencia2 = (F_medicion / 2) * np.arange(0, math.floor(N2 / 2)) / math.floor(N2 / 2)

            señal_limpia = []

            for i in range(0, len(F2)):
                if np.abs(F2[i]) > umbral_ruido:
                    señal_limpia.append(F2[i])
                elif np.abs(F2[i]) <= umbral_ruido:
                    señal_limpia.append(0)

            fi = np.fft.ifft(señal_limpia)
            plt.figure(figsize=(20, 5), facecolor='k', edgecolor='k')
            plt.xticks(color='white')
            plt.yticks(color='white')
            plt.grid(color='white')
            ax = plt.gca()
            ax.set_facecolor('k')
            plt.ylim(A1.min()-A1.std(), A1.max()+A1.std())
            plt.plot(x1, A1, label='Señal original',color='Dimgray',linewidth=1.5)
            plt.plot(x1, fi, color="red", label='Señal filtrada',linewidth=2)
            plt.xlabel('tiempo (s)',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16},color='white')
            plt.ylabel('Amplitud (mV)',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16},color='white')
            plt.legend(loc="upper left")
            plt.show(block=True)

    def Cancel(self):
            self.close()
            self.Menu = Analisis()
            self.Menu.show()

    #def MenuAnalizarr(self):
'''Clase para análisis Wavelet'''
class MenuWeb(QtWidgets.QMainWindow, Ui_MenuWB):
    def __init__(self):
        super(BaseMenuWB, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Aceptar.clicked.connect(self.Analizar)
        self.Cancelar.clicked.connect(self.VeMenuAnalizar)
    def VeMenuAnalizar(self):
        self.close()
        self.Menu = Analisis()
        self.Menu.show()
    def Analizar(self):
        Serie = SerieMetodo
#         time_s = len(Serie)/fmuestra
        time_s = float(self.duracion.text())
        freqm = int(self.frecm.text())
        fi = float(self.FrecuenciaInicial.text())
        ff = float(self.FrecuenciaFinal.text())
        ni = int(self.CicloInicial.text())
        nf = int(self.CiclosFinal.text())
        fint = float(self.IncrementoFrecuencias.text())
        df = pd.read_csv("Base.csv")
        signal = df[str(Serie)]
        spect= wv.MRA(signal*1000,fi,ff,fint,ni,nf,freqm) #Obtenemos el espectrograma
        print('CWT finished')
        plt.figure(figsize=(15,7)) #Declaramos el espacio de figura para graficar
        #Utilizamos la función imshow para graficar las intensidades de los valores de la matriz
        plt.imshow(spect,extent=[0,time_s,ff,fi],aspect='auto',cmap='turbo') 
        plt.colorbar(extend='both',label=r'Potencia $[mV^2/sHz]$')
        plt.clim(0, spect.max());
        plt.gca().invert_yaxis() #Acomodamos y etiquetamos los ejes
        plt.xlabel('Tiempo[s]')
        plt.ylabel('Frecuencia[Hz]')
        plt.title(f'Espectrograma en potencia: $|X (t,f)|^2$ - Serie: {Serie}')
        plt.show(block=True)
'''Clase para análisis SSA'''
class MenuSSA (QtWidgets.QMainWindow, Ui_MenuSSA):
    def __init__(self):
        super(BaseAnalizar_SSA, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv('Base.csv')
        self.Iniciar.clicked.connect(self.Analizar)
        self.Regresar.clicked.connect(self.VeMenuAnalizar)
    def VeMenuAnalizar(self):
        self.close()
        self.Menu = Analisis()
        self.Menu.show()
    def Analizar(self):
        import re
        Serie = SerieMetodo
        length = float(self.duracion.text())
        freqm = int(self.frecm.text())
        time_s = np.linspace(0,length,int(length*freqm))
        L = int(self.VentanaL.text())
        user = self.Ncomp.text()
        user2 = self.Ncomp2.text()
        Comp = re.findall('\d+',user)
        Comp2 = re.findall('\d+-\d+',user2)
        comp_int = []
        [comp_int.append(int(i)) for i in Comp]
        df = pd.read_csv('Base.csv')
        signal = df[str(Serie)]*1000
        lval,gklist,wMatrix = ssa.SSA(signal,L)
        print('SSA finished')
        plt.figure(figsize=(15,7))
        for i in Comp2:
                start,end =  int(re.findall('\d+',i)[0]),int(re.findall('\d+',i)[1])
                arange = np.arange(start,end+1)
                for j in arange:
                    graph_c = j
                    plt.plot(time_s,gklist[j-1], label= f'$C - {graph_c}$' )
                    plt.title(f'Componentes extraidas: Serie: {Serie}: {user} - Ventana: {L}')
                    plt.xlabel('Tiempo [s]')
                    plt.ylabel(r'Amplitud [mv]')
                    plt.grid()
                    plt.legend()
                    plt.show(block=False)
        for i in range(len(comp_int)):
            graph_c = comp_int[i]
            plt.plot(time_s,gklist[graph_c-1],label=f'$C - {graph_c}$')
            plt.title(f'Componentes extraidas: Serie: {Serie} - Ventana: {L}')
            plt.xlabel('Tiempo [s]')
            plt.ylabel(r'Amplitud [mv]')
            plt.legend()
            plt.show(block=False)
        plt.grid()
        if self.ScreeDbox.isChecked()==True:
            k=np.arange(len(lval))
            k=k+1
            fig,axs = plt.subplots(1,2,figsize=(15,5))
            axs[0].plot(k,lval,'-x',color='blue')
            axs[0].set_xscale('log')
            axs[0].set_yscale('log')
            axs[0].set_xlabel('Número de órden k')
            axs[0].set_ylabel(r'Varianza parcial $\lambda_k$ - Ventana {L}')
            axs[0].grid()

            axs[1].plot(k,lval/sum(lval),'-x',color='blue')
            axs[1].set_xscale('log')
            axs[1].set_yscale('log')
            axs[1].set_xlabel('Número de órden k')
            axs[1].set_ylabel(r'Varianza parcial fraccional $\lambda_k/\lambda_{tot}$ - Ventana: {L}')
            axs[1].grid()
        if self.wMatrizbox.isChecked()==True:
            x=np.arange(1, 20, 2)
            y=x+1
            plt.figure(figsize=(7,7)) #Declaramos el espacio de figura para graficar
            plt.imshow(wMatrix,cmap=plt.cm.binary);
            plt.title(f'Matriz de correlación - Serie:{Serie} - Ventana: {L}')
            plt.colorbar()
            plt.xticks(x,y)
            plt.yticks(x,y)
        plt.grid()
        plt.show(block=True)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


# In[ ]:




