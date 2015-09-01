# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 10:09:56 2015

@author: Antoine Arnoud
"""


import glob
import logging
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.cn_get_file_infos import file_infos


log = logging.getLogger(__name__)


# get the name of local folder for comptabilite national data
parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')


def file_parser(excelfile_name):
    log.info('Parsing {}'.format(excelfile_name))
    infos = file_infos(excelfile_name)
    if infos['tee_flag'] == 0:
        header = 1
        skiprows = 0
        skip_footer = 0
        index_col = None
        parse_cols = " A:end"

    df = pandas.read_excel(excelfile_name, header = header, skiprows = skiprows, skip_footer = skip_footer,
       index_col = index_col, parse_cols = parse_cols)
    print df[:10]
    # rename first column, and trim content
    new_columns = df.columns.values
    print new_columns
    new_columns[0] = 'code'
    new_columns[1] = 'description'
    df.columns = new_columns
    print df.code.dtype
    df['code'] = df['code'].astype('str')
    df['description'] = df['description'].str.lower()
    print df[:10]

    ressource_dummy = 0
    df['ressources'] = False
    if infos['filename'] == 't_7601':
        for ind in df.index:
            if df.ix[ind]['description'] == u"à destination du reste du monde":
                ressource_dummy = 1
            elif df.ix[ind]['description'] == u"en provenance du reste du monde":
                ressource_dummy = 0
            if ressource_dummy == 1:
                df.ix[ind, ['ressources']] = True
            else:
                df.ix[ind, ['ressources']] = False
    else:
        for ind in df.index:
            if df.ix[ind]['description'] == "ressources":
                ressource_dummy = 1
            elif df.ix[ind]['description'] == "emplois":
                ressource_dummy = 0
            if ressource_dummy == 1:
                df.ix[ind, ['ressources']] = True
            else:
                df.ix[ind, ['ressources']] = False

    if infos['filename'] == 't_1115':
        for ind in df.index:
            df.ix[ind, ['code']] = u'no code'

    df['source'] = infos['source']
    df['version'] = infos['version']  # .copy()
    df['file_title'] = infos['title']  # .copy()
    df['file_name'] = infos['filename']  # .copy()
    df['link'] = infos['link']  # .copy()
    df['institution'] = infos['agent']  # .copy()
    return df


def df_cleaner(df):
    # drop useless lines
    assert not df.empty
    assert len(df) > 0
    df = df[pandas.notnull(df.code)]
    df = df[pandas.notnull(df.description)]
    df = df[df.code != u'']
    df = df[df.code != u' ']
    df = df[df.description != u' ']
    df = df[df.description != u'']
    df = df[~df['code'].str.contains('\+')]
    df = df.drop_duplicates()
    df = df[df['code'] != 'nan']
    is_useless = df['value'].isnull() & df['code'].isin(['nan', 'no code'])
    df = df[~is_useless]
    return df


def df_tidy(df, folder_year):
    version_year = folder_year  # df['version'][0] not working
    list_years = range(1949, version_year + 1, 1)
    df = pandas.melt(
        df,
        id_vars = ['code', 'ressources', 'description', 'source', 'link', 'file_name',
            'file_title', 'version', 'institution'],
        value_vars = list_years,
        var_name = 'year'
        )
    df = df.drop_duplicates()
    return df


def non_tee_df_by_filename_generator(folder_year):
    non_tee_df_by_filename = dict()
    directory_path = os.path.join(cn_directory, 'comptes_annee_{}'.format(folder_year))
    assert os.path.exists(directory_path), '{} does not exist. Use cn_downloader to create it'.format(
        directory_path)
    list_of_files = glob.glob(os.path.join(directory_path, '*.xls'))
    for filename in list_of_files:
        assert os.path.exists(filename)
        infos = file_infos(filename)
        if infos is False:
            continue
        if infos['tee_flag'] == 1:  # = tee file
            continue

        df = file_parser(filename)
        df = df_tidy(df, int(infos['version']))
        df = df_cleaner(df)
        non_tee_df_by_filename[infos['filename']] = df
    return non_tee_df_by_filename
