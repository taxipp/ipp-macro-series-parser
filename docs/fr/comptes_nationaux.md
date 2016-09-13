# Comptes nationaux

### Télécharger les données de la comptabilité nationale

Le script [`cn_downloader`] (../../ipp-macro-series-parser/scripts/cn_downloader.py) permet le téléchargement des
données brutes de la comptabilité nationale depuis le site de l'INSEE. Vous pouvez choisir de télécharger l'ensemble des données publiées les dix dernières années, ou de choisir une ou plusieurs années, par exemple la dernière <span>&mdash;</span> qui contient aussi les agrégats (aux montants éventuellement corrigés) des années précédentes.

Une aide existe concernant les options à renseigner. Elle est accessible en exécutant:
```python
./ipp-macro-series-parser/scripts/cn_downloader.py -h
```
  
### Extraire des agrégats de la comptabilité nationale

Les fichiers de la comptabilité nationale sont de deux types :
- les tableaux économiques d'ensemble (TEE) : 1 fichier par année
- des tableaux thématiques : 1 par thème, contenant les valeurs des agrégats pour l'ensemble des années couvertes

Les programmes [`parser_tee.py`] (../../ipp_macro_series_parser/comptes_nationaux/parser_tee.py) et [`parser_non_tee.py`] (../../ipp_macro_series_parser/comptes_nationaux/parser_non_tee.py) respectivement nettoient et organisent les fichiers des deux types, appliquant la structure définie dans [`get_file_infos.py`] (../../ipp_macro_series_parser/comptes_nationaux/get_file_infos.py).

