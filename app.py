# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for
from flask_cors import CORS, cross_origin

from functools import wraps

import mysql.connector
import datetime
import pytz
import pusher

from model_recordatorio import db
from controller_recordatorio import recordatorio_bp

def get_db_connection():
    try:
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_23005026_bd",
            user="u760464709_23005026_usr",
            password="H6eriHv6?",
            port=3306,
            autocommit=True,
            connect_timeout=10
        )
        return con
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

con = get_db_connection()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://u760464709_23005026_usr:H6eriHv6?@185.232.14.52:3306/u760464709_23005026_bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "H6eriHv6?"
db.init_app(app)

app.register_blueprint(recordatorio_bp)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'idUsuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def pusherCategorias():
    try:        
        pusher_client = pusher.Pusher(
          app_id="2052295",
          key="2922c4803975e3f70a0d",
          secret="6b31b50d572bf754fe60",
          cluster="us2",
          ssl=True
        )
        
        pusher_client.trigger("canalCategorias", "eventoCategorias", {"message": "Categorias actualizadas!"})
    except Exception as e:
        print(f"Pusher error: {e}")
    
    return make_response(jsonify({}))

def pusherPendientes():
    try:
        pusher_client = pusher.Pusher(
            app_id="2052296",
            key="52712e9b9d8935dc32c5",
            secret="9249dda1e2e33c3d0233",
            cluster="us2",
            ssl=True
        )
        
        pusher_client.trigger("canalPendientes", "eventoPendientes", {"message": "Pendientes actualizados!"})
    except Exception as e:
        print(f"Pusher error: {e}")
    
    return make_response(jsonify({}))

@app.route("/")
def index():
    if 'idUsuario' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", session=session)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", session=session)

@app.route("/iniciarSesion", methods=["POST"])
def iniciarSesion():
    print("Login attempt received")
    con = get_db_connection()
    if not con:
        print("Database connection failed")
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        usuario    = request.form["txtUsuario"]
        contrasena = request.form["txtContrasena"]

        cursor = con.cursor(dictionary=True)
        sql    = """
        SELECT idUsuario, usuario
        FROM usuarios
        WHERE usuario = %s
        AND contrasena = %s
        """
        val    = (usuario, contrasena)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        if registros:
            session['idUsuario'] = registros[0]['idUsuario']
            session['username'] = registros[0]['usuario']
            return redirect(url_for('index'))
        else:
            return make_response(jsonify({"error": "Invalid credentials"}))
    except Exception as e:
        print(f"Login error: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": "Login failed"}))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/categorias")
@login_required
def categorias():
    return render_template("categorias.html")

@app.route("/tbodyCategorias")
@login_required
def tbodyCategorias():
    con = get_db_connection()
    if not con:
        print("Database connection failed")
        return render_template("tbodyCategorias.html", categorias=[])

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idCategoria,
               nombreCategoria
        FROM categorias
        ORDER BY idCategoria DESC
        LIMIT 10 OFFSET 0
        """

        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return render_template("tbodyCategorias.html", categorias=registros)
    except Exception as e:
        print(f"Error loading categorias: {e}")
        if con:
            con.close()
        return render_template("tbodyCategorias.html", categorias=[])

@app.route("/pendientes")
@login_required
def pendientes():
    return render_template("pendientes.html")

@app.route("/tbodyPendientes")
@login_required
def tbodyPendientes():
    con = get_db_connection()
    if not con:
        return render_template("tbodyPendientes.html", pendientes=[])

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT p.idPendiente,
               p.tituloPendiente,
               p.descripcion,
               p.estado,
               c.nombreCategoria
        FROM pendientes p
        LEFT JOIN categorias c ON p.idCategoria = c.idCategoria
        ORDER BY p.idPendiente DESC
        LIMIT 10 OFFSET 0
        """

        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return render_template("tbodyPendientes.html", pendientes=registros)
    except Exception as e:
        print(f"Error loading pendientes: {e}")
        if con:
            con.close()
        return render_template("tbodyPendientes.html", pendientes=[])

@app.route("/recordatorios")
@login_required
def recordatorios():
    return render_template("recordatorios.html")

