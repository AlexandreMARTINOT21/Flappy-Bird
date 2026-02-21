# Flappy Bird IA : Évolution par Algorithme Génétique

Ce projet met en scène une intelligence artificielle entraînée à jouer à Flappy Bird à l’aide d’un algorithme évolutif. L'objectif est de simuler la sélection naturelle pour faire émerger un comportement optimal capable de déjouer tous les obstacles du jeu.

---

## Principe du Projet

L’IA repose sur la génération initiale d’un grand nombre d’individus créés aléatoirement (1000 individus dans ce cas). Après chaque tentative dans l'environnement de jeu, un score de performance (fitness) leur est attribué.

### Le cycle évolutif
Le processus suit une boucle itérative rigoureuse :

1. Évaluation : Le score détermine la capacité d'un individu à se reproduire ou à disparaître.
2. Reproduction & Mutation : Un individu sélectionné transmet son réseau de neurones à la génération suivante avec des mutations aléatoires (modification du poids d'un ou plusieurs neurones).
3. Convergence : À mesure que les générations s'enchaînent, les réseaux de neurones convergent vers la solution la plus efficace pour atteindre l'objectif fixé.

---

### Gestion des Espèces
Les individus sont regroupés par espèces afin de préserver la diversité génétique :
* Limitation à 20 espèces : Seules les espèces les plus performantes sont conservées, tandis que les autres sont éliminées. Nous maintenons un certain nombre d'espèces pour favoriser l'exploration, tout en limitant ce nombre pour ne pas gêner l'exploitation des espèces dominantes. En effet, un nombre trop élevé d'espèces réduirait le nombre de descendants attribués aux meilleures lignées, limitant ainsi leur capacité à explorer les configurations de réseaux environnantes.
* Spéciation : Si un individu développe des caractéristiques supérieures et se démarque, il fonde une nouvelle espèce qui devient la base de la progression suivante.



### Paliers de Difficulté
L'évolution de l'IA est marquée par plusieurs étapes clés visibles lors de l'entraînement :
1. Franchissement du premier tuyau.
2. Maîtrise de l'ensemble des tuyaux immobiles.
3. Adaptation aux tuyaux mobiles.
4. Précision chirurgicale pour les tuyaux les plus rapides, où la fenêtre d'action est extrêmement courte.

---

## Résultats et Performances

Le système de sélection naturelle permet d'atteindre des résultats impressionnants :
L'IA adopte un comportement optimal à partir de la 50ème génération environ (variable selon l'aléa des phases de sélection), donnant naissance à un « oiseau invincible ».

Cet oiseau reste en vie indéfiniment. Lors des tests, en laissant tourner le programme plusieurs heures, le score a dépassé les 600 points. L'IA semble capable de gérer tous les cas de figure, effectuant ses sauts avec une précision millimétrée, condition sine qua non pour franchir les tuyaux mobiles à leur vitesse maximale.



---
