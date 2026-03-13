from . import maestros
from flask import render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from maestros.routes import maestros, maestros
from models import db
from models import Maestros

@maestros.route("/maestros",methods=['GET','POST'])

def index():
    create_form = forms.MaestrosForm(request.form)
    maestros_list = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maestros_list)

@maestros.route("/Maestro", methods=['GET', 'POST'])
def Maestro():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'POST' and create_form.validate():
        # 1. Validar si el nombre ya existe
        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        
        existente = Maestros.query.filter_by(nombre=nombre, apellidos=apellidos).first()
        
        if existente:
            flash(f"Error: El maestro ya está registrado.", "danger")
            return render_template("maestros/Maestro.html", form=create_form)

        # 2. Si no existe, proceder con el registro
        maes = Maestros(
            nombre=nombre,
            apellidos=apellidos,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(maes)
        db.session.commit()
        flash("Maestro registrado exitosamente", "success")
        return redirect(url_for('maestros.index'))
        
    return render_template("maestros/Maestro.html", form=create_form)

@maestros.route("/modificarMaestro", methods=['GET', 'POST'])
def modificarMaestro():
    create_form = forms.MaestrosForm(request.form)
    
    if request.method == 'GET':
        matricula = request.args.get('id') 
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            create_form.matricula.data = maes1.matricula
            create_form.nombre.data = maes1.nombre
            create_form.apellidos.data = maes1.apellidos
            create_form.email.data = maes1.email
            create_form.especialidad.data = maes1.especialidad

    if request.method == 'POST':
        matricula = create_form.matricula.data
        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        
        # Validar que el nuevo nombre no choque con OTRO registro diferente al actual
        # Usamos .filter(Maestros.matricula != matricula) para excluir al maestro que estamos editando
        choque_nombre = Maestros.query.filter(
            Maestros.nombre == nombre, 
            Maestros.apellidos == apellidos,
            Maestros.matricula != matricula
        ).first()

        if choque_nombre:
            flash(f"No se pudo actualizar: Ya existe otro maestro", "danger")
            return render_template("maestros/modificarMaestro.html", form=create_form)

        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            maes1.nombre = nombre
            maes1.apellidos = apellidos
            maes1.email = create_form.email.data
            maes1.especialidad = create_form.especialidad.data
            
            db.session.commit()
            flash("Datos actualizados correctamente", "success")
            return redirect(url_for('maestros.index'))

    return render_template("maestros/modificarMaestro.html", form=create_form)

@maestros.route("/detallesMaestro", methods=['GET', 'POST'])
def detallesMaestro():
    create_form = forms.MaestrosForm(request.form)
    matricula = request.args.get('id')
    maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
    
        
    return render_template("maestros/detallesMaestro.html", 
                           form=create_form, 
                           matricula=matricula, 
                           nombre=maes1.nombre, 
                           apellidos=maes1.apellidos, 
                           especialidad=maes1.especialidad, 
                           email=maes1.email) 



@maestros.route("/eliminarMaestro", methods=['GET', 'POST'])
def eliminarMaestro():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('id')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            create_form.matricula.data = maes1.matricula
            create_form.nombre.data = maes1.nombre
            create_form.apellidos.data = maes1.apellidos
            create_form.especialidad.data = maes1.especialidad
            create_form.email.data = maes1.email
        
            
    if request.method == 'POST':
        matricula = create_form.matricula.data
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            db.session.delete(maes1)
            db.session.commit()
        return redirect(url_for('maestros.index'))
        
    return render_template("maestros/eliminarMaestro.html", form=create_form)

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"