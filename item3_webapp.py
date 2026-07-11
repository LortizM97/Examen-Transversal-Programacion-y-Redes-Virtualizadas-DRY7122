# item3_webapp.py
# Script de gestión de usuarios con SQLite, hashing y servidor web en puerto 5800

import sqlite3
import hashlib
from flask import Flask, request, jsonify

# Inicializar aplicación Flask
app = Flask(__name__)

# Conexión a la base de datos SQLite
conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    password_hash TEXT NOT NULL
)
""")
conn.commit()

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insertar usuarios iniciales (integrantes del examen)
integrantes = ["Luis Ortiz", "Francisco Soto-Aguilar", "Cristian Castro", "Branco Solis"]
for nombre in integrantes:
    password = "clave123"  # puedes cambiar la contraseña a elección
    cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_password(password)))
conn.commit()

# Ruta para validar usuario
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    nombre = data.get("nombre")
    password = data.get("password")

    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()

    if row and row[0] == hash_password(password):
        return jsonify({"mensaje": f"Usuario {nombre} validado correctamente."})
    else:
        return jsonify({"mensaje": "Credenciales inválidas."}), 401

# Ruta para listar usuarios (solo para ver en DB Browser)
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    cursor.execute("SELECT nombre, password_hash FROM usuarios")
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(port=5800)
