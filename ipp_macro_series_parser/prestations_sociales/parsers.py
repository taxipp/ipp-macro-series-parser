#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os
import pandas as pd


"""Parse dépenses and béénficiaires of presattaions sociales to produce the dataframe stored in a HDF5 file
"""


from ipp_macro_series_parser.config import Config

log = logging.getLogger(__name__)

parser = Config()
prestations_sociales_directory = parser.get('data', 'prestations_sociales_directory')


def build_data_frame(section):
    assert section in ['beneficiaires', 'depenses']

    directory = os.path.join(
        prestations_sociales_directory,
        'les-{}-tous-regimes-de-prestations-familiales-et-sociales'.format(
            section
            ),
        )
    prefix = 'DepTR' if section == 'depenses' else 'BenTR'

    filenames = [filename for filename in os.listdir(directory) if filename.startswith(prefix)]

    result_data_frame = None
    for filename in sorted(filenames):
        year = filename[5:5 + 4]
        assert year.startswith('19') or year.startswith('20')
        year = int(year)
        file_path = os.path.join(directory, filename)
        log.info('Parsing {} data from year {} using {}'.format(section, year, file_path))
        data_frame = pd.read_csv(file_path, sep = ';', decimal = ',')
        data_frame.dropna(axis = 1, inplace = True, how = 'all')  # Remove NA columns
        columns_stripped = [
            column.replace(' ', '')
            for column in data_frame.columns
            ]
        new_columns = [
            column[:-5]
            if column.endswith(str(year))
            else column
            for column in columns_stripped
            ]
        data_frame.columns = new_columns
        data_frame['year'] = int(year)
        data_frame = pd.melt(data_frame, id_vars = ['year', 'Prestations'])
        result_data_frame = data_frame if result_data_frame is None else result_data_frame.merge(
            data_frame, how = 'outer')

    result_data_frame.year = result_data_frame.year.astype(int)
    return result_data_frame


def create_prestations_sociales_data_frames():
    store = pd.HDFStore(os.path.join(
        prestations_sociales_directory,
        'prestations_sociales.h5'
        ))
    for section in ['beneficiaires', 'depenses']:
        data_frame = build_data_frame(section)
        store[section] = data_frame


def build_histo_data_frames():
    directory = os.path.join(
        prestations_sociales_directory,
        'xls',
        )
    file_path = os.path.join(directory, u"bénéficiaire_tousrégimes2015.xls")
    # file_path = os.path(directory, u"histo_benef_presta.xls")
    # file_path = os.path(directory, u"histo_dépenses_tousrégimes")
    data_frame = pd.read_excel(file_path)
