# Dénombrements fiscaux 

### Objectif

On désire construire des agrégats fiscaux à partir des [dénombrements fiscaux fournis par la DGFiP (sous forme pdf)] 
(http://www2.impots.gouv.fr/documentation/statistiques/2042_nat/Impot_sur_le_revenu.htm) 
afin de les utiliser comme cales pour le modèle de microsimulation TAXIPP. Les fichiers au format Excel se trouvent dans 
le répertoire `D2042Nat` et l'on dispose également des dénombrements effectués lobs du développement d'openfisca dans le fichier `2042_national.xls`.

À cette fin, on écrit un programme qui reproduit ce qui a été réalisé à la main pour les années précédentes.
Le résultats se trouve dans le fichier ` Agrégats IPP - Données fiscales.xls ̀`.

Le chemin du répertoire contenant ces fichiers Excel doit être indiqué dans le [fichier de configuration] (https://github.com/taxipp/ipp-macro-series-parser/blob/master/config.ini#L17). 

### Préparer les données liés au dénombrements fiscaux

Afin de disposer d'un accès rapide aux données précédentes, il est utile de les stocker dans uen base de données au format HDF5. Le chemin du répertoire contenant ces fichiers HDF5 doit être indiqué dans le [fichier de configuration] (https://github.com/taxipp/ipp-macro-series-parser/blob/master/config.ini#L18). 

Cette base de données est générée par l'exécution du programme[denombrements_fiscaux_parser.py] (https://github.com/taxipp/ipp-macro-series-parser/blob/master/ipp_macro_series_parser/scripts/denombrements_fiscaux_parser.py)


### Production des agrégats







