from .connecciondb import Conneccion

def crear_tabla():
    conn = Conneccion()

    sql_libros = '''
        CREATE TABLE IF NOT EXISTS Libros (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL, 
            Autor TEXT NOT NULL, 
            Paginas INTEGER NOT NULL, 
            Precio REAL NOT NULL
        );
    '''
    
    sql_categorias = '''
        CREATE TABLE IF NOT EXISTS Categorias (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(150) NOT NULL
        );
    '''
        
    sql_libros_categorias = '''
        CREATE TABLE IF NOT EXISTS Libros_Categorias (
            libro_id INTEGER,
            categoria_id INTEGER,
            PRIMARY KEY (libro_id, categoria_id),
            FOREIGN KEY (libro_id) REFERENCES Libros(ID),
            FOREIGN KEY (categoria_id) REFERENCES Categorias(ID)
        );
    '''
    try:
        conn.cursor.execute(sql_libros)
        conn.cursor.execute(sql_categorias)
        conn.cursor.execute(sql_libros_categorias)
        
        categorias_preestablecidas = ['Ficción', 'Drama', 'Ciencia Ficción', 'Fantasía', 'Historia', 'Geografia', 'Biografía', 'Suspenso', 'Terror', 'Romance']
        for categoria in categorias_preestablecidas:
            conn.cursor.execute('INSERT OR IGNORE INTO Categorias (Nombre) VALUES (?)', (categoria,))
        
        conn.cerrar_con()
    except Exception as e:
        print(f'Ocurrio un error al crear la tabla {e}')


class Libro():

    def __init__(self, titulo, autor, paginas, precio):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.precio = precio
        
    def __str__(self):
        return f'Libro[{self.titulo},{self.autor},{self.paginas},{self.precio}]'
    
def guardar_libro(libro, categorias):
    conn = Conneccion()
    try:
        sql_libro = '''
            INSERT INTO Libros(Titulo, Autor, Paginas, Precio)
            VALUES (?, ?, ?, ?);
        '''
        conn.cursor.execute(sql_libro, (libro.titulo, libro.autor, libro.paginas, libro.precio))
        libro_id = conn.cursor.lastrowid

        for categoria in categorias:
            sql_libro_categoria = '''
                INSERT OR IGNORE INTO Libros_Categorias(libro_id, categoria_id)
                VALUES (?, (SELECT ID FROM Categorias WHERE Nombre = ?));
            '''
            conn.cursor.execute(sql_libro_categoria, (libro_id, categoria))

        conn.cerrar_con()
    except Exception as e:
        print(f'Ocurrio un error al guardar el libro {e}')
        
def guardar_categoria(nombre_categoria):
    conn = Conneccion()
    try:
        sql = '''
            INSERT INTO Categorias (Nombre)
            VALUES (?);
        '''
        conn.cursor.execute(sql, (nombre_categoria,))
        conn.cerrar_con()
    except Exception as e:
        print(f'Ocurrio un error al guardar la categoría {e}')

def listar_libros():
    conn = Conneccion()
    try:
        sql = '''
            SELECT l.ID, l.Titulo, l.Autor, l.Paginas, l.Precio, group_concat(c.Nombre)
            FROM Libros l
            LEFT JOIN Libros_Categorias lc ON l.ID = lc.libro_id
            LEFT JOIN Categorias c ON lc.categoria_id = c.ID
            GROUP BY l.ID, l.Titulo, l.Autor, l.Paginas, l.Precio
        '''
        conn.cursor.execute(sql)
        listar_libros = conn.cursor.fetchall()
        conn.cerrar_con()

        return listar_libros
    except Exception as e:
        print(f'Ocurrio un error al listar los libros {e}')
        return []
    
def listar_categorias():
    conn = Conneccion()
    try:
        sql = '''
            SELECT DISTINCT ID, Nombre FROM Categorias
        '''
        conn.cursor.execute(sql)
        listar_categorias = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_categorias
    except Exception as e:
        print(f'Ocurrio un error al listar las categorías {e}')
        return []


def listar_libros_categoria(id_categoria):
    conn = Conneccion()
    try:
        sql = '''
            SELECT l.ID, l.Titulo, l.Autor, l.Paginas, l.Precio, c.Nombre
            FROM Libros l
            INNER JOIN Libros_Categorias lc ON l.ID = lc.libro_id
            INNER JOIN Categorias c ON lc.categoria_id = c.ID
            WHERE c.ID = ?
        '''
        conn.cursor.execute(sql, (id_categoria,))
        listar_libros = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_libros
    except Exception as e:
        print(f'Ocurrio un error al listar los libros por categorías {e}')
        return []
    
def editar_libro(libro, categorias, id):
    conn = Conneccion()
    try:
        sql_libro = '''
            UPDATE Libros
            SET Titulo = ?, Autor = ?, Paginas = ?, Precio = ?
            WHERE ID = ?;
        '''
        conn.cursor.execute(sql_libro, (libro.titulo, libro.autor, libro.paginas, libro.precio, id))

        sql_borrar_categorias = '''
            DELETE FROM Libros_Categorias WHERE libro_id = ?;
        '''
        conn.cursor.execute(sql_borrar_categorias, (id,))

        for categoria in categorias:
            sql_libro_categoria = '''
                INSERT INTO Libros_Categorias(libro_id, categoria_id)
                VALUES (?, (SELECT ID FROM Categorias WHERE Nombre = ?));
            '''
            conn.cursor.execute(sql_libro_categoria, (id, categoria))

        conn.cerrar_con()
    except Exception as e:
        print(f'Ocurrio un error al editar el libro {e}')

def borrar_libro(id):
    conn = Conneccion()
    try:
        sql_libro = '''
            DELETE FROM Libros WHERE ID = ?;
        '''
        sql_libro_categoria = '''
            DELETE FROM Libros_Categorias WHERE libro_id = ?;
        '''
        conn.cursor.execute(sql_libro_categoria, (id,))
        conn.cursor.execute(sql_libro, (id,))
        conn.cerrar_con()
    except Exception as e:
        print(f'Ocurrio un error al borrar el libro {e}')