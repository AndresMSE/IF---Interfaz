import sys
from PyQt5 import uic, QtWidgets
import pandas as pd

# Cargamos los datod tipo Ui para poder representar el programa en interfaz


qtCreatorFile = "Menus.ui"  # Nombre del archivo aquí.
Acceso = "Acceso.ui"
Mensajes = "Mensajes.ui"
MenuFile="MenuFile.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
Ui_Acceso, BaseAcceso = uic.loadUiType(Acceso)
Ui_Mensaje, BaseMensaje = uic.loadUiType(Mensajes)
Ui_MenuFile, BaseMenuFile = uic.loadUiType(MenuFile)

#Definiremos el estado #No autaorizado, si se dio acceso al usuario cambiara a #Autorizado
Estado = "No autorizado"


class PrimerHoja(QtWidgets.QMainWindow, Ui_MainWindow):
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
        self.MenuFile = LectorCsv()
        if Estado=="Autorizado":
            self.MenuFile.show()







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




#Mandamos llamar la clase padre


class LectorCsv(QtWidgets.QMainWindow, Ui_MenuFile):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.Importar1.clicked.connect(self.getCSV)

    # Aquí van las nuevas funciones
    # Esta función abre el archivo CSV
    def getCSV(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filePath != "":
            print("Dirección", filePath)  # Opcional imprimir la dirección del archivo
            self.df = pd.read_csv(str(filePath))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PrimerHoja()
    window.show()
    sys.exit(app.exec_())
