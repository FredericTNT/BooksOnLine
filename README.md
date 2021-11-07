# BooksOnline

## Table des matières
1. [Informations générales](#Informations_générales)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Exécution](#Exécution)
## Informations_générales
***
Web scrapping du site http://books.toscrape.com
 + Génération d'un fichier csv pour chaque catégorie de livre
 + Téléchargement des images de couverture de chaque livre
## Technologies
***
Technologies utilisées dans ce projet :
* [Windows 10 Famille](https://docs.microsoft.com/fr-fr/windows/whats-new/whats-new-windows-10-version-21h1) : Version 21H1 
* [Python](https://docs.python.org/fr/3.10/) : Version 3.10.0
* [Library - requests](https://pypi.org/project/requests/2.26.0/) : Version 2.26.0
* [Library - beautifulsoup4](https://pypi.org/project/beautifulsoup4/4.10.0/) : Version 4.10.0
* [Library - csv342](https://pypi.org/project/csv342/1.0.1/) : Version 1.0.1
## Installation
***
Réaliser l'installation avec le terminal Windows PowerShell 

Le clonage (git clone) se fait dans un répertoire BooksOnline
```
$ git clone https://github.com/FredericTNT/BooksOnline
$ cd BooksOnline
$ python -m venv <nom environnement>
$ <nom environnement>/scripts/activate
$ pip install - r requirements.txt
```
## Exécution
***
L'application se lance en exécutant le programme bol.py dans l'environnement virtuel activé
```
$ python bol.py
```

Les fichiers csv et jpg sont générés dans le répertoire **/Books** et celui-ci est **supprimé**, s'il existe, au début de chaque exécution.

<!---
## FAQs
***
A list of frequently asked questions
1. **This is a question in bold**
Answer of the first question with _italic words_. 
2. __Second question in bold__ 
To answer this question we use an unordered list:
* First point
* Second Point
* Third point
3. **Third question in bold**
Answer of the third question with *italic words*.
4. **Fourth question in bold**
| Headline 1 in the tablehead | Headline 2 in the tablehead | Headline 3 in the tablehead |
|:--------------|:-------------:|--------------:|
| text-align left | text-align center | text-align right |
-->