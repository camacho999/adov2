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

class Time(db.Model):
    __tablename__ = "time"
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.Integer)

class Horarios(db.Model):
    __tablename__ = "horario"
    id = db.Column(db.Integer, primary_key = True)
    destino = db.Column(db.String(100), nullable = False)
    escala = db.Column(db.String, nullable = False)
    horario = db.Column(db.String, nullable = False)
    anden = db.Column(db.Integer, nullable = False)
    
#generando los Schema    






#creacion de rutas
@app.route('/', methods = ['GET'])  # Pagina Principal
def panel():
	return render_template('index.html') 


@app.route('/corridas', methods = ['GET', 'POST']) #vista de Corridas
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

    return render_template('corridas.html', corridas = Corrida.query, terminal = Terminal.query.first())

@app.route('/editar_terminal', methods = ['POST']) #Actualización de Terminal
def editar_terminal():
    if request.method == 'POST':
        mensaje = ""
        terminal = request.form['terminal']
        t = Terminal.query.first()
        if t is None:
            t = Terminal()
            t.terminal = terminal
            db.session.add(t)
            db.session.commit()
        else:    
            t.terminal = terminal 
            db.session.add(t)
            db.session.commit()

        mensaje = "La terminal fue actualizada correctamente a {}.".format(terminal)

    flash(mensaje)    
    return redirect(url_for('corridas'))    

@app.route('/modal1/<id>', methods = ['GET', 'POST']) # Modal para edicion de corridas
def modal1(id):
    id = id 
    return render_template('modal1.html', corrida = Corrida.query.filter(Corrida.id == id).first())


@app.route('/edith_corrida/<id>', methods = ['GET','POST']) # Ruta para modificacion de Corridas
def edit_corrida(id):
    if request.method == 'POST':
        id = id
        mensaje = ""
        nc = Corrida.query.filter(Corrida.id == id).first()
        n_escala = request.form['escala']
        
        if len(n_escala) == 0:
            mensaje = "Error: los campos no pueden quedar vacios."
        else:
            nc.escala = n_escala
            db.session.add(nc)
            db.session.commit()
            mensaje = "El horario fue modificado satisfactoriamente."
    flash(mensaje)
    return redirect(url_for('corridas'))

@app.route('/delete_corridas/<id>', methods = ['GET']) # Funcion para eliminacion de Corridas
def delete_corridas(id):
    id = id 
    Corrida.query.filter(Corrida.id == id).delete()
    db.session.commit()
    
    flash('Corrida Eliminada Satisfactoriamente')
        
    return redirect(url_for('corridas'))




@app.route('/horarios', methods = ['GET', 'POST']) # pagina de Horarios
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

    return render_template('horarios.html', horarios = Horarios.query, corridas = Corrida.query, time = Time.query.first())        

@app.route('/edith/<id>', methods = ['GET','POST']) # Ruta para editar horarios
def edit(id):
    if request.method == 'POST':
        id = id
        mensaje = ""
        hn = Horarios.query.filter(Horarios.id == id).first()
        n_horario = request.form['horario']
        n_anden = request.form['anden']
        if len(n_horario) == 0 or len(n_anden) == 0:
            mensaje = "Error: los campos no pueden quedar vacios."
        else:
            hn.horario = n_horario
            hn.anden = n_anden
            db.session.add(hn)
            db.session.commit()
            mensaje = "El horario fue modificado satisfactoriamente."
    flash(mensaje)
    return redirect(url_for('horarios'))                


@app.route('/delete/<id>', methods = ['GET']) # Funcion para eliminacion de Horarios
def delete(id):
    id = id 
    Horarios.query.filter(Horarios.id == id).delete()
    db.session.commit()
    
    flash('Horario Eliminado')
        
    return redirect(url_for('horarios'))


@app.route('/modal/<id>', methods = ['GET', 'POST']) # Modal para edicion de horarios
def modal(id):
    id = id 
    return render_template('modal.html', horario = Horarios.query.filter(Horarios.id == id).first())


@app.route('/time', methods = ['POST']) # Funcion para modificar el tiempo de de las transciciones
def time():
    mensaje = ""
    if request.method == 'POST':
        time = request.form['time']
        if int(time) == 0:
            mensaje = ("El valor proporcionado no es correcto. El tiempo no fue modificado")     
        else:
            t = Time.query.filter(Time.id == 1).first()
            if t is None:
                new_time = Time()
                new_time.time = time
                db.session.add(new_time)
                db.session.commit()
            else:
                t.time = time
                db.session.add(t)
                db.session.commit()

            mensaje=("El tiempo de transición fue modificado correctamente a {} segundos.".format(time))



    flash(mensaje)
    return redirect(url_for('horarios'))


@app.route('/display', methods = ['GET'])
def dispay():

    return(render_template('display.html', horario = Horarios.query.all(), terminal = Terminal.query.first(), tiempo = Time.query.first()))

if __name__ == '__main__': #funcion principal
    db.create_all()
    app.run(debug=True, host = "0.0.0.0")
