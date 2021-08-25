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
import CWT as WV

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

#Definiremos el estado #No autaorizado, si se dio acceso al usuario cambiara a #Autorizado
Estado = "No autorizado"
Archivo = 0

SerieMetodo= "Vacio"


#Ventana principal del programa
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QtBaseClass, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Boton.clicked.connect(self.AbrirAcceso)
        self.Boton.clicked.connect(self.close)
    def AbrirAcceso(self):
        # self.destroy()
        self.DarAcceso = Acceso()
        self.DarAcceso.show()

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
        self.ColorGrafico.addItems(list(['Rojo','Azul','Negro','Amarillo']))
        self.ColorGrafico_2.addItems(list(['Rojo', 'Azul', 'Negro', 'Amarillo']))
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
         fig, (ax1, ax2) = plt.subplots(2, 1)
         data_skip = 5

         def init_func():
             # ax.clear()
             plt.xlabel('Tiempo')
             plt.ylabel('voltaje')
             ax1.set_title(str(self.SerieTiempo.currentText()))
             ax2.set_title(str(self.SerieTiempo_2.currentText()))

         fig.tight_layout()
         def Selecionarcolor(text):

             if text == "Rojo":
                 colore = "red"
             if text == "Azul":
                 colore = "blue"
             if text == "Negro":
                 colore = "k"
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
         plt.show(block=True)
     def Aneade(self):

         def Selecionarcolor1(text):

             if text == "Rojo":
                 colore = "red"
             if text == "Azul":
                 colore = "blue"
             if text == "Negro":
                 colore = "k"
             if text == "Amarillo":
                 colore = "yellow"

             return colore
         # Tipo de Grafico primer serie
         TipoGrafico = str(self.TipoDeGraficoComboBox.currentText())

         if TipoGrafico =='Boxplot':
             Color = str(self.ColorGrafico.currentText())
             Color=Selecionarcolor1(Color)
             ax = sns.boxplot(data=self.df[str(self.SerieTiempo.currentText())], orient="h", color=Color)
             plt.show(block=True)
         if TipoGrafico == 'Linea':
             Color = str(self.ColorGrafico.currentText())
             Color=Selecionarcolor1(Color)
             ax = plt.plot(self.df[str(self.SerieTiempo.currentText())],color=Color)
             plt.show(block=True)
         if TipoGrafico =='Correlograma':
             df=pd.read_csv("Base.csv")
             df=pd.DataFrame(df)
             # Default heatmap
             p1 = sns.heatmap(df)
             plt.show(block=True)

         #Aneade 2
     def Aneade1(self):

             def Selecionarcolor1(text):

                 if text == "Rojo":
                     colore = "red"
                 if text == "Azul":
                     colore = "blue"
                 if text == "Negro":
                     colore = "k"
                 if text == "Amarillo":
                     colore = "yellow"

                 return colore

             # Tipo de Grafico primer serie
             TipoGrafico = str(self.TipoDeGraficoComboBox_2.currentText())

             if TipoGrafico == 'Boxplot':
                 Color = str(self.ColorGrafico_2.currentText())
                 Color = Selecionarcolor1(Color)
                 ax = sns.boxplot(data=self.df[str(self.SerieTiempo_2.currentText())], orient="h", color=Color)
                 plt.show(block=True)
             if TipoGrafico == 'Linea':
                 Color = str(self.ColorGrafico_2.currentText())
                 Color = Selecionarcolor1(Color)
                 ax = plt.plot(self.df[str(self.SerieTiempo_2.currentText())], color=Color)
                 plt.show(block=True)
             if TipoGrafico == 'Correlograma':
                 df = pd.read_csv("Base.csv")
                 df = pd.DataFrame(df)
                 # Default heatmap
                 p1 = sns.heatmap(df)
                 plt.show(block=True)


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




class Analisis(QtWidgets.QMainWindow, Ui_MenuAnalizar):
    def __init__(self):
        super(BaseMenuAnalizar, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Series.addItems(list(self.df.columns.values))
        self.Metodo.addItems(list(['Fourier','Transformada continua Wavelet']))
        self.Siguiente.clicked.connect(self.AbrirOpcionesMetodo)

    def AbrirOpcionesMetodo(self):
        Metodo = self.Metodo.currentText()
        global SerieMetodo
        SerieMetodo=self.Series.currentText()
        print(Metodo)
        if Metodo == "Fourier":
            self.close()
            self.MetFourier = MetFou()
            self.MetFourier.show()


class MetFou(QtWidgets.QMainWindow, Ui_MetodoFourier):
    def __init__(self):
        super(BaseMetodFourier, self).__init__()
        self.setupUi(self)
        self.df = pd.read_csv("Base.csv")
        self.Aceptar.clicked.connect(self.Analizare)
    def Analizare(self):
        Metodo ="Fourier"
        Serie= SerieMetodo
        print(Serie)
        if Metodo == "Fourier":
            Umbral1=self.Umbral.text()
            umbral_ruido = int(Umbral1)
            Tiempo_de_medicion = 0.002
            F_medicion = 1 / Tiempo_de_medicion
            df = pd.read_csv("Base.csv")
            A1=df[str(Serie)]
            N2 = len(A1)
            F2 = np.fft.fft(A1)
            import math
            x1 = Tiempo_de_medicion * np.arange(0, 1500)
            Frecuencia2 = (F_medicion / 2) * np.arange(0, math.floor(N2 / 2)) / math.floor(N2 / 2)

            señal_limpia = []

            for i in range(0, len(F2)):
                if np.abs(F2[i]) > umbral_ruido:
                    señal_limpia.append(F2[i])
                elif np.abs(F2[i]) <= umbral_ruido:
                    señal_limpia.append(0)

            fi = np.fft.ifft(señal_limpia)

            plt.figure(figsize=(20, 3))
            plt.ylim(-0.1, 0.1)
            plt.plot(x1, A1, label='Señal original')
            plt.plot(x1, fi, color="r", label='Señal filtrada')
            plt.xlabel('tiempo (s)',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16})
            plt.ylabel('Amplitud (v)',
                       fontdict={'color': 'black',
                                 'weight': 'bold',
                                 'size': 16})
            plt.legend(loc="upper left")
            plt.show(block=True)

        

class MenuWeB(QtWidgets.QMainWindow, Ui_MenuWB):
    def __init__(self):
        super(BaseMenuWB, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.Aceptar.clicked.connect(self.Analizar)
        self.Cancelar.clicked.connect(self.VeMenuAnalizar)
    def VeMenuAnalizar(self):
        self.close()
        self.Menu = Analisis()
        self.Menu.show()







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
