# -*- coding: utf-8 -*-


import logging
import os
import pandas
import pkg_resources
from ipp_macro_series_parser.config import Config

config_parser = Config()
xls_directory = os.path.join(config_parser.get('data', 'demographie_directory'), 'xls')


log = logging.getLogger(__name__)


def create_demographie_data_frame():
    data_frame = pandas.DataFrame()
    for year in range(1999, 2015 + 1):
        file_path = os.path.join(xls_directory, u'pyramide-des-ages-{}.xls'.format(year))
        skiprows = 5 - (year == 1999)
        parse_cols = "A:E"
        slice_start = 0
        slice_end = 101
        sheetname = 'France'

        if year <= 2010:
            sheetnames = ['France', u'France métropolitaine']
        elif year == 2011:
            sheetnames = ['{} France'.format(year), u"{} métropole".format(year)]
        else:
            sheetnames = ['Pyramide {} France'.format(year), u'Pyramide {} métropole'.format(year)]

        for sheetname in sheetnames:
            try:
                df = pandas.read_excel(
                    file_path,
                    sheetname = sheetname,
                    skiprows = skiprows,
                    parse_cols = parse_cols).iloc[slice_start:slice_end].copy()
                df['year'] = year
                if sheetname in ['France', u'France métropolitaine']:
                    df['champ'] = sheetname
                else:
                    df['champ'] = u'France métropolitaine' if u'métropole' in sheetname else 'France'
                # All column name on one line
                remove_cr = dict(
                    (column, column.replace(u"\n", " ").replace("  ", " ")) for column in df.columns)
                df.rename(columns = remove_cr, inplace = True)
                # Femmes _> Nombre de femmes etc
                df.rename(columns = dict(
                    Femmes = "Nombre de femmes",
                    Hommes = "Nombre d'hommes"), inplace = True)
                data_frame = pandas.concat((data_frame, df))
                del df
            except Exception, e:
                print year
                print sheetname
                raise e

    return pandas.melt(data_frame, id_vars = ['year', 'champ', u'Âge révolu', u'Année de naissance'])
