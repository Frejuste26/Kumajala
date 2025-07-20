# 🌍 KUMAJALA
### La parole qui voyage. La culture qui vit.

---

## 📝 Présentation du projet
**KUMAJALA** est une application web qui permet de **traduire du français vers des langues locales africaines** (Bété, Baoulé, Mooré, etc.), et de **restituer la traduction sous forme de texte et de voix**.  
Ce projet a été conçu dans le cadre de **l’AbiHack Hackathon** pour valoriser les langues africaines dans le numérique, à travers l'IA et le cloud.

---

## 🚩 Fonctionnalités MVP
✅ Traduction de phrases simples (français vers langues locales)  
✅ Synthèse vocale (Text-to-Speech) pour écouter la traduction  
✅ Base de données Firestore pour les expressions courantes  
✅ API REST propre et extensible  
✅ Frontend simple, clair, accessible

---

## 🔧 Technologies utilisées

### 🟦 Backend
- **Flask** (API REST)
- **Google Cloud Firestore** (NoSQL)
- **Gemini API (Google Generative AI)** (Fallback traduction)
- **Google Cloud Text-to-Speech (TTS)** (Synthèse vocale)
- **TensorFlow** (prévu pour futures améliorations IA)
- **Python 3.x**

### 🟩 Frontend
- **Vue.js**
- **Tailwind CSS**
- **Axios**

---

## 🛠️ Installation et lancement

### 🔹 1️⃣ Cloner le projet
```bash
git clone https://github.com/votre-user/kumajala.git
cd kumajala
```

## 🔹 2️⃣ Backend Flask

```bash
  cd kumajala-backend
  python -m venv venv
  source venv/bin/activate  # Windows : venv\Scripts\activate
  pip install -r requirements.txt
  python app.py
```
L'API tourne sur `http://localhost:5000`

## 🔹 3️⃣ Frontend Vue.js

```bash
  cd kumajala-frontend
  npm install
  npm run dev
```

Le frontend tourne sur `http://localhost:5173`

## 📂 Structure du projet

```css
kumajala-backend/
├── app.py
├── routes/
│   ├── translate.py
│   ├── speak.py
│   └── languages.py
├── services/
│   ├── firestore_service.py
│   ├── gemini_service.py
│   └── tts_service.py
├── data/
│   └── translations.json (backup)
├── requirements.txt

kumajala-frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── api/
│   └── App.vue
├── package.json
```

## 🚀 Endpoints API

| Méthode | Endpoint         | Description                               |
| ------- | ---------------- | ----------------------------------------- |
| `POST`  | `/api/translate` | Traduit une phrase vers une langue locale |
| `POST`  | `/api/speak`     | Génère l'audio d'une phrase traduite      |
| `GET`   | `/api/languages` | Liste des langues supportées              |

## Exemple de payload

```json
  POST /api/translate
  {
    "text": "Bonjour",
    "targetLanguage": "bété"
  }
```

## 🗃️ Firestore (Structure des données)

```json
  {
    "translations": {
      "Bonjour": {
        "bété": "Akwaba",
        "baoulé": "Mo ho",
        "mooré": "Ne y windga"
      }
    }
  }
```

## 🔊 Synthèse vocale (Google TTS)

- Restitution en .mp3 ou .ogg
- Langues et accents à personnaliser via Google Cloud TTS API

## 🛤️ Roadmap (post MVP)

- Ajout d'autres langues africaines
- Enrichissement communautaire des traductions
- IA contextuelle avec TensorFlow / NLP
- Déploiement cloud (Firebase Hosting / Google Cloud Run)
- Application mobile native

## 📊 Stack Résumée

| Backend   | IA / Cloud             | Frontend     |
| --------- | ---------------------- | ------------ |
| Flask     | Gemini API / Firestore | Vue.js       |
| Firestore | Google TTS API         | Tailwind CSS |

## 📜 Licence

Ce projet est open-source sous licence MIT.

## 🤝 Équipe Projet - AbiHack

| Nom       | Rôle                       |
| ----------| -------------------------- |
|(à décider)| Team Leader / Backend API  |
|(à décider)| Backend Firestore / Gemini |
|(à décider)| Frontend Vue / UX          |
|(à décider)| Frontend Vue / Intégration |

## 💡 Vision de KUMAJALA

> « Une langue qui disparaît, c’est une bibliothèque qui brûle. »
> KUMAJALA, c’est donner une voix numérique à nos langues africaines, pour qu’elles continuent à voyager et à vivre.
