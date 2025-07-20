import os
import base64
from typing import Optional, Dict, Any
from gtts import gTTS
from io import BytesIO

class TTSService:
    def __init__(self):
        """
        Initialise le service de synthèse vocale gTTS.
        Vérifie la disponibilité de la bibliothèque.
        """
        try:
            # gTTS est une bibliothèque Python, son "initialisation" ici
            # consiste principalement à s'assurer que les dépendances sont là.
            # Il n'y a pas d'API externe à configurer directement ici.
            self.is_available = True
            print("✅ Service gTTS initialisé avec succès (via la bibliothèque)")
        except Exception as e:
            # Capture les erreurs potentielles lors du chargement ou de l'initialisation de gTTS
            print(f"❌ Erreur d'initialisation gTTS: {e}")
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

        if not text.strip():
            return {
                'success': False,
                'error': "Le texte à synthétiser ne peut pas être vide."
            }

        try:
            # gTTS utilise des codes langue simples (ex: 'fr', 'en').
            # Nous extrayons la partie principale du code si elle contient un tiret (ex: 'fr-FR' -> 'fr').
            lang_code_simple = language_code.split('-')[0]

            # Instancie gTTS avec le texte et le code de langue simple
            tts = gTTS(text=text, lang=lang_code_simple)

            # Écrit l'audio dans un buffer en mémoire (BytesIO)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0) # Remettre le curseur au début du buffer pour la lecture

            # Encode l'audio en base64 pour le transfert via API
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

            return {
                'success': True,
                'audio_base64': audio_base64,
                'content_type': 'audio/mpeg', # gTTS génère toujours du MP3
                'text': text,
                'language_code': language_code
            }

        except Exception as e:
            print(f"❌ Erreur lors de la synthèse TTS avec gTTS pour le texte '{text}' en langue '{language_code}': {e}")
            return {
                'success': False,
                'error': f"Erreur lors de la génération audio: {str(e)}"
            }

    def _get_voice_config(self, language_code: str) -> Dict[str, Any]:
        """
        Cette méthode est obsolète avec gTTS car il n'y a pas de configuration de voix détaillée
        (comme le genre ou le nom de la voix spécifique) comme avec d'autres services TTS.
        Elle retourne une configuration générique.
        """
        print("WARN: _get_voice_config est appelée mais non applicable avec gTTS.")
        return {'language_code': language_code.split('-')[0], 'name': None, 'ssml_gender': None}

    def get_available_voices(self) -> Optional[list]:
        """
        Non applicable avec gTTS. Il n'y a pas de liste de voix disponibles à interroger
        ou à choisir explicitement comme avec des services TTS plus avancés.
        """
        print("WARN: get_available_voices est appelée mais non applicable avec gTTS.")
        return [] # Retourne une liste vide car gTTS ne liste pas les voix.

    def is_service_available(self) -> bool:
        """Vérifie si le service TTS est disponible."""
        return self.is_available

