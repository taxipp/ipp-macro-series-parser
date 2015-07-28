# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:22:19 2015

@author: sophie.cottet

This script recreates the different excel sheets of Agrégats IPP - Comptabilité nationale.xls
i.e. an economic / Piketty presentation of the Comptabilité nationale agregates.
"""

import pandas
from ipp_macro_series_parser.comptes_nationaux.cn_main import cn_df_generator
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import look_many, look_up
from ipp_macro_series_parser.comptes_nationaux.cn_output import reshape_to_long_for_output

table = cn_df_generator(2013)

list_CN1 = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
        {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'},
        {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'Revenu national brut en milliards d'},  # pas encore parmi données importées
    # Revenus versés par reste du monde
        {'code': 'D11', 'institution': 'S2', 'ressources': True, 'description': ''},  # salaires reçus par RDM
        {'code': 'D11', 'institution': 'S2', 'ressources': False, 'description': ''},  # salaires versés par RDM
        {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},  # ce qui suit compose les intérêts et dividendes versés par RDM ("provenance")
        {'code': 'D42', 'institution': 'S2', 'ressources': False, 'description': ''},
        {'code': 'D43', 'institution': 'S2', 'ressources': False, 'description': ''},
        {'code': 'D44', 'institution': 'S2', 'ressources': False, 'description': ''},
        {'code': 'D41', 'institution': 'S2', 'ressources': True, 'description': ''},  # ce qui suit compose les intérêts et dividendes versés par RDM
        {'code': 'D42', 'institution': 'S2', 'ressources': True, 'description': ''},
        {'code': 'D43', 'institution': 'S2', 'ressources': True, 'description': ''},
        {'code': 'D44', 'institution': 'S2', 'ressources': True, 'description': ''},
    # Dépréciation du capital fixe (CCF) : économie nationale, APUs, ISBLSM
        {'code': 'P51c', 'institution': 'S1', 'ressources': False, 'description': ''},
        {'code': 'P51c', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'P51c', 'institution': 'S15', 'ressources': False, 'description': ''},
    # Variables CN2, nécessaires pour reconstruction du Revenu national façon Piketty
        {'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': ''},  # salaires versés. il nous les faut pour à peu près toutes les institutions
        {'code': 'D11', 'institution': 'S12', 'ressources': False, 'description': ''},
        {'code': 'D11', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'D11', 'institution': 'S14', 'ressources': False, 'description': ''},
        {'code': 'D11', 'institution': 'S15', 'ressources': False, 'description': ''},
        {'code': 'B2n', 'institution': 'S14', 'ressources': False, 'description': ''},  # ENE ménages (ie loyers reçus)
        {'code': 'B3n', 'institution': 'S1', 'ressources': False, 'description': ''},   # Revenu mixte / non-salariés
        {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': ''},  # cotisations patronales effectives
        {'code': 'D121', 'institution': 'S12', 'ressources': False, 'description': ''},
        {'code': 'D121', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'D121', 'institution': 'S14', 'ressources': False, 'description': ''},
        {'code': 'D121', 'institution': 'S15', 'ressources': False, 'description': ''},
        {'code': 'D122', 'institution': 'S11', 'ressources': False, 'description': ''},  # cotisations patronales imputées
        {'code': 'D122', 'institution': 'S12', 'ressources': False, 'description': ''},
        {'code': 'D122', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'D122', 'institution': 'S14', 'ressources': False, 'description': ''},
        {'code': 'D122', 'institution': 'S15', 'ressources': False, 'description': ''},
        {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': ''},  # ENE SNF
        {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': ''},  # ENE SF
        {'code': 'D21', 'institution': 'S13', 'ressources': False, 'description': ''},  # impôts indirects : impôts nets sur les produits & impôts nets sur la production
        {'code': 'D31', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'D29', 'institution': 'S13', 'ressources': False, 'description': ''},
        {'code': 'D39', 'institution': 'S13', 'ressources': False, 'description': ''}  # NB : D39 est aussi dans un autre compte (le compte d'exploitation) pour les APUs, en emplois. donc bien renseigner ressources..
    ]
# pour qu'il choppe revenu national il faudrait insérer code de ce type dans get_file_infos :
#        elif filename == 't_1115':
#            agent = 'S1'  # (économie nationale)
#            title = 'PIB et RNB par habitant'
# ne marche pas. pb de parser ? organisation du fichier n'est pas compatible ?

extract = look_many(table, list_CN1)
extract[['year']] = extract[['year']].astype(int)  # sinon double les années

extract_thin = extract.drop_duplicates()  # regarder quels étaient ces duplicates

# extract_tidy = reshape_to_long_for_output(extract)

# ou (étape par étape, en en rajoutant pour trouver & fixer le bug) :
del extract_thin['file_name']
del extract_thin['link']
del extract_thin['source']
del extract_thin['version']
del extract_thin['description']
# extract_thinner = extract_thin.drop_duplicates(subset = ('code', 'year', 'institution', 'ressources'))
extract_thinner = extract_thin.drop_duplicates(subset = ('code', 'year', 'institution', 'ressources', 'file_title'))
df = extract_thinner.set_index(['year', 'code', 'ressources', 'institution', 'file_title'])
df2 = df.drop_duplicates()  # cette étape est nécessaire pour que ça bug pas à la suivante (unstack)
# df3 = df2.unstack(level = 'year')
df3 = df.unstack(level = 'year')
df4 = df3.transpose()
df5 = df4.reset_index(1)
df5.reset_index(drop = True)

# list = [
#        {'code': , 'institution': '', 'ressources': , 'description': ''},
#        {'code': , 'institution': '', 'ressources': , 'description': ''}
#       ]

cotisations = [{'code': 'D121', 'institution': None, 'ressources': False, 'description': ''},
        {'code': 'D122', 'institution': None, 'ressources': False, 'description': ''}]
look_many(2013, cotisations)
cotis1 = {'code': 'D121', 'institution': None, 'ressources': False, 'description': ''}
look_up(2013, cotis1)
iscotis = table['code'] == 'D121'
cotis = table[iscotis]
ismenages = table['institution'] == 'S14'
cotismen = table[iscotis & ismenages]
notmen = table['institution'] != 'S14'
cotisnot = table[iscotis & notmen]
isressource = table['ressources'] == True
cotisressource = table[isressource & iscotis]
isrdm = table['institution'] == 'S2'
cotisrdm = table[iscotis & isrdm]

isrdm_2 = extract['institution'] == 'S2'
isD11 = extract['code'] == 'D11'
D11rdm = extract[isrdm_2 & isD11]  # l'info se trouve aussi dans les TEE donc il y a des D11 Emplois
rdm_extr = extract[isrdm_2]

isD41 = extract['code'] == 'D41'
D41rdm = extract[isrdm_2 & isD41]  # idem donc ok
