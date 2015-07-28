# -*- coding: utf-8 -*-


from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import cn_df_generator
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import look_many
from ipp_macro_series_parser.comptes_nationaux import cn_output


folder_year = 2013
entry_by_index_list = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
             {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'}]


df = cn_df_generator(folder_year)
df = look_many(df, entry_by_index_list)
df = cn_output.reshape_to_long_for_output(df)
cn_output.df_long_to_csv(df, 'IPP_test.csv')
