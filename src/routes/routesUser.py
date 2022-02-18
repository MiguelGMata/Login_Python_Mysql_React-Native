from flask import Blueprint, jsonify, request, redirect, url_for, session
from config.config import mysql
from flask_cors import cross_origin
import bcrypt

routes_user = Blueprint("routes_user", __name__)


#-------------------------------------------------------------------------
@cross_origin
@routes_user.route('/signUp', methods=['POST'])
def signUp():
    try:
        if  request.method == 'POST':
                data=(
                    request.json['nameUser'], 
                    request.json['email'],
                    bcrypt.hashpw(
                        request.json['password'].encode('utf-8'), 
                        bcrypt.gensalt()
                    ) 
                )
                cur = mysql.cursor()
                cur.execute("INSERT INTO users (nameUser, email, password) VALUES (%s,%s,%s)",(data))
                mysql.commit()
                session['email'] = data[1]
                return jsonify({'message': 'Nous avons bien reçu votre inscription, vous pouvez dès maintenant vous connecter !', 'exito': True})#, redirect(url_for('login'))   
        else:
            return jsonify({'errorMsg': 'Erreur, Utilisateur non ajouté'})
    except Exception as ex:
        return jsonify({'errorMsg': "Erreur utilisateur non ajouté", 'exito': False})

#-------------------------------------------------------------------------
@routes_user.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        email = (request.json['email'])
        password = request.json['password'].encode('utf-8')
        cur = mysql.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",[email])
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            if bcrypt.hashpw(password, user[3].encode('utf-8')) == user[3].encode('utf-8'):
                session['email'] = user[2]
                return jsonify({'message': 'Utilisateur connecté', 'user': user[0]})#, redirect(url_for('profil', id=id))
            else:
                return jsonify({'message': "L'email ne marche pas"})
        else:
           return jsonify({'message': "Erreur l'utilisateur ne marche pas"})
    else:
        return redirect(url_for('singUp'))


#-------------------------------------------------------------------------

@routes_user.route('/profil/<id>', methods=['GET'])
def profil(id):
    try:
        data = (id)
        cur = mysql.cursor()
        sql = "SELECT * FROM users WHERE id ='{0}'".format(id)
        cur.execute(sql)
        data = cur.fetchone()
        if data != None:
            user = {'id': data[0], 'nameUser': data[1], 'email': data[2]}
            return jsonify({'user': user, 'messagee': 'Utilisateur trouvée'})
        else:
            return jsonify({'message': 'Erreur, utilisateur non trouvée'})
    except Exception as ex:
         return jsonify({'message': 'Erreur'})

#-------------------------------------------------------------------------
@routes_user.route('/logout', methods=["GET", "POST"])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Session fermer'})
    except Exception as ex:
        return jsonify({'message': 'Erreur'})