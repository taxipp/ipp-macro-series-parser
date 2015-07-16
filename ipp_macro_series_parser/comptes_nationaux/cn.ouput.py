# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:13:25 2015

@author: Antoine
"""



# builds up the output dataframe

# revenu national depuis 1949 avec description
df = df_t_1115[df_t_1115['name'] == 'revenu_national']
df = df.loc[:, ['year', 'value']]
df = df.sort('year', ascending = 0)
df.rename(columns={'year': 'year', 'value': 'Revenu national (milliards EUR)'}, inplace=True)


# create the excel table
def save_xls(df, output_filename):  # needs to pip install xlsxwriter as well as xlwt ?
    writer = pandas.ExcelWriter(output_filename + '.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index = None)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def save_several_xls(list_dfs, xls_path):
    writer = pandas.ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer, 'sheet%s' % n)
    writer.save()


save_xls(df, 'tableau_compta_nat_{}'.format(last_year))
os.system('start excel.exe tableau_compta_nat_{}.xlsx'.format(last_year))
# df_list = dict_df_tee_actifs.values()
# save_several_xls(df_list, 'df_list.xlsx')

# print df_melted.loc[2, 'value']

# print pandas.ExcelFile(excelfile_name).sheet_names
# df = excelfile.parse("Sheet 1")
# print df
# print df.head
