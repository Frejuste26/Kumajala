from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import des routes
from routes.translate import translate_bp as translate
from routes.speak import speak_bp as speak
from routes.languages import languages_bp as languages

# Charger les variables d'environnement
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration CORS pour permettre les requêtes depuis le frontend
    CORS(app, origins=['http://localhost:5173'])
    
    # Configuration de l'app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kumajala-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # Enregistrement des blueprints
    app.register_blueprint(translate, url_prefix='/kumajala-api/v1')
    app.register_blueprint(speak, url_prefix='/kumajala-api/v1')
    app.register_blueprint(languages, url_prefix='/kumajala-api/v1')
    
    # Route de base pour tester l'API
    @app.route('/')
    def home():
        return jsonify({
            'message': 'KUMAJALA API - Valorisation des langues Africaines.',
            'version': '1.0.0',
            'endpoints': {
                'translate': '/kumajala-api/v1/translate',
                'speak': '/kumajala-api/v1/speak',
                'languages': '/kumajala-api/v1/languages'
            }
        })
    
    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint non trouvé'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Erreur interne du serveur'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)