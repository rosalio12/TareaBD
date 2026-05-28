"""
NIVEL 1 — Ejercicios completos
Esquema: users / Cursos

Antes de empezar, crea la DB ejecutando el setup al final de este archivo.
Cada función tiene un ejercicio. Completa las líneas con "pass".

Para ver las soluciones, ejecuta:
    python 03_ejercicios.py --soluciones
"""

import sqlite3
import sys

DB_PATH = "Chalio.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# EJERCICIOS - SELECT
# =========================================================

def select_01():
    """Mostrar todos los datos de todos los users."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  
    for r in cursor.fetchall():
        print(dict(r))
    conn.close()


def select_02():
    """Mostrar nombre y telefono de todos los users."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, telefono FROM users")
    for r in cursor.fetchall():
        print(dict(r))
    conn.close()


def select_03():
    """Mostrar nombre y créditos de los cursos ordenados por créditos descendente."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, creditos FROM cursos"
    "               ORDER BY creditos DESC ") 
    for r in cursor.fetchall():
        print(dict(r))
    conn.close()


def select_04():
    """Mostrar nombre del estudiante, nombre del curso y nota (JOIN)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT e.nombre AS estudiante, c.nombre AS curso, i.nota FROM users AS e"
    "               INNER JOIN inscripciones AS i " 
    "               ON e.id = i.estudiante_id" 
    "               INNER JOIN cursos AS c" 
    "               ON c.id = i.curso_id") 
    for r in cursor.fetchall():
        print(dict(r))
    conn.close()


def select_05():
    """Mostrar cuántos users hay (columna: total)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) AS total FROM users""")  
    print(dict(cursor.fetchone()))
    conn.close()


# =========================================================
# EJERCICIOS - INSERT
# =========================================================

def insert_01():
    """Insertar user: María Torres con telefono."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(nombre, telefono) VALUES('María Torres', '600123456')")
    conn.commit()
    print("[OK] User insertado.")
    conn.close()


def insert_02():
    """Insertar curso: Historia del Arte, créditos 3."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cursos(nombre, creditos) VALUES('Historia del Arte', 3);")  
    conn.commit()
    print("[OK] Curso insertado.")
    conn.close()


def insert_03():
    """Inscribir a Ana López (id=1) en Bases de Datos (id=3)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inscripciones(estudiante_id, curso_id) VALUES(1,3);")
    conn.commit()
    print("[OK] Inscripcion insertada.")
    conn.close()


def insert_04():
    """Insertar dos users a la vez: Valentina Ruiz y Mateo Torres."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO users(nombre, telefono) VALUES(?, ?)",
        [
            ('Valentina Ruiz', '600111222'),
            ('Mateo Torres', '600333444')
        ]
    )
    conn.commit()
    print("[OK] users insertados.")
    conn.close()


# =========================================================
# EJERCICIOS - UPDATE
# =========================================================

def update_01():
    """Actualizar telefono de Carlos Mendoza (id=2)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET telefono = '600999888' WHERE id = 2")
    conn.commit()
    print("[OK] Telefono actualizado.")
    conn.close()


def update_02():
    """Cambiar créditos de Inglés Técnico (id=4) a 3."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE cursos SET creditos = 3 WHERE id = 4")
    conn.commit()
    print("[OK] Creditos actualizados.")
    conn.close()


def update_03():
    """Poner nota 14.5 a Sofía Ramírez (id=5) en Programación Python (curso_id=2)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE inscripciones SET nota = 14.5 WHERE estudiante_id = 5 AND curso_id = 2")
    conn.commit()
    print("[OK] Nota actualizada.")
    conn.close()


# =========================================================
# EJERCICIOS - DELETE
# =========================================================

def delete_01():
    """Eliminar la inscripción con id=5."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscripciones WHERE id = 5") 
    conn.commit()
    print("[OK] Inscripcion eliminada.")
    conn.close()


def delete_02():
    """Eliminar inscripciones con nota NULL."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscripciones WHERE nota IS NULL") 
    conn.commit()
    print(f"[OK] {cursor.rowcount} inscripcion(es) eliminada(s).")
    conn.close()


def delete_03():
    """Eliminar cursos sin users inscritos (usar NOT IN)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cursos
        WHERE id NOT IN (SELECT curso_id FROM inscripciones)""")  
    conn.commit()
    print(f"[OK] {cursor.rowcount} curso(s) eliminado(s).")
    conn.close()

# =========================================================
# SETUP: crear DB con datos
# =========================================================

def crear_db():
    import os
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT
        );
        CREATE TABLE cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            creditos INTEGER NOT NULL CHECK(creditos > 0)
        );
        CREATE TABLE inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            fecha_inscripcion DATE DEFAULT CURRENT_DATE,
            nota REAL CHECK(nota >= 0 AND nota <= 20),
            FOREIGN KEY (estudiante_id) REFERENCES users(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        );
        INSERT INTO users(nombre, telefono) VALUES
            ('Ana López', '600100200'),
            ('Carlos Mendoza', '600200300'),
            ('Lucía Fernández', '600300400'),
            ('Pedro García', '600400500'),
            ('Sofía Ramírez', '600500600');
        INSERT INTO cursos VALUES
            (1, 'Matemáticas I', 'Álgebra y cálculo', 5),
            (2, 'Programación en Python', 'Introducción con Python', 4),
            (3, 'Bases de Datos', 'Bases relacionales', 4),
            (4, 'Inglés Técnico', 'Inglés aplicado a tecnología', 2);
        INSERT INTO inscripciones (id, estudiante_id, curso_id, fecha_inscripcion, nota) VALUES
            (1, 1, 1, '2024-03-05', 18.5),
            (2, 1, 2, '2024-03-05', 16.0),
            (3, 2, 1, '2024-03-06', 14.0),
            (4, 2, 3, '2024-03-06', 17.5),
            (5, 3, 2, '2024-03-07', 19.0),
            (6, 3, 3, '2024-03-07', 15.5),
            (7, 4, 1, '2024-03-08', 12.0),
            (8, 4, 4, '2024-03-08', 18.0),
            (9, 5, 2, '2024-03-09', NULL),
            (10, 5, 3, '2024-03-09', NULL);
    """)
    conn.commit()
    conn.close()
    print(f"[OK] Base de datos '{DB_PATH}' creada.\n")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    if "--soluciones" in sys.argv:
        crear_db()
        print("Soluciones creadas.") 
    crear_db()
    select_01()
    select_02()
    select_03()
    select_04()
    select_05()
else:
        crear_db()
        print("Ejercicios creados.")



