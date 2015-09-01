# -*- coding: utf-8 -*-


import pandas


from ipp_macro_series_parser.comptes_nationaux import cn_parser_tee
from ipp_macro_series_parser.comptes_nationaux import cn_parser_non_tee
from ipp_macro_series_parser.comptes_nationaux import cn_parser_main
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import get_or_construct_value


def test_duplicate_tee_df():
    folder_year = 2013
    tee_df_by_year = cn_parser_tee.tee_df_by_year_generator(folder_year)
    for key, df in tee_df_by_year.items():
        for element in df.duplicated():
            assert element == 0, "There are duplicate rows in TEE " + key + ", in folder: comptes_annees " + folder_year


def test_duplicate_non_tee_df():
    folder_year = 2013
    non_tee_df_by_filename = cn_parser_non_tee.non_tee_df_by_filename_generator(folder_year)
    for key, df in non_tee_df_by_filename.items():
        for element in df.duplicated():
            assert element == 0, "There are duplicate rows in " + key + ", in folder: comptes_annees " + folder_year


def test_cn_main1():
    try:
        cn_parser_main.get_comptes_nationaux_data(2013)
        result = True
    except:
        result = False
    assert result, "The final table of comptabilite nationale could not be generated in cn_main"


def test_cn_main2():
    df = cn_parser_main.get_comptes_nationaux_data(2013)
    for element in df.duplicated():
        assert element == 0, "The final table of comptabilite nationale contains duplicates"


def test_get_or_construct_value():

    folder_year = 2013

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
    df = cn_parser_main.get_comptes_nationaux_data(folder_year)
    serie, formula = get_or_construct_value(df, variable_name, overall_dict, years = range(1949, 2014))
    assert isinstance(serie, pandas.DataFrame)
    assert serie.columns == [variable_name]
    assert all(serie[variable_name] == 0)
