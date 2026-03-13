from flask import render_template, request, redirect, url_for, flash
from . import cursos # Importas el objeto Blueprint desde el __init__.py local
import forms
from models import db, Curso
from models import Maestros,Alumnos,Inscription

@cursos.route("/cursos", methods=['GET', 'POST'])
def index():
    create_form = forms.CurseForm(request.form)
    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_db]
    curso = Curso.query.all()
    return render_template("cursos/listadoCur.html", form=create_form, curso=curso, lista=curso)

@cursos.route("/consultar_inscritos/<int:id>")
def consultar_inscritos(id):
    curso_obj = Curso.query.get_or_404(id)
    return render_template("cursos/lista_inscritos.html", 
                           curso=curso_obj, 
                           alumnos=curso_obj.alumnos)

@cursos.route("/inscribir-alumno", methods=['GET', 'POST'])
def inscribir_alumno(curso_id=None):
    form = forms.InscripcionForm(request.form)
    
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()]
    form.cursos_id.choices = [(c.id, c.nombre) for c in Curso.query.all()]

    if request.method == 'GET' and curso_id:
        form.cursos_id.data = curso_id

    if request.method == 'POST':
        id_alumn = form.alumno_id.data
        id_curs = form.cursos_id.data
        
        existe = Inscription.query.filter_by(alumno_id=id_alumn, cursos_id=id_curs).first()
        
        if existe:
            flash("Error: Este alumno ya se encuentra inscrito en esta materia.", "warning")
            return render_template("cursos/Cursos.html", form=form)
        
        nueva_ins = Inscription(
            alumno_id = id_alumn,
            cursos_id = id_curs
        )
        db.session.add(nueva_ins)
        db.session.commit()
        return redirect(url_for('cursos.index'))
            
    return render_template("cursos/Cursos.html", form=form)

@cursos.route("/agregar-curso", methods=['GET', 'POST'])
def agregar_curso():
    create_form = forms.CurseForm(request.form)
    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_db]

    if request.method == "POST":
        curso_nuevo = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(curso_nuevo)
        db.session.commit()
        return redirect(url_for('cursos.index'))
    return render_template("cursos/crearCurso.html", form=create_form)

@cursos.route("/detalles-curso", methods=['GET', 'POST'])
def detalles():
    id = request.args.get('id')
    curso_obj = db.session.query(Curso).filter(Curso.id == id).first()
    
    return render_template("cursos/detallesCurso.html", curso=curso_obj)

@cursos.route("/modificar-curso", methods=['GET', 'POST'])
def modificar():
    create_form = forms.CurseForm(request.form)
    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_db]
    id = request.args.get('id')

    if request.method == 'GET':
        curso_obj = db.session.query(Curso).filter(Curso.id == id).first()
        if curso_obj:
            create_form.id.data = curso_obj.id
            create_form.nombre.data = curso_obj.nombre
            create_form.descripcion.data = curso_obj.descripcion
            create_form.maestro_id.data = curso_obj.maestro_id
        
    if request.method == 'POST':
        curso_obj = db.session.query(Curso).filter(Curso.id == id).first()
        if curso_obj:
            curso_obj.nombre = create_form.nombre.data
            curso_obj.descripcion = create_form.descripcion.data
            curso_obj.maestro_id = create_form.maestro_id.data
            
            db.session.add(curso_obj)
            db.session.commit()
            return redirect(url_for('cursos.index'))
            
    return render_template("cursos/modificarCurso.html", form=create_form)


@cursos.route("/eliminar-curso", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.CurseForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso_obj = db.session.query(Curso).filter(Curso.id == id).first()
        # Llenado manual para que el HTML "Readonly" muestre los datos
        create_form.id.data = curso_obj.id
        create_form.nombre.data = curso_obj.nombre
        create_form.descripcion.data = curso_obj.descripcion
        
    if request.method == 'POST':
        id = request.args.get('id')
        curso_obj = Curso.query.get(id)
        db.session.delete(curso_obj)
        db.session.commit()
        return redirect(url_for('cursos.index'))
        
    return render_template("cursos/eliminarCurso.html", form=create_form)