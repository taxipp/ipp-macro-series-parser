# -*- coding: utf-8 -*-

import os
import pkg_resources
from ipp_macro_series_parser.config import Config

from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import (
	look_up, look_many, get_or_construct_value)
from ipp_macro_series_parser.comptes_nationaux import cn_output
from ipp_macro_series_parser.comptes_nationaux import cn_sheets_lists

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')
cn_hdf = parser.get('data', 'cn_hdf_directory')
cn_xls = parser.get('data', 'cn_csv_directory')


# inputs

folder_year = 2013

entry_by_index_list = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
             {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'},
             {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': None}]


overall_dict = {
    'pib': {
        'code': None,
        'institution': 'S1',
        'ressources': False,
        'description': 'PIB'
        },
    'complicated_var': {
        'code': None,
        'institution': 'S1',
        'ressources': False,
        'description': 'PIB0',
        'formula': '2*pib - pib - pib + pib*pib - pib^2'
        },
    'very_complicated_var': {
        'code': None,
        'institution': 'S1',
        'ressources': False,
        'description': 'PIB0',
        'formula': 'complicated_var^2'
        }
    }
variable_name = 'very_complicated_var'

overall_dict_2 = {
    'Interets_verses_par_rdm': {
        'code': 'D41',
        'institution': 'S2',
        'ressources': False,
        'description': ''
        },
    'Dividendes_verses_par_rdm_D42': {
        'code': 'D42',
        'institution': 'S2',
        'ressources': False,
        'description': ''
        },
    'Dividendes_verses_par_rdm_D43': {
        'code': 'D43',
        'institution': 'S2',
        'ressources': False,
        'description': ''},
    'Revenus_propriete_verses_par_rdm': {
        'code': 'D44',
        'institution': 'S2',
        'ressources': False,
        'description': ''},
    'Interets_verses_au_rdm': {
        'code': 'D41',
        'institution': 'S2',
        'ressources': True,
        'description': ''},
    'Dividendes_verses_au_rdm_D42': {
        'code': 'D42',
        'institution': 'S2',
        'ressources': True,
        'description': ''
        },
    'Dividendes_verses_au_rdm_D43': {
        'code': 'D43',
        'institution': 'S2',
        'ressources': True,
        'description': ''
        },
    'Revenus_propriete_verses_au_rdm': {
        'code': 'D44',
        'institution': 'S2',
        'ressources': True,
        'description': ''
        },
    'Interets_dividendes_nets_verses_par_rdm': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'description': 'Interets et dividendes verses par RDM, nets',
        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42 + Dividendes_verses_par_rdm_D43 + Revenus_propriete_verses_par_rdm - Interets_verses_au_rdm - Dividendes_verses_au_rdm_D42 - Dividendes_verses_au_rdm_D43 - Revenus_propriete_verses_au_rdm'
        }
    }


# outputs

df = get_comptes_nationaux_data(folder_year)

df0 = look_up(df, {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': None})

null_entry_df = look_up(df, {
                        'code': None,
                        'institution': 'S2',
                        'ressources': False,
                        'description': 'Interets et dividendes verses par RDM, nets',
                        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42 + Dividendes_verses_par_rdm_D43 + Revenus_propriete_verses_par_rdm - Interets_verses_au_rdm - Dividendes_verses_au_rdm_D42 - Dividendes_verses_au_rdm_D43 - Revenus_propriete_verses_au_rdm'
                        })

#df1 = look_many(df, entry_by_index_list)
#
#df2 = cn_output.reshape_to_long_for_output(df1)
#
#cn_output.df_long_to_csv(df2, 'IPP_test.txt')
#
#CN1 = cn_output.output_for_sheets(
#    cn_sheets_lists.list_CN1, 2013,
#    os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.txt')
#    )


value2, formula2 = get_or_construct_value(df, 'Interets_dividendes_nets_verses_par_rdm',
                                          overall_dict_2, years = range(1949, 2014))
print value2
print formula2
