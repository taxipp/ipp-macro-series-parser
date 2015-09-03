# -*- coding: utf-8 -*-


# TAXIPP -- A French microsimulation model
# By: IPP <taxipp@ipp.eu>
#
# Copyright (C) 2012, 2013, 2014, 2015 IPP
# https://github.com/taxipp
#
# This file is part of TAXIPP.
#
# TAXIPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# TAXIPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ipp_macro_series_parser.denombrements_fiscaux.test_denombrements import (
    create_index_by_variable_name,
    formula_by_variable_name,
    level_2_formula_by_variable_name
    )
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_fiscaux_parser import denombrements_fiscaux_df_generator
from ipp_macro_series_parser.data_extraction import get_or_construct_value


def test_run_through():
    years = [2006, 2007, 2008]
    df = denombrements_fiscaux_df_generator(years = years)
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)

    variable_name = 'interets_imposes_au_prelevement_liberatoire'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = years)
    variable_name = 'dividendes_imposes_au_prelevement_liberatoire'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = years)
    variable_name = 'revenus_imposes_au_prelevement_liberatoire'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = years, fill_value = 0)
    variable_name = 'assurances_vie_imposees_au_prelevement_liberatoire'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = years)
    variable_name = 'f2da'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = years)
