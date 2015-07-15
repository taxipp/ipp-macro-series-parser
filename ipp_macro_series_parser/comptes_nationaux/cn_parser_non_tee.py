# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 10:09:56 2015

@author: Antoine Arnoud
"""


import pandas
import os
import glob


dirname = "C:/Users/Antoine/Documents/data_aggregates/"
year = 2013
excelfile_name = dirname + "comptes_annee_{}/t_7101.xls".format(year)


def file_parameters(excelfile_name):
    filename = os.path.splitext(excelfile_name)[0]
    filename = os.path.split(excelfile_name)[1].split('.')[0]
    filename = filename.lower()
    print 'this is the filename: ' + filename

    file_source = 'INSEE Comptabilite Nationale'
    file_source_link = 'http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_{}.zip'.format(year)
    file_zip_year = os.path.dirname(excelfile_name)

    if filename.startswith('tee'):
        annee = str(filename[-4:])
        actor = 'economie'  # (societes non financieres)
        title = 'TEE ' + str(annee)
        data_type = 1  # 'tee'
        file_source = 'INSEE Compta Nat ' + filename
    else:
        header = 1
        skiprows = 0
        skip_footer = 0
        index_col = None
        parse_cols = " A:end"
        annee = 'all'
        data_type = 0  # 'not tee'
        skip = 0

    if filename == 't_7101':
        actor = 'S11'  # (societes non financieres)
        title = 'Compte des societes non financieres'
    elif filename == 't_7201':
        actor = 'S12'  # (societes financieres)
        title = 'Compte des societes non financieres'
    elif filename == 't_7301':
        actor = 'S13'  # (administrations publiques)
        title = 'Compte des administrations puliques'
    elif filename == 't_7401':
        actor = 'S14'  # (menages)
        title = 'Compte des menages'
    elif filename == 't_7501':
        actor = 'S15'  # (isbl)
        title = 'Compte des institutions sans but lucratif au service des menages'
    elif filename == 't_7601':
        actor = 'S2'  # (reste du monde)
        title = 'Operations avec le reste du monde'

    # elif filename == 't_3101':
    #    actor = 'S13'  # (administrations publiques)
    #    title = 'Dette des administrations publiques (S13) au sens de Maastricht et sa répartition par sous-secteur'
    # elif filename == 't_3201':
    #   actor = 'S13'  # (administrations publiques)
    #    title = 'Dette et recettes des administrations publiques'

    else:
        parameters = False
        skip = 1

    if skip == 0:
        parameters = {'actor': actor,
                      'title': title,
                      'annee': annee,
                      'filename': filename,
                      'header': header,
                      'skiprows': skiprows,
                      'skip_footer': skip_footer,
                      'index_col': index_col,
                      'parse_cols': parse_cols,
                      'data_type': data_type,
                      'source': file_source,
                      'link': file_source_link,
                      'version': file_zip_year
                      }
    return parameters


def file_parser(excelfile_name):
    parameters = file_parameters(excelfile_name)
    df = pandas.read_excel(excelfile_name, header = parameters['header'],
                       skiprows = parameters['skiprows'], skip_footer = parameters['skip_footer'],
                       index_col = parameters['index_col'], parse_cols = parameters['parse_cols'])

    # rename first column, and trim content
    new_columns = df.columns.values
    new_columns[0] = 'code'
    new_columns[1] = 'description'
    df.columns = new_columns
    df['source'] = parameters['source']
    df['version'] = parameters['version']
    return df


def df_cleaner(df):
    # df['description'] = df['description'].astype(str)
    df['description'] = df['description'].str.lower()
    ressource_dummy = 0
    df['ressources'] = False
    for ind in df.index:
        if df.ix[ind]['description'] == "ressources":
            ressource_dummy = 1
        if df.ix[ind]['description'] == "emplois":
            ressource_dummy = 0
        if ressource_dummy == 1:
            df.ix[ind, ['ressources']] = True
        else:
            df.ix[ind, ['ressources']] = False
    # drop useless lines
    df = df[pandas.notnull(df.code)]
    df = df[pandas.notnull(df.description)]
    df = df[df.code != u'']
    df = df[df.code != u' ']
    df = df[df.description != u' ']
    df = df[df.description != u'']
    df = df[df['code'].str.contains('\+') == False]
    return df


def df_tidy(df):
    version_year = folder_year  # df['version'][0] not working
    list_years = range(1949, version_year + 1, 1)
    df = pandas.melt(df, id_vars=['name', 'code', 'ressources', 'description', 'source'],
                     value_vars = list_years, var_name='year')
    return df


# TO DO BELOW
def df_generator(folder_year):
    dico = dict()
    # dirname =
#    scrptPth = os.path.dirname(os.path.realpath(__file__))  # gives real path
#    for file in os.listdir(scrptPth):  # instead of for filnames in os.listdir()
#        with open(os.path.joim(scrptPth, file)) as filename:
#            # if not os.path.isfile(filename):
#            # continue
    path_to_dir = dirname + '/comptes_annee_{}/*.xls'.format(folder_year)
    list_of_files = glob.glob(path_to_dir)
    for filename in list_of_files:
        parameters = file_parameters(filename)
        if parameters is False:
            continue
        if parameters['data_type'] == 1:  # = tee file
            print 'tee file'
            continue

        df = file_parser(filename)
        df = df_cleaner(df)
        df = df_tidy(df)
        dico[parameters['filename']] = df
    return dico


df = df_generator(2013)


# test:
folder_year = 2013
path_to_dir = dirname + 'comptes_annee_{}/*.xls'.format(folder_year)
list_of_files = glob.glob(path_to_dir)









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
