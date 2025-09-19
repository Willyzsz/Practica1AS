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
