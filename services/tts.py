import os
import base64
from typing import Optional, Dict, Any
from gtts import gTTS
from io import BytesIO

class TTSService:
    def __init__(self):
        try:
            self.is_available = True
            print("Service gTTS initialisé avec succès (via la bibliothèque)")
        except Exception as e:
            # This catch might be for cases where gTTS itself fails to load or other unexpected issues
            print(f"Erreur d'initialisation gTTS: {e}")
            self.is_available = False

    def synthesize_speech(self, text: str, language_code: str = "fr") -> Optional[Dict[str, Any]]:
        """
        Synthétise la parole à partir du texte en utilisant gTTS.
        language_code doit être un code ISO 639-1 (ex: 'fr', 'en').
        """
        if not self.is_available:
            return {
                'success': False,
                'error': "Service TTS non disponible (gTTS initialisation échouée)"
            }

        try:
            # gTTS utilise des codes langue simples (ex: 'fr', 'en').
            # Nous extrayons la partie principale du code si elle contient un tiret.
            lang_code_simple = language_code.split('-')[0]

            # Instancie gTTS
            tts = gTTS(text=text, lang=lang_code_simple)

            # Écrit l'audio dans un buffer en mémoire
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0) # Remettre le curseur au début du buffer

            # Encode l'audio en base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

            return {
                'success': True,
                'audio_base64': audio_base64,
                'content_type': 'audio/mpeg', # gTTS génère toujours du MP3
                'text': text,
                'language_code': language_code
            }

        except Exception as e:
            print(f"Erreur lors de la synthèse TTS avec gTTS: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # Les méthodes suivantes ne sont pas applicables ou nécessaires avec gTTS
    # car gTTS ne fournit pas de contrôle fin sur les voix ni de liste des voix disponibles.
    def _get_voice_config(self, language_code: str) -> Dict[str, Any]:
        """
        Cette méthode est obsolète avec gTTS car il n'y a pas de configuration de voix détaillée.
        Elle retourne une configuration générique ou lève une erreur si appelée.
        """
        print("WARN: _get_voice_config est appelée mais non applicable avec gTTS.")
        return {'language_code': language_code.split('-')[0], 'name': None, 'ssml_gender': None}

    def get_available_voices(self) -> Optional[list]:
        """
        Non applicable avec gTTS. Il n'y a pas de liste de voix disponibles à interroger.
        """
        print("WARN: get_available_voices est appelée mais non applicable avec gTTS.")
        return [] # Retourne une liste vide car gTTS ne liste pas les voix.

    def is_service_available(self) -> bool:
        """Vérifie si le service TTS est disponible"""
        return self.is_available