@app.route("/tbodyRecordatorios")
@login_required
def tbodyRecordatorios():
    con = get_db_connection()
    if not con:
        return render_template("tbodyRecordatorios.html", recordatorios=[])

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT r.idRecordatorio,
               p.tituloPendiente,
               c.nombreCategoria,
               r.mensaje,
               r.fechaHora
        FROM recordatorios r
        INNER JOIN pendientes p ON r.idPendiente = p.idPendiente
        LEFT JOIN categorias c ON r.idCategoria = c.idCategoria
        ORDER BY r.idRecordatorio DESC
        LIMIT 10 OFFSET 0
        """

        cursor.execute(sql)
        registros = cursor.fetchall()

        # Format datetime
        for registro in registros:
            if registro["fechaHora"]:
                fecha_hora = registro["fechaHora"]
                registro["fechaHora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
                registro["fecha"] = fecha_hora.strftime("%d/%m/%Y")
                registro["hora"] = fecha_hora.strftime("%H:%M:%S")

        cursor.close()
        con.close()
        return render_template("tbodyRecordatorios.html", recordatorios=registros)
    except Exception as e:
        print(f"Error loading recordatorios: {e}")
        if con:
            con.close()
        return render_template("tbodyRecordatorios.html", recordatorios=[])

# CRUD operations for Categorias
@app.route("/categoria", methods=["POST"])
@login_required
def guardarCategoria():
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        id = request.form.get("id")
        nombre = request.form["nombre"]
        
        cursor = con.cursor()

        if id:
            sql = """
            UPDATE categorias
            SET nombreCategoria = %s
            WHERE idCategoria = %s
            """
            val = (nombre, id)
        else:
            sql = """
            INSERT INTO categorias (nombreCategoria)
            VALUES (%s)
            """
            val = (nombre,)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()
        con.close()

        pusherCategorias()
        
        return make_response(jsonify({"success": True}))
    except Exception as e:
        print(f"Error saving categoria: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

@app.route("/categoria/<int:id>", methods=["GET"])
@login_required
def obtenerCategoria(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idCategoria, nombreCategoria
        FROM categorias
        WHERE idCategoria = %s
        """
        val = (id,)
        
        cursor.execute(sql, val)
        registro = cursor.fetchone()
        cursor.close()
        con.close()

        if registro:
            return make_response(jsonify(registro))
        else:
            return make_response(jsonify({"error": "Categoria not found"}), 404)
    except Exception as e:
        print(f"Error getting categoria: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

@app.route("/categoria/<int:id>", methods=["DELETE"])
@login_required
def eliminarCategoria(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        cursor = con.cursor()
        sql = """
        DELETE FROM categorias
        WHERE idCategoria = %s
        """
        val = (id,)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()
        con.close()

        pusherCategorias()
        
        return make_response(jsonify({"success": True}))
    except Exception as e:
        print(f"Error deleting categoria: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

# CRUD operations for Pendientes
@app.route("/pendiente", methods=["POST"])
@login_required
def guardarPendiente():
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        id = request.form.get("id")
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        estado = request.form["estado"]
        idCategoria = request.form.get("idCategoria") or None
        
        cursor = con.cursor()

        if id:
            sql = """
            UPDATE pendientes
            SET tituloPendiente = %s,
                descripcion = %s,
                estado = %s,
                idCategoria = %s
            WHERE idPendiente = %s
            """
            val = (titulo, descripcion, estado, idCategoria, id)
        else:
            sql = """
            INSERT INTO pendientes (tituloPendiente, descripcion, estado, idCategoria)
            VALUES (%s, %s, %s, %s)
            """
            val = (titulo, descripcion, estado, idCategoria)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()
        con.close()

        pusherPendientes()
        
        return make_response(jsonify({"success": True}))
    except Exception as e:
        print(f"Error saving pendiente: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

@app.route("/pendiente/<int:id>", methods=["GET"])
@login_required
def obtenerPendiente(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT p.idPendiente, p.tituloPendiente, p.descripcion, p.estado, p.idCategoria, c.nombreCategoria
        FROM pendientes p
        LEFT JOIN categorias c ON p.idCategoria = c.idCategoria
        WHERE p.idPendiente = %s
        """
        val = (id,)
        
        cursor.execute(sql, val)
        registro = cursor.fetchone()
        cursor.close()
        con.close()

        if registro:
            return make_response(jsonify(registro))
        else:
            return make_response(jsonify({"error": "Pendiente not found"}), 404)
    except Exception as e:
        print(f"Error getting pendiente: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

@app.route("/pendiente/<int:id>", methods=["DELETE"])
@login_required
def eliminarPendiente(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        cursor = con.cursor()
        sql = """
        DELETE FROM pendientes
        WHERE idPendiente = %s
        """
        val = (id,)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()
        con.close()

        pusherPendientes()
        
        return make_response(jsonify({"success": True}))
    except Exception as e:
        print(f"Error deleting pendiente: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

## La ruta /recordatorio ahora es manejada por el blueprint recordatorio_bp

# Get all categorias for dropdowns
@app.route("/categorias/all")
@login_required
def getAllCategorias():
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idCategoria, nombreCategoria
        FROM categorias
        ORDER BY nombreCategoria
        """

        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error loading all categorias: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

# Get all pendientes for dropdowns
@app.route("/pendientes/all")
@login_required
def getAllPendientes():
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idPendiente, tituloPendiente
        FROM pendientes
        ORDER BY tituloPendiente
        """

        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error loading all pendientes: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
