# 🇨🇮 Quiz Interactif — Côte d'Ivoire & Technologie

Une application de quiz desktop développée en Python avec Tkinter, conçue pour tester vos connaissances sur la **culture ivoirienne** et les **technologies modernes** (Python & Cybersécurité).

---

## 📋 Fonctionnalités

- **Deux onglets thématiques** : Côte d'Ivoire et Technologie
- **6 catégories de quiz** : Culture, Gastronomie, Sport, Ethnies, Python, Cybersécurité
- **Minuteur de 35 secondes** par question avec affichage circulaire animé
- **Système de paliers** façon "Qui veut gagner des millions ?" (jusqu'à 1M de points)
- **Feedback immédiat** avec explication de la bonne réponse
- **Questions mélangées** aléatoirement à chaque partie
- **Barre de progression** et score en temps réel
- **Scrollbar personnalisée** (fine, apparaît au survol)
- **Écran de résultats** avec pourcentage et niveau de performance

---

## 🗂️ Structure du projet

```
quiz_app/
│
├── quiz_app.py          # Application principale (interface + logique)
├── quiz_data.json       # Base de données des questions
└── README.md            # Documentation
```

---

## ⚙️ Prérequis

- Python **3.8 ou supérieur**
- Le module `tkinter` (inclus par défaut avec Python)

> ⚠️ Sur certaines distributions Linux, tkinter doit être installé séparément :
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🚀 Lancement

```bash
python quiz_app.py
```

---

## 📁 Format de `quiz_data.json`

Le fichier JSON doit contenir une clé `"categories"`. Chaque catégorie suit cette structure :

```json
{
  "categories": [
    {
      "id": "culture",
      "titre": "Culture Générale",
      "description": "Histoire et traditions ivoiriennes",
      "emoji": "🏛️",
      "couleur": "#FFD700",
      "region": "Côte d'Ivoire",
      "questions": [
        {
          "question": "Quelle est la capitale économique de la Côte d'Ivoire ?",
          "options": ["Abidjan", "Yamoussoukro", "Bouaké", "San-Pédro"],
          "reponse": "Abidjan",
          "region": "Géographie",
          "explication": "Abidjan est la capitale économique et la plus grande ville du pays."
        }
      ]
    }
  ]
}
```

### Champs requis par question

| Champ         | Type   | Description                                      |
|---------------|--------|--------------------------------------------------|
| `question`    | string | Intitulé de la question                          |
| `options`     | array  | Liste de 4 choix de réponse                      |
| `reponse`     | string | La bonne réponse (doit correspondre à une option)|
| `region`      | string | Thème ou sous-catégorie affiché dans le jeu      |
| `explication` | string | *(Optionnel)* Explication affichée après réponse |

---

## 🎮 Catégories disponibles

### 🇨🇮 Côte d'Ivoire
| ID            | Titre         |
|---------------|---------------|
| `culture`     | Culture       |
| `gastronomie` | Gastronomie   |
| `sport`       | Sport         |
| `ethnies`     | Ethnies       |

### 💻 Technologie
| ID              | Titre          |
|-----------------|----------------|
| `python`        | Python         |
| `cybersecurite` | Cybersécurité  |

---

## 🏆 Système de paliers

| Palier | Points |
|--------|--------|
| 1      | 100    |
| 2      | 200    |
| 3      | 300    |
| 4      | 500    |
| 5      | 1 000  |
| 6      | 2 000  |
| 7      | 4 000  |
| 8      | 8 000  |
| 9      | 16 000 |
| 10     | 32 000 |
| 11     | 64 000 |
| 12     | 1 000 000 |

---

## 📊 Niveaux de résultat

| Score     | Mention         |
|-----------|-----------------|
| 100%      | 🥇 Champion !   |
| 80 – 99%  | ⭐ Excellent !  |
| 60 – 79%  | 👍 Très bien !  |
| 40 – 59%  | 😊 Pas mal !    |
| < 40%     | 💪 Courage !    |

---

## 🛠️ Architecture du code

| Classe / Fonction | Rôle                                                            |
|-------------------|-----------------------------------------------------------------|
| `charger(ids)`    | Charge les catégories depuis `quiz_data.json`                  |
| `PanneauQuiz`     | Gère l'affichage et la logique d'un onglet de quiz             |
| `Application`     | Fenêtre principale avec les deux onglets et l'en-tête          |

---

## 👨‍💻 Auteur

Développé avec ❤️ à **Abidjan, Côte d'Ivoire**.
