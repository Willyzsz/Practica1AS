# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import pytz

from flask_cors import CORS, cross_origin

# Database connection function
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

# Initialize connection
con = get_db_connection()

app = Flask(__name__)
CORS(app)

def pusherCategorias():
    try:
        import pusher
        
        pusher_client = pusher.Pusher(
          app_id="2046005",
          key="e57a8ad0a9dc2e83d9a2",
          secret="8a116dd9600a3b04a3a0",
          cluster="us2",
          ssl=True
        )
        
        pusher_client.trigger("canalCategorias", "eventoCategorias", {"message": "Categorias actualizadas!"})
    except Exception as e:
        print(f"Pusher error: {e}")
    
    return make_response(jsonify({}))

def pusherPendientes():
    try:
        import pusher
        
        pusher_client = pusher.Pusher(
          app_id="2046005",
          key="e57a8ad0a9dc2e83d9a2",
          secret="8a116dd9600a3b04a3a0",
          cluster="us2",
          ssl=True
        )
        
        pusher_client.trigger("canalPendientes", "eventoPendientes", {"message": "Pendientes actualizados!"})
    except Exception as e:
        print(f"Pusher error: {e}")
    
    return make_response(jsonify({}))

def pusherRecordatorios():
    try:
        import pusher
        
        pusher_client = pusher.Pusher(
          app_id="2046005",
          key="e57a8ad0a9dc2e83d9a2",
          secret="8a116dd9600a3b04a3a0",
          cluster="us2",
          ssl=True
        )
        
        pusher_client.trigger("canalRecordatorios", "eventoRecordatorios", {"message": "Recordatorios actualizados!"})
    except Exception as e:
        print(f"Pusher error: {e}")
    
    return make_response(jsonify({}))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app")
def app2():
    return render_template("login.html")

@app.route("/iniciarSesion", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def iniciarSesion():
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        usuario    = request.form["txtUsuario"]
        contrasena = request.form["txtContrasena"]

        cursor = con.cursor(dictionary=True)
        sql    = """
        SELECT idUsuario
        FROM usuarios

        WHERE usuario = %s
        AND contrasena = %s
        """
        val    = (usuario, contrasena)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Login error: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")

@app.route("/tbodyCategorias")
def tbodyCategorias():
    con = get_db_connection()
    if not con:
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
def pendientes():
    return render_template("pendientes.html")

@app.route("/tbodyPendientes")
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
def recordatorios():
    return render_template("recordatorios.html")

@app.route("/tbodyRecordatorios")
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

# Search routes for each table
@app.route("/categorias/buscar", methods=["GET"])
def buscarCategorias():
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        args = request.args
        busqueda = args["busqueda"]
        busqueda = f"%{busqueda}%"
        
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idCategoria,
               nombreCategoria
        FROM categorias
        WHERE nombreCategoria LIKE %s
        ORDER BY idCategoria DESC
        LIMIT 10 OFFSET 0
        """
        val = (busqueda,)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error searching categorias: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

@app.route("/pendientes/buscar", methods=["GET"])
def buscarPendientes():
    if not con.is_connected():
        con.reconnect()

    args = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT p.idPendiente,
           p.tituloPendiente,
           p.descripcion,
           p.estado,
           c.nombreCategoria

    FROM pendientes p
    LEFT JOIN categorias c ON p.idCategoria = c.idCategoria

    WHERE p.tituloPendiente LIKE %s
    OR    p.descripcion LIKE %s
    OR    p.estado LIKE %s
    OR    c.nombreCategoria LIKE %s

    ORDER BY p.idPendiente DESC

    LIMIT 10 OFFSET 0
    """
    val = (busqueda, busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()
    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []
    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/recordatorios/buscar", methods=["GET"])
def buscarRecordatorios():
    if not con.is_connected():
        con.reconnect()

    args = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
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

    WHERE p.tituloPendiente LIKE %s
    OR    c.nombreCategoria LIKE %s
    OR    r.mensaje LIKE %s

    ORDER BY r.idRecordatorio DESC

    LIMIT 10 OFFSET 0
    """
    val = (busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()
        
        # Format datetime
        for registro in registros:
            if registro["fechaHora"]:
                fecha_hora = registro["fechaHora"]
                registro["fechaHora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
                registro["fecha"] = fecha_hora.strftime("%d/%m/%Y")
                registro["hora"] = fecha_hora.strftime("%H:%M:%S")
                
    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []
    finally:
        con.close()

    return make_response(jsonify(registros))

# CRUD operations for Categorias
@app.route("/categoria", methods=["POST"])
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

@app.route("/categoria/<int:id>")
def editarCategoria(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idCategoria, nombreCategoria
        FROM categorias
        WHERE idCategoria = %s
        """
        val = (id,)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error loading categoria for edit: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

# CRUD operations for Pendientes
@app.route("/pendiente", methods=["POST"])
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

@app.route("/pendiente/<int:id>")
def editarPendiente(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idPendiente, tituloPendiente, descripcion, estado, idCategoria
        FROM pendientes
        WHERE idPendiente = %s
        """
        val = (id,)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error loading pendiente for edit: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

# CRUD operations for Recordatorios
@app.route("/recordatorio", methods=["POST"])
def guardarRecordatorio():
    con = get_db_connection()
    if not con:
        return make_response(jsonify({"error": "Database connection failed"}))

    try:
        id = request.form.get("id")
        idPendiente = request.form["idPendiente"]
        idCategoria = request.form.get("idCategoria") or None
        mensaje = request.form["mensaje"]
        fechaHora = request.form.get("fechaHora") or datetime.datetime.now(pytz.timezone("America/Matamoros"))
        
        cursor = con.cursor()

        if id:
            sql = """
            UPDATE recordatorios
            SET idPendiente = %s,
                idCategoria = %s,
                mensaje = %s,
                fechaHora = %s
            WHERE idRecordatorio = %s
            """
            val = (idPendiente, idCategoria, mensaje, fechaHora, id)
        else:
            sql = """
            INSERT INTO recordatorios (idPendiente, idCategoria, mensaje, fechaHora)
            VALUES (%s, %s, %s, %s)
            """
            val = (idPendiente, idCategoria, mensaje, fechaHora)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()
        con.close()

        pusherRecordatorios()
        
        return make_response(jsonify({"success": True}))
    except Exception as e:
        print(f"Error saving recordatorio: {e}")
        if con:
            con.close()
        return make_response(jsonify({"error": str(e)}))

@app.route("/recordatorio/<int:id>")
def editarRecordatorio(id):
    con = get_db_connection()
    if not con:
        return make_response(jsonify([]))

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idRecordatorio, idPendiente, idCategoria, mensaje, fechaHora
        FROM recordatorios
        WHERE idRecordatorio = %s
        """
        val = (id,)

        cursor.execute(sql, val)
        registros = cursor.fetchall()
        cursor.close()
        con.close()

        return make_response(jsonify(registros))
    except Exception as e:
        print(f"Error loading recordatorio for edit: {e}")
        if con:
            con.close()
        return make_response(jsonify([]))

# Get all categorias for dropdowns
@app.route("/categorias/all")
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
