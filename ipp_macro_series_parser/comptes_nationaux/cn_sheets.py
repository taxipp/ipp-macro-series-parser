# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:22:19 2015

@author: sophie.cottet

This script recreates the different excel sheets of Agrégats IPP - Comptabilité nationale.xls
i.e. an economic / Piketty presentation of the Comptabilité nationale agregates.
"""

import os
import pkg_resources
from ipp_macro_series_parser.config import Config

from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import cn_df_generator
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import look_many
from ipp_macro_series_parser.comptes_nationaux.cn_output import reshape_to_long_for_output, df_long_to_csv

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')


def output_for_sheets(entry_by_index_list, excel_file_name):
    list_variables = entry_by_index_list
    table = cn_df_generator(2013)

    extract = look_many(table, list_variables)
    extract = extract.drop_duplicates()
    extract = extract.drop_duplicates((u'code', u'institution', u'ressources', u'value',
       u'year'))  # this eliminates doubles, i.e. identical info coming from distinct sources (eg. TEE and Compte)

    df = reshape_to_long_for_output(extract)

    df_long_to_csv(df, excel_file_name)
    return df


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


CN1 = output_for_sheets(list_CN1, os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.csv'))
