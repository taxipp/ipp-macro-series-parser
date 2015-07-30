# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:22:19 2015

@author: sophie.cottet

This script gives the list dictionnaries of the variables needed to recreate the different excel sheets of
'Agrégats IPP - Comptabilité nationale.xls', i.e. the economic / Piketty presentation of the Comptabilité nationale
agregates.
These lists are called by the function cn_output.output_for_sheets.
TODO: a function which calls them all, applies formulas and formats the excel sheet so as to reproduce the actual
formatting.
"""


# CN1

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
        {'code': 'D21', 'institution': 'S13', 'ressources': True, 'description': ''},  # impôts indirects : impôts nets sur les produits & impôts nets sur la production
        {'code': 'D31', 'institution': 'S13', 'ressources': True, 'description': ''},
        {'code': 'D29', 'institution': 'S13', 'ressources': True, 'description': ''},
        {'code': 'D39', 'institution': 'S13', 'ressources': True, 'description': ''}  # NB : D39 est aussi dans un autre compte (le compte d'exploitation) pour les APUs, en emplois. donc bien renseigner ressources..
    ]

# CN2

list_CN2 = [{'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': ''},  # salaires versés. il nous les faut pour à peu près toutes les institutions
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
        {'code': 'D21', 'institution': 'S13', 'ressources': True, 'description': ''},  # impôts indirects : impôts nets sur les produits & impôts nets sur la production
        {'code': 'D31', 'institution': 'S13', 'ressources': True, 'description': ''},
        {'code': 'D29', 'institution': 'S13', 'ressources': True, 'description': ''},
        {'code': 'D39', 'institution': 'S13', 'ressources': True, 'description': ''}]
