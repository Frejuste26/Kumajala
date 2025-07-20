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
    Endpoint pour traduire du français vers une langue locale africaine.
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

        # --- DEBUGGING PRINTS START HERE ---
        print(f"\nDEBUG: Requête de traduction reçue: '{text}' vers '{target_language}'")
        print(f"DEBUG: FirestoreService est en mode local: {firestore_service.use_local_data}")

        # Recherche dans la base de données d'abord
        translation = firestore_service.get_translation(text, target_language)
        source = 'database'
        print(f"DEBUG: Résultat de la recherche Firestore/locale pour '{text}': '{translation}'")

        # Si pas trouvé dans la BD, utiliser Gemini comme fallback
        if not translation: # This condition triggers if translation is None or empty string
            print(f"DEBUG: Traduction non trouvée dans la base de données. Tentative avec Gemini.")
            if gemini_service.is_service_available():
                translation = gemini_service.translate_text(text, target_language)
                source = 'gemini'
                print(f"DEBUG: Résultat de la traduction Gemini: '{translation}'")

                # Sauvegarder la traduction Gemini pour usage futur
                if translation and translation != "TRADUCTION_IMPOSSIBLE":
                    print(f"DEBUG: Sauvegarde de la traduction Gemini dans la base de données.")
                    firestore_service.save_translation(text, target_language, translation)
            else:
                print("DEBUG: Service Gemini non disponible pour le fallback.")
        # --- DEBUGGING PRINTS END HERE ---

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
        print(f"❌ Erreur lors de la traduction dans la route translate: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@translate_bp.route('/translate/batch', methods=['POST'])
def translate_batch():
    """
    Endpoint pour traduire plusieurs textes en une seule requête.
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
        for text_item in texts: # Renommé 'text' en 'text_item' pour éviter le conflit de nom
            if not text_item or not isinstance(text_item, str):
                continue

            text_item = text_item.strip()
            if not text_item:
                continue

            # Recherche dans la base de données
            translation = firestore_service.get_translation(text_item, target_language)
            source = 'database'

            # Fallback vers Gemini
            if not translation and gemini_service.is_service_available():
                translation = gemini_service.translate_text(text_item, target_language)
                source = 'gemini'

                # Sauvegarder la traduction
                if translation and translation != "TRADUCTION_IMPOSSIBLE":
                    firestore_service.save_translation(text_item, target_language, translation)

            translations.append({
                'text': text_item,
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
        print(f"❌ Erreur lors de la traduction batch: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500


# NOUVEL ENDPOINT POUR L'AJOUT/MODIFICATION MANUELLE DE TRADUCTIONS
@translate_bp.route('/translations/manage', methods=['POST'])
def manage_translation():
    """
    Endpoint pour ajouter ou modifier manuellement une traduction.
    Requiert: frenchText, targetLanguage, newTranslation
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'Aucune donnée fournie'}), 400

        french_text = data.get('frenchText', '').strip()
        target_language = data.get('targetLanguage', '').strip().lower()
        new_translation = data.get('newTranslation', '').strip()

        if not french_text or not target_language or not new_translation:
            return jsonify({
                'success': False,
                'error': 'Les champs "frenchText", "targetLanguage" et "newTranslation" sont requis.'
            }), 400

        # Validation de la langue cible
        supported_languages = [lang['code'] for lang in firestore_service.get_supported_languages()]
        if target_language not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Langue cible non supportée. Langues disponibles: {", ".join(supported_languages)}'
            }), 400
        
        # Appel du service Firestore pour la mise à jour
        success = firestore_service.update_translation_manual(french_text, target_language, new_translation)

        if success:
            return jsonify({
                'success': True,
                'message': 'Traduction mise à jour/ajoutée avec succès.',
                'frenchText': french_text,
                'targetLanguage': target_language,
                'newTranslation': new_translation
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Échec de la mise à jour/ajout de la traduction.'
            }), 500

    except Exception as e:
        print(f"❌ Erreur lors de la gestion manuelle de la traduction: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur lors de la gestion manuelle de la traduction',
            'details': str(e)
        }), 500
