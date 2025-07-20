from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import des Blueprints depuis le dossier 'routes'
from routes.translate import translate_bp
from routes.speak import speak_bp
from routes.languages import languages_bp

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

def create_app():
    """
    Crée et configure l'application Flask.
    """
    app = Flask(__name__)
    
    # Configuration CORS pour permettre les requêtes depuis le frontend Vue.js
    # Assurez-vous que 'http://localhost:5173' est l'URL de votre frontend en développement.
    CORS(app, origins=['http://localhost:5173'])
    
    # Configuration de l'application Flask
    # La clé secrète est utilisée pour la sécurité des sessions, etc.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kumajala-secret-key-default')
    # Le mode DEBUG est activé si FLASK_ENV est 'development'
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # Enregistrement des blueprints pour organiser les routes de l'API
    # Chaque blueprint est préfixé par '/kumajala-api/v1'
    app.register_blueprint(translate_bp, url_prefix='/kumajala-api/v1')
    app.register_blueprint(speak_bp, url_prefix='/kumajala-api/v1')
    app.register_blueprint(languages_bp, url_prefix='/kumajala-api/v1')
    
    # Route de base pour tester l'API et fournir des informations générales
    @app.route('/')
    def home():
        """
        Retourne des informations de base sur l'API Kumajala.
        """
        return jsonify({
            'message': 'KUMAJALA API - Valorisation des langues Africaines.',
            'version': '1.0.0',
            'endpoints': {
                'translate': '/kumajala-api/v1/translate',
                'speak': '/kumajala-api/v1/speak',
                'languages': '/kumajala-api/v1/languages',
                'manage_translations': '/kumajala-api/v1/translations/manage' # Ajout de l'endpoint de gestion
            }
        })
    
    # Gestionnaire d'erreurs pour les requêtes non trouvées (404)
    @app.errorhandler(404)
    def not_found(error):
        """
        Gère les erreurs 404 (Not Found).
        """
        return jsonify({'error': 'Endpoint non trouvé', 'details': str(error)}), 404
    
    # Gestionnaire d'erreurs pour les erreurs internes du serveur (500)
    @app.errorhandler(500)
    def internal_error(error):
        """
        Gère les erreurs 500 (Internal Server Error).
        """
        return jsonify({'error': 'Erreur interne du serveur', 'details': str(error)}), 500
    
    return app

if __name__ == '__main__':
    # Crée l'application Flask
    app = create_app()
    
    # Lance le serveur Flask
    # host='0.0.0.0' rend l'application accessible depuis n'importe quelle adresse IP
    # port=5000 est le port par défaut de Flask
    # debug=True active le mode débogage (rechargement automatique, messages d'erreur détaillés)
    app.run(host='0.0.0.0', port=5000, debug=True)
