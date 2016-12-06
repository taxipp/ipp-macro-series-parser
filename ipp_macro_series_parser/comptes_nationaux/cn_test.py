# -*- coding: utf-8 -*-

import os
import pandas
import pkg_resources
from ipp_macro_series_parser.config import Config
from pandas.util.testing import assert_frame_equal

from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import (
    look_many, look_up, get_or_construct_value, get_or_construct_data)
from ipp_macro_series_parser.comptes_nationaux.sheets_lists import generate_CN1_variables, generate_CN2_variables

parser = Config()
cn_directory = parser.get('data', 'cn_directory')
cn_hdf = parser.get('data', 'cn_hdf_directory')
cn_csv = parser.get('data', 'cn_csv_directory')
tests_directory = parser.get('data', 'tests_directory')

tests_data = os.path.join(
    pkg_resources.get_distribution('ipp-macro-series-parser').location,
    'ipp_macro_series_parser/tests/data')


def get_tidy_data(year):
    df = get_comptes_nationaux_data(year)
    return df


# INPUTS


def create_list_dicts_for_look_many():
    list_var = [
        {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': ''},
        {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': ''}
        ]
    return list_var


def create_dict_for_test_get_value_empty():
    dict_var = dict(notfound_arg = {
        'code': '',
        'institution': 'S2',
        'ressources': False,
        'description': '',
        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'
        })
    return dict_var


def create_dict_revenus_rdm():
    dict_var = {
        'Salaires_verses_au_rdm': {
            'code': 'D11', 'institution': 'S2', 'ressources': True, 'description': ''
            },
        'Salaires_verses_par_rdm': {
            'code': 'D11', 'institution': 'S2', 'ressources': False, 'description': ''
            },
        'Interets_verses_par_rdm': {
            'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''
            },
        'Dividendes_verses_par_rdm_D42': {
            'code': 'D42', 'institution': 'S2', 'ressources': False, 'description': ''
            },
        'Dividendes_verses_par_rdm_D43': {
            'code': 'D43', 'institution': 'S2', 'ressources': False, 'description': ''
            },
        'Revenus_de_la_propriete_verses_par_rdm': {
            'code': 'D44', 'institution': 'S2', 'ressources': False, 'description': ''
            },
        'Interets_verses_au_rdm': {
            'code': 'D41', 'institution': 'S2', 'ressources': True, 'description': ''
            },
        'Dividendes_verses_au_rdm_D42': {
            'code': 'D42', 'institution': 'S2', 'ressources': True, 'description': ''
            },
        'Dividendes_verses_au_rdm_D43': {
            'code': 'D43', 'institution': 'S2', 'ressources': True, 'description': ''
            },
        'Revenus_de_la_propriete_verses_au_rdm': {
            'code': 'D44', 'institution': 'S2', 'ressources': True, 'description': ''
            },
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
    return dict_var


def create_dict_w_squares():
    dict_var = {
        'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},
        'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                          'description': ''},
        'Just_a_sum_of_D41_and_D42': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                                      'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'},
        'Square_of_sum': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                          'formula': 'Just_a_sum_of_D41_and_D42^2'}
        }
    return dict_var


def create_dict_profits():
    dict_var = {
        'ene_snf': {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},
        'ene_sf': {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Profits_des_societes': {'formula': 'ene_snf + ene_sf'}
        }
    return dict_var


def create_dict_sal_cot_soc():
    dict_var = {
        'cs_eff_empl_SNF': {
            'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_eff_empl_SF': {
            'code': 'D121', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_eff_empl_APU': {
            'code': 'D121', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_eff_empl_Menages': {
            'code': 'D121', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_eff_empl_ISBLSM': {
            'code': 'D121', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_imput_empl_SNF': {
            'code': 'D122', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_imput_empl_SF': {
            'code': 'D122', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_imput_empl_APU': {
            'code': 'D122', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True
            },
        'cs_imput_empl_Menages': {
            'code': 'D122', 'institution': 'S14', 'ressources': False, 'drop': True
            },
        'cs_imput_empl_ISBLSM': {
            'code': 'D122', 'institution': 'S15', 'ressources': False, 'drop': True
            },
        'Sal_verses_SNF': {
            'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True
            },
        'Sal_verses_SF': {
            'code': 'D11', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True
            },
        'Sal_cs_verses_societes': {
            'formula': 'Sal_verses_SNF + Sal_verses_SF + cs_eff_empl_SNF + cs_eff_empl_SF + cs_imput_empl_SNF + cs_imput_empl_SF'
            },
        }
    return dict_var


def create_double_dict():
    dict_var = {
        'Interets verses par rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': ''},
        'Dividendes verses par rdm D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                         'description': ''}
        }
    return dict_var


def create_mult_dict_formula():
    dict_var = {
        'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': '',
                                    'drop': True},
        'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False,
                                         'description': '', 'drop': True},
        'Just a sum of D41 and D42': {'code': '', 'institution': 'S2', 'ressources': False, 'description': '',
                                      'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42'}
        }
    return dict_var


