# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 10:09:56 2015

@author: Antoine Arnoud
"""

import pandas
import os

# user enters the last year to be considered (download zip from this year, with data on past years too)
# last_year = raw_input("Please enter most recent date")
last_year = "2013"
years_list = range(1949, int(last_year) + 1, 1)

# user chooses the folder containing ther excel files from INSEE
# root = Tkinter.Tk()
# dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
# if len(dirname) > 0:
#    print "You chose %s" % dirname
dirname = "C:/Users/Antoine/Documents/GitHub/ipp/"

# File PIB (INSEE) : t_1101
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_1101.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0,
                       skip_footer = 4, index_col = None, parse_cols = "B:end")
df['source'] = 'INSEE Compta Nat PIB File t_1101.xls'

# rename first column, and trim content
df.rename(columns = {'Unnamed: 0': 'description'}, inplace=True)
# longer code: new_columns = df.columns.values ;  new_columns[0] = 'description'; df.columns = new_columns
df['description'] = df['description'].map(lambda x: x.strip().lower())

# create new column with name of variable (not very useful)
df['name'] = df['description'].map(lambda x: x.strip().split(' ', 1)[0])

# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.description != '']

# change few names
# add fbcf (formation brut de capital fixe) the second time "administrations publiques" and "menages" appear.
df.ix[df.duplicated('description') == True, ['description']] = df['description'].map(lambda x: x + ' fbcf')
# better names
df.ix[df.description == u'produit intérieur brut', ['name']] = 'pib'
df.ix[df.description == u'total', ['name']] = 'ressources'
df.ix[df.description == u'dépenses de consommation finale', ['name']] = 'consommation_finale'
df.ix[df.description == u'ménages', ['name']] = 'conso_menages'
df.ix[df.description == u'administrations publiques', ['name']] = 'conso_pub'
df.ix[df.description == u'institutions sans but lucratif au service des ménages', ['name']] = 'conso_isbl'
df.ix[df.description == u'formation brute de capital fixe', ['name']] = 'fbcf'
df.ix[df.description == u'sociétés et entreprises individuelles financières', ['name']] = 'fbcf_finance'
df.ix[df.description == u'sociétés et entreprises individuelles non financières', ['name']] = 'fbcf_non_finance'
df.ix[df.description == u'ménages hors entrepreneurs individuels', ['name']] = 'fbcf_menages'
df.ix[df.description == u'administrations publiques fbcf', ['name']] = 'fbcf_pub'
df.ix[df.description == u'institutions sans but lucratif au service des ménages fbcf', ['name']] = 'fbcf_isbl'
df.ix[df.description == u'variation de stocks', ['name']] = 'variation_stocks'
df.ix[df.description == u'demande intérieure hors stocks', ['name']] = 'demande_int_hors_stocks'
df.ix[df.description == u'demande intérieure y compris stocks', ['name']] = 'demand_int_avec_stocks'

# tidy the table
df_t_1101 = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'],
                        value_vars = years_list, var_name='year')


# File VA (INSEE): t_1105
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_1105.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0,
                       skip_footer = 4, index_col = None, parse_cols = "B:end")
df['source'] = 'INSEE Compta Nat PIB File t_1105.xls'

# rename first column, and trim content
df.rename(columns={'Unnamed: 0': 'description'}, inplace=True)
df['description'] = df['description'].map(lambda x: x.strip().lower())

# create new column with name of variable
df['name'] = ['pib_production', 'va', 'impots_produits', 'subventions_produits',
'pib_demande', 'conso_finale', 'fbc', 'exportations', 'importations', 'pib_revenus',
'salaires', 'ebe_rmb', 'impots_production_et_importations', 'subventions']

# tidy the table
df_t_1105 = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'],
                        value_vars = years_list, var_name='year')


# File PIB (INSEE): t_1106
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_1106.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0,
                       skip_footer = 4, index_col = None, parse_cols = "B:end")
df['source'] = 'INSEE Compta Nat VA File t_1106.xls'

# rename first column, and trim content
df.rename(columns={'Unnamed: 0': 'description'}, inplace=True)
df['description'] = df['description'].map(lambda x: x.strip().lower())

# create new column with name of variable
df['code'] = ['S11', 'S12', 'S13', 'S14', 'S15', 'S1_VA']

# tidy the table
df_t_1106 = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'],
                        value_vars = years_list, var_name='year')


# File VA (INSEE): t_1107
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_1107.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0,
                       skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_1107.xls'

# rename first column, and trim content
new_columns = df.columns.values
df.rename(columns={'Unnamed: 0': 'code', 'Unnamed: 1': 'description'}, inplace=True)
df['description'] = df['description'].map(lambda x: x.strip().lower())

# create new column with code name of variable
df['name'] = ['VA_brute', 'salaires', 'salaire_bruts', 'cotisations_employeurs',
'impots_production', 'subventions_exploitation', 'ebe', 'rmb_revenu_mixte_brut']

# tidy the table
df_t_1107 = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'],
                        value_vars = years_list, var_name='year')

# File Emploi (INSEE): t_1100 and t_1109
#############################################################################

# File Capital (INSEE): t_1110 and t_1111 (net) and t_1112 (consommation de capital)
#############################################################################


# File VA (INSEE): t_1115
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_1115.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0,
                       skip_footer = 7, index_col = None, parse_cols = "B:end")
df['source'] = 'INSEE Compta Nat VA File t_1115.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'description'
df.columns = new_columns

# create new column with code name of variable
df['name'] = ['population', 'pib', 'revenu_national', 'pib_2010eur', 'revenu_national_2010eur', 'pib_par_hab', 'revenue_national_par_hab', 'pib_par_hab_2010eur', 'revenu_national_par_hab_2010eur']

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_1115 = df_melted


# File VA (INSEE): t_7101
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_7101.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0, skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_7101.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'code'
new_columns[1] = 'description'
df.columns = new_columns

# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.code != u'']
df = df[df.code != u' ']
df = df[pandas.isnull(df.code) != 1]

# creat column ressources or emplois:
df['ressources']   = [True, True, True, False, False, True, False, False,False,False,False,False,False,False,False,False, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, True, True, True, True, True, True, True, False, False, False, False, False]

# create new column with code name of variable
# df['name'] =

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_7101 = df_melted



# File VA (INSEE): t_7201
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_7201.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0, skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_7201.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'code'
new_columns[1] = 'description'
df.columns = new_columns

# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.code != u'']
df = df[df.code != u' ']
df = df[pandas.isnull(df.code) != 1]

# creat column ressources or emplois:
df['ressources']   = [True, True, True, False, False, True, False, False,False,False,False,False,False,False,False,False, True, True, True, True, True, True, True, True, True,  False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, False, True, True, True, True, True, True, True, False, False, False, False, False]

# create new column with code name of variable
# df['name'] =

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_7201 = df_melted


# File VA (INSEE): t_7301
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_7301.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0, skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_7301.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'code'
new_columns[1] = 'description'
df.columns = new_columns

# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.code != u'']
df = df[df.code != u' ']
df = df[pandas.isnull(df.code) != 1]

# creat column ressources or emplois:
col = [True] * 4 + [False] * 2 + [True] + [False] * 10 + [True] * 24 + [False] * 9 + [True] * 21 + [False] * 20 + [True] + [False] * 4 + [True] * 9 + [False] * 5 + [True] + [False] * 4 + [True] + [False] * 2
df['ressources'] = col

# create new column with code name of variable
# df['name'] =

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_7301 = df_melted


# File VA (INSEE): t_7401
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_7401.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0, skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_7401.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'code'
new_columns[1] = 'description'
df.columns = new_columns

# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.code != u'']
df = df[df.code != u' ']
df = df[pandas.isnull(df.code) != 1]

# creat column ressources or emplois:
col = [True] * 3  + [False] * 2 + [True] + [False] * 12 + [True] * 13 + [False] * 4 + [True] * 10 + [False] * 14 + [True] * 1 + [False] * 2 + [True] * 8 + [False] * 6 + [True] * 4 + [False] * 1 + [True] + [False] * 2
df['ressources'] = col

# create new column with code name of variable
# df['name'] =

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_7401 = df_melted


# File VA (INSEE): t_7601
#############################################################################
# define path to the excel file, open copy into DataFrame (needs pip install xlrd)
excelfile_name = dirname + "comptes_annee_{}/t_7601.xls".format(last_year)
df = pandas.read_excel(excelfile_name, header = 1, skiprows = 0, skip_footer = 4, index_col = None, parse_cols = "A:end")
df['source'] = 'INSEE Compta Nat VA File t_7601.xls'

# rename first column, and trim content
new_columns = df.columns.values
new_columns[0] = 'code'
new_columns[1] = 'description'
df.columns = new_columns


# drop useless lines
df = df[df.description != 'ressources']
df = df[df.description != 'emplois']
df = df[df.code != u'']
df = df[df.code != u' ']
df = df[pandas.isnull(df.code) != 1]

# creat column ressources or emplois:
col = [False] * 1 + [True] * 1 + [None] + [False] * 27 + [True] * 32 + [None]
df['ressources'] = col

# create new column with code name of variable
# df['name'] =x

# tidy the table
df_melted = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'], value_vars = years_list, var_name='year')
df_t_7601 = df_melted

#
#
#
#
#
#
#
#
#
#
#

## File TEE (INSEE)
##############################################################################
dict_df_tee_actifs = dict()
dict_df_tee_passifs = dict()

for annee in range(1949, int(last_year) + 1):
    excelfile_name = dirname + "comptes_annee_{}/Tee_{}.xls".format(last_year, annee)

# actifs
    col_names = ['code', 'description', 'S1', 'S11', 'S12', 'S13', 'S14', 'S15', 'impots', 'S2', 'biens_services', 'total']
    df = pandas.read_excel(excelfile_name, sheetname ='EA_{}'.format(annee), header = None, skiprows = 4, skip_footer = 2, index_col = None, parse_cols = "A:end", names = col_names)
    df['source'] = 'INSEE Compta Nat TEE File'
    df['year'] = annee
    df.ix[df.description == u'Total des actifs', ['code']] = 'total_actifs'
    # df['name'] = ""

    # drop useless lines
    df = df[pandas.isnull(df.code) != 1]             # if code is nan, it means it is blank line, or title
    df = df[df['code'].str.contains(' ') == False]   # if there is space, means that it is title, not code
    df = df.drop_duplicates('code')                  # drop duplicates : when code is the same
    df = df.set_index('code')

    dict_df_tee_actifs[annee] = df

# passifs
    col_names = ['total', 'biens_services', 'S2', 'impots', 'S15', 'S14', 'S13', 'S12', 'S11', 'S1', 'code', 'description']
    df = pandas.read_excel(excelfile_name, sheetname ='RP_{}'.format(annee), header = None, skiprows = 4, skip_footer = 2, index_col = None, parse_cols = "A:end", names = col_names)
    df['source'] = 'INSEE Compta Nat TEE File'
    df['year'] = annee
    df.ix[df.description == u'Total des passifs et valeur nette', ['code']] = 'total_passifs'

    # drop useless lines
    df = df[pandas.isnull(df.code) != 1]             # if code is nan, it means it is blank line, or title
    df = df[df['code'].str.contains(' ') == False]   # if there is space, means that it is title, not code
    df = df.drop_duplicates('code')                  # drop duplicates : when code is the same! ATTENTION: some have same code but are different things
    df = df.set_index('code')

    dict_df_tee_passifs[annee] = df


# builds up the output dataframe

# revenu national depuis 1949 avec description
df = df_t_1115[df_t_1115['name'] == 'revenu_national']
df = df.loc[:, ['year', 'value']]
df = df.sort('year', ascending = 0)
df.rename(columns={'year': 'annee', 'value': 'Revenu national (milliards EUR)'}, inplace=True)


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
