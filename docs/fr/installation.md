# Installation et configuration

> Note: Cette documentation est en cours d'écriture.

## Installation

Clonez le répertoire Git ipp-macro-series-parser sur votre ordinateur et installez le package Python.
En supposant que vous êtes sur votre répertoire de travail :

```
git clone https://github.com/taxipp/ipp-macro-series-parser
cd ipp-macro-series-parser
pip install -e .
```

## Configuration

Renommez config.ini en config_local.ini, et remplacez None par les chemins des dossiers dans lesquels vous souhaitez sauvergarder les données qui seront téléchargées ou produites.
Par exemple, les données téléchargées à  l'aide du script comptes_nationaux seront sauvegardées dans le dossier de votre choix, que vous aurez indiqué dans cn_directory.

