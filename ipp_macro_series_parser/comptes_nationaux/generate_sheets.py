# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:11:31 2015

@author: sophie.cottet
"""

from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import get_or_construct_data
from ipp_macro_series_parser.comptes_nationaux.sheets_lists import (
    generate_CN1_variables, generate_CN2_variables, generate_CN11_variables, generate_CN12_variables)


year = 2012


def get_tidy_data(year):
    df = get_comptes_nationaux_data(year)
    return df


def generate_CN1(year):
    df = get_tidy_data(year)
    variables_CN1 = generate_CN1_variables(year)
    values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, year + 1))
    return values_CN1, formulas_CN1

# valCN1_2013 = generate_CN1(2013)


def generate_CN2(year):
    df = get_tidy_data(year)
    variables_CN2 = generate_CN2_variables(year)
    values_CN2, formulas_CN2 = get_or_construct_data(df, variables_CN2, range(1949, year + 1))
    return values_CN2, formulas_CN2


def generate_CN11(year):
    df = get_tidy_data(year)
    variables_CN11 = generate_CN11_variables(year)
    values_CN11, formulas_CN11 = get_or_construct_data(df, variables_CN11, range(1949, year + 1))
    return values_CN11, formulas_CN11

# cn11_2013 = generate_CN11(2013)[0]
# cn11_2012 = generate_CN11(2012)[0]


def generate_CN12(year):
    df = get_tidy_data(year)
    variables_CN12 = generate_CN12_variables(year)
    values_CN12, formulas_CN12 = get_or_construct_data(df, variables_CN12, range(1949, year + 1))
    return values_CN12, formulas_CN12

# valCN12_2013 = generate_CN12(2013)[0]
# valCN12_2012 = generate_CN12(2012)[0]
