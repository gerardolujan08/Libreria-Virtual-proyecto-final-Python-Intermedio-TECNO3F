import tkinter as tk
from cliente.vista import Frame, barrita_menu
from modelo.consultas_dao import crear_tabla

def main(): 
    ventana = tk.Tk()
    ventana.title('Libreria Virtual')
    ventana.iconbitmap('Libreria/img/book.ico')
    ventana.resizable(False,  False)
    
    app = Frame(root=ventana)
    barrita_menu(ventana, app)

    ventana.mainloop()
    
if __name__ == '__main__':
    crear_tabla()
    main()
