# -*- coding: utf-8 -*-

import os
import pkg_resources
from ipp_macro_series_parser.config import Config

from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import cn_df_generator
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import look_many
from ipp_macro_series_parser.comptes_nationaux import cn_output
from ipp_macro_series_parser.comptes_nationaux import cn_sheets_lists

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')


folder_year = 2013
entry_by_index_list = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
             {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'},
             {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': None}]
df = cn_df_generator(folder_year)
df1 = look_many(df, entry_by_index_list)
df2 = cn_output.reshape_to_long_for_output(df1)
cn_output.df_long_to_csv(df2, 'IPP_test.csv')


CN1 = cn_output.output_for_sheets(
    cn_sheets_lists.list_CN1, 2013,
    os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.txt')
    )
