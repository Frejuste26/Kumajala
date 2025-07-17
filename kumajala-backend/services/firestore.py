import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import json

class FirestoreService:
    def __init__(self):
        # Initialisation du client Firestore
        # S'assurer que GOOGLE_APPLICATION_CREDENTIALS est défini
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            # Fallback vers les données locales si pas de Firebase
            self.use_local_data = True
            self.load_local_translations()
        else:
            try:
                self.db = firestore.Client()
                self.use_local_data = False
            except Exception as e:
                print(f"Erreur connexion Firestore: {e}")
                self.use_local_data = True
                self.load_local_translations()
    
    def load_local_translations(self):
        """Charge les traductions depuis le fichier JSON local"""
        try:
            with open('data/translations.json', 'r', encoding='utf-8') as f:
                self.local_translations = json.load(f)
        except FileNotFoundError:
            # Créer des données par défaut si le fichier n'existe pas
            self.local_translations = {
                "translations": {
                    "Bonjour": {
                        "bété": "Akwaba",
                        "baoulé": "Mo ho",
                        "mooré": "Ne y windga"
                    },
                    "Comment allez-vous?": {
                        "bété": "Bi ye né?",
                        "baoulé": "Wo ho tè n?",
                        "mooré": "Fo laafi?"
                    },
                    "Merci": {
                        "bété": "Akpé",
                        "baoulé": "Akpé",
                        "mooré": "Barka"
                    },
                    "Au revoir": {
                        "bété": "Kan na",
                        "baoulé": "Kan na",
                        "mooré": "Nan kã pãalem"
                    },
                    "Oui": {
                        "bété": "Yoo",
                        "baoulé": "Yoo",
                        "mooré": "Yãa"
                    },
                    "Non": {
                        "bété": "Kou",
                        "baoulé": "Kou",
                        "mooré": "Ayi"
                    },
                    "Bonne nuit": {
                        "bété": "Dè wèlè",
                        "baoulé": "Dè wèlè",
                        "mooré": "Sẽn-doogo"
                    },
                    "Je m'appelle": {
                        "bété": "Man yi tɔ",
                        "baoulé": "Man yi tɔ",
                        "mooré": "Ma yiire"
                    },
                    "Où est": {
                        "bété": "Kpá nyɛ",
                        "baoulé": "Kpá nyɛ",
                        "mooré": "Fo bee"
                    },
                    "Combien": {
                        "bété": "Kpé nyɛ",
                        "baoulé": "Kpé nyɛ",
                        "mooré": "Yãa"
                    }
                }
            }
    
    def get_translation(self, text, target_language):
        """Récupère une traduction depuis Firestore ou les données locales"""
        if self.use_local_data:
            return self._get_local_translation(text, target_language)
        else:
            return self._get_firestore_translation(text, target_language)
    
    def _get_local_translation(self, text, target_language):
        """Récupère une traduction depuis les données locales"""
        translations = self.local_translations.get("translations", {})
        if text in translations and target_language in translations[text]:
            return translations[text][target_language]
        return None
    
    def _get_firestore_translation(self, text, target_language):
        """Récupère une traduction depuis Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return data.get(target_language)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération Firestore: {e}")
            return None
    
    def save_translation(self, text, target_language, translation):
        """Sauvegarde une traduction dans Firestore"""
        if self.use_local_data:
            return self._save_local_translation(text, target_language, translation)
        else:
            return self._save_firestore_translation(text, target_language, translation)
    
    def _save_local_translation(self, text, target_language, translation):
        """Sauvegarde une traduction localement"""
        try:
            if "translations" not in self.local_translations:
                self.local_translations["translations"] = {}
            
            if text not in self.local_translations["translations"]:
                self.local_translations["translations"][text] = {}
            
            self.local_translations["translations"][text][target_language] = translation
            
            # Sauvegarder dans le fichier JSON
            os.makedirs('data', exist_ok=True)
            with open('data/translations.json', 'w', encoding='utf-8') as f:
                json.dump(self.local_translations, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur sauvegarde locale: {e}")
            return False
    
    def _save_firestore_translation(self, text, target_language, translation):
        """Sauvegarde une traduction dans Firestore"""
        try:
            doc_ref = self.db.collection('translations').document(text)
            doc_ref.set({
                target_language: translation
            }, merge=True)
            return True
        except Exception as e:
            print(f"Erreur sauvegarde Firestore: {e}")
            return False
    
    def get_supported_languages(self):
        """Retourne la liste des langues supportées"""
        return [
            {
                'code': 'bété',
                'name': 'Bété',
                'region': 'Côte d\'Ivoire'
            },
            {
                'code': 'baoulé',
                'name': 'Baoulé',
                'region': 'Côte d\'Ivoire'
            },
            {
                'code': 'mooré',
                'name': 'Mooré',
                'region': 'Burkina Faso'
            }
        ]