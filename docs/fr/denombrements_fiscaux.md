# Dénombrements fiscaux 

### Objectif

On désire construire des agrégats fiscaux à partir des [dénombrements fiscaux fournis par la DGFiP (sous forme pdf)] 
(http://www2.impots.gouv.fr/documentation/statistiques/2042_nat/Impot_sur_le_revenu.htm) 
afin de les utiliser comme cales pour le modèle de microsimulation TAXIPP. Les fichiers au format Excel se trouvent dans 
le répertoire `D2042Nat` et l'on dispose également des dénombrements effectués lobs du développement d'openfisca dans le fichier `2042_national.xls`.

À cette fin, on écrit un programme qui reproduit ce qui a été réalisé à la main pour les années précédentes.
Le résultats se trouve dans le fichier ` Agrégats IPP - Données fiscales.xls ̀`.

Le chemin du répertoire contenant ces fichiers Excel doit être indiqué dans le [fichier de configuration] (../../config.ini#L17). 

### Préparer les données liés au dénombrements fiscaux

Afin de disposer d'un accès rapide aux données précédentes, il est utile de les stocker dans uen base de données au format HDF5. Le chemin du répertoire contenant ces fichiers HDF5 doit être indiqué dans le [fichier de configuration] (../../config.ini#L18). 

Cette base de données est générée par l'exécution du programme [denombrements_fiscaux_parser.py] (../../ipp_macro_series_parser/scripts/denombrements_fiscaux_parser.py)

### Production des agrégats

Les nouveaux agrégats IPP sont généés à partir de fonctions se trouvant dans [`le module agregats_ipp`] (../../ipp_macro_series_parser/denombrements_fiscaux/agregats_ipp.py), 
notamment:
 - `build_agregagtes` qui construit les agrégats qui sont mis en forme par la fonction suivante,
 - `build_irpp_tables` qui construit des tables similaires à celles produites par l'IPP sous forme de fichiers Excel.
 
Les formules utilisées pour construire ces agrégats se trouvent également dans [`le module agregats_ipp`] (../../ipp_macro_series_parser/denombrements_fiscaux/agregats_ipp.py)
notamment:
 - `formula_by_variable_name` qui définit les agrégats de premier niveau à partir des cases des feuilles d'impôts
 - `level_2_formula_by_variable_name` qui définit les agrégats de niveau supérieur à partir des agrégats de premier niveau
 
### Validation

Afin de valider les tables produites, elles sont comparées aux tableaux Excel de l'IPP par exécution d'[un test spécifique] (../../ipp_macro_series_parser/tests/test_denombrements_fiscaux.py).
La vérification des agrégats de plus bas niveaux se fait à l'aide d'[un autre test] (../../ipp_macro_series_parser/tests/test_denombrements_fiscaux_debug.py) fort utile pour le débogage en tout genre (erreur sur les valeur des cases dans les tableaux, changement de formule, etc).   







