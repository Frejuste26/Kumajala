# 🌍 KUMAJALA
### La parole qui voyage. La culture qui vit.

---

## 📝 Présentation du projet
**KUMAJALA** est une application web innovante qui permet de **traduire du français vers des langues locales africaines** (Bété, Baoulé, Mooré, Agni), et de **restituer la traduction sous forme de texte et de voix**.  

Ce projet a été conçu dans le cadre de **l'AbiHack Hackathon** pour valoriser les langues africaines dans le numérique, en combinant l'intelligence artificielle (Gemini) et les services cloud (Google Cloud).

---

## ✨ Fonctionnalités

### 🎯 MVP (Version 1.0)
✅ **Traduction intelligente** : Français → Langues africaines locales  
✅ **Cache haute performance** : Réponses ultra-rapides pour les traductions fréquentes  
✅ **Fallback IA avec Gemini** : Traductions contextuelles pour nouveaux textes  
✅ **Synthèse vocale** : Écouter les traductions (Text-to-Speech via gTTS)  
✅ **Base de données Firestore** : Stockage cloud ou local selon configuration  
✅ **API REST robuste** : Gestion d'erreurs, validation, logging  
✅ **Traduction batch** : Traduire plusieurs textes en une seule requête  
✅ **Gestion manuelle** : Ajouter/modifier des traductions  
✅ **Recherche de traductions** : Trouver rapidement des expressions  

### 🚀 Fonctionnalités Avancées
✅ **Retry automatique** : Gestion des erreurs réseau avec backoff exponentiel  
✅ **Validation intelligente** : Détection de traductions invalides  
✅ **Statistiques de cache** : Monitoring des performances  
✅ **Pagination** : Gestion efficace de grandes quantités de données  
✅ **Support multilingue** : Architecture extensible pour nouvelles langues  

---

## 🌐 Langues Supportées

| Langue   | Code     | Région            | Statut        |
|----------|----------|-------------------|---------------|
| Bété     | `bété`   | Côte d'Ivoire     | ✅ Traduction |
| Baoulé   | `baoulé` | Côte d'Ivoire     | ✅ Traduction |
| Mooré    | `mooré`  | Burkina Faso      | ✅ Traduction |
| Agni     | `agni`   | Côte d'Ivoire     | ✅ Traduction |
| Français | `fr`     | Global            | ✅ Source     |

