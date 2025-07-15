# 🚀Plan Technique MVP Kumajala 48h / 4 Développeurs

## 🎯 Objectif du MVP :
👉 Traduire texte court (phrase) depuis le français → une langue locale (ex : bété, baoulé, mooré)
👉 Restituer en texte + voix générée synthétique (TTS).
👉 Interface Web simple et fonctionnelle.

## 📅 Planning des 48h en Sprint Agile

| Heure       | Tâche principale                                 | Responsable (profil conseillé) |
| ----------- | ------------------------------------------------ | ------------------------------ |
| **H 0-2**   | Réunion d’équipe / Découpage MVP / Setup projets | Tous ensemble                  |
| **H 3-10**  | Backend API (traduction / TTS) + DB (MongoDB)    | 2 Dev Backend                  |
| **H 3-10**  | Frontend (UI maquette, base Vue/React)           | 2 Dev Frontend                 |
| **H 10-14** | Liaison Front/Back + Test première requête       | Tous                           |
| **H 14-20** | Voix (Text-to-Speech) + Restitution audio        | Backend Dev                    |
| **H 14-20** | Affinage UI, design basique, ergonomie           | Frontend Dev                   |
| **H 20-24** | Intégration totale + Test MVP                    | Tous                           |
| **Jour 2**  | Correction bugs / Affinage / Démo / Présentation | Tous                           |

## 🛠️ Architecture Technique Simple :

### Frontend :
- **Framework** : React.js (ou Vue.js selon l'équipe)
- **Pages MVP** :
  - Page d’accueil avec champ texte d’entrée
  - Sélecteur de langue (français → langue locale)
  - Résultat affiché en texte + bouton “Écouter”
- **Appels API REST** : vers backend (Node.js, Python, Java, etc.)

### Backend :
- choix de l'équipe (préférence simplicité)
- **MongoDB/Fibase** (hébergement Atlas, stocke vocabulaire, expressions)
- **Endpoints essentiels** :
  - `POST /translate`: reçoit le texte, renvoie la traduction
  - `GET /languages`:  liste des langues supportées
  - `POST /speak`: génère audio à partir du texte

## 🧑‍💻 Répartition des rôles (4 Devs)

| Dev | Mission principale                            | Techno                            |
| --- | --------------------------------------------- | --------------------------------- |
| 1   | Backend API traduction / TTS                  | Flask, Firebase, TensorFlow       |
| 2   | Backend intégration TTS / Data / Optimisation | Flask, TTS API (GCP) |
| 3   | Frontend UI / Appel API                       | React / Vue / Tailwind CSS        |
| 4   | Frontend UX / Voix / Tests                    | React / Vue / Tailwind CSS        |

## 🔑 Solutions IA / API pour gagner du temps :

| Problème   | Solution rapide MVP                                                                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Traduction | **Dataset prérempli** (fichier JSON / Mongo) pour mots simples, proverbes, phrases basiques. Pas besoin de créer un modèle d’IA complet pour ce MVP. |
| TTS        | **Google Cloud Text-to-Speech** (voix africaines neutres ou personnalisées si dispo) / Coqui.ai / Azure TTS                                          |
| API REST   | Express, simple, endpoints clairs                                                                                                                    |
| UI / Front | Tailwind CSS pour aller vite et proprement                                                                                                           |

## 📂 Structure des fichiers Backend (Exemple) :

```bash
  kumajala-backend/
  ├── app.js
  ├── routes/
  │   ├── translate.js
  │   └── speak.js
  ├── controllers/
  │   ├── translateController.js
  │   └── speakController.js
  ├── models/
  │   └── phraseModel.js
  ├── data/
  │   └── translations.json
  └── package.json
```

## 📂 Structure des fichiers Frontend (Exemple Vue / React) :

```bash
  kumajala-frontend/
  ├── src/
  │   ├── components/
  │   ├── pages/
  │   ├── App.vue / App.jsx
  │   ├── api/
  │   │   └── api.js (appels vers backend)
  │   └── assets/
  └── package.json
```

## 📊 Base de Données Exemples (JSON / MongoDB) :

```json
  {
    "fr": {
      "Bonjour": "Akwaba",
      "Merci": "Nè",
      "Comment ça va ?": "I bé fô ?"
    },
    "bété": {
      "Akwaba": "Bienvenue",
      "Nè": "Merci",
      "I bé fô ?": "Comment vas-tu ?"
    }
  }
```

## 🔥 Livrables concrets en 48h :
- [x] Frontend simple, clair, utilisable
- [x] Backend API REST qui répond correctement
- [x] Traduction basique entre 2-3 langues max
- [x] Voix générée qui lit la traduction
- [x] Présentation fonctionnelle pour AbiHack
