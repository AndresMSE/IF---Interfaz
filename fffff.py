import pandas as pd


def junta_csv(salida, archivos):
    """
    Crea un archivo .csv a partir de multiples
    archivos .csv con una sola columna

    :param salida: Nombre del archivo de salida.
    :param archivos: Lista de archivos de entrada.
                     Son .csv con header en la primera fila.
    """
    # La lista handles contiene el file object de los
    # archivos abiertos. Al agotarse el archivo, la
    # posición es reemplazada con None
    handles = [] # Archivos de entrada
    headers = [] # Headers de cada archivo de entrada
    #
    #   Abrir los archivos de entradas, leer los headers
    #
    for arch in archivos:
        file_handle = open(arch, "r")
        handles.append(file_handle)
        headers.append(file_handle.readline().strip())
    #
    #   Procesar los archivos de entrada hasta agotarlos
    #   todos.
    #
    with open(salida, "w") as out:
        #   Formar la primera linea con los headers de
        #   las columnas.
        header = ",".join(headers)
        out.write(f"{header}\n")

        #   Cuando se acaba un archivo, asignamos None
        #   en su posición dentro de handles; por tanto
        #   mientras haya un handle distinto de None,
        #   seguimos iterando.
        while any(handles):
            fila = []
            #   Leer una fila de cada archivo para
            #   formar una fila de salida.
            for index in range(len(handles)):
                celda = ''  # Valor por default para la celda.
                if handles[index] is not None:
                    dato = handles[index].readline()
                    if dato:
                        celda = dato.strip()
                    else:
                        #   Se agotó este archivo.
                        handles[index].close()
                        handles[index] = None

                fila.append(celda)

            if any(handles):
                #   Grabar la fila de salida.
                salida = ','.join(fila)
                out.write(f"{salida}\n")

    #   Cerrar archivo de salida
    out.close()

archivos = ["Jenny.csv","Base.csv"]
# junta_csv("Base.csv", archivos)

Data=pd.read_csv('Jenny.csv')
Data=pd.DataFrame(Data)

Base=pd.DataFrame(range(1400))

N=max(len(Base),len(Data))

for i in range(len(Data)):
     Base.append(["Nan"],ignore_index=True)