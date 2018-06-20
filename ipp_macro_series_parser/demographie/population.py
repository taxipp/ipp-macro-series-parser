# -*- coding:utf-8 -*-

from __future__ import division


import logging
import numpy as np
import os
import pandas as pd

"""
Library of functions for build_parameters.py
"""

input_file_name_default = 'projpop0760_FECcentESPcentMIGcent.xls'


log = logging.getLogger(__name__)


def check_directory_existence(directory):
    if not os.path.exists(directory):
        log.info('Creating directory {}'.format(directory))
        os.makedirs(directory)


def get_data(input_directory, file_name = None, sheetname = None, taille = 110):

    data_path = os.path.join(
        input_directory,
        file_name
        )

    assert os.path.exists(data_path)

    feuille = pd.read_excel(
        data_path,
        sheetname = sheetname,
        skiprows = 2,
        header = 2,
        )

    feuille.index.names = ['age']
    feuille.drop(feuille.columns[0], axis=1, inplace=True)
    data = feuille[:taille]

    return data.copy()


def builder_kernel(input_dir = None, input_file_name = input_file_name_default, sheetname = None,
        output_dir = None, output_file_name = None, to_do_if_csv = None, to_do_always = None, uniform_weight = None,
        taille = 110, to_csv = False):
    """
    Core function to read the excel file and output a df or csv
    Used in the build_* functions
    """
    data = get_data(
        input_dir,
        input_file_name,
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
            data = to_do_if_csv(data, uniform_weight)

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


def build_deaths(to_csv = False, input_dir = None, output_dir = None, uniform_weight = 200):
    """
    Create the df/csv containing death numbers
    """

    assert input_dir is not None
    assert output_dir is not None

    genders = ['male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['nbre_decesH', 'nbre_decesF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['decesH.csv', 'decesF.csv']
        ))

    def to_do_deaths(data, uniform_weight):
        data.drop(108, inplace = True)
        data = (data / uniform_weight).round()
        return(data)

    for k in genders:
        if to_csv:
            for gender in genders:
                builder_kernel(
                    input_dir = input_dir,
                    input_file_name = input_file_name_default,
                    sheetname = sheetname_by_gender[gender],
                    output_dir = output_dir,
                    output_file_name = output_file_name_by_gender[gender],
                    to_do_if_csv = to_do_deaths,
                    uniform_weight = uniform_weight,
                    taille = 110,
                    to_csv = True
                    )
        else:
            data_by_gender = dict(
                (
                    gender,
                    builder_kernel(
                        input_dir = input_dir,
                        sheetname = sheetname_by_gender[gender],
                        taille = 110,
                        to_csv = False
                        )
                    )
                for gender in genders
                )

            return data_by_gender


def build_mortality_rates(to_csv = False, input_dir = None, output_dir = None, uniform_weight = 200):
    """
    Create the df/csv containing death rates
    """

    assert input_dir is not None
    assert output_dir is not None

    genders = ['male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['hyp_mortaliteH', 'hyp_mortaliteF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['hyp_mortaliteH.csv', 'hyp_mortaliteF.csv']
        ))

    def to_do_mortality(data):
        data = data / 10**4
        return data

    for k in genders:
        if to_csv:
            for gender in genders:
                builder_kernel(
                    input_dir = input_dir,
                    input_file_name = input_file_name_default,
                    sheetname = sheetname_by_gender[gender],
                    output_dir = output_dir,
                    output_file_name = output_file_name_by_gender[gender],
                    to_do_always = to_do_mortality,
                    uniform_weight = uniform_weight,
                    taille = 110,
                    to_csv = True
                    )
        else:
            data_by_gender = dict(
                (
                    gender,
                    builder_kernel(
                        input_dir = input_dir,
                        sheetname = sheetname_by_gender[gender],
                        taille = 110,
                        to_csv = False,
                        to_do_always = to_do_mortality,
                        )
                    )
                for gender in genders
                )

            return data_by_gender


