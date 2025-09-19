from flask import Blueprint, request, jsonify
from service_recordatorio import RecordatorioService

recordatorio_bp = Blueprint("recordatorio", __name__)
recordatorio_service = RecordatorioService()

@recordatorio_bp.route("/recordatorio", methods=["POST"])
def crear_recordatorio():
    data = request.get_json()
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    fecha_hora = data.get("fecha_hora")
    id_pendiente = data.get("id_pendiente")

    if not all([titulo, descripcion, fecha_hora, id_pendiente]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        nuevo_recordatorio = recordatorio_service.crear_recordatorio(
            titulo, descripcion, fecha_hora, id_pendiente
        )
        return jsonify(nuevo_recordatorio), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500