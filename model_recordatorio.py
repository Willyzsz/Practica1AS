
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = "categorias"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String(100), nullable=False)

class Pendiente(db.Model):
    __tablename__ = "pendientes"
    idPendiente = db.Column(db.Integer, primary_key=True)
    tituloPendiente = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    idCategoria = db.Column(db.Integer, db.ForeignKey("categorias.idCategoria"), nullable=True)

class Recordatorio(db.Model):
    __tablename__ = "recordatorios"
    idRecordatorio = db.Column(db.Integer, primary_key=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey("categorias.idCategoria"), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    fechaHora = db.Column(db.DateTime, nullable=False)
    idPendiente = db.Column(db.Integer, db.ForeignKey("pendientes.idPendiente"), nullable=False)
