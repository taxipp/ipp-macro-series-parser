# -*- coding: utf-8 -*-


import pandas
import os
import pkg_resources
from pandas.util.testing import assert_frame_equal

from ipp_macro_series_parser.comptes_nationaux import parser_tee
from ipp_macro_series_parser.comptes_nationaux import parser_non_tee
from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import get_or_construct_value, get_or_construct_data
from ipp_macro_series_parser.comptes_nationaux.sheets_lists import generate_CN1_variables
from ipp_macro_series_parser.comptes_nationaux.cn_test import read_CN1, read_profits_societes, create_dict_profits

from ipp_macro_series_parser.config import Config
parser = Config()
cn_csv = parser.get('data', 'cn_csv_directory')
tests_data = os.path.join(
    pkg_resources.get_distribution('ipp-macro-series-parser').location,
    'ipp_macro_series_parser/tests/data')


def test_duplicate_tee_df():
    folder_year = 2013
    tee_df_by_year = parser_tee.tee_df_by_year_generator(folder_year)
    for key, df in tee_df_by_year.items():
        for element in df.duplicated():
            assert element == 0, "There are duplicate rows in TEE " + key + ", in folder: comptes_annees " + folder_year


def test_duplicate_non_tee_df():
    folder_year = 2013
    non_tee_df_by_filename = parser_non_tee.non_tee_df_by_filename_generator(folder_year)
    for key, df in non_tee_df_by_filename.items():
        for element in df.duplicated():
            assert element == 0, "There are duplicate rows in " + key + ", in folder: comptes_annees " + folder_year


def test_cn_parser_main_1():
    try:
        get_comptes_nationaux_data(2013)
        result = True
    except:
        result = False
    assert result, "The final table of comptabilite nationale could not be generated in cn_parser_main"


def test_cn_parser_main_2():
    df = get_comptes_nationaux_data(2013)
    for element in df.duplicated():
        assert element == 0, "The final table of comptabilite nationale contains duplicates"


def test_get_or_construct_value1():
    folder_year = 2013
    overall_dict = {
        'pib': {
            'code': 'B1g/PIB',
            'institution': 'S1',
            'description': 'PIB'
            },
        'complicated_var': {
            'code': None,
            'description': 'PIB0',
            'formula': '2*pib - pib - pib + pib*pib - pib^2'
            },
        'very_complicated_var': {
            'code': None,
            'description': 'PIB0',
            'formula': 'complicated_var^2'
            }
        }
    df = get_comptes_nationaux_data(folder_year)

    variable_name = 'pib'
    pib_serie = get_or_construct_value(df, variable_name, overall_dict, years = range(1949, 2014))
    variable_name = 'very_complicated_var'
    serie, formula = get_or_construct_value(df, variable_name, overall_dict, years = range(1949, 2014))
    assert isinstance(serie, pandas.DataFrame)
    assert serie.columns == [variable_name]
    assert all(serie[variable_name] == 0), serie[variable_name]


def test_get_or_construct_data_profits():  # copied on the one in cn_test
    df = get_comptes_nationaux_data(2013)

    values_profits_societes_target = read_profits_societes()
    dict_profits = create_dict_profits()
    values_profits_societes = get_or_construct_data(df, dict_profits)[0]

    assert_frame_equal(values_profits_societes, values_profits_societes_target)


def test_get_or_construct_data_CN1():  # copied on the one in cn_test
    df = get_comptes_nationaux_data(2013)
    values_CN1_target = read_CN1(2013)
    variables_CN1 = generate_CN1_variables(2013)
    values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, 2014))
    print values_CN1.columns
    print values_CN1_target.columns
    assert_frame_equal(values_CN1, values_CN1_target)
