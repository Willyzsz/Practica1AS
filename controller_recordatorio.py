from flask import Blueprint, request, jsonify
from service_recordatorio import RecordatorioService

recordatorio_bp = Blueprint("recordatorio", __name__)
recordatorio_service = RecordatorioService()

@recordatorio_bp.route("/recordatorio", methods=["POST"])
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