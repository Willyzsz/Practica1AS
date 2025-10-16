from model_recordatorio import Recordatorio, db

class RecordatorioRepository:
    def insert_recordatorio(self, idCategoria, mensaje, fechaHora, idPendiente):
        nuevo_recordatorio = Recordatorio(
            idCategoria=idCategoria,
            mensaje=mensaje,
            fechaHora=fechaHora,
            idPendiente=idPendiente
        )
        db.session.add(nuevo_recordatorio)
        db.session.commit()
        return {"idRecordatorio": nuevo_recordatorio.idRecordatorio, "idCategoria": nuevo_recordatorio.idCategoria, "mensaje": nuevo_recordatorio.mensaje, "fechaHora": nuevo_recordatorio.fechaHora, "idPendiente": nuevo_recordatorio.idPendiente}

    def get_recordatorio(self, id):
        recordatorio = Recordatorio.query.get(id)
        if recordatorio:
            return {
                "idRecordatorio": recordatorio.idRecordatorio,
                "idCategoria": recordatorio.idCategoria,
                "mensaje": recordatorio.mensaje,
                "fechaHora": recordatorio.fechaHora,
                "idPendiente": recordatorio.idPendiente
            }
        return None

    def update_recordatorio(self, id, idCategoria, mensaje, fechaHora, idPendiente):
        recordatorio = Recordatorio.query.get(id)
        if recordatorio:
            recordatorio.idCategoria = idCategoria
            recordatorio.mensaje = mensaje
            recordatorio.fechaHora = fechaHora
            recordatorio.idPendiente = idPendiente
            db.session.commit()
            return {
                "idRecordatorio": recordatorio.idRecordatorio,
                "idCategoria": recordatorio.idCategoria,
                "mensaje": recordatorio.mensaje,
                "fechaHora": recordatorio.fechaHora,
                "idPendiente": recordatorio.idPendiente
            }
        return None

    def delete_recordatorio(self, id):
        recordatorio = Recordatorio.query.get(id)
        if recordatorio:
            db.session.delete(recordatorio)
            db.session.commit()
            return True
        return False