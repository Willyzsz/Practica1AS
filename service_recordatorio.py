from repository_recordatorio import RecordatorioRepository

class RecordatorioService:
    def __init__(self):
        self.repo = RecordatorioRepository()

    def crear_recordatorio(self, titulo, descripcion, fecha_hora, id_pendiente):
        if not all([titulo, descripcion, fecha_hora, id_pendiente]):
            raise ValueError("Faltan datos obligatorios")

        return self.repo.insert_recordatorio(
            titulo, descripcion, fecha_hora, id_pendiente
        )
