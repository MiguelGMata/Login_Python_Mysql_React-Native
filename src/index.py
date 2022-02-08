from app import app
from dotenv import load_dotenv

def page_erreur(error):
    return"<h1>Erreur 404, page non trouvée.</h1>", 404
    
if __name__ == '__main__':
    load_dotenv()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.register_error_handler(404, page_erreur)
    app.run(port = 3000, debug = True)

