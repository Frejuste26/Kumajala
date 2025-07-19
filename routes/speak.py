from flask import Blueprint, request, jsonify
# --- CHANGE THIS LINE ---
# From: from services.tts import TTSService
# To:   from services.tts_service import TTSService
from services.tts import TTSService # Correct import path for your TTSService class
import time

speak_bp = Blueprint('speak', __name__)

# Initialisation du service TTS
tts_service = TTSService()

@speak_bp.route('/speak', methods=['POST'])
def speak():
    """
    Endpoint pour générer l'audio d'un texte traduit
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
        # Ensure language_code is 'fr' or 'en' for gTTS.
        # If frontend sends 'fr-FR', gTTS will use 'fr' from the tts_service logic.
        language_code = data.get('languageCode', 'fr').strip()

        if not text:
            return jsonify({
                'success': False,
                'error': 'Texte à synthétiser manquant'
            }), 400

        # Limitation de la longueur du texte
        if len(text) > 1000:
            return jsonify({
                'success': False,
                'error': 'Le texte est trop long (maximum 1000 caractères)'
            }), 400

        # Vérification de la disponibilité du service
        if not tts_service.is_service_available():
            return jsonify({
                'success': False,
                'error': 'Service de synthèse vocale indisponible'
            }), 503

        # Synthèse vocale
        # The synthesize_speech method no longer takes a 'voice_name' parameter with gTTS.
        result = tts_service.synthesize_speech(text, language_code)

        if not result:
            return jsonify({
                'success': False,
                'error': 'Échec de la synthèse vocale (réponse TTS service vide)' # More specific error message
            }), 500

        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Erreur inconnue lors de la synthèse')
            }), 500

        # Calcul du temps de traitement
        processing_time = round((time.time() - start_time) * 1000, 2)

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
        print(f"Erreur lors de la synthèse vocale dans la route speak: {e}") # Clarify log origin
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500
