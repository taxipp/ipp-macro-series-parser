# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 12:36:01 2015

@author: Antoine
"""

import pandas
import os


dirname = "C:/Users/Antoine/Documents/data_aggregates/"


def tee_file_info(excelfile_name):
    # return 'INSEE Comptabilite Nationale' + os.path.splitext(excelfile_name)[0]
    filename = os.path.splitext(excelfile_name)[0]
    year = filename[-4:]
    file_source = 'INSEE Comptabilite Nationale'
    file_source_link = 'http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_{}.zip'.format(year)
    file_zip_year = os.path.dirname(excelfile_name)
    return {'source': file_source, 'link': file_source_link, 'version': file_zip_year, 'year': year}


def tee_file_parser(excelfile_name):
    col_names_actifs = ['code', 'description', 'S1', 'S11', 'S12', 'S13', 'S14',
        'S15', 'impots', 'S2', 'biens_services', 'total']
    col_names_passifs = ['total', 'biens_services', 'S2', 'impots', 'S15', 'S14', 'S13',
        'S12', 'S11', 'S1', 'code', 'description']

    header = None
    skiprows = 0  # prviously 4
    skip_footer = 0  # previously 2 but unnecessary since cleaner
    index_col = None
    parse_cols = "A:end"

    df_ea = pandas.read_excel(excelfile_name, sheetname = 1, header = header,
                              skiprows = skiprows, skip_footer = skip_footer,
                              index_col = index_col, parse_cols = parse_cols,
                              names = col_names_actifs)
    df_rp = pandas.read_excel(excelfile_name, sheetname = 2, header = header,
                              skiprows = skiprows, skip_footer = skip_footer,
                              index_col = index_col, parse_cols = parse_cols,
                              names = col_names_passifs)
    df_ea['ressources'] = True
    df_rp['ressources'] = False

    for df in [df_ea, df_rp]:
        df['year'] = tee_file_info(excelfile_name)['year']
        df['version'] = tee_file_info(excelfile_name)['version']
        df['source'] = tee_file_info(excelfile_name)['link']
        # df['source'] = file_source(excelfile_name)
    result = df_ea.append(df_rp, ignore_index = True)
    return result


def tee_folder_parser(folder_year, list_years):  # last year of data
    assert max(list_years) <= folder_year, "the folder does not contain the year(s) demanded"
    dict_df_tee = dict()
    for year in list_years:
        excelfile_name = dirname + "comptes_annee_{}/Tee_{}.xls".format(folder_year, year)
        df = tee_file_parser(excelfile_name)
        dict_df_tee[year] = df
    return dict_df_tee


def tee_df_cleaner(tee_df):
    tee_df = tee_df.drop_duplicates()
    tee_df = tee_df[pandas.notnull(tee_df.code)]             # if code is nan, it means it is blank line, or title
    tee_df = tee_df[pandas.notnull(tee_df.description)]     # same as above
    tee_df = tee_df[tee_df['code'].str.contains(' ') == False]   # at least on eline sums up two previous lines with space after + so will be deleted
    return tee_df


def tee_df_generator(folder_year, list_years = None):
    if list_years is None:
        print 'The user did not provide a list of years. I will generate all years from 1949 up to ', folder_year
        list_years = range(1949, folder_year + 1, 1)
    if type(list_years) is int:
        list_years = [list_years]
    dico = tee_folder_parser(folder_year, list_years)
    for year in list_years:
        dico[year] = tee_df_cleaner(dico[year])
    return dico
