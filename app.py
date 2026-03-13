from flask import Flask, render_template, request, redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask import g
from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos

import forms

from models import db
from models import Alumnos
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
app.register_blueprint(cursos)
db.init_app(app)
migrate=Migrate(app, db)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.route("/",methods=['GET','POST'])
def inicio():
	return render_template('index.html')

#@app.route("/index")
#def index():
#	return render_template('404.html'),404



if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(debug=True)
