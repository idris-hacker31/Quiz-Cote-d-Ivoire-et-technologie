# 📚 IDRIS Pro Library — Bibliothèque en ligne

Application de gestion de bibliothèque en ligne avec interface graphique **PySide6** et recommandations de lecture personnalisées grâce à l'**IA Claude d'Anthropic**.

---

## ✨ Fonctionnalités

- **Catalogue complet** : 35+ livres répartis en rayons Adultes et Enfants (romans, contes, poésies, fables, nouvelles…)
- **Gestion des emprunts** : suivi multi-exemplaires avec horodatage de chaque emprunt
- **Recommandations IA** : Claude analyse le catalogue et propose 3 livres adaptés à l'âge de l'emprunteur
- **Recherche globale** : par titre, auteur ou sous-catégorie
- **Statistiques en temps réel** : nombre de titres, exemplaires, disponibles, empruntés
- **Persistance des données** : sauvegarde automatique en JSON

---

## 🛠️ Prérequis

- Python **3.9+**
- Une clé API Anthropic ([obtenir une clé](https://console.anthropic.com/))

---

## 📦 Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-utilisateur/idris-pro-library.git
cd idris-pro-library

# 2. Installer les dépendances
pip install PySide6 anthropic

# 3. Configurer la clé API
export ANTHROPIC_API_KEY="sk-ant-..."   # Linux / macOS
set ANTHROPIC_API_KEY=sk-ant-...        # Windows (CMD)
$env:ANTHROPIC_API_KEY="sk-ant-..."     # Windows (PowerShell)

# 4. Lancer l'application
python idris_pro_library.py
```

---

## 🚀 Utilisation

### Navigation principale

| Page | Description |
|---|---|
| **Accueil** | Statistiques globales, accès aux rayons et liste des auteurs |
| **Rayon Adultes** | Romans, contes, poésies, nouvelles (Dadié, Kourouma, Hugo…) |
| **Rayon Enfants** | Contes, fables, dessins animés (Perrault, La Fontaine, Dahl…) |
| **Recherche** | Recherche transversale dans tout le catalogue |
| **Emprunts** | Liste de tous les exemplaires actuellement empruntés |

### Emprunter un livre

1. Naviguez jusqu'à la fiche d'un livre disponible
2. Cliquez sur **"Emprunter le livre"**
3. Renseignez le **nom** et l'**âge** de l'emprunteur
4. (Optionnel) Cliquez sur **"Générer les recommandations IA"** pour obtenir 3 suggestions personnalisées
5. Confirmez l'emprunt

### Logique de recommandation par tranche d'âge

| Âge | Profil | Catalogue proposé |
|---|---|---|
| < 18 ans | Enfant / Adolescent | Rayon Enfants uniquement |
| 18 – 42 ans | Jeune adulte | Catalogue complet |
| > 42 ans | Adulte confirmé | Rayon Adultes, classiques et œuvres engagées |

---

## 📂 Structure du projet

```
idris-pro-library/
├── idris_pro_library.py    # Application principale (fichier unique)
├── bibliotheque_data.json  # Base de données (générée automatiquement)
└── README.md
```

### Architecture interne

```
Livre                   # Modèle de données d'un livre
Bibliotheque            # Gestionnaire du catalogue (CRUD + persistance JSON)
RecoWorker (QThread)    # Appel asynchrone à l'API Anthropic
BorrowDialog (QDialog)  # Formulaire d'emprunt avec intégration IA
App (QMainWindow)       # Fenêtre principale et routeur de navigation
├── PageAccueil         # Tableau de bord et accès aux rayons
├── PageCategorie       # Liste filtrée par rayon et sous-catégorie
├── PageFiche           # Détail d'un livre, emprunt et retour
├── PageRecherche       # Recherche globale
└── PageEmprunts        # Liste de tous les emprunts en cours
```

---

## 📖 Catalogue inclus

| Auteur | Nationalité | Catégorie | Œuvres |
|---|---|---|---|
| Bernard Binlin Dadié | Ivoirien | Adultes | 8 |
| Ahmadou Kourouma | Ivoirien | Adultes | 5 |
| Victor Hugo | Français | Adultes | 6 |
| Charles Perrault | Français | Enfants | 6 |
| Jean de La Fontaine | Français | Enfants | 5 |
| Antoine de Saint-Exupéry | Français | Enfants | 1 |
| Roald Dahl | Britannique | Enfants | 5 |

Chaque livre est disponible en **5 exemplaires** par défaut.

---

## ⚙️ Configuration avancée

### Modifier le nombre d'exemplaires par défaut

Dans la méthode `_peupler()` de la classe `Bibliotheque`, chaque `Livre` accepte un paramètre `nb_exemplaires` :

```python
Livre("Titre", "Auteur", "Nationalité", "Catégorie", "Sous-cat", 2024,
      "Résumé…", nb_exemplaires=10)  # ← modifier ici
```

### Ajouter un livre au catalogue

Ajoutez une entrée dans `_peupler()` ou directement dans `bibliotheque_data.json` :

```json
{
  "titre": "Nouveau Livre",
  "auteur": "Prénom Nom",
  "nationalite": "Nationalité",
  "categorie": "Adultes",
  "sous_categorie": "Romans",
  "annee": 2024,
  "resume": "Description du livre.",
  "nb_exemplaires": 5,
  "dates_emprunts": []
}
```

### Réinitialiser le catalogue

Supprimez le fichier `bibliotheque_data.json` et relancez l'application. Le catalogue d'origine sera recréé automatiquement.

---

## 🤖 Intégration IA (Anthropic Claude)

Les recommandations sont générées par **claude-sonnet-4-20250514** via un thread dédié (`RecoWorker`) pour ne pas bloquer l'interface.

L'application fonctionne **sans clé API** : le bouton de recommandation affichera un message d'erreur, mais toutes les autres fonctionnalités resteront disponibles.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

*Développé avec ❤️ — PySide6 · Anthropic Claude · Python*
