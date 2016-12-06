# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 12:36:01 2015

@author: Antoine


This file is a generator of dataframe for TEE files of comptabilite nationale.
The main funtion is tee_df_generator(). It takes as argument the year of the folder (folder_year)
i.e. the year of data released by INSEE, and as optional argument, a list
of years representing the years of interest (list_years). Note that the folder (folder_year)
always contains all the tee files for all previous years since 1949. Of course, the years in list_years must be
anterior or equal to folder_year.

Other functions are:
tee_file_info : use the path and name of a file to get informations about the tee excel file
tee_file_parser: transform the excel file into a pandas dataframe
tee_folder_parser: transform all the TEE excel files in a given folder into a datafrane
"""


import logging
import os
import pandas


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.get_file_infos import file_infos


log = logging.getLogger(__name__)


# get the name of local folder for comptabilite national data
parser = Config()
cn_directory = parser.get('data', 'cn_directory')


def tee_file_parser(excelfile_name):
    infos = file_infos(excelfile_name)

    col_names_actifs = ['code', 'description', 'S1', 'S11', 'S12', 'S13', 'S14',
        'S15', 'impots', 'S2', 'biens_services', 'total']
    col_names_passifs = ['total', 'biens_services', 'S2', 'impots', 'S15', 'S14', 'S13',
        'S12', 'S11', 'S1', 'code', 'description']

    header = None
    skiprows = 0  # prviously 4
    skip_footer = 0  # previously 2 but unnecessary since cleaner
    index_col = None
    parse_cols = "A:end"

    assert os.path.exists(excelfile_name), \
        'Cannot find file {}. Use cn_dowloader to load and unzip the raw CN files'.format(excelfile_name)
    df_ea = pandas.read_excel(excelfile_name, sheetname = 1, header = header, skiprows = skiprows,
                              skip_footer = skip_footer, index_col = index_col, parse_cols = parse_cols,
                              names = col_names_actifs, na_values = ['0'])
    df_rp = pandas.read_excel(excelfile_name, sheetname = 2, header = header, skiprows = skiprows,
                              skip_footer = skip_footer, index_col = index_col, parse_cols = parse_cols,
                              names = col_names_passifs, na_values = ['0'])
    df_ea['ressources'] = False
    df_rp['ressources'] = True

    for df in [df_ea, df_rp]:
        df['year'] = int(infos['year'])
        df['version'] = infos['version']
        df['source'] = infos['source']
        df['link'] = infos['link']
        df['file_title'] = infos['title']
        df['file_name'] = infos['filename']

    result = df_ea.append(df_rp, ignore_index = True)
    return result


def tee_folder_parser(folder_year, list_years):
    assert max(list_years) <= folder_year, "the folder does not contain the year(s) demanded"
    dict_df_tee = dict()
    for year in list_years:
        excelfile_name = os.path.join(cn_directory, 'comptes_annee_{}/Tee_{}.xls'.format(folder_year, year))
        # TODO: change directory to hdf_directory as this is where is stored the big dataframe
        df = tee_file_parser(excelfile_name)
        dict_df_tee[str(year)] = df
    return dict_df_tee


def tee_df_cleaner(tee_df):
    tee_df = tee_df.drop_duplicates(inplace = False)
    tee_df = tee_df[pandas.notnull(tee_df.code)]             # if code is nan, it means it is blank line, or title
    tee_df = tee_df[pandas.notnull(tee_df.description)]
    tee_df = tee_df[tee_df['code'].str.contains(' ') == False]  # for line summing up previous lines using " + "
    return tee_df


def tee_df_tidy(df):
    list_institutions = ['S1', 'S11', 'S12', 'S13', 'S14', 'S15', 'impots', 'S2', 'biens_services', 'total']
    df = pandas.melt(df, id_vars=['code', 'ressources', 'description', 'source', 'link', 'file_name',
                                  'file_title', 'version', 'year'],
                     value_vars = list_institutions, var_name='institution')
    df = df.drop_duplicates()
    df = df.drop_duplicates((u'code', u'ressources', u'description', u'source', u'link',
       u'file_name', u'file_title', u'version', u'year', u'institution'))  # fixes pb of code P51c
    return df


def tee_df_by_year_generator(folder_year, list_years = None):
    if list_years is None:
        log.info(
            'User did not provide list of years. I will generate TEE dataframe for every year from 1949 to {}'.format(
                folder_year)
            )
        list_years = range(1949, folder_year + 1, 1)
    if type(list_years) is int:
        list_years = [list_years]
    tee_df_by_year = tee_folder_parser(folder_year, list_years)
    for key, df in tee_df_by_year.items():
        tee_df_by_year[key] = tee_df_tidy(tee_df_cleaner(df))
    return tee_df_by_year
