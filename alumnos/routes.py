from . import alumnos
from flask import render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from alumnos.routes import alumnos, alumnos
from models import db
from models import Alumnos,Curso

@alumnos.route("/alumnos",methods=['GET','POST'])
def index():
	create_form=forms.UserForm(request.form)
	alumno=Alumnos.query.all()
	return render_template("alumnos/listadoAlum.html",form=create_form,alumno=alumno)

@alumnos.route("/Alumnos", methods=['GET','POST'])
def Alumno():
	create_form=forms.UserForm(request.form)
	if request.method=="POST":
		alum=Alumnos(nombre=create_form.nombre.data,
			   		apellidos=create_form.apellidos.data,
					email=create_form.email.data,
					telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/Alumnos.html",form=create_form)

@alumnos.route("/detalles", methods=['GET','POST'])
def detalles():
	create_form=forms.UserForm(request.form)
	if request.method=="GET":
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
	return render_template("alumnos/detalles.html",nombre=nombre,apellidos=apellidos,email=email,telefono=telefono)

@alumnos.route("/modificar", methods=['GET','POST'])
def modificar():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alm1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		create_form.id.data=alm1.id
		create_form.nombre.data=alm1.nombre
		create_form.apellidos.data=alm1.apellidos
		create_form.email.data=alm1.email
		create_form.telefono.data=alm1.telefono
		
	if request.method == 'POST':
		id=request.args.get('id')
		alm1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alm1.id=id
		alm1.nombre=create_form.nombre.data
		alm1.apellidos=create_form.apellidos.data
		alm1.email=create_form.email.data
		alm1.telefono=create_form.telefono.data
		db.session.add(alm1)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/modificar.html", form=create_form)

@alumnos.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alm1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		create_form.id.data=alm1.id
		create_form.nombre.data=alm1.nombre
		create_form.apellidos.data=alm1.apellidos
		create_form.email.data=alm1.email
		create_form.telefono.data=alm1.telefono
		
	if request.method == 'POST':
		id=request.args.get('id')
		alm1 = Alumnos.query.get(id)
		db.session.delete(alm1)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/eliminar.html", form=create_form)

@alumnos.route("/perfil-academico/<int:id>")
def perfil_academico(id):
    # Buscamos al alumno o lanzamos 404 si no existe
    alumno_obj = Alumnos.query.get_or_404(id)
    
    # 'cursos' es el nombre que definimos en el backref del modelo
    # Esto nos da la lista de objetos 'Curso' automáticamente
    cursos_del_alumno = alumno_obj.cursos 
    
    return render_template("alumnos/perfil_academico.html", 
                           alumno=alumno_obj, 
                           cursos=cursos_del_alumno)

@alumnos.route("/buscar-alumno-cursos", methods=['GET', 'POST'])
def buscar_por_nombre():
    alumno_encontrado = None
    cursos = []
    busqueda_realizada = False
    
    todos_los_alumnos = Alumnos.query.all()
    
    if request.method == 'POST':
        busqueda_realizada = True
        alumno_id = request.form.get('alumno_id')
        
        if alumno_id:
            alumno_encontrado = Alumnos.query.get(alumno_id)
            if alumno_encontrado:
                cursos = alumno_encontrado.cursos
                
    return render_template("cursos/buscadorCursos.html", 
                           alumno=alumno_encontrado, 
                           cursos=cursos, 
                           alumnos_list=todos_los_alumnos, # Pasamos la lista completa
                           busqueda_realizada=busqueda_realizada)