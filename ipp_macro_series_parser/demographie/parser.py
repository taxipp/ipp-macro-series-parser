# -*- coding: utf-8 -*-


# TAXIPP -- A French microsimulation model
# By: IPP <taxipp@ipp.eu>
#
# Copyright (C) 2012, 2013, 2014, 2015 IPP
# https://github.com/taxipp
#
# This file is part of TAXIPP.
#
# TAXIPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# TAXIPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import pandas
import pkg_resources
from ipp_macro_series_parser.config import Config

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
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
