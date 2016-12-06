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
    file_path = os.path.join(directory, u"historique_dépenses_depuis 1946.xls")

    # sheetname = u'données histo D'
    sheetname = u'données histo M'
    # sheetname = u'données histo MD'

    data_frame = pd.read_excel(file_path, sheetname = sheetname, header = 1, inbdex_col = 0)
    print data_frame
    dico = {
        'af': 'Allocations familiales (AF)',
        'af_base': None,
        'af_majoration': None,
        'af_allocation_forfaitaire': None,
        'cf': 'Complément familial (CF)',
        'paje_base': 'PAJE  naissance adoption de base (AB)',
        'paje_naissance': 'PAJE naissance adoption',
        'paje_clca': 'PAJE complément (optionnel) libre choix activité PréPARE',  # contient également le COLCA
        'paje_clmg': 'PAJE complément mode de garde (CMG)',
        'ars': 'Allocation de rentrée scolaire (ARS)',
        'aeeh': 'Allocation d’éducation de l’enfant handicapé de base',
        'asf': 'Allocation de soutien familial (ASF)',
        'aspa',
        'aah': ' Allocation adultes handicapés de base',
        'caah': 'Majoration pour la vie autonome (MVA) - Complément AAH',
        'rsa': ' Revenu solidarité active (RSA versé yc prime, créances, indus)',
        'rsa_activite': 'RSA activité (hors RSA Jeunes)',
        'aefa': 'Prime exceptionnelle décembre RSA (Etat)',
        'api': 'Allocation de parent isolé (API)',
        'psa': None,
        'aides_logement',
        'alf': 'Allocation logement familiale (ALF)',
        'als': 'Allocation logement sociale (ALS)',
        'apl': 'Aide personnalisée au logement (APL)',
        },


if __name__ == '__main__':
    build_histo_data_frames()
