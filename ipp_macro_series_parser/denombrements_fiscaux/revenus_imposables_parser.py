# -*- coding: utf-8 -*-


import logging
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config

config_parser = Config()

xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
hdf_directory = config_parser.get('data', 'denombrements_fiscaux_hdf')


log = logging.getLogger(__name__)


def get_impot_revenu_national():
    data_frame_by_year = dict()
    for year in range(2004, 2014):
        file_path = os.path.join(xls_directory, u'revenus de {}.xls'.format(year))
        if year <= 2005:
            skiprows = 5
        elif year == 2006:
            skiprows = 4
        else:
            skiprows = 3
        data_frame = pandas.read_excel(
            file_path,
            skiprows = skiprows,
            na_values = 'n.d.',
            parse_cols = 'B:K',
            ).dropna(how = 'all', axis = 0)
        first_column = data_frame.columns[0]
        data_frame.set_index(first_column, inplace = True)
        data_frame.columns = [
            u'Nombre de foyers fiscaux',
            u'Revenu fiscal de référence des foyers fiscaux',
            u'Impôt net',
            u'Nombre de foyers fiscaux imposés',
            u'Revenu fiscal de référence des foyers fiscaux imposés',
            u'Traitements et salaires (montants)',
            u'Traitements et salaires (nombre de foyers concernés)',
            u'Retraites et pensions (montants)',
            u'Retraites et pensions (nombre de foyers concernés)',
            ]
        data_frame.drop(data_frame.index[0], inplace = True)
        data_frame.dropna(how = 'all', axis = 0, inplace = True)

        amount_columns = [
            u'Revenu fiscal de référence des foyers fiscaux',
            u'Impôt net',
            u'Revenu fiscal de référence des foyers fiscaux imposés',
            u'Traitements et salaires (montants)',
            u'Retraites et pensions (montants)'
            ]
        number_columns = [
            u'Nombre de foyers fiscaux',
            u'Nombre de foyers fiscaux imposés',
            u'Traitements et salaires (nombre de foyers concernés)',
            u'Retraites et pensions (nombre de foyers concernés)',
            ]

        if year == 2010:
            for col in number_columns:
                data_frame[col] = data_frame[col] * 1e3

            for col in amount_columns:
                data_frame[col] = data_frame[col] * 1e9

        data_frame_by_year[year] = data_frame

    total_data_frame_by_year = dict()
    for year, data_frame in data_frame_by_year.iteritems():
        data_frame = data_frame.loc['Total'].copy()
        data_frame = data_frame.reset_index(name = 'value')
        data_frame.rename(columns = {'index': 'variable'}, inplace = True)
        data_frame['year'] = year
        total_data_frame_by_year[year] = data_frame

    return pandas.concat(total_data_frame_by_year.values())


def build_excel(file_path = None):
    assert file_path is not None
    data_frame = get_impot_revenu_national()
    data_frame.to_excel(file_path)
