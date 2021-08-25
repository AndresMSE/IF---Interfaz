import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sys
from PyQt5 import uic, QtWidgets



MenuGraficas='MenuGraficar.ui'
Ui_MenuGraficas,BaseGraficas=uic.loadUiType(MenuGraficas)

class MGraficas(QtWidgets.QMainWindow, Ui_MenuGraficas):
    def __init__(self):
        super(BaseGraficas, self).__init__()
        self.df = pd.read_csv("Base.csv")
        self.setupUi(self)
        # Botones
        # Cancelar
        #self.Cancelar.clicked.connect(self.RegresaMenu)
        self.SerieTiempo.addItems(list(self.df.columns.values))
        self.SerieTiempo_2.addItems(list(self.df.columns.values))
        self.Graficar.clicked.connect(self.Graficas)
        self.ColorGrafico.addItems(list(['Rojo', 'Azul', 'Negro', 'Amarillo']))
        self.ColorGrafico_2.addItems(list(['Rojo', 'Azul', 'Negro', 'Amarillo']))
        self.TipoDeGraficoComboBox.addItems(list(['Animacion', 'Boxplot', 'Linea', 'Correlograma']))
        self.TipoDeGraficoComboBox_2.addItems(list(['Animacion', 'Boxplot', 'Linea', 'Correlograma']))

    def Graficas(self):

        # Importacion de Excell
        df = pd.read_csv("Jenny.csv", )
        Reposo = df["reposo"].values
        Esfuerzo = df["esfuerzo"].values
        Meditacion = df["meditacion"].values

        x = np.arange(0, 1500, 3 / 1500)
        y = Meditacion

        fig, (ax1, ax2) = plt.subplots(2, 1)

        data_skip = 20

        def init_func():
            # ax.clear()
            plt.xlabel('Tiempo')
            plt.ylabel('voltaje')
            plt.title('uu')
            ax1.set_title('ax1 title')
            ax2.set_title('ax2 title')

        fig.tight_layout()

        def update_plot(i):
            ax1.plot(x[i:i + data_skip], y[i:i + data_skip], color='k')
            ax2.plot(x[i:i + data_skip], y[i:i + data_skip], color='red')
            # ax.scatter(x[i], y[i], marker='o', color='r')

        anim = FuncAnimation(fig,
                             update_plot,
                             frames=np.arange(0, len(y), data_skip),
                             init_func=init_func,
                             interval=200)
        plt.show(block=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MGraficas()
    window.show()
    sys.exit(app.exec_())

