from wtforms import Form
from wtforms import StringField,IntegerField,PasswordField,SelectField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form): 
    id=IntegerField('id')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido')
        ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido')
        ])
    email=EmailField('Correo',[
        validators.Email(message='Ingrese un correo valido')
        ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El teléfono es requerido')
        ])

class MaestrosForm(Form):
    matricula=IntegerField('id')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido')
        ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido')
        ])
    especialidad = StringField('especialidad', [
        validators.DataRequired(message='La especialidad es requerido')
        ])
    email=EmailField('Correo',[
        validators.Email(message='Ingrese un correo valido')
        ])
    
class CurseForm(Form):
    id=IntegerField('id')
    nombre=StringField('nombre', [validators.DataRequired(message='El campo es requerido')])
    descripcion=StringField('descripcion',[validators.DataRequired(message='El campo es requerido')])
    maestro_id = SelectField('Maestro Asignado', coerce=int, validators=[
        validators.DataRequired(message='Debe asignar un maestro al curso')
    ])

class InscripcionForm(Form):
    alumno_id = SelectField('Alumno', coerce=int)
    cursos_id = SelectField('Curso', coerce=int)