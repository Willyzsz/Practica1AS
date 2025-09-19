from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Recordatorio(db.Model):
    __tablename__ = "recordatorios"
    idRecordatorio = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    id_pendiente = db.Column(db.Integer, db.ForeignKey("pendientes.idPendiente"), nullable=False)
