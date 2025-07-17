from flask import Blueprint, jsonify
from services.firestore import FirestoreService

languages_bp = Blueprint('languages', __name__)

# Initialisation du service Firestore
firestore_service = FirestoreService()

@languages_bp.route('/languages', methods=['GET'])
def get_languages():
    """
    Endpoint pour récupérer la liste des langues supportées
    """
    try:
        languages = firestore_service.get_supported_languages()
        
        return jsonify({
            'success': True,
            'languages': languages,
            'totalLanguages': len(languages)
        })
        
    except Exception as e:
        print(f"Erreur lors de la récupération des langues: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@languages_bp.route('/languages/<language_code>', methods=['GET'])
def get_language_info(language_code):
    """
    Endpoint pour récupérer les informations d'une langue spécifique
    """
    try:
        language_code = language_code.lower().strip()
        languages = firestore_service.get_supported_languages()
        
        # Recherche de la langue
        language_info = None
        for lang in languages:
            if lang['code'] == language_code:
                language_info = lang
                break
        
        if not language_info:
            return jsonify({
                'success': False,
                'error': f'Langue "{language_code}" non trouvée'
            }), 404
        
        return jsonify({
            'success': True,
            'language': language_info
        })
        
    except Exception as e:
        print(f"Erreur lors de la récupération des informations de langue: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@languages_bp.route('/languages/<language_code>/translations', methods=['GET'])
def get_language_translations(language_code):
    """
    Endpoint pour récupérer toutes les traductions disponibles pour une langue
    """
    try:
        language_code = language_code.lower().strip()
        
        # Vérifier si la langue est supportée
        supported_languages = [lang['code'] for lang in firestore_service.get_supported_languages()]
        if language_code not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Langue "{language_code}" non supportée'
            }), 404
        
        # Pour l'instant, retourner les traductions depuis les données locales
        # Dans une version future, cela pourrait interroger directement Firestore
        if firestore_service.use_local_data:
            translations = firestore_service.local_translations.get("translations", {})
            language_translations = {}
            
            for french_text, trans_dict in translations.items():
                if language_code in trans_dict:
                    language_translations[french_text] = trans_dict[language_code]
        else:
            # TODO: Implémenter la récupération depuis Firestore
            language_translations = {}
        
        return jsonify({
            'success': True,
            'languageCode': language_code,
            'translations': language_translations,
            'totalTranslations': len(language_translations)
        })
        
    except Exception as e:
        print(f"Erreur lors de la récupération des traductions: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500