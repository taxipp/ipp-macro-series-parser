# -*- coding:utf-8 -*-

from __future__ import division


import logging
import os
import pandas as pd


from ipp_macro_series_parser.config import Config


"""
Library of functions for build_parameters.py
"""

input_file_name_default = 'projpop0760_FECcentESPcentMIGcent.xls'


log = logging.getLogger(__name__)


def check_directory_existence(directory):
    if not os.path.exists(directory):
        log.info('Creating directory {}'.format(directory))
        os.makedirs(directory)


def get_data(input_directory = None, file_name = None, input_file_path = None, sheetname = None, taille = 110):

    assert (file_name is None) or (input_file_path is None)

    if file_name is not None:
        assert input_directory is not None
        input_file_path = os.path.join(
            input_directory,
            file_name
            )

    assert os.path.exists(input_file_path), input_file_path

    feuille = pd.read_excel(
        input_file_path,
        sheetname = sheetname,
        skiprows = 0,
        header = 4,
        )

    feuille.index.names = ['age']
    assert (feuille[feuille.columns[0]][0:taille-1] == range(taille-1)).all()
    feuille.loc[feuille.columns[0],taille] = taille
    feuille.drop(feuille.columns[0], axis=1, inplace=True)
    data = feuille[:taille]
    cols = [col for col in data.columns if 'Unnamed' not in str(col)]
    return data[cols].copy()


def builder_kernel(input_dir = None, input_file_name = None, sheetname = None,
        output_dir = None, output_file_name = None, to_do_if_csv = None, to_do_always = None,
        taille = 110, to_csv = False, input_file_path = None):
    """
    Core function to read the excel file and output a df or csv
    Used in the build_* functions
    """
    assert (input_file_name is None) or (input_file_path is None)

    data = get_data(
        input_dir,
        input_file_name,
        input_file_path,
        sheetname,
        taille = taille
        ).reset_index()

    del data['age']

    if to_do_always is not None:
        data = to_do_always(data)

    if to_csv:
        check_directory_existence(output_dir)

        output_path = os.path.join(
            output_dir,
            output_file_name
            )

        if to_do_if_csv is not None:
            data = to_do_if_csv(data)

        columns_for_liam = ['age', 'period'] + [''] * (len(data.columns) - 1)
        first_row = ','.join([''] + [str(year) for year in data.columns])
        header = ','.join(columns_for_liam) + '\n' + first_row + '\n'

        data.to_csv(
            output_path,
            index = True,
            header = False
            )

        with open(output_path, 'r') as input_file:
            data = input_file.read().splitlines(True)

        with open(output_path, 'w') as output_file:
            output_file.writelines(header)
            output_file.writelines(data)

    else:
        return data


def build_mortality_rates(to_csv = False, input_file_path = None, output_dir = None):
    """
    Create the df/csv containing death rates
    """

    genders = ['male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['hyp_mortaliteH', 'hyp_mortaliteF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['hyp_mortaliteH.csv', 'hyp_mortaliteF.csv']
        ))
    taille = 121

    def to_do_mortality(data):
        data = data / 10**4
        return data

    if to_csv:
        for gender in genders:
            builder_kernel(
                input_file_path = input_file_path,
                sheetname = sheetname_by_gender[gender],
                output_dir = output_dir,
                output_file_name = output_file_name_by_gender[gender],
                to_do_always = to_do_mortality,
                taille = taille,
                to_csv = True
                )
    else:
        data_by_gender = dict(
            (
                gender,
                builder_kernel(
                    input_file_path = input_file_path,
                    sheetname = sheetname_by_gender[gender],
                    taille = taille,
                    to_csv = False,
                    to_do_always = to_do_mortality,
                    )
                )
            for gender in genders
            )

        dataframes = list()
        for gender, dataframe in data_by_gender.items():
            dataframe.index.name = 'age'
            dataframe.columns.name = 'period'
            dataframe = dataframe.stack('period').reset_index()
            dataframe['sexe'] = False if gender == 'male' else True  # homme = False, femme = True
            dataframe.rename(columns = {0: 'value'}, inplace = True)
            dataframe = dataframe.set_index(['period', 'sexe', 'age'])
            assert len(dataframe.columns) == 1
            dataframes.append(dataframe)

        return pd.concat(dataframes).sort_index()


def build_population(to_csv = False, input_file_path = None, output_dir = None):
    """
    Create the df/csv containing planned population
    """

    genders = ['male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['populationH', 'populationF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['populationH.csv', 'populationF.csv']
        ))

    taille = 109


    if to_csv:
        for gender in genders:
            builder_kernel(
                input_file_path = input_file_path,
                sheetname = sheetname_by_gender[gender],
                output_dir = output_dir,
                output_file_name = output_file_name_by_gender[gender],
                to_do_always = None,
                taille = taille,
                to_csv = True
                )
    else:
        data_by_gender = dict(
            (
                gender,
                builder_kernel(
                    input_file_path = input_file_path,
                    sheetname = sheetname_by_gender[gender],
                    taille = taille,
                    to_csv = False,
                    to_do_always = None,
                    )
                )
            for gender in genders
            )

        dataframes = list()
        for gender, dataframe in data_by_gender.items():
            dataframe.index.name = 'age'
            dataframe.columns.name = 'period'
            dataframe = dataframe.stack('period').reset_index()
            dataframe['sexe'] = False if gender == 'male' else True  # homme = False, femme = True
            dataframe.rename(columns = {0: 'value'}, inplace = True)
            dataframe = dataframe.set_index(['period', 'sexe', 'age'])
            assert len(dataframe.columns) == 1
            dataframes.append(dataframe)

        return pd.concat(dataframes).sort_index()


if __name__ == '__main__':
    config = Config()
    insee_projections_directory = config.get('data', 'insee_projections')
    insee_2070_projections_filename_by_hypothese = {
        'centrale': 'Proj_démo_INSEE_2016_Hypothèse_centrale.xls',
        'jeune': 'Proj_démo_INSEE_2016_Population_jeune.xls',
        'vieille': 'Proj_démo_INSEE_2016_Population_vieille.xls',
        }
    for hypothese, filename in insee_2070_projections_filename_by_hypothese.items():
        input_file_path = os.path.join(insee_projections_directory, filename)
        output_path = os.path.join('/home/benbel/temp', hypothese, 'population.csv')
        df = build_population(input_file_path = input_file_path)
        check_directory_existence(os.path.dirname(output_path))
        df.to_csv(output_path)
