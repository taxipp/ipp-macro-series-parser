# -*- coding: utf-8 -*-


import os
import pkg_resources

from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import get_or_construct_data
from ipp_macro_series_parser.comptes_nationaux.sheets_lists import variables_CN1, variables_CN2

parser = Config()
cn_directory = parser.get('data', 'cn_directory')
cn_hdf = parser.get('data', 'cn_hdf_directory')
cn_csv = parser.get('data', 'cn_csv_directory')
tests_directory = parser.get('data', 'tests_directory')

tests_data = os.path.join(
    pkg_resources.get_distribution('ipp-macro-series-parser').location,
    'ipp_macro_series_parser/tests/data')

df = get_comptes_nationaux_data(2013)

values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, 2014))
values_CN2, formulas_CN2 = get_or_construct_data(df, variables_CN2, range(1949, 2014))
