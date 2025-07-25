import os
from google.cloud import firestore
import json

class FirestoreService:
    def __init__(self):
        # Initialisation du client Firestore
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            print("⚠️ GOOGLE_APPLICATION_CREDENTIALS non définie. Utilisation des données locales.")
            self.use_local_data = True
            self.load_local_translations()
        else:
            try:
                self.db = firestore.Client()
                self.use_local_data = False
                print("✅ Service Firestore initialisé avec succès.")
            except Exception as e:
                print(f"❌ Erreur connexion Firestore: {e}. Fallback vers les données locales.")
                self.use_local_data = True
                self.load_local_translations()

        # Métadonnées des langues (hardcodées pour le MVP du hackathon)
        self._language_metadata = {
            'bété': {'code': 'bété', 'name': 'Bété', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'baoulé': {'code': 'baoulé', 'name': 'Baoulé', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'mooré': {'code': 'mooré', 'name': 'Mooré', 'region': 'Burkina Faso', 'code_gtts': 'fr'},
            'agni': {'code': 'agni', 'name': 'Agni', 'region': 'Côte d\'Ivoire', 'code_gtts': 'fr'},
            'fr': {'code': 'fr', 'name': 'Français', 'region': 'Global', 'code_gtts': 'fr'}
        }


    def load_local_translations(self):
        """Charge les traductions depuis le fichier JSON local (data/language.json)."""
        try:
            script_dir = os.path.dirname(__file__)
            json_path = os.path.join(script_dir, '..', 'data', 'language.json') # Chemin vers language.json

            with open(json_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self.local_translations = {}
                # Assurez-vous que la structure "fr" existe au niveau supérieur
                if "fr" in raw_data:
                    self.local_translations["fr"] = {
                        k.lower(): v for k, v in raw_data["fr"].items()
                    }
                else:
                    # Si la structure n'a pas de clé "fr" au premier niveau,
                    # considérez que raw_data est directement le dictionnaire des traductions.
                    # Adaptez ceci si votre fichier JSON a une structure racine différente.
                    self.local_translations = raw_data
                print(f"INFO: Traductions locales chargées depuis {json_path}.")

        except FileNotFoundError:
            print("WARN: Fichier data/language.json non trouvé. Création de données par défaut.")
            self.local_translations = {
                "fr": {
                    "bonjour": {
                        "bété": "Akwaba", "baoulé": "Mo ho", "mooré": "Ne y windga", "agni": "Agni oh"
                    },
                    "comment allez-vous?": {
                        "bété": "Bi ye né?", "baoulé": "Wo ho tè n?", "mooré": "Fo laafi?", "agni": "Aka kye?"
                    },
                    "merci": {
                        "bété": "Akpé", "baoulé": "Mo", "mooré": "Barika", "agni": "Akpé"
                    },
                    "au revoir": {
                        "bété": "Kan na", "baoulé": "Kan na", "mooré": "Nan kã pãalem", "agni": "Aka na"
                    },
                    "oui": {
                        "bété": "Yoo", "baoulé": "Yoo", "mooré": "Yãa", "agni": "Aoo"
                    },
                    "non": {
                        "bété": "Kou", "baoulé": "Kou", "mooré": "Ayi", "agni": "N'an"
                    },
                    "bonne nuit": {
                        "bété": "Dè wèlè", "baoulé": "Dè wèlè", "mooré": "Sẽn-doogo", "agni": "Anwielé"
                    },
                    "je m'appelle": {
                        "bété": "Man yi tɔ", "baoulé": "Man yi tɔ", "mooré": "Ma yiire", "agni": "Mina yɛ"
                    },
                    "où est": {
                        "bété": "Kpá nyɛ", "baoulé": "Kpá nyɛ", "mooré": "Fo bee", "agni": "Wan ye?"
                    },
                    "combien": {
                        "bété": "Kpé nyɛ", "baoulé": "Kpé nyɛ", "mooré": "Kpé nyɛ", "agni": "Kye o?"
                    },
                    "s'il vous plaît": {
                        "bété": "Akpé o", "baoulé": "Akpé o", "mooré": "Tõnd pa", "agni": "Kpaa"
                    },
                    "excusez-moi": {
                        "bété": "Pardon", "baoulé": "Pardon", "mooré": "Tõnd wii", "agni": "Pardon"
                    },
                    "ça va": {
                        "bété": "Bi dè", "baoulé": "Wo dè", "mooré": "A laafi", "agni": "Aka ya?"
                    },
                    "boire": {
                        "bété": "Nyɛ", "baoulé": "Nyɛ", "mooré": "Nyu", "agni": "Nyu"
                    },
                    "manger": {
                        "bété": "Dyi", "baoulé": "Dyi", "mooré": "Di", "agni": "Di"
                    },
                    "dormir": {
                        "bété": "Dè", "baoulé": "Dè", "mooré": "Sẽn", "agni": "Dè"
                    },
                    "maison": {
                        "bété": "Kpè", "baoulé": "Kpè", "mooré": "Yiri", "agni": "Aso"
                    },
                    "eau": {
                        "bété": "Nyɛ", "baoulé": "Nyɛ", "mooré": "Koom", "agni": "Nsu"
                    },
                    "argent": {
                        "bété": "Kpɛ", "baoulé": "Kpɛ", "mooré": "Galaga", "agni": "Sika"
                    },
                    "travail": {
                        "bété": "Wɔ", "baoulé": "Wɔ", "mooré": "Tuma", "agni": "Adwuma"
                    }
                }
            }
            self._save_local_translations_to_file() # Sauvegarde les données par défaut
        except Exception as e:
            print(f"❌ Erreur lors du chargement des traductions locales: {e}")
            self.local_translations = {"fr": {}} # Assure que le dictionnaire est toujours initialisé

    def _save_local_translations_to_file(self):
        """Sauvegarde les données locales dans le fichier JSON (data/language.json)."""
        try:
            script_dir = os.path.dirname(__file__)
            json_path = os.path.join(script_dir, '..', 'data', 'language.json') # Chemin vers language.json
            os.makedirs(os.path.dirname(json_path), exist_ok=True) # Crée le dossier 'data' si inexistant
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.local_translations, f, ensure_ascii=False, indent=2)
            print(f"INFO: Traductions locales sauvegardées dans {json_path}.")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde des traductions locales dans le fichier: {e}")

    def get_translation(self, text, target_language):
        """Récupère une traduction depuis Firestore ou les données locales"""
        text_lower = text.lower()
        if self.use_local_data:
            return self._get_local_translation(text_lower, target_language)
        else:
            return self._get_firestore_translation(text_lower, target_language)

    def _get_local_translation(self, text_lower, target_language):
        """Récupère une traduction depuis les données locales"""
        translations = self.local_translations.get("fr", {})
        if text_lower in translations and target_language in translations[text_lower]:
            return translations[text_lower][target_language]
        return None

    def _get_firestore_translation(self, text_lower, target_language):
        """Récupère une traduction depuis Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text_lower)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                return data.get(target_language)
            return None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération Firestore: {e}")
            return None

    def save_translation(self, text, target_language, translation):
        """Sauvegarde une traduction dans Firestore ou localement"""
        text_lower = text.lower()
        if self.use_local_data:
            return self._save_local_translation(text_lower, target_language, translation)
        else:
            return self._save_firestore_translation(text_lower, target_language, translation)

    def _save_local_translation(self, text_lower, target_language, translation):
        """Sauvegarde une traduction localement"""
        try:
            if "fr" not in self.local_translations:
                self.local_translations["fr"] = {}

            if text_lower not in self.local_translations["fr"]:
                self.local_translations["fr"][text_lower] = {}

            self.local_translations["fr"][text_lower][target_language] = translation

            self._save_local_translations_to_file() # Sauvegarde après chaque modification

            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde locale: {e}")
            return False

    def _save_firestore_translation(self, text_lower, target_language, translation):
        """Sauvegarde une traduction dans Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text_lower)
            doc_ref.set({
                target_language: translation
            }, merge=True) # Utiliser set avec merge=True pour ajouter/mettre à jour un champ sans écraser le document entier
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde Firestore: {e}")
            return False

    def update_translation_manual(self, french_text: str, target_language: str, new_translation: str) -> bool:
        """
        Met à jour ou ajoute manuellement une traduction spécifique.
        Ceci est utilisé pour corriger ou ajouter des traductions.
        """
        french_text_lower = french_text.lower()
        print(f"DEBUG: Tentative de mise à jour manuelle: '{french_text}' en '{target_language}' avec '{new_translation}'")

        if self.use_local_data:
            try:
                if "fr" not in self.local_translations:
                    self.local_translations["fr"] = {}
                if french_text_lower not in self.local_translations["fr"]:
                    self.local_translations["fr"][french_text_lower] = {}

                self.local_translations["fr"][french_text_lower][target_language] = new_translation
                self._save_local_translations_to_file() # Sauvegarde après chaque modification manuelle
                print(f"INFO: Traduction locale mise à jour/ajoutée pour '{french_text_lower}' en '{target_language}'.")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour manuelle locale: {e}")
                return False
        else:
            try:
                doc_ref = self.db.collection('translations').document(french_text_lower)
                doc_ref.set({
                    target_language: new_translation
                }, merge=True)
                print(f"INFO: Traduction Firestore mise à jour/ajoutée pour '{french_text_lower}' en '{target_language}'.")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour manuelle Firestore: {e}")
                return False

    def get_supported_languages(self):
        """
        Retourne la liste des langues supportées (hardcodée pour le MVP du hackathon).
        """
        # Retourne simplement les valeurs du dictionnaire _language_metadata
        # Trié par nom de langue pour un affichage cohérent
        return sorted(self._language_metadata.values(), key=lambda x: x['name'])
