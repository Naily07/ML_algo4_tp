# 🤖 Tic-Tac-Toe avec Minimax et Apprentissage Automatique

Ce projet implémente un **jeu de morpion (Tic-Tac-Toe)** intégrant :
- Une intelligence artificielle basée sur **l'algorithme Minimax**
- Un **modèle de classification entraîné** avec **Keras** pour imiter les décisions optimales

---
## 🌐 Démo en ligne

👉 Joue contre l'IA ici :  
📎 **[https://tic-tac-toe-minmax.vercel.app/](https://tic-tac-toe-minmax.vercel.app/)**


## 📁 Structure du projet

- `Min_max_tic_toe.py` : 
  - Code principal d’apprentissage
  - Génération automatique de données avec Minimax
  - Entraînement d’un modèle MLP (réseau de neurones)

- `ia_morpion.h5` : modèle Keras sauvegardé après entraînement

---

## 🧠 Fonctionnalités

- ✅ Génération intelligente du dataset à l’aide de l’algorithme Minimax
- 🧠 Entraînement d’un modèle de prédiction de coups (classification multiclasses)
- 🔄 Standardisation du plateau pour que l’IA apprenne toujours depuis la perspective du joueur courant
- 🔐 Filtrage des coups invalides lors de la prédiction
- 📊 Affichage du coup proposé par le modèle

---

## 🚀 Lancer l'entraînement

python Min_max_tic_toe.ipynb
