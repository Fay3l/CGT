# CGT
Le projet CGT est une application qui utilise l'intelligence artificielle (IA) pour créer des images. Ces images contiennent un jeu de devinettes appelé "Qui suis-je ?". Chaque image présente cinq indices pour aider à deviner la réponse.

L'application peut générer ces images en trois langues : français, allemand et anglais. Une fois les images créées, elles sont envoyées et publiées sur la plateforme TikTok.

En résumé, le projet CGT utilise l'IA pour créer des jeux de devinettes visuels en plusieurs langues et les partage sur TikTok.

## Architecture et fichiers principaux
Voici une vue d’ensemble de l’architecture et des fichiers :

`api.py`
Contient la logique principale pour générer les images, ajouter les textes, gérer les polices, etc.
Exemple de fonction : create_template_clues qui ouvre un template, ajoute le texte, gère la mise en page, etc.
Voir l’extrait dans api.py.

`test.py`
Sert à tester différentes fonctionnalités du projet, comme la recherche de fichiers, la lecture de fichiers, etc.
Contient des fonctions utilitaires et des scripts de test.
Voir l’extrait dans test.py.

`README.md`

Présente le projet, son objectif et son fonctionnement général.
Voir README.md.

**template/**

Dossier contenant les images modèles (templates) pour chaque langue et numéro d’indice.

**Autres fichiers/dossiers**

Fichiers de configuration (requirements.txt, .env, etc. s’ils existent)
Dossiers pour stocker les images générées, les polices, etc.

## Environnement technique

Le projet **CGT** s’appuie sur un ensemble de technologies et d’outils pour assurer la génération et la publication automatisée de contenus visuels multilingues.
Voici les principaux composants :

**Python**
Utilisé comme langage principal pour le développement de la logique applicative, la gestion des fichiers et l’automatisation des tâches.

**Pillow**
Bibliothèque Python dédiée à la manipulation d’images : ouverture, modification, ajout de texte et sauvegarde des fichiers générés.

**API d’intelligence artificielle**
Permet la génération automatique des indices et des réponses dans plusieurs langues (français, anglais, allemand).

**Fichiers de données**
Utilisation de fichiers texte pour stocker les listes de personnalités, thèmes ou autres éléments nécessaires à la génération des devinettes.

**Templates d’images**
Images modèles servant de base à la création des visuels, organisées par langue et par numéro d’indice.

**HTML/CSS**
Utilisés pour la création de pages d’information et la présentation des conditions d’utilisation.

## Installation

Voici les étapes générales pour installer et lancer le projet :

Cloner le dépôt

```sh
git clone <url_du_depot>
cd CGT
```

Installer les dépendances Si un fichier requirements.txt existe :

```sh
pip install -r requirements.txt
```

Sinon, installer les dépendances principales (ex: Pillow pour la gestion d’images) :

```sh
pip install pillow
```

Préparer les templates et polices

Vérifier que le dossier template contient les images modèles pour chaque langue.
Ajouter les fichiers de police nécessaires dans le dossier approprié.
Lancer le script principal Adapter selon le point d’entrée (ex: api.py) :
```sh
python api.py
```

## Résumé

**CGT** génère des images de devinettes multilingues pour TikTok.
L’architecture repose sur des scripts Python pour la génération d’images et la gestion des templates.
Installation classique Python (clonage, dépendances, lancement).
Voir les fichiers api.py, test.py, README.md pour plus de détails.

### Author
 ---
Fayel MOHAMED mohamed.fayel@yahoo.com