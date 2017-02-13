#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import logging
import os
import sys
import pandas as pd

from ipp_macro_series_parser.config import Config

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

parser = Config()
prelevements_sociaux_source = parser.get('data', 'prelevements_sociaux_source').decode('utf-8')
prelevements_sociaux_directory = parser.get('data', 'prelevements_sociaux_directory')

assert prelevements_sociaux_source != 'None', \
    "Set prelevements_sociaux_source in the data section of you config[_local].ini file to a valid directory"
assert prelevements_sociaux_directory != 'None', \
    "Set prelevements_sociaux_directory in the data section of you config[_local].ini file to a valid directory"


def prelevements_sociaux_downloader():

    sheetname1 = 'CSG-CRDS (V&M)'
    sheetname2 = 'Recettes CSG (CCSS)'
 #   sheetname3 = 'Calcul_assietteCSG'

    file_path = prelevements_sociaux_source.encode('iso8859_1')
    df1 = pd.read_excel(file_path, sheetname = sheetname1, encoding='utf-8')
    df2 = pd.read_excel(file_path, sheetname = sheetname2, encoding='utf-8')
 #   df3 = pd.read_excel(file_path, sheetname = sheetname3, encoding='utf-8')

    dict_df = {sheetname1: df1, sheetname2: df2}

    return dict_df


def prelevements_sociaux_cleaner(dict_df, var):

    ## Clean CSG-CRDS: ##
    if var == "recette_csg_crds":
        df1 = dict_df['CSG-CRDS (V&M)'].reset_index()
        # Columns
        df1 = df1.iloc[:, 0:3]
        # Names
        df1.columns = ["annee", "recette_csg", "recette_crds"]
        # Drop lines
        df1 = df1.iloc[1:17]
        # Convert to euros
        df1[["recette_csg", "recette_crds"]] = df1[["recette_csg", "recette_crds"]] * 1e6
        df1.iloc[14:, 1:3] = df1.iloc[14:, 1:3] / 6.57

    ## Clean CSG par revenus ##
    if var == "recette_csg_by_type":
        df1 = dict_df['Recettes CSG (CCSS)'].reset_index()
        # Columns
        df1 = df1.iloc[:, [1, 2, 3, 9, 10, 11, 12, 13, 14, 18]]
        # Names
        df1.columns = ["annee", "csg_total", "csg_activite", "csg_remplacement", "csg_capital", "csg_placement",
                       "csg_patrimoine", "csg_majo_pen", "csg_jeux", "source"]
        # Drop lines
        df1 = df1.iloc[1:27]
        # Convert to euros
        df1 = df1.iloc[:, 1:9] * 1e9

    file_name = var + '.csv'
    save_path = os.path.join(prelevements_sociaux_directory, "clean", file_name)
    df1.to_csv(save_path)


def main_parse():
    raw_data = prelevements_sociaux_downloader()
    prelevements_sociaux_cleaner(dict_df = raw_data, var = "recette_csg_crds")
    prelevements_sociaux_cleaner(dict_df = raw_data, var = "recette_csg_by_type")


if __name__ == "__main__":
    sys.exit(main_parse())
