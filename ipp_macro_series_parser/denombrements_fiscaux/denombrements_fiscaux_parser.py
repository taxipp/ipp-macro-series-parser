# -*- coding: utf-8 -*-


import numpy
import os
import pandas
import pkg_resources
from ipp_macro_series_parser.config import Config

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
# hdf_directory = config_parser.get('data', 'denombrements_fiscaux_hdf')



def parse_ipp_denombrements(year = None, years = None):
    if year is not None and years is None:
        years = [year]

    file_path = os.path.join(xls_directory, u'Agrégats IPP - Données fiscales.xls')

    def parse_bloc(name = None, sheetname = '2042-montant', skiprows = 0, parse_cols = None, slice_start = None, slice_end = None,
                   prefix = ''):
        assert name is not None
        df = pandas.read_excel(
            file_path,
            na_values = '-',
            sheetname = sheetname,
            skiprows = skiprows,
            parse_cols = parse_cols).iloc[slice_start:slice_end]
        df.columns = ['year'] + ( prefix + df.columns[1:].str.lower()).tolist()
        try:
            df = df.convert_objects(convert_numeric=True)
            df = df.astype(float)
            df.year = df.year.astype(int)
        except Exception, e:
            print e
            return name, df
        return name, df

    # Fiche principale

    # 1 - Traitements, salaire, prime pour l'emploi, pensions et rentes
    traitements_salaires = dict(
        name = 'traitements_salaires',
        sheetname = '2042-montant',
        skiprows = 4,
        parse_cols = 'A:AB',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f1',
        )

    prime_emploi = dict(
        name = 'prime_emploi',
        sheetname = '2042-montant',
        skiprows = 25,
        parse_cols = 'A:K',
        slice_start = 1,
        slice_end = 17,
        prefix = 'f1',
        )

    pension_retraite = dict(
        name = 'pension_retraite',
        sheetname = '2042-montant',
        skiprows = 46,
        parse_cols = 'A:M',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f1',
        )

    rentes_viageres_titre_onereux = dict(
        name = 'rentes_viageres_titre_onereux',
        sheetname = '2042-montant',
        skiprows = 68,
        parse_cols = 'A:E',
        slice_start = 1,
        slice_end = 17,
        prefix = 'f1',
        )

    # 2 - Revenus des valeurs et capitaux mobiliers

    prelevement_forfaitaire_liberatoire = dict(
        name = 'prelevement_forfaitaire_liberatoire',
        sheetname = '2042-montant',
        skiprows = 89,
        parse_cols = 'A:D',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    revenus_avec_abattement = dict(
        name = 'revenus_avec_abattement',
        sheetname = '2042-montant',
        skiprows = 111,
        parse_cols = 'A:E',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    revenus_sans_abattement = dict(
        name = 'revenus_sans_abattement',
        sheetname = '2042-montant',
        skiprows = 133,
        parse_cols = 'A:D',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    autres_revenus_financiers = dict(
        name = 'autres_revenus_financiers',
        sheetname = '2042-montant',
        skiprows = 154,
        parse_cols = 'A:I',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    # 3 - Plus values et gains taxables à 16% (18% à partir de 2008)

    plus_values = dict(
        name = 'plus_values',
        sheetname = '2042-montant',
        skiprows = 199,
        parse_cols = 'A:C',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f3',
        )

    # 4 - Revenus fonciers
    # TODO: copier coller d'une note
    # Pour les dénombrements de 96 à 2001, on ne connait plus le détail des différents déficits mais seulement total agrégé (case total def)
    # Comme les parts des différents déficits sur le déficit total est pratiquement constant dans le temps, on assume donc que la répartition du déficit total entre les différents déficits est constant entre 96 et 2001 et égal à son niveau de 2003
    # TODO: virer 2012 à 2014 ?
    revenus_fonciers = dict(
        name = 'revenus_foncier',
        sheetname = '2042-montant',
        skiprows = 222,
        parse_cols = 'A:H',
        slice_start = 1,
        slice_end = 20,
        prefix = 'f3',
        )

    contribution_revenus_locatifs = dict(
        name = 'contribution_revenus_locatifs',
        sheetname = '2042-montant',
        skiprows = 246,
        parse_cols = 'A:C',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f4',
        )

    # 5- Revenus exceptionnels ou différés

    revenus_exceptionnels = dict(
        name = 'revenus_exceptionnels',
        sheetname = '2042-montant',
        skiprows = 268,
        parse_cols = 'A:B',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f5',
        )

    # 6- Charges déductibles et imputations diverses

    charges_deductibles = dict(
        name = 'charges_deductibles',
        sheetname = '2042-montant',
        skiprows = 316,
        parse_cols = 'A:I',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f6',
        )

    epargne_retraite = dict(
        name = 'epargne_retraite',
        sheetname = '2042-montant',
        skiprows = 338,
        parse_cols = 'A:O',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f6',
        )

    # 7- Charges ouvrant droit à réduction ou à crédit d'impôt

    reductions_credits_impot = dict(
        name = 'reductions_credits_impot',
        sheetname = '2042-montant',
        skiprows = 360,
        parse_cols = 'A:BH',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f7',
        )

    # 8- Autres imputations, reprises de réductions d'impôt, conventions internationales, divers

    autres_imputations = dict(
        name = 'autres_imputations',
        sheetname = '2042-montant',
        skiprows = 383,
        parse_cols = 'A:L',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f7',
        )

    # Fiche complémentaire

    # 1- Gains de levée d'options

    options = dict(
        name = 'options',
        sheetname = '2042C - montant',
        skiprows = 5,
        parse_cols = 'A:I',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f1',
        )

    name, df = parse_bloc(**options)
    df.dtypes
    df.year

    # salaires exonérés

    salaires_exoneres = dict(
        name = 'salaires_exoneres',
        sheetname = '2042C - montant',
        skiprows = 26,
        parse_cols = 'A:I',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f1',
        )

    # crédit d'impôt mobilité
    # TODO; nothing in agrégats IPP

    # 3- Plus-values et gains divers

    plus_values_complementaire = dict(
        name = 'plus_values_complementaire',
        sheetname = '2042C - montant',
        skiprows = 67,
        parse_cols = 'A:T',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f3',
        )

    # 4- Revenus fonciers

    revenus_fonciers_complementaire = dict(
        name = 'revenus_fonciers_complementaire',
        sheetname = '2042C - montant',
        skiprows = 88,
        parse_cols = 'A:B',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f4',
        )

    # 5- Revenus et plus-values des professions non salariées

    prime_emploi_complementaire = dict(
        name = 'prime_emploi_complementaire',
        sheetname = '2042C - montant',
        skiprows = 111,
        parse_cols = 'A:G',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )

    name, df = parse_bloc(**prime_emploi_complementaire)
    print df.dtypes
    df.year


    blocs = [
        traitements_salaires,
        prime_emploi,
        pension_retraite,
        rentes_viageres_titre_onereux,
        prelevement_forfaitaire_liberatoire,
        revenus_avec_abattement,
        revenus_sans_abattement,
        autres_revenus_financiers,
        plus_values,
        revenus_fonciers,
        contribution_revenus_locatifs,
        revenus_exceptionnels,
        charges_deductibles,
        epargne_retraite,
        reductions_credits_impot,
        autres_imputations,
        options,
        plus_values_complementaire,
        revenus_fonciers_complementaire,
        ]

    x = dict(parse_bloc(**bloc) for bloc in blocs)

    return x



def denombrements_fiscaux_df_generator(year = None, years = None):
    """
    Generates the table with all the data from Dénombrements Fiscaux .

    Parameters
    ----------
    year : int
        year of DGFIP data (coincides with year of declaration)
    years : list of integers
        list of years of interest. Optional.

    Example
    --------
    >>> table_2013 = denombrements_fiscaux_df_generator(year = 2013)

    Returns the main table of dénombrements fiscaux for the year 2013.
    """
    if year is not None and years is None:
        years = [year]

    df = pandas.read_excel(os.path.join(xls_directory, '2042_national.xls'), sheetname = 'montant')
    assert df.dtypes.apply(lambda x: numpy.issubdtype(x, numpy.float)).all(), df.dtypes
    df = df.stack()
    df = df.reset_index()
    df.rename(columns = {'level_0': 'code', 'level_1': 'year', 0: 'value'}, inplace = True)
    df[['year']] = df[['year']].astype(int)
    return df.loc[df.year.isin(years)].copy() if years is not None else df.copy()


def save_df_to_hdf(df, hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    df.to_hdf(file_path, key)
    pandas.DataFrame().to_hdf


def import_hdf_to_df(hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    store = pandas.HDFStore(file_path)
    df = store[key]
    return df
