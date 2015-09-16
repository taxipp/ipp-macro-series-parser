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


from ipp_macro_series_parser.denombrements_fiscaux.agregats_ipp import (
    create_index_by_variable_name,
    formula_by_variable_name,
    level_2_formula_by_variable_name
    )
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_fiscaux_parser import (
    create_denombrements_fiscaux_data_frame
    )
from ipp_macro_series_parser.data_extraction import get_or_construct_value


def test_run_through():
    years = [2006, 2007, 2008, 2009]
    df = create_denombrements_fiscaux_data_frame(years = years)
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


def test_corrections():
    years = [2006, 2007, 2008, 2009]
    df = create_denombrements_fiscaux_data_frame(years = years)
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)

    test_by_variable = dict(
        # Correction of f5io in 2008 in Agrégats IPP
        benefices_agricoles_forfait_imposables = [
            {'year': 2006, 'target': 896512850},
            {'year': 2008, 'target': 883970587},
            ],
        benefices_agricoles_reels_imposables = [
            {'year': 2006, 'target': 5150417953},
            {'year': 2008, 'target': 6515953706},
            ],
        benefices_agricoles_reels_sans_cga_imposables = [
            {'year': 2006, 'target': 165830038},
            ],
        benefices_agricoles_reels_deficits = [
            {'year': 2006, 'target': 519217942},
            ],
        benefices_agricoles_reels_sans_cga_deficits = [
            {'year': 2006, 'target': 208934263},
            ],
        # deficits_industriels_commerciaux

        )

    def assert_value_construction(variable_name, test):
        year = test['year']
        target = test['target']
        value = get_or_construct_value(df, variable_name, index_by_variable_name, years = years)[0].loc[year]
        assert all(value == target), "{} for {}: got {} instead of {}".format(variable_name, year, value.values, target)

    for variable_name, tests in test_by_variable.iteritems():
        for test in tests:
            yield assert_value_construction, variable_name, test
