from flask import Flask, render_template, request, flash,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os



dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
#Creacion de instancia Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MYKEY'
db = SQLAlchemy(app)
ma = Marshmallow(app)

#modelo de base de datos

class Corrida(db.Model):
    __tablename__ = "corrida"
    id = db.Column(db.Integer, primary_key = True)
    destino = db.Column(db.String(100), nullable = False)
    escala = db.Column(db.String, nullable = False)
    

class Terminal(db.Model):
    __tablename__ = "terminal"
    id = db.Column(db.Integer, primary_key = True)
    terminal = db.Column(db.String, nullable = False)

class Horarios(db.Model):
    __tablename__ = "horario"
    id = db.Column(db.Integer, primary_key = True)
    destino = db.Column(db.String(100), nullable = False)
    escala = db.Column(db.String, nullable = False)
    horario = db.Column(db.String, nullable = False)
    anden = db.Column(db.Integer, nullable = False)
    
#generando los Schema    






#creacion de rutas
@app.route('/', methods = ['GET'])
def panel():
	return render_template('index.html')


@app.route('/corridas', methods = ['GET', 'POST'])
def corridas():
    if request.method == 'POST':
        mensaje = ""
        destino = request.form['destino']
        escala = request.form['escala']
        if len(destino) == 0 or len(escala) == 0:
            mensaje = "Error Todos Los Campos Son Obligatorios"
        else: 
            new_corrida = Corrida()
            new_corrida.destino = destino
            new_corrida.escala = escala 
            db.session.add(new_corrida)
            db.session.commit()    
            mensaje = "Nueva Corrida Creada Con Exito"
        
        flash(mensaje)

        return redirect(url_for('corridas'))

    return render_template('corridas.html', corridas = Corrida.query)


@app.route('/horarios', methods = ['GET', 'POST'])
def horarios():
    if request.method == 'POST':
        mensaje = ""
        destino = request.form['destino']
        escala = request.form['escala']
        horario = request.form['horarios']
        anden = request.form['anden']
        if len(destino) == 0 or len(escala) == 0 or len(horario) == 0 or len(anden) == 0:
            mensaje = "Error Todos Los Campos Son Obligatorios"
        else:
            new_horario = Horarios()
            new_horario.destino = destino 
            new_horario.escala = escala 
            new_horario.horario = horario 
            new_horario.anden = anden 
            db.session.add(new_horario)
            db.session.commit()
            mensaje = "Nuevo Horario Agregado Con Exito"   
        flash(mensaje)
        return redirect(url_for('horarios'))

    return render_template('horarios.html', horarios = Horarios.query, corridas = Corrida.query)        

@app.route('/edit/<id>', methods = ['GET','POST'])
def edit(id):

    flash('aun no edita pero ya casi')
    return redirect(url_for('horarios'))


@app.route('/delete/<id>', methods = ['GET'])
def delete(id):
    id = id 
    Horarios.query.filter(Horarios.id == id).delete()
    db.session.commit()
    
    flash('Horario Eliminado')
        
    return redirect(url_for('horarios'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
