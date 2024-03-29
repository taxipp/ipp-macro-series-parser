


import os

from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import look_many


parser = Config()
excel_output_directory = parser.get('data', 'cn_csv_directory')


def reshape_to_long_for_output(df):
    """
    Unmelts the data, using the years as variables (columns).

    Parameters
    ----------
    df : DataFrame
        DataFrame generated by get_comptes_nationaux_data(year) and/or look_many(df, my_selection)

    Example
    --------
    >>> from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import get_comptes_nationaux_data
    >>> from ipp_macro_series_parser.data_extraction import look_many
    >>> table2013 = get_comptes_nationaux_data(2013)
    >>> my_selection = [{'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIB'},
    ...             {'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIN'}]
    >>> df = look_many(table2013, my_selection)
    >>> df_reshaped = reshape_to_long_for_output(df)

    Returns a slice of get_comptes_nationaux_data(2013) containing the gross product (PIB) and the net product (PIN) of
    the whole economy (S1), for all years. Observations are indexed by code (PIB, PIN) and values are given per year.
    The dataframe is reshaped vertically, each row corresponding to a year, and each column to an observation
    (PIB or PIN)
    """
    del df['file_name']
    del df['link']
    del df['source']
    del df['version']
    del df['description']

    df = df.set_index(['year', 'code', 'ressources', 'institution', 'file_title'])
    df = df.unstack(level = 'year')

    df = df.transpose()
    df = df.reset_index(1)
    df.reset_index(drop = True)

    return df


def reshape_to_wide_for_output(df):
    """
    Unmelts the data, using the years as variables (rows).

    Parameters
    ----------
    df : DataFrame
        DataFrame generated by get_comptes_nationaux_data(year) and/or look_many(df, my_selection

    Example
    --------
    >>> from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import get_comptes_nationaux_data
    >>> from ipp_macro_series_parser.data_extraction import look_many
    >>> table2013 = get_comptes_nationaux_data(2013)
    >>> my_selection = [{'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIB'},
    ...             {'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIN'}]
    >>> df = look_many(table2013, my_selection)
    >>> df_reshaped = reshape_to_wide_for_output(df)

    Returns a slice of get_comptes_nationaux_data(2013) containing the gross product (PIB) and the net product (PIN) of
    the whole economy (S1), for all years. Observations are indexed by code (PIB, PIN) and values are given per year.
    The dataframe is reshaped horizontally, each column corresponding to a year, and each row to an observation
    (PIB or PIN)
    """
    del df['file_name']
    del df['link']
    del df['source']
    del df['version']
    del df['description']

    df = df.set_index(['code', 'ressources', 'institution', 'file_title', 'year'])
    df = df.unstack(level = 'year')

    levels = df.columns.levels
    labels = df.columns.labels
    df.columns = levels[1][labels[1]]

    return df


def df_long_to_csv(df, csv_file_name):
    """
    Output the dataframe to a csv file (tab separated).

    Parameters
    ----------
    df : DataFrame
        DataFrame generated by reshape_to_long_for_output(df)
    csv_file_name : string
        path to the output csv file. Extension should be .txt (and not .csv) in order to be read by Excel.

    Example
    --------
    >>> from ipp_macro_series_parser.config import Config
    >>> config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    ... )
    >>> from ipp_macro_series_parser.comptes_nationaux.cn_parser_main import get_comptes_nationaux_data
    >>> from ipp_macro_series_parser.data_extraction import look_many
    >>> cn_directory = parser.get('data', 'cn_directory')
    >>> table2013 = get_comptes_nationaux_data(2013)
    >>> my_selection = [{'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIB'},
    ...             {'code': None, 'institution': 'S1', 'ressources': False,
    ...             'description': 'PIN'}]
    >>> df = look_many(table2013, my_selection, years = range(1990, 2014))
    >>> df_reshaped = reshape_to_long_for_output(df)
    >>> df_long_to_csv(df_reshaped, os.path.join(cn_directory, 'output', '2013.txt'))

    Returns None. Creates a csv file containing the gross product (PIB) and the net product (PIN) of the whole
    economy (S1), for all years. Observations are indexed by code (PIB, PIN) and values are given per year.
    The dataframe is shaped vertically, each row corresponding to a year, and each column to an observation
    (PIB or PIN)
    """
    if not os.path.exists(excel_output_directory):
        os.mkdir(excel_output_directory)
    df.to_csv(os.path.join(excel_output_directory, csv_file_name), tupleize_cols = False, index = None, na_rep = 'NaN',
              sep=';')


def output_for_sheets(entry_by_index_list, version_year, csv_file_name):
    """
    Output the final data needed to recreate a sheet of "Agrégats IPP - Comptabilité nationale" into a csv file.

    Parameters
    ----------
    entry_by_index : dictionnary
        A dictionnary with keys 'code', 'institution', 'ressources', 'year', 'description'.
    version_year : int
        Year of the version of Comptabilité Nationale data the user wishes to have (most often the latest version).
    csv_file_name : string
        path to the output csv file. Extension should be .txt (and not .csv) in order to be read by Excel.

    Example
    --------
    >>> CN1 = cn_output.output_for_sheets(
    ...    cn_sheets_lists.list_CN1, 2013,
    ...    os.path.join(cn_directory, u'Agrégats IPP - Comptabilité nationale.txt')
    ...    )

    Returns None. Creates a csv file containing the values of all the variables needed to construct sheet CN1, for all
    years. Each column is a variable, i.e. a tuple containing the agregates's code, the institution concerned,
    whether it is Ressources or Emplois, and the file from where the data was extracted.

    Note
    ------
    The first drop_duplicates() should be unnecessary : the presence of drop_duplicates in the parsers should
    eliminate the need for that.

    The second drop_duplicates(), i.e. a drop_duplicates on all variables except those referring to the source file,
    is essential to avoid the same data being repeated in different columns when it is sourced from different files
    (typically, TEE and a Comptes nationaux file).
    """
    list_variables = entry_by_index_list
    table = get_comptes_nationaux_data(version_year)

    extract = look_many(table, list_variables)
    extract = extract.drop_duplicates()
    extract = extract.drop_duplicates((u'code', u'institution', u'ressources', u'value',
       u'year'))  # this eliminates doubles, i.e. identical info coming from distinct sources (eg. TEE and Compte)

    df = reshape_to_long_for_output(extract)

    df_long_to_csv(df, csv_file_name)
    return df
