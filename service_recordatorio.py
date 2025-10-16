from repository_recordatorio import RecordatorioRepository

class RecordatorioService:
    def __init__(self):
        self.repo = RecordatorioRepository()

    def crear_recordatorio(self, idCategoria, mensaje, fechaHora, idPendiente):
        if not all([idCategoria, mensaje, fechaHora, idPendiente]):
            raise ValueError("Faltan datos obligatorios")

        return self.repo.insert_recordatorio(
            idCategoria, mensaje, fechaHora, idPendiente
        )

    def obtener_recordatorio(self, id):
        return self.repo.get_recordatorio(id)

    def actualizar_recordatorio(self, id, idCategoria, mensaje, fechaHora, idPendiente):
        if not all([idCategoria, mensaje, fechaHora, idPendiente]):
            raise ValueError("Faltan datos obligatorios")

        return self.repo.update_recordatorio(
            id, idCategoria, mensaje, fechaHora, idPendiente
        )

    def eliminar_recordatorio(self, id):
        return self.repo.delete_recordatorio(id)