# OUTPUTS


def tests_look_up():
    df = get_tidy_data(2013)

    data_precise = look_up(df, {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': None})
    # should be DataFrame of size 65x11
    data_large = look_up(df, {'institution': 'S2', 'ressources': False, 'description': ''})
    # should be DataFrame of size 5477x11
    data_inexistant = look_up(df, {'code': 'ceci nest pas un code de compta nat', 'institution': 'S2',
                                   'ressources': False, 'description': ''})
    # should be empty series
    data_inexistant_2 = look_up(df, {'code': '', 'institution': 'S2', 'ressources': False, 'description': ''})
    # should be empty series
    data_empty_because_formula = look_up(df, {'code': 'D12', 'institution': 'S2', 'ressources': False,
                                              'description': '', 'formula': 'now it should be empty'})
    # should be empty series

    # TODO: tests on DF sizes, rather than a 'return'
    return (
        data_precise, data_large, data_inexistant, data_inexistant_2, data_empty_because_formula
        )


def test_look_many():
    df = get_tidy_data(2013)
    list_ENE = create_list_dicts_for_look_many()
    ene_societes = look_many(df, list_ENE)
    return ene_societes


# - test reshape_to_long_for_output
# def test_reshape_to_long():
#    df2 = reshape_to_long_for_output(df)


# - test df_long_to_csv
# def test_long_to_csv():
#    df_long_to_csv(df2, 'IPP_test.txt')


# TODO: test output_for_sheets
# CN1 = output_for_sheets(
#    cn_sheets_lists.list_CN1, 2013,
#    os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.txt')
#    )


def test_get_or_construct_value_empty():
    df = get_tidy_data(2013)
    incomplete_overall_dict = create_dict_for_test_get_value_empty()
    value_empty, formula_of_empty = get_or_construct_value(df, 'notfound_arg', incomplete_overall_dict)
    # should return KeyError because components of formula are not in dict
    # TODO: assert KeyError...
    return value_empty


def test_get_or_construct_value_working():
    df = get_tidy_data(2013)

    simple_dict = {'Interets verses par rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False}}
    dict_with_div = {
        'Interets_verses_par_rdm': {
            'code': 'D41', 'institution': 'S2', 'ressources': False
            },
        'Interets_verses_par_rdm / 100': {
            'code': 'D41', 'institution': 'S2', 'ressources': False, 'formula': 'Interets_verses_par_rdm / 100'
            }
        }
    dict_sal_cot_soc = create_dict_sal_cot_soc()
    dict_revenus_rdm = create_dict_revenus_rdm()
    dict_with_squares = create_dict_w_squares()
    dict_profits = create_dict_profits()

    value_simple_dict, formula_simple_dict = get_or_construct_value(
        df, 'Interets verses par rdm', simple_dict, years = range(1949, 2014)
        )
    value_div, formula_div = get_or_construct_value(
        df, 'Interets_verses_par_rdm / 100', dict_with_div, years = range(1949, 2014)
        )
    value_sq, formula_sq = get_or_construct_value(
        df, 'Square_of_sum', dict_with_squares, years = range(1949, 2014)
        )
    value_rdm_net, formula_rdm_net = get_or_construct_value(
        df, 'Interets_et_dividendes_verses_par_rdm_nets', dict_revenus_rdm, years = range(1949, 2014)
        )
    values_profits, formulas_profits = get_or_construct_value(
        df, 'Profits_des_societes', dict_profits, years = range(1949, 2014)
        )
    value_sal_cs, formula_sal_cs = get_or_construct_value(
        df, 'Sal_cs_verses_societes', dict_sal_cot_soc, years = range(1978, 2014)
        )

    return value_simple_dict, value_div, value_sq, value_rdm_net, values_profits, value_sal_cs


def tests_get_or_construct_data():
    df = get_tidy_data(2013)

    double_dict = create_double_dict()
    dict_revenus_rdm = create_dict_revenus_rdm()
    dict_with_squares = create_dict_w_squares()
    dict_profits = create_dict_profits()
    dict_sal_cot_soc = create_dict_sal_cot_soc()
    mult_dict_with_formula = create_mult_dict_formula()

    values_double, formulas_double = get_or_construct_data(df, double_dict)
    values_double_w_formula, formulas_double_w_formula = get_or_construct_data(df, mult_dict_with_formula)
    values_complex, formulas_complex = get_or_construct_data(df, dict_with_squares)
    values_profits_societes, formulas_profits_societes = get_or_construct_data(df, dict_profits)
    values_revenus_reste_du_monde, formulas_revenus_reste_du_monde = get_or_construct_data(
        df, dict_revenus_rdm, range(1949, 2014)
        )
    values_sal_cs, formulas_sal_cs = get_or_construct_data(df, dict_sal_cot_soc, years = range(1949, 2014))

    return (
        values_double, values_double_w_formula, values_complex, values_profits_societes, values_revenus_reste_du_monde
        )


def create_and_save_dfs_get_or_construct_data():  # NB : should no longer be executed - already saved
    tuple_of_dfs = tests_get_or_construct_data()
#    values_double_dict = tuple_of_dfs[0]
#    values_double_plus_formula = tuple_of_dfs[1]
#    values_w_squares = tuple_of_dfs[2]
    values_profits_societes = tuple_of_dfs[3]
#    values_revenus_rdm = tuple_of_dfs[4]

    values_profits_societes.to_hdf(os.path.join(tests_data, 'values_profits_societes.h5'), 'profits_societes')


def create_and_save_CN1(year):  # NB : should no longer be executed - already saved
    file_path = (os.path.join(tests_data, 'values_CN1_{}.h5'.format(year)))
    assert not os.path.exists(file_path), 'CN1 sheet with {} data already generated and saved'.format(year)
    df = get_tidy_data(year)
    variables_CN1 = generate_CN1_variables(year)
    values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, year + 1))
    values_CN1.to_hdf(file_path, 'CN1')


def read_profits_societes():
    profits_societes = pandas.read_hdf(os.path.join(tests_data, 'values_profits_societes.h5'), 'profits_societes')
    return profits_societes


def read_CN1(year):
    values_CN1 = pandas.read_hdf(os.path.join(tests_data, 'values_CN1_{}.h5'.format(year)), 'CN1')
    return values_CN1


def test_profits_societes():
    df = get_tidy_data(2013)
    values_profits_societes_target = read_profits_societes()
    dict_profits_societes = create_dict_profits()
    values_profits_societes = get_or_construct_data(df, dict_profits_societes)[0]

    assert_frame_equal(values_profits_societes, values_profits_societes_target)


def test_CN1(year):
    df = get_tidy_data(year)
    values_CN1_target = read_CN1(year)
    variables_CN1 = generate_CN1_variables(year)
    values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, year + 1))

    assert_frame_equal(values_CN1, values_CN1_target)


