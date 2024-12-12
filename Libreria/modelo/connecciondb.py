import sqlite3
from tkinter import messagebox

class Conneccion():
    def __init__(self):
        self.base_datos = 'Libreria/ddbb/libreria.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar_con(self):
        self.conexion.commit()
        self.conexion.close()
        
def desconectar_db():
    try:
        conexion = Conneccion()
        conexion.cerrar_con()
        messagebox.showinfo('Desconexion', 'Se ha desconectado de la base de datos')
    except Exception as e:
        print(f'Ocurrio un error al desconectar la base de datos: {e}')
        messagebox.showerror('Error', f'No se ha podido desconectar de la base de datos: {e}')