import os
import google.generativeai as genai
from typing import Optional

class GeminiService:
    def __init__(self):
        # Configuration de l'API Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️ GEMINI_API_KEY non définie. Service Gemini indisponible.")
            self.is_available = False
            return

        try:
            genai.configure(api_key=api_key)
            # Utiliser gemini-2.0-flash comme spécifié dans les instructions
            # C'est généralement plus rapide et plus économique pour ce type de tâche.
            self.model = genai.GenerativeModel('gemini-2.0-flash')
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
            print("DEBUG: GeminiService non disponible, skipping translation.")
            return None

        try:
            # Construction du prompt contextualisé
            prompt = self._build_translation_prompt(text, target_language)

            # Génération de la réponse
            # Utilisation de generate_content pour un appel non-streaming
            response = self.model.generate_content(prompt)

            # Vérification de la structure de la réponse avant d'accéder à .text
            # Gemini peut parfois ne pas retourner de texte directement dans 'response.text'
            # mais dans response.candidates[0].content.parts[0].text
            translated_content = ""
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    translated_content += part.text
            else:
                print(f"WARN: Réponse Gemini inattendue ou vide pour le texte '{text}'.")
                return None # Retourne None si la structure de réponse n'est pas celle attendue

            if translated_content:
                # Nettoyer la réponse pour extraire seulement la traduction
                translation = self._clean_response(translated_content)
                # Vérifier si la traduction nettoyée est un marqueur d'impossibilité
                if translation.upper() == "TRADUCTION_IMPOSSIBLE":
                    print(f"INFO: Gemini a indiqué 'TRADUCTION_IMPOSSIBLE' pour '{text}' en '{target_language}'.")
                    return None # Retourne None pour que le fallback soit activé si c'est le cas
                return translation

            return None

        except Exception as e:
            print(f"❌ Erreur lors de la traduction Gemini pour '{text}' en '{target_language}': {e}")
            return None

    def _build_translation_prompt(self, text: str, target_language: str) -> str:
        """
        Construit un prompt contextualisé pour la traduction de phrases, expressions ou textes.
        """
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
            },
            'agni': { # Ajout du contexte pour Agni
                'description': 'langue parlée principalement en Côte d\'Ivoire, dans la région de l\'Est',
                'examples': 'Bonjour = Agni oh, Merci = Akpé, Au revoir = Aka na'
            },
            'fr': { # Ajout du contexte pour le Français si besoin (bien que ce soit la source)
                'description': 'langue française',
                'examples': ''
            }
        }

        context = language_contexts.get(target_language, {
            'description': f'langue africaine locale: {target_language}',
            'examples': ''
        })

        prompt = f"""
Tu es un expert en traduction vers les langues africaines locales.
Ton objectif est de traduire précisément le texte français suivant vers le {target_language}.
Le texte peut être une phrase, une expression ou un paragraphe.

Contexte de la langue cible:
- Le {target_language} est une {context['description']}.

Exemples de traductions en {target_language}:
{context['examples']}

Texte français à traduire: "{text}"

Instructions de traduction:
1. Traduis le texte français en {target_language}.
2. Fournis UNIQUEMENT la traduction, sans aucune explication, préfixe ou suffixe.
3. Respecte la grammaire et la structure de la langue {target_language}.
4. Adapte la traduction au contexte culturel local si pertinent.
5. Si tu ne peux absolument pas fournir une traduction fiable ou pertinente pour ce texte en {target_language}, réponds exactement "TRADUCTION_IMPOSSIBLE".

Traduction en {target_language}:
"""
        return prompt

    def _clean_response(self, response: str) -> str:
        """Nettoie la réponse de Gemini pour extraire la traduction"""
        response = response.strip()

        # Supprimer les guillemets si présents au début et à la fin
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1].strip()

        # Supprimer les préfixes explicatifs ou les phrases d'introduction
        # Ajout de quelques variations et de marques de ponctuation
        prefixes_to_remove = [
            'Traduction:', 'Traduction :', 'Translation:', 'Translation :',
            'Réponse:', 'Réponse :', 'En', 'Le texte traduit est:',
            'Voici la traduction en', 'La traduction est:', 'Traduction en',
            'La traduction de', 'Traduction du français vers le',
            f'Traduction en {response.split(":")[0].strip()}:' # Pour capturer "Traduction en Baoulé: "
        ]

        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()): # Comparaison insensible à la casse
                response = response[len(prefix):].strip()
                break # Arrêter après avoir trouvé le premier préfixe

        # Nettoyage final des espaces et des retours à la ligne
        response = response.strip()

        return response

    def is_service_available(self) -> bool:
        """Vérifie si le service Gemini est disponible"""
        return self.is_available
