# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:15:06 2015

@author: Antoine
"""

import os


def file_infos(excelfile_name):
    filename = os.path.split(excelfile_name)[1].split('.')[0]  # name of the file, without extension
    filename = filename.lower()
    file_version = os.path.dirname(excelfile_name)
    file_version = file_version[-4:]
    file_source = 'INSEE Comptabilite Nationale'
    file_source_link = 'http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_{}.zip'.format(file_version)

    skip = 0

    # TEE (tableau economique d'ensemble) file
    if filename.startswith('tee'):
        year = str(filename[-4:])
        agent = 'economie'
        title = 'TEE'
        tee_flag = 1  # 'tee'

    # Non TEE file
    else:
        year = ''
        agent = ''
        title = ''
        tee_flag = 0  # 'not tee'

    # could be automatized (in the parser method by reading the first cell and cutting in 3: name of file, title, agent)
        if filename == 't_7101':
            agent = 'S11'  # (societes non financieres)
            title = 'Compte des societes non financieres'
        elif filename == 't_7201':
            agent = 'S12'  # (societes financieres)
            title = 'Compte des societes financieres'
        elif filename == 't_7301':
            agent = 'S13'  # (administrations publiques)
            title = 'Compte des administrations puliques'
        elif filename == 't_7401':
            agent = 'S14'  # (menages)
            title = 'Compte des menages'
        elif filename == 't_7501':
            agent = 'S15'  # (isbl)
            title = 'Compte des institutions sans but lucratif au service des menages'
        elif filename == 't_7601':
            agent = 'S2'  # (reste du monde)
            title = 'Operations avec le reste du monde'

    # to be completed for all the files of interest in the folder
    # elif filename == 't_3101':
    #    agent = 'S13'  # (administrations publiques)
    #    title = 'Dette des administrations publiques (S13) au sens de Maastricht et sa répartition par sous-secteur'
    # elif filename == 't_3201':
    #   agent = 'S13'  # (administrations publiques)
    #    title = 'Dette et recettes des administrations publiques'

        else:
            skip = 1

    if skip == 0:
        parameters = dict()
        parameters = {'agent': agent, 'title': title, 'year': year, 'filename': filename,
        'tee_flag': tee_flag, 'source': file_source, 'link': file_source_link, 'version': file_version}
    else:
        parameters = False

    return parameters