def build_fertility_rates(to_csv = False, input_dir = None, output_dir = None, uniform_weight = 200):
    """
    Create the df/csv containing fertility rates
    """

    assert input_dir is not None
    assert output_dir is not None

    genders = ['all']

    sheetname_by_gender = dict(zip(
        genders,
        ['Hyp_fecondite']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['hyp_fecondite.csv']
        ))

    def to_do_fertility(data):
        data = data / 10**4
        return(data)

    for k in genders:
        if to_csv:
            for gender in genders:
                builder_kernel(
                    input_dir = input_dir,
                    input_file_name = input_file_name_default,
                    sheetname = sheetname_by_gender[gender],
                    output_dir = output_dir,
                    output_file_name = output_file_name_by_gender[gender],
                    to_do_always = to_do_fertility,
                    uniform_weight = uniform_weight,
                    taille = 37,
                    to_csv = True
                    )
        else:
            data_by_gender = dict(
                (
                    gender,
                    builder_kernel(
                        input_dir = input_dir,
                        sheetname = sheetname_by_gender[gender],
                        taille = 37,
                        to_csv = False,
                        to_do_always = to_do_fertility,
                        )
                    )
                for gender in genders
                )

            return data_by_gender


def build_migration(to_csv = False, input_dir = None, output_dir = None, uniform_weight = 200):
    """
    Create the df/csv containing net migration
    """
    assert input_dir is not None
    assert output_dir is not None

    genders = ['male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['hyp_soldemigH', 'hyp_soldemigF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['hyp_soldemigH.csv', 'hyp_soldemigF.csv']
        ))

    for k in genders:
        if to_csv:
            for gender in genders:
                builder_kernel(
                    input_dir = input_dir,
                    input_file_name = input_file_name_default,
                    sheetname = sheetname_by_gender[gender],
                    output_dir = output_dir,
                    output_file_name = output_file_name_by_gender[gender],
                    uniform_weight = uniform_weight,
                    taille = 110,
                    to_csv = True
                    )
        else:
            data_by_gender = dict(
                (
                    gender,
                    builder_kernel(
                        input_dir = input_dir,
                        sheetname = sheetname_by_gender[gender],
                        taille = 110,
                        to_csv = False,
                        )
                    )
                for gender in genders
                )

            return data_by_gender


def rescale_migration(input_dir = None, output_dir = None):
    """
    Creates the csv containing net outmigration rates from the raw migration
    and total population
    """

    genders = ['total', 'male', 'female']

    sheetname_by_gender = dict(zip(
        genders,
        ['populationTot', 'populationH', 'populationF']
        ))

    output_file_name_by_gender = dict(zip(
        genders,
        ['hyp_soldemigT_custom.csv', 'hyp_soldemigH_custom.csv', 'hyp_soldemigF_custom.csv']
        ))

    population_insee_by_gender = dict(
        (
            gender,
            builder_kernel(
                input_dir = input_dir,
                sheetname = sheetname_by_gender[gender],
                to_csv = False,
                taille = 109
                )
            )
        for gender in genders
        )

    migration_insee_by_gender = dict(
        (
            gender,
            pd.read_csv(
                os.path.join(
                    output_dir,
                    'hyp_soldemig{}.csv'.format(suffix)
                    ),
                header = 1,
                index_col = 0
                )
            )
        for gender, suffix in dict(female = 'F', male = 'H').iteritems()
        )

    with open(os.path.join(output_dir, 'hyp_soldemigH.csv'), 'r') as header_file:
        header = header_file.read().splitlines(True)[:2]

    for gender, migration in migration_insee_by_gender.iteritems():
        migration = migration[0:len(population_insee_by_gender[gender])]

        migration_extract_total = migration.copy().sum()
        migration_extract = np.maximum(migration.copy(), 0)
        # Resclaing to deal with emigration
        migration_extract = migration_extract * migration_extract_total / migration_extract.sum()
        total_population = population_insee_by_gender[gender]
        migration_extract.columns = [int(k) for k in migration_extract.columns]
        migration_extract = pd.DataFrame(
            migration_extract.copy().astype(float).values / total_population.astype(float).values
            )

        check_directory_existence(output_dir)
        file_path = os.path.join(output_dir, output_file_name_by_gender[gender])
        migration_extract.to_csv(file_path, index = True, header = False)

        with open(file_path, 'r') as input_file:
            data = input_file.read().splitlines(True)

        with open(file_path, 'w') as output_file:
            output_file.writelines(header)
            output_file.writelines(data)
