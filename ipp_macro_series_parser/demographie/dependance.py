# -*- coding:utf-8 -*-


from __future__ import division


import logging
import numpy as np
import os
import pandas as pd

from liam2.importer import array_to_disk_array
from ipp_macro_series_parser.scripts.utils import line_prepender

log = logging.getLogger(__name__)


def check_directory_existence(directory):
    if not os.path.exists(directory):
        log.info('Creating directory {}'.format(directory))
        os.makedirs(directory)


def build_prevalence_2010(input_dir = None, output_dir = None, uniform_weight = None,
        drees_filename = 'dss43_horizon_2060.xls', output_filename = 'dependance_prevalence_2010.csv'):
    data_path = os.path.join(input_dir, drees_filename)
    data = pd.read_excel(
        data_path,
        sheetname ='Tab2',
        header = 3,
        parse_cols = 'B:O',
        skip_footer = 4
        )
    columns_to_delete = [
        column for column in data.columns if column.startswith('Unnamed') or column.startswith('Ensemble')]
    for column in columns_to_delete:
        del data[column]
    data.index = [index.year for index in data.index]
    data.columns = range(1, 7)
    check_directory_existence(output_dir)
    csv_file_path = os.path.join(output_dir, output_filename)
    data = pd.DataFrame(data.xs(2010)).T
    data = np.round(data / uniform_weight)
    data.astype(int).to_csv(csv_file_path, index = False)
    line_prepender(csv_file_path, 'age_category')


def build_prevalence_all_years(globals_node = None, output_dir = None, input_dir = None, to_csv = None,
        drees_filename = 'dss43_horizon_2060.xls'):
    assert globals_node or to_csv
    data_path = os.path.join(
        input_dir,
        drees_filename)
    data = pd.read_excel(
        data_path,
        sheetname ='Tab6A',
        header = 3,
        parse_cols = 'B:E',
        skip_footer = 3
        )

    # "Au 1er janvier"
    data.columns = ['year', 'dependants_optimiste', 'DEPENDANTS', 'dependants_pessimiste']
    data.set_index('year', inplace = True)
    data = data.reindex(index = range(2010, 2061)).interpolate(method = 'polynomial', order = 7)
    data.index = [int(str(year - 1)) for year in data.index]
    data.index.name = "PERIOD"
    if globals_node:
        array_to_disk_array(
            globals_node,
            'dependance_prevalence_all_years',
            data.DEPENDANTS.values
            )

    elif to_csv:
        check_directory_existence(output_dir)
        csv_file_path = os.path.join(output_dir, 'dependance_prevalence_all_years.csv')
        data = data.reset_index()[['PERIOD', 'DEPENDANTS']]
        data.astype(int) \
            .to_csv(csv_file_path, index = False)
