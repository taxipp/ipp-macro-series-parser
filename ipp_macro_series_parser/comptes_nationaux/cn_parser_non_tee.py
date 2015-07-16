# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 10:09:56 2015

@author: Antoine Arnoud
"""


import glob
import os
import pandas
import pkg_resources

from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.cn_get_file_infos import file_infos


# get the name of local folder for comptabilite national data
parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')


def file_parser(excelfile_name):
    infos = file_infos(excelfile_name)
#    if infos['tee_flag'] == 1:
#        header = None
#        skiprows = 0  # prviously 4
#        skip_footer = 0  # previously 2 but unnecessary since cleaner
#        index_col = None
#        parse_cols = "A:end"

    if infos['tee_flag'] == 0:
        header = 1
        skiprows = 0
        skip_footer = 0
        index_col = None
        parse_cols = " A:end"

    df = pandas.read_excel(excelfile_name, header = header,
                       skiprows = skiprows, skip_footer = skip_footer,
                       index_col = index_col, parse_cols = parse_cols)

    # rename first column, and trim content
    new_columns = df.columns.values
    new_columns[0] = 'code'
    new_columns[1] = 'description'
    df.columns = new_columns

    df['description'] = df['description'].str.lower()

    ressource_dummy = 0
    df['ressources'] = False
    for ind in df.index:
        if df.ix[ind]['description'] == "ressources":
            ressource_dummy = 1
        elif df.ix[ind]['description'] == "emplois":
            ressource_dummy = 0
        if ressource_dummy == 1:
            df.ix[ind, ['ressources']] = True
        else:
            df.ix[ind, ['ressources']] = False

    df['source'] = infos['source']
    df['version'] = infos['version']
    df['file_title'] = infos['title']
    df['file_name'] = infos['filename']
    df['link'] = infos['link']
    df['institution'] = infos['agent']
    return df


def df_cleaner(df):
    # drop useless lines
    df = df[pandas.notnull(df.code)]
    df = df[pandas.notnull(df.description)]
    df = df[df.code != u'']
    df = df[df.code != u' ']
    df = df[df.description != u' ']
    df = df[df.description != u'']
    df = df[df['code'].str.contains('\+') == False]
    return df


def df_tidy(df, folder_year):
    version_year = folder_year  # df['version'][0] not working
    list_years = range(1949, version_year + 1, 1)
    df = pandas.melt(df, id_vars=['code', 'ressources', 'description', 'source', 'link', 'file_name',
                                  'file_title', 'version', 'institution'],
                     value_vars = list_years, var_name='year')
    return df


def non_tee_df_generator(folder_year):
    dico = dict()
    path_to_dir = os.path.join(cn_directory, 'comptes_annee_{}'.format(folder_year), '*.xls')
    list_of_files = glob.glob(path_to_dir)
    for filename in list_of_files:
        infos = file_infos(filename)
        if infos is False:
            continue
        if infos['tee_flag'] == 1:  # = tee file
            continue

        df = file_parser(filename)
        df = df_cleaner(df)
        df = df_tidy(df, int(infos['version']))
        dico[infos['filename']] = df
    return dico
