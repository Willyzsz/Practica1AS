from flask import Blueprint, request, jsonify
from service_recordatorio import RecordatorioService
from functools import wraps

recordatorio_bp = Blueprint("recordatorio", __name__)
recordatorio_service = RecordatorioService()

# Authentication decorator for blueprint
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session, redirect, url_for
        if 'idUsuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@recordatorio_bp.route("/recordatorio", methods=["POST"])
@login_required
def crear_recordatorio():
    if request.is_json:
        data = request.get_json()
        idCategoria = data.get("idCategoria")
        mensaje = data.get("mensaje")
        fechaHora = data.get("fechaHora")
        idPendiente = data.get("idPendiente")
    else:
        idCategoria = request.form.get("idCategoria")
        mensaje = request.form.get("mensaje")
        fechaHora = request.form.get("fechaHora")
        idPendiente = request.form.get("idPendiente")

    if not all([idCategoria, mensaje, fechaHora, idPendiente]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        nuevo_recordatorio = recordatorio_service.crear_recordatorio(
            idCategoria, mensaje, fechaHora, idPendiente
        )
        return jsonify(nuevo_recordatorio), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recordatorio_bp.route("/recordatorio/<int:id>", methods=["GET"])
@login_required
def obtener_recordatorio(id):
    try:
        recordatorio = recordatorio_service.obtener_recordatorio(id)
        if recordatorio:
            return jsonify(recordatorio), 200
        else:
            return jsonify({"error": "Recordatorio not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recordatorio_bp.route("/recordatorio/<int:id>", methods=["PUT"])
@login_required
def actualizar_recordatorio(id):
    if request.is_json:
        data = request.get_json()
        idCategoria = data.get("idCategoria")
        mensaje = data.get("mensaje")
        fechaHora = data.get("fechaHora")
        idPendiente = data.get("idPendiente")
    else:
        idCategoria = request.form.get("idCategoria")
        mensaje = request.form.get("mensaje")
        fechaHora = request.form.get("fechaHora")
        idPendiente = request.form.get("idPendiente")

    if not all([idCategoria, mensaje, fechaHora, idPendiente]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        recordatorio_actualizado = recordatorio_service.actualizar_recordatorio(
            id, idCategoria, mensaje, fechaHora, idPendiente
        )
        return jsonify(recordatorio_actualizado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recordatorio_bp.route("/recordatorio/<int:id>", methods=["DELETE"])
@login_required
def eliminar_recordatorio(id):
    try:
        resultado = recordatorio_service.eliminar_recordatorio(id)
        if resultado:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Recordatorio not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500