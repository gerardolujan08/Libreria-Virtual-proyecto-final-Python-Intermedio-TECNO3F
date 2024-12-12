import tkinter as tk
from tkinter import ttk, messagebox
from modelo.consultas_dao import Libro, crear_tabla, guardar_libro, listar_libros, listar_categorias, listar_libros_categoria, editar_libro, borrar_libro
from modelo.connecciondb import desconectar_db

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=600, height=400)
        self.root = root
        self.id_libro = None
        self.pack()

        self.label_form()
        self.input_form()
        self.botones_principales()
        self.cargar_categorias()
        self.bloquear_campos()
        self.mostrar_tabla()

    def label_form(self):
        self.label_titulo = tk.Label(self, text="Título:")
        self.label_titulo.config(font=('Arial', 12, 'bold'))
        self.label_titulo.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_autor = tk.Label(self, text="Autor:")
        self.label_autor.config(font=('Arial', 12, 'bold'))
        self.label_autor.grid(row=1, column=0, padx=10, pady=10)

        self.label_paginas = tk.Label(self, text="Páginas:")
        self.label_paginas.config(font=('Arial', 12, 'bold'))
        self.label_paginas.grid(row=2, column=0, padx=10, pady=10)

        self.label_precio = tk.Label(self, text="Precio:")
        self.label_precio.config(font=('Arial', 12, 'bold'))
        self.label_precio.grid(row=3, column=0, padx=10, pady=10)

        self.label_categoria = tk.Label(self, text="Categoría:")
        self.label_categoria.config(font=('Arial', 12, 'bold'))
        self.label_categoria.grid(row=4, column=0, padx=10, pady=10)

    def input_form(self):
        self.titulo = tk.StringVar()
        self.entry_titulo = tk.Entry(self, textvariable=self.titulo)
        self.entry_titulo.config(width=50)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=10)

        self.autor = tk.StringVar()
        self.entry_autor = tk.Entry(self, textvariable=self.autor)
        self.entry_autor.config(width=50)
        self.entry_autor.grid(row=1, column=1, padx=10, pady=10)

        self.paginas = tk.StringVar()
        self.entry_paginas = tk.Entry(self, textvariable=self.paginas)
        self.entry_paginas.config(width=50)
        self.entry_paginas.grid(row=2, column=1, padx=10, pady=10)

        self.precio = tk.StringVar()
        self.entry_precio = tk.Entry(self, textvariable=self.precio)
        self.entry_precio.config(width=50)
        self.entry_precio.grid(row=3, column=1, padx=10, pady=10)
        
    def cargar_categorias(self):
        categorias = listar_categorias() 
        y = [] 
        for categoria in categorias:
            if len(categoria) > 1:
                if categoria[1] not in y:
                    y.append(categoria[1]) 
        
        self.categorias = ['Seleccione Una'] + y 
        self.entry_categoria = ttk.Combobox(self, state="readonly") 
        self.entry_categoria['values'] = self.categorias 
        self.entry_categoria.current(0) 
        self.entry_categoria.config(width=25) 
        self.entry_categoria.grid(row=4, column=1, padx=10, pady=10)
        
    def botones_principales(self):
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.btn_alta.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_alta.grid(row=5, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text='Guardar', command=self.guardar_campos)
        self.btn_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#0D2A83', cursor='hand2', activebackground='#7594F5', activeforeground='#000000')
        self.btn_guardar.grid(row=5, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text='Cancelar', command=self.bloquear_campos)
        self.btn_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2', activebackground='#F35B5B', activeforeground='#000000')
        self.btn_cancelar.grid(row=5, column=2, padx=10, pady=10)

    def guardar_campos(self):
        libro = Libro(
            self.titulo.get(),
            self.autor.get(),
            self.paginas.get(),
            self.precio.get()
        )

        categoria_seleccionada = [self.entry_categoria.get()]
        
        if self.id_libro is None:
            guardar_libro(libro, categoria_seleccionada)
        else:
            editar_libro(libro, categoria_seleccionada, int(self.id_libro))

        self.bloquear_campos()
        self.mostrar_tabla()

    def habilitar_campos(self):
        self.entry_titulo.config(state='normal')
        self.entry_autor.config(state='normal')
        self.entry_paginas.config(state='normal')
        self.entry_precio.config(state='normal')
        self.entry_categoria.config(state='normal')
        self.btn_guardar.config(state='normal')
        self.btn_cancelar.config(state='normal')
        self.btn_alta.config(state='disabled')

    def bloquear_campos(self):
        self.entry_titulo.config(state='disabled')
        self.entry_autor.config(state='disabled')
        self.entry_paginas.config(state='disabled')
        self.entry_precio.config(state='disabled')
        self.entry_categoria.config(state='disabled')
        self.btn_guardar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.titulo.set('')
        self.autor.set('')
        self.paginas.set('')
        self.precio.set('')
        self.entry_categoria.current(0)
        self.id_libro = None

    def mostrar_tabla(self):
        self.lista_libros = listar_libros()
        self.lista_libros.reverse()
        self.actualizar_tabla(self.lista_libros)
        
    def actualizar_tabla(self, libros):
        self.tabla = ttk.Treeview(self, columns=('Título', 'Autor', 'Páginas', 'Precio', 'Categoría'))
        self.tabla.grid(row=6, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=6, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Título')
        self.tabla.heading('#2', text='Autor')
        self.tabla.heading('#3', text='Páginas')
        self.tabla.heading('#4', text='Precio')
        self.tabla.heading('#5', text='Categoría')
        
        for libro in libros:
            if len(libro) == 6:
                self.tabla.insert('', 0, text=libro[0], values=(libro[1], libro[2], libro[3], libro[4], libro[5]))

        self.btn_editar = tk.Button(self, text='Editar', command=self.editar_registro)
        self.btn_editar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_editar.grid(row=7, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text='Eliminar', command=self.eliminar_registro)
        self.btn_delete.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2', activebackground='#F35B5B', activeforeground='#000000')
        self.btn_delete.grid(row=7, column=1, padx=10, pady=10)
        
    def editar_registro(self):
        try:
            self.id_libro = self.tabla.item(self.tabla.selection())['text']
            self.titulo_libro = self.tabla.item(self.tabla.selection())['values'][0]
            self.autor_libro = self.tabla.item(self.tabla.selection())['values'][1]
            self.paginas_libro = self.tabla.item(self.tabla.selection())['values'][2]
            self.precio_libro = self.tabla.item(self.tabla.selection())['values'][3]
            self.categoria_libro = self.tabla.item(self.tabla.selection())['values'][4].split(',')

            self.habilitar_campos()
            self.titulo.set(self.titulo_libro)
            self.autor.set(self.autor_libro)
            self.paginas.set(self.paginas_libro)
            self.precio.set(self.precio_libro)
            self.entry_categoria.set(self.categoria_libro)
        except Exception as e: 
            print(f"Error al editar el registro: {e}")
            
    def eliminar_registro(self):
        try:
            self.id_libro = self.tabla.item(self.tabla.selection())['text']
            borrar_libro(int(self.id_libro))
            self.mostrar_tabla()
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")
    
def barrita_menu(root, frame):
    barra = tk.Menu(root)
    root.config(menu=barra, width=300, height=300)
    menu_inicio = tk.Menu(barra, tearoff=0)
    menu_consultas = tk.Menu(barra, tearoff=0)
    menu_acerca = tk.Menu(barra, tearoff=0)
    menu_ayuda = tk.Menu(barra, tearoff=0)

    # Menu principal
    barra.add_cascade(label='Inicio', menu=menu_inicio)
    barra.add_cascade(label='Consultas', menu=menu_consultas)
    barra.add_cascade(label='Acerca de..', menu=menu_acerca)
    barra.add_cascade(label='Ayuda', menu=menu_ayuda)

    # Sub-menus
    menu_inicio.add_command(label='Conectar DB', command=crear_tabla)
    menu_inicio.add_command(label='Desconectar DB', command=desconectar_db)
    menu_inicio.add_separator()
    menu_inicio.add_command(label='Salir', command=root.destroy)

    menu_consultas.add_command(label='Listar Libros', command=lambda: mostrar_libros_gui(frame))
    menu_consultas.add_command(label='Listar Categorías', command=lambda: mostrar_categorias_gui(frame))

    menu_acerca.add_command(label='Desarrollador', command=lambda: messagebox.showinfo("Acerca del Desarrollador", "Este proyecto fue desarrollado por Gerardo Luján, en colaboración con TECNO3F"))

    menu_ayuda.add_command(label='Contactanos', command=lambda: messagebox.showinfo("Contacto", "Email: gerardolujan@gmail.com"))
    
def mostrar_libros_gui(frame):
    libros = listar_libros()
    libros.reverse()
    frame.actualizar_tabla(libros)
        
def mostrar_categorias_gui(frame):
    categorias = listar_categorias()
    categorias.reverse()
    categorias_libros = []
    libros_unicos = set()
    
    for categoria in categorias:
        id_categoria = categoria[0]
        libros_categoria = listar_libros_categoria(id_categoria)
        
        for libro in libros_categoria:
            if libro not in libros_unicos:
                libros_unicos.add(libro)
                categorias_libros.append(libro)
        
    frame.actualizar_tabla(categorias_libros)