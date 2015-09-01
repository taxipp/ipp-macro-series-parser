# -*- coding: utf-8 -*-

import os
import pkg_resources
from ipp_macro_series_parser.config import Config

from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import (
    look_many, look_up, get_or_construct_value, get_or_construct_data)
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

list_ENE = [
    {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': ''},
    {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': ''}
    ]

incomplete_overall_dict = dict(notfound_arg = {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'})

simple_dict = {'Interets verses par rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False}}

dict_with_div = {
    'Interets_verses_par_rdm': {
        'code': 'D41', 'institution': 'S2', 'ressources': False
        },
    'Interets_verses_par_rdm / 100': {
        'code': 'D41', 'institution': 'S2', 'ressources': False, 'formula': 'Interets_verses_par_rdm / 100'
        }
    }

dict_with_squares = {
    'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                      'description': ''},
    'Just_a_sum_of_D41_and_D42': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                                  'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'},
    'Square_of_sum': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                      'formula': 'Just_a_sum_of_D41_and_D42^2'}
    }

dict_revenus_rdm = {
    'Salaires_verses_au_rdm': {'code': 'D11', 'institution': 'S2', 'ressources': True, 'description': ''},
    'Salaires_verses_par_rdm': {'code': 'D11', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Dividendes_verses_par_rdm_D43': {'code': 'D43', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Revenus_de_la_propriete_verses_par_rdm': {'code': 'D44', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Interets_verses_au_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': True, 'description': ''},
    'Dividendes_verses_au_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': True, 'description': ''},
    'Dividendes_verses_au_rdm_D43': {'code': 'D43', 'institution': 'S2', 'ressources': True, 'description': ''},
    'Revenus_de_la_propriete_verses_au_rdm': {'code': 'D44', 'institution': 'S2', 'ressources': True, 'description': ''},
    'Salaires_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Salaires_verses_par_rdm - Salaires_verses_au_rdm'},
    'Interets_et_dividendes_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42 + Dividendes_verses_par_rdm_D43 + Revenus_de_la_propriete_verses_par_rdm - Interets_verses_au_rdm - Dividendes_verses_au_rdm_D42 - Dividendes_verses_au_rdm_D43 - Revenus_de_la_propriete_verses_au_rdm'},
    'Revenus_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Salaires_verses_par_rdm_nets + Interets_et_dividendes_verses_par_rdm_nets'}}

dict_profits = {
    'ene_snf': {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},
    'ene_sf': {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
    'Profits_des_societes': {'formula': 'ene_snf + ene_sf'}
    }

dict_sal_cot_soc = {
        'cs_eff_empl_SNF': {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_SF': {'code': 'D121', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_APU': {'code': 'D121', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_Menages': {'code': 'D121', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_ISBLSM': {'code': 'D121', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_SNF': {'code': 'D122', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_SF': {'code': 'D122', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_APU': {'code': 'D122', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_Menages': {'code': 'D122', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_ISBLSM': {'code': 'D122', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'Sal_verses_SNF': {'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},
        'Sal_verses_SF': {'code': 'D11', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Sal_cs_verses_societes': {
            'formula': 'Sal_verses_SNF + Sal_verses_SF + cs_eff_empl_SNF + cs_eff_empl_SF + cs_imput_empl_SNF + cs_imput_empl_SF'},
    }

double_dict = {
    'Interets verses par rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},
    'Dividendes verses par rdm D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                     'description': ''}
    }

mult_dict_with_formula = {
    'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': '',
                                'drop': True},
    'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                     'description': '', 'drop': True},
    'Just a sum of D41 and D42': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                                  'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'}
    }

# outputs

# - test get_comptes_nationaux_data
df = get_comptes_nationaux_data(folder_year)

# - tests look_up
data_precise = look_up(df, {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': None})
# should be DataFrame of size 65x11
data_large = look_up(df, {'institution': 'S2', 'ressources': False, 'description': ''})
# should be DataFrame of size 5477x11
data_inexistant = look_up(df, {'code': 'ceci nest pas un code de compta nat', 'institution': 'S2', 'ressources': False,
                               'description': ''})
# should be empty series
data_inexistant_2 = look_up(df, {'code': '', 'institution': 'S2', 'ressources': False, 'description': ''})
# should be empty series
data_empty_because_formula = look_up(df, {'code': 'D12', 'institution': 'S2', 'ressources': False, 'description': '',
                                          'formula': 'now it should be empty'})
# should be empty series

# - test look_many
ene_societes = look_many(df, list_ENE)

# - test reshape_to_long_for_output
# df2 = reshape_to_long_for_output(df)
# - test df_long_to_csv
# df_long_to_csv(df2, 'IPP_test.txt')
# - test output_for_sheets
# CN1 = output_for_sheets(
#    cn_sheets_lists.list_CN1, 2013,
#    os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.txt')
#    )

# - tests get_or_construct_value
#value_empty, formula_of_empty = get_or_construct_value(df, 'notfound_arg', incomplete_overall_dict)
# should return KeyError because components of formula are not in dict
value_simple_dict, formula_simple_dict = get_or_construct_value(df, 'Interets verses par rdm', simple_dict)
value_div, formula_div = get_or_construct_value(df, 'Interets_verses_par_rdm / 100', dict_with_div)
value_sq, formula_sq = get_or_construct_value(df, 'Square_of_sum', dict_with_squares)
value_rdm_net, formula_rdm_net = get_or_construct_value(df, 'Interets_et_dividendes_verses_par_rdm_nets', dict_revenus_rdm)
values_profits, formulas_profits = get_or_construct_value(df, 'Profits_des_societes', dict_profits)
value_sal_cs, formula_sal_cs = get_or_construct_value(df, 'Sal_cs_verses_societes', dict_sal_cot_soc, years = range(1978, 2014))

# - tests for get_or_construct_data
values_double, formulas_double = get_or_construct_data(df, double_dict)
values_double_w_formula, formulas_double_w_formula = get_or_construct_data(df, mult_dict_with_formula)
values_complex, formulas_complex = get_or_construct_data(df, dict_with_squares)
values_profits_societes, formulas_profits_societes = get_or_construct_data(df, dict_profits)
values_revenus_reste_du_monde, formulas_revenus_reste_du_monde = get_or_construct_data(df, dict_revenus_rdm, range(1996, 2014))
values_sal_cs, formulas_sal_cs = get_or_construct_data(df, dict_sal_cot_soc, years = range(1978, 2014))

# tests with CN1
values_CN1, formulas_CN1 = get_or_construct_data(df, cn_sheets_lists.variables_CN1, range(1978, 2014))
