from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return "<h1>Serveur en route dans le port 3000 Test.</h1>"

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return "<h1>register</h1>"
    else:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password))
        mysql.connection.commit()
        
        session['email'] = request.json['email']
        return jsonify({'user': name,'mensage': 'Utilisateur ajouté'}), redirect(url_for('login'))   
        

@app.route('/home', methods=['GET'])
def users():
    try:
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM users"
        cur.execute(sql)
        datos = cur.fetchall()
        users = []
        for fila in datos:
            user = {'id': fila[0], 'name': fila[1], 'email': fila[2], 'password': fila[3]}
            users.append(user)
        return jsonify({'Users': users, 'mensaje': "Liste de utilisateurs.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/profil/<id>', methods=['GET'])
def profil(id):
    try:
        data = (id)
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE id ='{0}'".format(id)
        cur.execute(sql)
        data = cur.fetchone()
        if data != None:
            user = {'id': data[0], 'name': data[1], 'email': data[2]}
            return jsonify({'user': user, 'mensage': 'Utilisateur trouvée'})
        else:
            return jsonify({'mensage': 'Erreur, utilisateur non trouvée'})
    except Exception as ex:
        return jsonify({'mensage': 'Erreur'})


def page_erreur(error):
    return"<h1>Erreur 404, page non trouvée.</h1>", 404
    
if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.register_error_handler(404, page_erreur)
    app.run(port = 3000, debug = True)
  

