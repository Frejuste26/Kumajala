import os
import base64
from typing import Optional, Dict, Any
from google.cloud import texttospeech

class TTSService:
    def __init__(self):
        # Configuration du service Text-to-Speech
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            print("⚠️  GOOGLE_APPLICATION_CREDENTIALS non définie. Service TTS indisponible.")
            self.is_available = False
            return
        
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.is_available = True
            print("✅ Service Google TTS initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur d'initialisation Google TTS: {e}")
            self.is_available = False
    
    def synthesize_speech(self, text: str, language_code: str = "fr-FR") -> Optional[Dict[str, Any]]:
        """
        Synthétise la parole à partir du texte
        """
        if not self.is_available:
            return None
        
        try:
            # Configuration de la voix selon la langue
            voice_config = self._get_voice_config(language_code)
            
            # Préparation du texte
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configuration de la voix
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config['language_code'],
                name=voice_config.get('name'),
                ssml_gender=voice_config['ssml_gender']
            )
            
            # Configuration audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0
            )
            
            # Synthèse
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Encoder l'audio en base64 pour l'envoi via JSON
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            return {
                'success': True,
                'audio_base64': audio_base64,
                'content_type': 'audio/mpeg',
                'text': text,
                'language_code': language_code
            }
            
        except Exception as e:
            print(f"Erreur lors de la synthèse TTS: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_voice_config(self, language_code: str) -> Dict[str, Any]:
        """
        Retourne la configuration de voix selon la langue
        """
        voice_configs = {
            'fr-FR': {
                'language_code': 'fr-FR',
                'name': 'fr-FR-Standard-A',
                'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE
            },
            'en-US': {
                'language_code': 'en-US',
                'name': 'en-US-Standard-A',
                'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE
            },
            # Pour les langues locales, utiliser une voix française par défaut
            'bété': {
                'language_code': 'fr-FR',
                'name': 'fr-FR-Standard-B',
                'ssml_gender': texttospeech.SsmlVoiceGender.MALE
            },
            'baoulé': {
                'language_code': 'fr-FR',
                'name': 'fr-FR-Standard-C',
                'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE
            },
            'mooré': {
                'language_code': 'fr-FR',
                'name': 'fr-FR-Standard-D',
                'ssml_gender': texttospeech.SsmlVoiceGender.MALE
            }
        }
        
        return voice_configs.get(language_code, voice_configs['fr-FR'])
    
    def get_available_voices(self) -> Optional[list]:
        """
        Récupère la liste des voix disponibles
        """
        if not self.is_available:
            return None
        
        try:
            voices = self.client.list_voices()
            
            available_voices = []
            for voice in voices.voices:
                available_voices.append({
                    'name': voice.name,
                    'language_codes': list(voice.language_codes),
                    'ssml_gender': voice.ssml_gender.name
                })
            
            return available_voices
            
        except Exception as e:
            print(f"Erreur lors de la récupération des voix: {e}")
            return None
    
    def is_service_available(self) -> bool:
        """Vérifie si le service TTS est disponible"""
        return self.is_available