from flask import Blueprint, request, jsonify
from services.firestore import FirestoreService
from services.gemini import GeminiService
import time

translate_bp = Blueprint('translate', __name__)

# Initialisation des services
firestore_service = FirestoreService()
gemini_service = GeminiService()

@translate_bp.route('/translate', methods=['POST'])
def translate():
    """
    Endpoint pour traduire du français vers une langue locale africaine
    """
    start_time = time.time()
    
    try:
        # Validation des données d'entrée
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée fournie'
            }), 400
        
        text = data.get('text', '').strip()
        target_language = data.get('targetLanguage', '').strip().lower()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Texte à traduire manquant'
            }), 400
        
        if not target_language:
            return jsonify({
                'success': False,
                'error': 'Langue cible manquante'
            }), 400
        
        # Validation de la langue cible
        supported_languages = [lang['code'] for lang in firestore_service.get_supported_languages()]
        if target_language not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Langue non supportée. Langues disponibles: {", ".join(supported_languages)}'
            }), 400
        
        # Recherche dans la base de données d'abord
        translation = firestore_service.get_translation(text, target_language)
        source = 'database'
        
        # Si pas trouvé dans la BD, utiliser Gemini comme fallback
        if not translation and gemini_service.is_service_available():
            translation = gemini_service.translate_text(text, target_language)
            source = 'gemini'
            
            # Sauvegarder la traduction Gemini pour usage futur
            if translation and translation != "TRADUCTION_IMPOSSIBLE":
                firestore_service.save_translation(text, target_language, translation)
        
        # Si toujours pas de traduction
        if not translation:
            return jsonify({
                'success': False,
                'error': 'Traduction non disponible pour ce texte',
                'text': text,
                'targetLanguage': target_language
            }), 404
        
        # Vérifier si la traduction est impossible
        if translation == "TRADUCTION_IMPOSSIBLE":
            return jsonify({
                'success': False,
                'error': 'Ce texte ne peut pas être traduit dans cette langue',
                'text': text,
                'targetLanguage': target_language
            }), 422
        
        # Calcul du temps de traitement
        processing_time = round((time.time() - start_time) * 1000, 2)
        
        # Réponse de succès
        return jsonify({
            'success': True,
            'translation': translation,
            'text': text,
            'targetLanguage': target_language,
            'source': source,
            'processingTime': f"{processing_time}ms"
        })
        
    except Exception as e:
        print(f"Erreur lors de la traduction: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@translate_bp.route('/translate/batch', methods=['POST'])
def translate_batch():
    """
    Endpoint pour traduire plusieurs textes en une seule requête
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée fournie'
            }), 400
        
        texts = data.get('texts', [])
        target_language = data.get('targetLanguage', '').strip().lower()
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                'success': False,
                'error': 'Liste de textes manquante ou invalide'
            }), 400
        
        if not target_language:
            return jsonify({
                'success': False,
                'error': 'Langue cible manquante'
            }), 400
        
        # Validation de la langue cible
        supported_languages = [lang['code'] for lang in firestore_service.get_supported_languages()]
        if target_language not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Langue non supportée. Langues disponibles: {", ".join(supported_languages)}'
            }), 400
        
        # Traduction de chaque texte
        translations = []
        for text in texts:
            if not text or not isinstance(text, str):
                continue
                
            text = text.strip()
            if not text:
                continue
            
            # Recherche dans la base de données
            translation = firestore_service.get_translation(text, target_language)
            source = 'database'
            
            # Fallback vers Gemini
            if not translation and gemini_service.is_service_available():
                translation = gemini_service.translate_text(text, target_language)
                source = 'gemini'
                
                # Sauvegarder la traduction
                if translation and translation != "TRADUCTION_IMPOSSIBLE":
                    firestore_service.save_translation(text, target_language, translation)
            
            translations.append({
                'text': text,
                'translation': translation,
                'source': source,
                'success': translation is not None and translation != "TRADUCTION_IMPOSSIBLE"
            })
        
        return jsonify({
            'success': True,
            'translations': translations,
            'targetLanguage': target_language,
            'totalProcessed': len(translations)
        })
        
    except Exception as e:
        print(f"Erreur lors de la traduction batch: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500