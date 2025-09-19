from model_recordatorio import Recordatorio, db

class RecordatorioRepository:
    def insert_recordatorio(self, titulo, descripcion, fecha_hora, id_pendiente):
        nuevo_recordatorio = Recordatorio(
            titulo=titulo,
            descripcion=descripcion,
            fecha_hora=fecha_hora,
            id_pendiente=id_pendiente
        )
        db.session.add(nuevo_recordatorio)
        db.session.commit()
        return {"idRecordatorio": nuevo_recordatorio.idRecordatorio, "titulo": nuevo_recordatorio.titulo, "descripcion": nuevo_recordatorio.descripcion, "fecha_hora": nuevo_recordatorio.fecha_hora, "id_pendiente": nuevo_recordatorio.id_pendiente}