> ⚠️ **Note TTS** : La synthèse vocale utilise actuellement gTTS qui ne supporte pas nativement les langues africaines. Les traductions sont prononcées avec un accent français. Voir [Alternatives TTS](#-alternatives-tts-recommandées) pour des solutions.

---

## 🔧 Technologies Utilisées

### 🟦 Backend (Python)
- **Flask 2.3.3** - Framework web léger et performant
- **Google Cloud Firestore 2.13.1** - Base de données NoSQL cloud
- **Gemini 2.0 Flash** (via google-generativeai 0.3.2) - IA pour traduction contextuelle
- **gTTS 2.5.4** - Synthèse vocale (Text-to-Speech)
- **Tenacity** - Retry logic avec backoff exponentiel
- **Python 3.9+** - Langage backend

### 🟩 Frontend
- **Vue.js 3** - Framework JavaScript progressif
- **Tailwind CSS** - Framework CSS utility-first
- **Axios** - Client HTTP pour les requêtes API

### ☁️ Cloud & Services
- **Google Cloud Platform** (Firestore, potentiellement Cloud Run)
- **Gemini API** - IA générative de Google
- **Google Text-to-Speech** (recommandé pour production)

---

## 🛠️ Installation et Lancement

### 📋 Prérequis
- Python 3.9 ou supérieur
- Node.js 16+ et npm
- Compte Google Cloud (optionnel, pour Firestore)
- Clé API Gemini (optionnel, pour traductions IA)

### 🔹 1️⃣ Cloner le projet
```bash
git clone https://github.com/votre-user/kumajala.git
cd kumajala
```

### 🔹 2️⃣ Configuration Backend

#### Installation des dépendances
```bash
cd kumajala-backend
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

#### Configuration des variables d'environnement
Créer un fichier `.env` à la racine de `kumajala-backend/` :

```env
# Clé API Gemini (optionnel)
GEMINI_API_KEY=votre_cle_api_gemini

# Google Cloud (optionnel pour Firestore)
GOOGLE_APPLICATION_CREDENTIALS=chemin/vers/serviceAccountKey.json

# Flask
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_flask

# Mode de stockage (laissez vide pour mode local)
# GOOGLE_APPLICATION_CREDENTIALS non définie = mode local automatique
```

#### Lancement du backend
```bash
python app.py
```
✅ L'API tourne sur `http://localhost:5000`

### 🔹 3️⃣ Configuration Frontend

```bash
cd kumajala-frontend
npm install
npm run dev
```
✅ Le frontend tourne sur `http://localhost:5173`

---

## 📂 Structure du Projet

```
kumajala/
├── kumajala-backend/
│   ├── app.py                      # Point d'entrée Flask
│   ├── requirements.txt            # Dépendances Python
│   ├── .env                        # Variables d'environnement (à créer)
│   ├── routes/                     # Routes API (Blueprints)
│   │   ├── translate.py           # Routes de traduction
│   │   ├── speak.py               # Routes de synthèse vocale
│   │   └── languages.py           # Routes de gestion des langues
│   ├── services/                   # Services métier
│   │   ├── firestore.py           # Service Firestore/Local
│   │   ├── gemini.py              # Service Gemini AI
│   │   └── tts.py                 # Service Text-to-Speech
│   └── data/
│       └── language.json          # Base locale de traductions
│
└── kumajala-frontend/
    ├── src/
    │   ├── components/            # Composants Vue réutilisables
    │   ├── pages/                 # Pages de l'application
    │   ├── api/                   # Services API Axios
    │   └── App.vue                # Composant racine
    ├── package.json
    └── tailwind.config.js
```

---

## 🚀 Documentation API

### Base URL
```
http://localhost:5000/kumajala-api/v1
```

### 📍 Endpoints Principaux

#### 1️⃣ Traduction

**POST `/translate`** - Traduire un texte
```json
// Requête
{
  "text": "Bonjour, comment allez-vous?",
  "targetLanguage": "baoulé"
}

// Réponse
{
  "success": true,
  "translation": "Mo ho, wo ho tè n?",
  "text": "Bonjour, comment allez-vous?",
  "targetLanguage": "baoulé",
  "source": "cache",
  "processingTime": "15.23ms"
}
```

**POST `/translate/batch`** - Traduire plusieurs textes
```json
// Requête
{
  "texts": ["bonjour", "merci", "au revoir"],
  "targetLanguage": "mooré",
  "continueOnError": true
}

// Réponse
{
  "success": true,
  "translations": [
    {
      "index": 0,
      "text": "bonjour",
      "translation": "Ne y windga",
      "source": "cache",
      "success": true
    }
  ],
  "summary": {
    "total": 3,
    "successful": 3,
    "failed": 0
  }
}
```

**POST `/translations/manage`** - Ajouter/Modifier une traduction
```json
{
  "frenchText": "bonne journée",
  "targetLanguage": "agni",
  "newTranslation": "Nna pa"
}
```

**GET `/translations/search`** - Rechercher des traductions
```
GET /translations/search?q=bonjour&targetLanguage=baoulé&limit=20
```

#### 2️⃣ Synthèse Vocale

**POST `/speak`** - Générer l'audio d'un texte
```json
// Requête
{
  "text": "Mo ho",
  "languageCode": "baoulé",
  "useCache": true
}

// Réponse
{
  "success": true,
  "audioBase64": "//uQxAAA...",
  "contentType": "audio/mpeg",
  "actualTTSLanguage": "fr",
  "cached": false,
  "audioSizeBytes": 12345,
  "warning": "La langue 'baoulé' n'est pas supportée..."
}
```

**GET `/speak/languages`** - Langues TTS supportées  
**GET `/speak/alternatives`** - Alternatives TTS recommandées  
**POST `/speak/check-language`** - Vérifier support d'une langue  
**GET `/speak/cache/stats`** - Statistiques du cache audio  
**POST `/speak/cache/clear`** - Vider le cache audio  

#### 3️⃣ Langues

**GET `/languages`** - Liste des langues supportées
```json
{
  "success": true,
  "languages": [
    {
      "code": "bété",
      "name": "Bété",
      "region": "Côte d'Ivoire",
      "code_tts": "fr"
    }
  ],
  "totalLanguages": 5
}
```

**GET `/languages/<code>`** - Détails d'une langue  
**GET `/languages/<code>/translations`** - Toutes les traductions d'une langue  
**GET `/languages/cache/stats`** - Statistiques du cache  
**POST `/languages/cache/clear`** - Vider le cache  

---

## 🗃️ Structure des Données

### Firestore (Structure Cloud)
```json
{
  "translations": {
    "bonjour_hash": {
      "source": "fr",
      "text": "bonjour",
      "languages": {
        "bété": "Akwaba",
        "baoulé": "Mo ho",
        "mooré": "Ne y windga",
        "agni": "Agni oh"
      },
      "metadata": {
        "updated_at": "2025-01-15T10:30:00Z",
        "version": 1
      }
    }
  }
}
```

### Local (data/language.json)
```json
{
  "fr": {
    "bonjour": {
      "bété": "Akwaba",
      "baoulé": "Mo ho",
      "mooré": "Ne y windga",
      "agni": "Agni oh"
    },
    "merci": {
      "bété": "Akpé",
      "baoulé": "Mo",
      "mooré": "Barika",
      "agni": "Akpé"
    }
  }
}
```

---

## 🔐 Sécurité et Bonnes Pratiques

### ✅ Validations Implémentées
- Limitation de longueur des textes (5000 caractères)
- Validation des codes de langue
- Protection contre les injections
- Gestion stricte des erreurs
- Logging sécurisé (pas de données sensibles)

### 🛡️ Recommandations
- [ ] Ajouter authentification JWT pour endpoints de gestion
- [ ] Implémenter rate limiting (limite de requêtes par IP)
- [ ] Configurer HTTPS en production
- [ ] Utiliser des secrets managers pour les clés API
- [ ] Ajouter monitoring et alertes

---

## ⚠️ Limitations Connues

### Synthèse Vocale (TTS)
❌ **gTTS ne supporte pas les langues africaines locales**  
- Les traductions en Bété, Baoulé, Mooré et Agni sont prononcées en français
- L'accent et la prononciation ne sont pas authentiques

### 🔊 Alternatives TTS Recommandées

| Service | Support | Qualité | Coût |
|---------|---------|---------|------|
| **Google Cloud TTS** | Multilingue étendu | ⭐⭐⭐⭐⭐ | Payant |
| **Azure Speech** | 100+ langues | ⭐⭐⭐⭐⭐ | Payant |
| **Coqui TTS** | Personnalisable | ⭐⭐⭐⭐ | Gratuit |
| **Enregistrements natifs** | Authentique | ⭐⭐⭐⭐⭐ | Variable |

Pour obtenir les recommandations complètes :
```bash
GET /kumajala-api/v1/speak/alternatives
```

---

## 🛤️ Roadmap

### 🎯 Version 1.1 (Court terme)
- [ ] Migration vers Google Cloud TTS ou Azure Speech
- [ ] Ajout de tests unitaires et d'intégration
- [ ] Documentation Swagger/OpenAPI
- [ ] Système d'authentification (JWT)
- [ ] Rate limiting

### 🚀 Version 2.0 (Moyen terme)
- [ ] Support de 10+ langues africaines
- [ ] Contribution communautaire (crowdsourcing)
- [ ] Détection automatique de langue
- [ ] Traduction multilingue (pas seulement depuis français)
- [ ] Application mobile (React Native / Flutter)

### 🌟 Version 3.0 (Long terme)
- [ ] IA contextuelle avancée (NLP avec TensorFlow)
- [ ] Reconnaissance vocale (Speech-to-Text)
- [ ] Marketplace de traductions communautaires
- [ ] API publique pour développeurs tiers
- [ ] Support hors-ligne (Progressive Web App)

---

## 📊 Performance

### Temps de Réponse Moyens
- **Cache hit** : 10-20ms
- **Gemini AI** : 500-2000ms
- **Synthèse vocale** : 200-800ms

### Capacités
- **Traduction simple** : 5000 caractères max
- **Traduction batch** : 100 textes max (1000 chars chacun)
- **Cache** : 100 audios en mémoire
- **Pagination** : 1-1000 résultats par page

---

## 🧪 Tests

### Lancer les tests (à implémenter)
```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Coverage
pytest --cov=services --cov=routes
```

---

## 🚢 Déploiement

### Option 1 : Google Cloud Run
```bash
# Build et push de l'image Docker
gcloud builds submit --tag gcr.io/[PROJECT-ID]/kumajala-backend
gcloud run deploy kumajala-api --image gcr.io/[PROJECT-ID]/kumajala-backend
```

### Option 2 : Heroku
```bash
heroku create kumajala-api
git push heroku main
```

### Option 3 : VPS (Ubuntu)
```bash
# Installation avec Gunicorn + Nginx
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📜 Licence

Ce projet est open-source sous licence **MIT**.

```
MIT License

Copyright (c) 2025 Équipe KUMAJALA - AbiHack

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 🤝 Équipe Projet - AbiHack

| Rôle | Responsabilités |
|------|-----------------|
| **Team Leader** | Architecture globale, coordination |
| **Backend Lead** | API Flask, services, Firestore |
| **AI/ML Engineer** | Intégration Gemini, validation traductions |
| **Frontend Lead** | Interface Vue.js, UX/UI |
| **DevOps** | Déploiement, CI/CD, monitoring |

---

## 🙏 Contributions

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. Créer une **branche** (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

### Guidelines
- Suivre PEP 8 pour Python
- Ajouter des tests pour nouvelles fonctionnalités
- Documenter les changements dans le README
- Respecter la structure du projet

---

## 📞 Contact & Support

- **Email** : contact@kumajala.org (à configurer)
- **GitHub Issues** : [github.com/votre-user/kumajala/issues](https://github.com/votre-user/kumajala/issues)
- **Discord** : [Rejoindre le serveur](https://discord.gg/kumajala) (à créer)

---

## 💡 Vision de KUMAJALA

> « Une langue qui disparaît, c'est une bibliothèque qui brûle. »  
> — Amadou Hampâté Bâ

**KUMAJALA**, c'est donner une voix numérique à nos langues africaines, pour qu'elles continuent à voyager, à vivre et à prospérer dans l'ère digitale.

Nous croyons que la technologie peut être un pont entre tradition et modernité, entre générations, entre cultures. Chaque traduction est une graine plantée pour préserver et faire grandir notre héritage linguistique.

---

## 📈 Statistiques du Projet

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Vue.js](https://img.shields.io/badge/Vue.js-3-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-MVP-orange)

---

**Fait avec ❤️ pour l'Afrique et ses langues**  
**#AbiHack #TechForGood #PreserveOurLanguages**