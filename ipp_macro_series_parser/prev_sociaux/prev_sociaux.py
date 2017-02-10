#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import argparse
import logging
import os
import pickle
import sys
import urllib
import urllib2
import shutil
import pandas as pd

from ipp_macro_series_parser.config import Config



app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

parser = Config()
prev_sociaux_source = parser.get('data', 'prev_sociaux_source')
os.path.exists(prev_sociaux_source)
os.path.exists(prev_sociaux_source.decode('utf-8').encode('iso8859_1'))
save_path = parser.get('data', 'prev_sociaux_savepath')

assert prev_sociaux_source != 'None', \
    "Set prev_sociaux_source in the data section of you config[_local].ini file to a valid directory"
assert save_path != 'None', \
    "Set prev_sociaux_directory in the data section of you config[_local].ini file to a valid directory"



def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(obj, name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

    
    
def save_df_to_hdf(df, hdf_file_name, key):
    file_path = os.path.join(save_path, hdf_file_name)
    df.to_hdf(file_path, key)
        
        
    
def prelevements_sociaux_downloader():

    sheetname1 = 'CSG-CRDS (V&M)'
    sheetname2 = 'Recettes CSG (CCSS)'
    sheetname3 = 'Calcul_assietteCSG'
    
    file_path = prev_sociaux_source.decode('utf-8').encode('iso8859_1')
    df1 = pd.read_excel(file_path, sheetname = sheetname1, encoding='utf-8')
    df2 = pd.read_excel(file_path, sheetname = sheetname2, encoding='utf-8')
    df3 = pd.read_excel(file_path, sheetname = sheetname3, encoding='utf-8')
    
    dict_df = {sheetname1:df1,sheetname2:df2,sheetname3:df3}    

    return dict_df

    
def prelevements_sociaux_cleaner(dict_df, var):

    ### Clean CSG-CRDS: ###
    if var == "recette_csg_crds":
        df1 = dict_df['CSG-CRDS (V&M)'].reset_index()
        # Columns 
        df1 = df1.iloc[:,0:3]            
        # Names
        df1.columns = ["annee", "recette_csg", "recette_crds"]           
        # Drop lines
        df1 = df1.iloc[1:17]              
        # Convert to euros
        df1[["recette_csg", "recette_crds"]] = df1[["recette_csg", "recette_crds"]]*1000000
        df1.iloc[14:,1:3] = df1.iloc[14:,1:3]/6.57
    

    save_df_to_hdf(df1, 'prev_sociaux.h5', var)

    

def main():
    raw_data = prelevements_sociaux_downloader()
    prelevements_sociaux_cleaner(dict_df = raw_data, var = "recette_csg_crds")
    


if __name__ == "__main__":
    sys.exit(main())
