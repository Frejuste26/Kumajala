from flask import Blueprint, request, jsonify
from services.tts import TTSService # Correct import path for your TTSService class
import time

speak_bp = Blueprint('speak', __name__)

# Initialisation du service TTS
tts_service = TTSService()

@speak_bp.route('/speak', methods=['POST'])
def speak():
    """
    Endpoint pour générer l'audio d'un texte traduit.
    """
    start_time = time.time()

    try:
        # Validation des données d'entrée
        data = request.get_json()

        if not data:
            print("❌ Erreur: Aucune donnée fournie pour la synthèse vocale.")
            return jsonify({
                'success': False,
                'error': 'Aucune donnée fournie'
            }), 400

        text = data.get('text', '').strip()
        # language_code est la langue dans laquelle le texte a été traduit,
        # gTTS l'utilisera pour la synthèse.
        language_code = data.get('languageCode', 'fr').strip()

        if not text:
            print("❌ Erreur: Texte à synthétiser manquant.")
            return jsonify({
                'success': False,
                'error': 'Texte à synthétiser manquant'
            }), 400

        # Limitation de la longueur du texte pour éviter les abus et les longs traitements
        if len(text) > 1000:
            print(f"❌ Erreur: Texte trop long ({len(text)} chars) pour la synthèse vocale.")
            return jsonify({
                'success': False,
                'error': 'Le texte est trop long (maximum 1000 caractères)'
            }), 400

        # Vérification de la disponibilité du service TTS
        if not tts_service.is_service_available():
            print("❌ Erreur: Service de synthèse vocale indisponible.")
            return jsonify({
                'success': False,
                'error': 'Service de synthèse vocale indisponible'
            }), 503

        print(f"DEBUG: Tentative de synthèse vocale pour '{text[:50]}...' en '{language_code}'")
        # Synthèse vocale via le service TTSService
        result = tts_service.synthesize_speech(text, language_code)

        if not result or not result.get('success'):
            error_message = result.get('error', 'Erreur inconnue lors de la synthèse vocale.')
            print(f"❌ Échec de la synthèse vocale: {error_message}")
            return jsonify({
                'success': False,
                'error': error_message
            }), 500

        # Calcul du temps de traitement
        processing_time = round((time.time() - start_time) * 1000, 2)
        print(f"✅ Synthèse vocale réussie en {processing_time}ms.")

        # Réponse de succès
        return jsonify({
            'success': True,
            'audioBase64': result['audio_base64'],
            'contentType': result['content_type'],
            'text': text,
            'languageCode': language_code,
            'processingTime': f"{processing_time}ms"
        })

    except Exception as e:
        print(f"❌ Erreur inattendue lors de la synthèse vocale dans la route speak: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

