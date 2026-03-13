import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 

class Alumnos(db.Model):
    __tablename__="alumnos"
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apellidos=db.Column(db.String(50))
    email=db.Column(db.String(100))
    telefono=db.Column(db.String(50))
    created_date=db.Column(db.DateTime, default=datetime.datetime.now)

    # Relación Muchos a Muchos con Cursos
    cursos = db.relationship('Curso',
                            secondary='inscripciones',
                            back_populates='alumnos')

class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    # Relación Uno a Muchos con Curso
    cursos = db.relationship('Curso', back_populates='maestro')

class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    # Clave foránea corregida
    maestro_id = db.Column(
        db.Integer,
        db.ForeignKey('maestros.matricula'),
        nullable=False # <--- Corregido
    ) 

    # Referencias a nombres de clases corregidas (Maestros y Alumnos)
    maestro = db.relationship('Maestros', back_populates='cursos')
    alumnos = db.relationship(
        'Alumnos',
        secondary='inscripciones',
        back_populates='cursos',
    )   

class Inscription(db.Model):
    __tablename__ ='inscripciones'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(
        db.Integer, 
        db.ForeignKey('alumnos.id'),
        nullable=False
    )

    cursos_id = db.Column(
        db.Integer,
        db.ForeignKey('cursos.id'),
        nullable=False
    )

    fecha_inscripcion = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Corregido el nombre de la columna y agregada la coma para la tupla
    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'cursos_id', name='uq_alumno_curso'),
    )

