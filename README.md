# 🌍 KUMAJALA
### La parole qui voyage. La culture qui vit.

---

## 📝 Présentation du projet
**KUMAJALA** est une application web innovante conçue pour briser les barrières linguistiques en traduisant le français vers des langues africaines locales (Bété, Baoulé, Mooré, Agni, etc.), et en restituant la traduction sous forme de texte et de voix.

Développé dans le cadre de l'AbiHack Hackathon, ce projet vise à valoriser et préserver la richesse des langues africaines dans l'ère numérique, en tirant parti des avancées de l'Intelligence Artificielle et des technologies cloud.

---

## 🚩 Fonctionnalités MVP
- [x] **Traduction Multilingue** : Traduction précise du français vers plusieurs langues africaines locales.
- [x] **Synthèse Vocale (Text-to-Speech)** : Écoutez les traductions pour une meilleure prononciation et immersion.
- [x] **Base de Connaissances Intelligente** : Utilisation d'une base de données Firestore (ou locale) pour les expressions courantes, optimisée par l'API Gemini pour les traductions plus complexes.
- [x] **Gestion Manuelle des Traductions** : Possibilité d'ajouter ou de modifier des traductions existantes pour affiner la base de données.
- [x] **Copie Rapide** : Copiez instantanément le texte traduit dans le presse-papiers.
- [x] **Notifications Utilisateur** : Système de notifications non-bloquantes pour un feedback clair et rapide.
- [x] **API RESTful Robuste** : Une API propre, modulaire et extensible pour une intégration facile.
- [x] **nterface Utilisateur Intuitive** : Un frontend clair, réactif et accessible, avec un mode sombre personnalisable.
---

## 🔧 Technologies utilisées

### 🟦 Backend
- **Flask**: Framework web Python pour la construction de l'API REST.
- **Google Cloud Firestore**: Base de données NoSQL pour le stockage des traductions (ou fichier JSON local en mode développement/fallback).
- **Gemini API (Google Generative AI)**: Moteur de traduction avancé pour les requêtes non trouvées en base de données.
- **gTTS (Google Text-to-Speech)**: Bibliothèque Python pour la synthèse vocale.
- **TensorFlow** (prévu pour futures améliorations IA)
- **Python 3.x**

### 🟩 Frontend
- **Vue.js**: Framework JavaScript progressif pour l'interface utilisateur.
- **Vue Router**: Pour la gestion de la navigation entre les pages.
- **Vue Composables**: Pour la logique réutilisable et la gestion de l'état (ex: notifications, thème).
- **Lucide Icons**: Bibliothèque d'icônes légère et personnalisable.
- **Axios**: Client HTTP basé sur les Promesses pour les requêtes API.

---

## 🛠️ Installation et lancement

### 🔹 1️⃣ Cloner le projet
```bash
git clone https://github.com/keifrejuste26/kumajala.git
cd kumajala
```

## 🔹 2️⃣ Configuration des variables d'environnement

Créez un fichier `.env` à la racine du dossier `backend/` et ajoutez-y votre clé API Gemini :

```bash
  GEMINI_API_KEY=votre_cle_api_gemini_ici
  SECRET_KEY=une_cle_secrete_pour_flask
  FLASK_ENV=development # Pour activer le mode debug de Flask
```
**Note** : Pour la connexion à Firestore en production, assurez-vous que la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS est configurée pour pointer vers le fichier de vos identifiants de service Google Cloud.

## 🔹 3️⃣ Backend Flask

```bash
  cd kumajala-backend
  python -m venv venv
  source venv/bin/activate # Sur Windows : venv\Scripts\activate
  pip install -r requirements.txt
  pip install python-dotenv # Installez si ce n'est pas déjà fait pour charger .env
  python app.py
```

L'API sera accessible sur `http://localhost:5000` (ou votre adresse IP locale si configuré).

## 🔹 4️⃣ Frontend Vue.js
```bash
  cd kumajala-frontend
  npm install
  npm run dev
```

Le frontend sera accessible sur `http://localhost:5173` (ou votre adresse IP locale si configuré).

## 📂 Structure du projet

