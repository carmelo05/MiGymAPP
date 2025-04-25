from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import bcrypt
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔌 Conexión a MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Wu%JHh6k#KzShP"),
        database=os.getenv("DB_NAME", "gimnasio_db"),
        buffered=True
    )

# 🏗️ Inicialización DB
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                email VARCHAR(100),
                password VARCHAR(255),
                telefono VARCHAR(20),
                fecha_nacimiento DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rutinas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                genero ENUM('masculino', 'femenino'),
                dia_semana VARCHAR(15),
                ejercicios TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                titulo VARCHAR(255),
                fecha DATE,
                descripcion TEXT
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM rutinas")
        if cursor.fetchone()[0] == 0:
            rutinas = [
                ('masculino', 'lunes', 'Press de banca\nFondos\nAperturas con mancuernas\nFlexiones'),
                ('masculino', 'martes', 'Dominadas\nRemo con barra\nPull-over\nPeso muerto'),
                ('masculino', 'miércoles', 'Sentadillas\nPrensa de piernas\nZancadas\nElevaciones de talón'),
                ('masculino', 'jueves', 'Cardio: 30 minutos trote\nAbdominales crunch\nPlancha 3x1min\nBicicleta estática'),
                ('masculino', 'viernes', 'Curl de bíceps\nTríceps en polea\nCurl martillo\nExtensión de tríceps'),
                ('masculino', 'sábado', 'Entrenamiento funcional\nEstiramientos\nYoga suave\nCaminata al aire libre'),
                ('masculino', 'domingo', 'Descanso'),
                ('femenino', 'lunes', 'Glúteos en polea\nSentadillas con peso\nElevaciones laterales de pierna\nHip thrust'),
                ('femenino', 'martes', 'Espalda baja\nRemo con mancuerna\nPeso muerto rumano\nCardio HIIT 20min'),
                ('femenino', 'miércoles', 'Piernas completas\nZancadas con mancuerna\nPrensa de piernas\nElevación de talones'),
                ('femenino', 'jueves', 'Cardio moderado 30min\nCrunch abdominal\nElevación de piernas\nPlancha'),
                ('femenino', 'viernes', 'Brazos y hombros\nCurl de bíceps\nElevaciones laterales\nTríceps con mancuernas'),
                ('femenino', 'sábado', 'Yoga + movilidad\nCaminata ligera\nEstiramiento completo\nEjercicios de respiración'),
                ('femenino', 'domingo', 'Descanso'),
            ]
            cursor.executemany("""
                INSERT INTO rutinas (genero, dia_semana, ejercicios)
                VALUES (%s, %s, %s)
            """, rutinas)
            print("✅ Rutinas predeterminadas insertadas.")

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        print("❌ Error al inicializar la base de datos:", e)

# 🌐 Rutas frontend (HTML)
@app.route("/")
def index():
    return render_template("index.html")  # Carga tu archivo index.html

# (Opcional) Rutas adicionales si mueves más HTML a templates
@app.route("/<page>")
def load_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return "Página no encontrada", 404

# 🧾 Registro
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    telefono = data.get("telefono")
    fecha_nacimiento = data.get("fechaNacimiento")

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (username, email, password, telefono, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, password_hash, telefono, fecha_nacimiento))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Usuario registrado con MySQL."}), 200
    except mysql.connector.IntegrityError:
        return jsonify({"success": False, "message": "Ese nombre de usuario ya existe."}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"MySQL error: {str(e)}"}), 500

# 🔐 Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            stored_hash = result[0]
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                return jsonify({"success": True, "username": username}), 200
            else:
                return jsonify({"success": False, "message": "Contraseña incorrecta."}), 401
        else:
            return jsonify({"success": False, "message": "Usuario no encontrado."}), 404

    except Exception as e:
        return jsonify({"success": False, "message": f"Error al hacer login: {str(e)}"}), 500

# 🗓️ Crear evento
@app.route("/eventos", methods=["POST"])
def crear_evento():
    data = request.json
    username = data.get("username")
    titulo = data.get("titulo")
    fecha = data.get("fecha")
    descripcion = data.get("descripcion")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO eventos (username, titulo, fecha, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (username, titulo, fecha, descripcion))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Evento creado correctamente."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Error al crear evento: {str(e)}"}), 500

# 🗓️ Obtener eventos
@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    username = request.args.get("username")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eventos WHERE username = %s", (username,))
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "eventos": eventos}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Error al obtener eventos: {str(e)}"}), 500

# 🚀 Iniciar la app
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")






