#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import logging
import os
import platform
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
    sheetname3 = 'Calcul_assietteCSG'

    if platform.system == 'Windows':
        file_path = prelevements_sociaux_source.encode('iso8859_1')
        df1 = pd.read_excel(file_path, sheetname = sheetname1, encoding='utf-8')
        df2 = pd.read_excel(file_path, sheetname = sheetname2, encoding='utf-8')
        df3 = pd.read_excel(file_path, sheetname = sheetname3, encoding='utf-8')
    else:
        file_path = prelevements_sociaux_source
        df1 = pd.read_excel(file_path, sheetname = sheetname1)
        df2 = pd.read_excel(file_path, sheetname = sheetname2)
        df3 = pd.read_excel(file_path, sheetname = sheetname3)

    data_frame_by_sheet = {sheetname1: df1, sheetname2: df2, sheetname3: df3}

    return data_frame_by_sheet


def prelevements_sociaux_cleaner(data_frame_by_sheet, var):
    # Clean CSG-CRDS
    if var == "recette_csg_crds":
        df1 = data_frame_by_sheet['CSG-CRDS (V&M)'].reset_index()
        # Columns
        df1 = df1.iloc[:, 0:3]
        # Names
        df1.columns = ["annee", "recette_csg", "recette_crds"]
        # Drop lines
        df1 = df1.iloc[1:17]
        # Convert to euros
        df1[["recette_csg", "recette_crds"]] = df1[["recette_csg", "recette_crds"]] * 1e6
        df1.iloc[14:, 1:3] = df1.iloc[14:, 1:3] / 6.57

    # Clean recette CSG par revenus
    if var == "recette_csg_by_type":
        df1 = data_frame_by_sheet['Recettes CSG (CCSS)'].reset_index()
        # Columns
        df1 = df1.iloc[:, [1, 2, 3, 9, 10, 11, 12, 13, 14, 18]].copy()
        # Names
        df1.columns = ["annee", "csg_total", "csg_activite", "csg_remplacement", "csg_capital", "csg_placement",
            "csg_patrimoine", "csg_majo_pen", "csg_jeux", "source"]
        # Drop lines
        df1 = df1.iloc[1:27].copy()
        # Convert to euros
        df1.iloc[:, 1:9] = df1.iloc[:, 1:9] * 1e9
        df1.annee = df1.annee.astype(int)

     # Clean assiette CSG par revenus (jusqu'à 2012)
    if var == "assiette_csg_by_type":
        df1 = data_frame_by_sheet['Calcul_assietteCSG'].reset_index()

        # Columns
        df1 = df1[list(df1.columns[1:12]) + list(df1.columns[13:24])].copy()
        # Names
        df1.columns = ["annee",
                           "assiette_csg_sal", "assiette_csg_sal_priv", "assiette_csg_sal_pub",
                           "assiette_csg_non_sal",
                           "assiette_csg_rempl", "assiette_csg_rempl_cho", "assiette_csg_rempl_ret",
                           "assiette_csg_cap", "assiette_csg_cap_pat", "assiette_csg_cap_pla",
                           "recette_csg_crds_sal", "recette_csg_crds_sal_priv", "recette_csg_crds_sal_pub",
                           "recette_csg_crds_non_sal",
                           "recette_csg_crds_rempl", "recette_csg_crds_rempl_cho", "recette_csg_crds_rempl_ret",
                           "recette_csg_crds_cap", "recette_csg_crds_cap_pat", "recette_csg_crds_cap_pla",
                           "recette_csg_crds_total"]
        # Drop lines
        df1 = df1.iloc[3:19].copy()
        # Convert to euros
        df1.iloc[:, 1:] = df1.iloc[:, 1:] * 1e9
        df1.annee = df1.annee.astype(int)

    file_name = var + '.csv'
    save_path = os.path.join(prelevements_sociaux_directory, "clean", file_name)
    (df1
        .set_index('annee')
        .transpose()
        .sort_index(axis = 1)
        .to_csv(save_path)
        )


def main_parse():
    raw_data = prelevements_sociaux_downloader()
    prelevements_sociaux_cleaner(data_frame_by_sheet = raw_data, var = "recette_csg_crds")
    prelevements_sociaux_cleaner(data_frame_by_sheet = raw_data, var = "recette_csg_by_type")
    prelevements_sociaux_cleaner(data_frame_by_sheet = raw_data, var = "assiette_csg_by_type")


if __name__ == "__main__":
    sys.exit(main_parse())