```bash
  kumajala/
  ├── kumajala-backend/
  │   ├── app.py
  │   ├── api/
  │   │   ├── translate.py
  │   │   ├── speak.py
  │   │   └── languages.py
  │   ├── services/
  │   │   ├── firestore.py
  │   │   ├── gemini.py
  │   │   └── tts.py
  │   ├── data/
  │   │   └── language.json (traductions locales de fallback)
  │   └── requirements.txt
  ├── kumajala-frontend/
  │   ├── src/
  │   │   ├── components/
  │   │   │   ├── NotificationToast.vue
  │   │   │   └── ... (autres composants)
  │   │   ├── views/
  │   │   │   ├── Home.vue
  │   │   │   ├── TranslatorPage.vue
  │   │   │   ├── About.vue
  │   │   │   └── Setting.vue
  │   │   ├── api/
  │   │   │   └── axiosConfig.js
  │   │   ├── composables/
  │   │   │   └── useNotifications.js
  │   │   ├── assets/
  │   │   │   ├── base.css
  │   │   │   └── main.css
  │   │   └── App.vue
  │   ├── package.json
  │   └── vite.config.js
  └── README.md
```

## 🚀 Endpoints API

| Méthode | Endpoint         | Description                               |
| ------- | ---------------- | ----------------------------------------- |
| `GET`   | `/kumajala-api/v1/`| Informations de base sur l'API |
| `POST`  | `/kumajala-api/v1/translate` | Traduit une phrase vers une langue locale |
| `POST`  | `/kumajala-api/v1/translations/manage` | Ajoute ou met à jour manuellement une traduction |
| `POST`  | `/kumajala-api/v1/speak`     | Génère l'audio d'une phrase traduite      |
| `GET`   | `/kumajala-api/v1/languages` | Liste des langues supportées              |
| `GET`   | `/kumajala-api/v1/languages/{code}` | Informations sur une langue spécifique |
| `GET`   | `/kumajala-api/v1/languages/{code}/translations` | Liste des traductions connues pour une langue |

## Exemple de payload

```json
POST /kumajala-api/v1/translate
Content-Type: application/json

{
  "text": "Bonjour, comment allez-vous ?",
  "targetLanguage": "baoulé"
}
```

## 🗃️ Structure des données Firestore (Collection `translations`)

Chaque document dans la collection `translations` est nommé d'après le texte français (en minuscules) et contient des champs pour chaque langue cible :


```json
{
  "bonjour": {
    "bété": "Akwaba",
    "baoulé": "Mo ho",
    "mooré": "Ne y windga",
    "agni": "Agni oh"
  },
  "comment allez-vous?": {
    "bété": "Bi ye né?",
    "baoulé": "Wo ho tè n?",
    "mooré": "Fo laafi?",
    "agni": "Aka kye?"
  }
}
```

## 🔊 Synthèse vocale (Google TTS)

Le service utilise la bibliothèque `gTTS` pour convertir le texte en parole, générant des fichiers audio au format MP3. Les codes de langue sont basés sur ISO 639-1.

## 🛤️ Roadmap (post MVP)

Voici les améliorations envisagées pour l'avenir du projet :

- **Ajout de nouvelles langues africaines** : Étendre la couverture linguistique.
- **Enrichissement communautaire des traductions** : Mettre en place un système collaboratif pour que les utilisateurs puissent soumettre et valider des traductions.
- **IA contextuelle avancée** : Intégrer des modèles NLP plus sophistiqués (potentiellement avec TensorFlow) pour une traduction plus nuancée et contextuelle.
- **Déploiement cloud complet** : Déployer le backend sur Google Cloud Run et le frontend sur Firebase Hosting pour une accessibilité mondiale.
- **Application mobile native** : Développer des applications iOS et Android pour une expérience utilisateur optimisée sur mobile.
- **Amélioration des performances** : Optimisation des requêtes Gemini et de la gestion des données pour des temps de réponse encore plus rapides.

## 📊 Stack Résumée

| Catégorie  | Technologies   |  
| --------- | ---------------------- | 
|**Backend**| Flask, Python |
|**IA / Cloud**| Gemini API, Google Cloud Firestore, gTTS |       
| **Frontend** | Vue.js, Vue Router, Vue Composables, Axios |

## 📜 Licence

Ce projet est open-source sous licence MIT.

## 🤝 Équipe Projet - AbiHack

| Nom       | Rôle                       |
| ----------| -------------------------- |
|Kei Fréjuste| Team Leader / Backend API  |
|Kei Fréjuste & Nango Ebrotie Vital| Backend Firestore / Gemini |
|Sanné-Tia Chrys| Frontend Vue / UX          |
|Kei Fréjuste | Frontend Vue / Intégration |

## 💡 Vision de KUMAJALA

> « Une langue qui disparaît, c’est une bibliothèque qui brûle. »
> KUMAJALA, c’est donner une voix numérique à nos langues africaines, pour qu’elles continuent à voyager et à vivre.
