from flask import Blueprint, request, jsonify
from services.tts import TTSService
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
        language_code = data.get('languageCode', 'fr-FR').strip()
        
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
        result = tts_service.synthesize_speech(text, language_code)
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Échec de la synthèse vocale'
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
        print(f"Erreur lors de la synthèse vocale: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500

@speak_bp.route('/speak/voices', methods=['GET'])
def get_voices():
    """
    Endpoint pour récupérer la liste des voix disponibles
    """
    try:
        # Vérification de la disponibilité du service
        if not tts_service.is_service_available():
            return jsonify({
                'success': False,
                'error': 'Service de synthèse vocale indisponible'
            }), 503
        
        # Récupération des voix disponibles
        voices = tts_service.get_available_voices()
        
        if voices is None:
            return jsonify({
                'success': False,
                'error': 'Impossible de récupérer la liste des voix'
            }), 500
        
        return jsonify({
            'success': True,
            'voices': voices,
            'totalVoices': len(voices)
        })
        
    except Exception as e:
        print(f"Erreur lors de la récupération des voix: {e}")
        return jsonify({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }), 500