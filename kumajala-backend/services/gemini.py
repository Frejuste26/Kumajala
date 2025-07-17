import os
import google.generativeai as genai
from typing import Optional

class GeminiService:
    def __init__(self):
        # Configuration de l'API Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY non définie. Service Gemini indisponible.")
            self.is_available = False
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_available = True
            print("✅ Service Gemini initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur d'initialisation Gemini: {e}")
            self.is_available = False
    
    def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """
        Traduit un texte vers une langue africaine locale en utilisant Gemini
        """
        if not self.is_available:
            return None
        
        try:
            # Construction du prompt contextualisé
            prompt = self._build_translation_prompt(text, target_language)
            
            # Génération de la réponse
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Nettoyer la réponse pour extraire seulement la traduction
                translation = self._clean_response(response.text)
                return translation
            
            return None
            
        except Exception as e:
            print(f"Erreur lors de la traduction Gemini: {e}")
            return None
    
    def _build_translation_prompt(self, text: str, target_language: str) -> str:
        """Construit un prompt contextualisé pour la traduction"""
        
        language_contexts = {
            'bété': {
                'description': 'langue parlée principalement en Côte d\'Ivoire, dans la région du centre-ouest',
                'examples': 'Bonjour = Akwaba, Merci = Akpé, Au revoir = Kan na'
            },
            'baoulé': {
                'description': 'langue akan parlée en Côte d\'Ivoire, principalement dans la région du centre',
                'examples': 'Bonjour = Mo ho, Merci = Akpé, Au revoir = Kan na'
            },
            'mooré': {
                'description': 'langue parlée principalement au Burkina Faso par le peuple Mossi',
                'examples': 'Bonjour = Ne y windga, Merci = Barka, Au revoir = Nan kã pãalem'
            }
        }
        
        context = language_contexts.get(target_language, {
            'description': f'langue africaine locale: {target_language}',
            'examples': ''
        })
        
        prompt = f"""
Tu es un expert en traduction vers les langues africaines locales.

Traduis le texte français suivant vers le {target_language} ({context['description']}).

Texte à traduire: "{text}"

Langue cible: {target_language}

Exemples de traductions en {target_language}:
{context['examples']}

Instructions importantes:
- Fournis UNIQUEMENT la traduction, sans explication
- Respecte la grammaire et la structure de la langue {target_language}
- Si le texte ne peut pas être traduit, réponds "TRADUCTION_IMPOSSIBLE"
- Adapte la traduction au contexte culturel local

Traduction:
"""
        
        return prompt
    
    def _clean_response(self, response: str) -> str:
        """Nettoie la réponse de Gemini pour extraire la traduction"""
        # Supprimer les préfixes courants
        response = response.strip()
        
        # Supprimer les guillemets si présents
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        
        # Supprimer les préfixes explicatifs
        prefixes_to_remove = [
            'Traduction:', 'Traduction :', 'Translation:', 'Translation :',
            'Réponse:', 'Réponse :', 'En', 'Le texte traduit est:'
        ]
        
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        return response
    
    def is_service_available(self) -> bool:
        """Vérifie si le service Gemini est disponible"""
        return self.is_available