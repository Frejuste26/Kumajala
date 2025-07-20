from flask import Blueprint, jsonify, request
from services.firestore import FirestoreService

languages_bp = Blueprint('languages', __name__)

# Initialisation du service Firestore
firestore_service = FirestoreService()

@languages_bp.route('/languages', methods=['GET'])
def get_languages():
    """
    Endpoint pour récupérer la liste des langues supportées.
    """
    try:
        languages = firestore_service.get_supported_languages()
        
        return jsonify({
            'success': True,
            'languages': languages,
            'totalLanguages': len(languages)
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des langues: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@languages_bp.route('/languages/<language_code>', methods=['GET'])
def get_language_info(language_code):
    """
    Endpoint pour récupérer les informations d'une langue spécifique.
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
        print(f"❌ Erreur lors de la récupération des informations de langue: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@languages_bp.route('/languages/<target_language_code>/translations', methods=['GET'])
def get_language_translations(target_language_code):
    """
    Endpoint pour récupérer toutes les traductions disponibles du français vers une langue cible spécifique.
    Note: Pour l'instant, cela ne retourne que les traductions stockées localement.
    La récupération de toutes les traductions pour une langue cible depuis Firestore nécessiterait
    une approche de requête différente (par exemple, une collection de sous-documents par langue,
    ou une itération sur tous les documents de la collection 'translations' et filtrage côté serveur).
    """
    try:
        target_language_code = target_language_code.lower().strip()
        
        # Vérifier si la langue cible est supportée
        supported_languages = [lang['code'] for lang in firestore_service.get_supported_languages()]
        if target_language_code not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Langue cible "{target_language_code}" non supportée'
            }), 404
        
        language_translations = {}

        if firestore_service.use_local_data:
            # Accéder à la structure correcte des traductions locales
            # self.local_translations est de la forme {"fr": {"texte_fr": {"lang_cible": "traduction"}}}
            french_translations = firestore_service.local_translations.get("fr", {})
            
            for french_text, translations_for_text in french_translations.items():
                if target_language_code in translations_for_text:
                    language_translations[french_text] = translations_for_text[target_language_code]
            
        else:
            # TODO: Implémenter la récupération de toutes les traductions pour une langue cible depuis Firestore.
            # Cela pourrait impliquer:
            # 1. Une requête de collection pour tous les documents de 'translations'.
            # 2. Pour chaque document, vérifier si le champ 'target_language_code' existe et l'ajouter.
            # C'est potentiellement coûteux si la collection est grande.
            # Une meilleure structure Firestore pourrait être 'translations_by_lang/{lang_code}/{french_text_doc}'
            # ou d'utiliser des requêtes de collection groupées si la structure le permet.
            print(f"WARN: Récupération de toutes les traductions pour '{target_language_code}' depuis Firestore n'est pas implémentée.")
            pass # Pour l'instant, ne fait rien et retourne un dictionnaire vide si Firestore est utilisé.
        
        return jsonify({
            'success': True,
            'languageCode': target_language_code,
            'translations': language_translations,
            'totalTranslations': len(language_translations)
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des traductions pour la langue cible: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

