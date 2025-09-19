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
