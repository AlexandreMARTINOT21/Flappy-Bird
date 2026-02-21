# Flappy Bird IA : Évolution par Algorithme Génétique

Ce projet met en scène une intelligence artificielle entraînée à jouer à **Flappy Bird** à l’aide d’un algorithme évolutif. L'objectif est de simuler la sélection naturelle pour faire émerger un comportement optimal capable de déjouer tous les obstacles du jeu.

---

## Principe du Projet

L’IA repose sur la génération initiale d’un grand nombre d’individus créés aléatoirement (**1000 individus**). Après chaque tentative dans l'environnement de jeu, un score de performance (fitness) leur est attribué. 

### Le cycle évolutif
Le processus suit une boucle itérative rigoureuse :

1. **Évaluation** : Le score détermine la capacité d'un individu à se reproduire ou à disparaître.
2. **Reproduction & Mutation** : Un individu sélectionné transmet son réseau de neurones à la génération suivante avec des **mutations aléatoires** (modification du poids de un ou plusieurs neurones).
3. **Convergence** : À mesure que les générations s'enchaînent, les réseaux de neurones convergent vers la solution la plus efficace pour répondre à notre cible.

---

## Concepts

### Gestion des Espèces
Les individus sont regroupés par espèces afin de préserver la diversité génétique :
* **Limitation à 20 espèces** : Seules les espèces les plus performantes sont conservées, tandis que les autres sont éliminées.
* **Diversité** : Ce mécanisme permet d'éviter qu'une espèce moyennement efficace ne bloque l'évolution globale. Si un individu développe des caractéristiques supérieures, il forme une nouvelle espèce qui devient la base de la progression suivante.

### Paliers de Difficulté
L'évolution de l'IA est marquée par plusieurs étapes clés visibles lors de l'entraînement :
1. Franchissement du premier tuyau.
2. Maîtrise de l'ensemble des tuyaux immobiles.
3. Adaptation aux **tuyaux mobiles**.
4. Précision chirurgicale pour les tuyaux les plus rapides, où la fenêtre d'action est extrêmement courte.

---

## Résultats et Performances

Le système de sélection naturelle permet d'atteindre des résultats impressionnants :
* **Génération 59** : L'IA atteint un comportement optimal a partir des générations 50,variable ensuite selon l'aléatoire, donnant naissance à un **« oiseau invincible »**.
* **Score observé** : Dans la démonstration, l'IA traverse plus de **200 tuyaux**. En laissant le programme tourner, le score dépasse facilement les **600**, l'oiseau restant en vie indéfiniment.
* **Adaptabilité** : L'IA est capable de gérer les 4 vitesses de déplacement des tuyaux, effectuant ses sauts avec une précision millimétrée.

---
