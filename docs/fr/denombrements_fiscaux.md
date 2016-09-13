# Dénombrements fiscaux 

### Objectif

On désire construire des agrégats fiscaux à partir des [dénombrements fiscaux fournis par la DGFiP (sous forme pdf)] 
(http://www2.impots.gouv.fr/documentation/statistiques/2042_nat/Impot_sur_le_revenu.htm) 
afin de les utiliser comme cales pour le modèle de microsimulation TAXIPP. Les fichiers au format Excel se trouvent dans 
le répertoire `D2042Nat` et l'on dispose également des dénombrements effectués lobs du développement d'openfisca dans le fichier  
`2042_national.xls`.

Pour cela, on écrit un programme qui reproduit ce qui a été fait à la main pour les années précédentes.
Le résultats se trouve dans le fichier ` Agrégats IPP - Données fiscales.xls ̀`.

Le chemin vers le répertoire contenant ces fichiers Excel doit être indiqué dans le [fichier de configuration] (https://github.com/taxipp/ipp-macro-series-parser/blob/master/config.ini#L17). 

### Préparer les données liés au dénombrements fiscaux





