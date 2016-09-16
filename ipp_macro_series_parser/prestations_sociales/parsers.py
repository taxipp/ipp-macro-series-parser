#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os
import padnas as pd
import pkg_resources

"""Parse dépenses and béénficiaires of presattaions sociales to produce the dataframe stored in a HDF5 file
"""


from ipp_macro_series_parser.config import Config

log = logging.getLogger(__name__)


parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
prestations_sociales_directory = parser.get('data', 'prestations_sociales_directory')


def create_depenses_data_frame():
    pass


def create_beneficiaires_data_frame():

    directory = os.path.join(
        prestations_sociales_directory,
        'les-beneficiaires-tous-regimes-de-prestations-familiales-et-sociales',
        )

    filenames = [filename for filename in os.listdir(directory) if filename.startswith('BenTR')]

    result_data_frame = None

    for filename in sorted(filenames):
        year = filename[5:5 + 4]
        assert year.startswith('19') or year.startswith('20')
        year = int(year)
        file_path = os.path.join(directory, filename)
        log.info('Parsing bénéficiaires data from year {} using {}'.format(year, file_path))
        data_frame = pd.read_csv(file_path, sep = ';', decimal = ',')
        data_frame.dropna(axis = 1, inplace = True)  # Remove NA columns
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
        data_frame['year'] = year
        data_frame = pd.melt(data_frame, id_vars = ['year', 'Prestations'])
        result_data_frame = data_frame if result_data_frame is None else result_data_frame.merge(data_frame, how = 'outer')