def test_compare_sheets_to_IPP():  # WIP. for now it only generates the first two sheets, to be compared to Agrégats IPP
    df = get_tidy_data(2012)
    variables_CN1 = generate_CN1_variables(2012)
    variables_CN2 = generate_CN2_variables(2012)
    values_CN1_2012, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, 2013))
    values_CN2_2012, formulas_CN2 = get_or_construct_data(df, variables_CN2, range(1949, 2013))
    return values_CN1_2012, values_CN2_2012
# TODO: parse the corresponding sheets in Agrégats IPP - Comptabilité nationale, and read, to assert_frame_equal
# NB: normal si Impôts indirects (CN2) ne sont pas les mêmes :
# NB : on a des variables calculées qui sont NaN pour une série d'année, alors qu'Agrégats IPP a mis en 0 les variables
# d'input n'existant pas pour des années (du coup là le calcul se fait).


# LE RUN
if __name__ == '__main__':

    # create_and_save_CN1(2013)  -- should no longer be done
    # test_CN1(2013)

    cn1_2013_cible = read_CN1(2013)

    # create_and_save_dfs_get_or_construct_data()  -- should no longer be done
    # test_profits_societes()

    # df = get_tidy_data(2013)
    # variables_CN1 = generate_CN1_variables(2013)
    # variables_CN2 = generate_CN2_variables(2013)
    # values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, 2014))
    # values_CN2, formulas_CN2 = get_or_construct_data(df, variables_CN2, range(1949, 2014))

    # df_2011 = get_tidy_data(2011)
    # variables_CN1_2011 = generate_CN1_variables(2011)
    # variables_CN2_2011 = generate_CN2_variables(2011)
    # values_CN1_2011 = get_or_construct_data(df_2011, variables_CN1_2011, range(1949, 2012))[0]
    # values_CN2_2011 = get_or_construct_data(df_2011, variables_CN2_2011, range(1949, 2012))[0]

    # create_and_save_CN1(2012)  -- should no longer be done
    # test_CN1(2012)
    # values_CN1_2012, values_CN2_2012 = test_compare_sheets_to_IPP()

    # df_2012 = get_tidy_data(2012)
    # variables_CN1_2012 = generate_CN1_variables(2012)
    # values_CN1_2012 = get_or_construct_data(df_2012, variables_CN1_2012, range(1949, 2013))[0]
    # variables_CN2_2012 = generate_CN2_variables(2012)
    # values_CN2_2012 = get_or_construct_data(df_2012, variables_CN2_2012, range(1949, 2013))[0]
