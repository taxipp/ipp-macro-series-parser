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


import copy
import logging
import pandas
import re


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.input_data_builders.build_openfisca_survey_data.base import (
    year_specific_by_generic_data_frame_name)

from openfisca_survey_manager.survey_collections import SurveyCollection

from ipp_macro_series_parser.denombrements_fiscaux.agregats_ipp import (
    build_ipp_tables,
    create_index_by_variable_name,
    formula_by_variable_name,
    level_2_formula_by_variable_name
    )
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_fiscaux_parser import (
    denombrements_fiscaux_df_generator
    )
from ipp_macro_series_parser.data_extraction import get_or_construct_value


log = logging.getLogger(__name__)


def test(year = None):
    assert year is not None
    erfs_survey_collection = SurveyCollection.load(
        collection = 'erfs', config_files_directory = config_files_directory)

    year_specific_by_generic = year_specific_by_generic_data_frame_name(year)
    survey = erfs_survey_collection.get_survey('erfs_{}'.format(year))

    erf_individus = survey.get_values(
        table = year_specific_by_generic["erf_indivi"],
        variables = ['noindiv', 'wprm'],
        )
    foyer = survey.get_values(table = year_specific_by_generic["foyer"])
    # rename variable to fxzz ou ^f[0-9][a-z]{2}")
    regex = re.compile("^_[0-9][a-z]{2}")
    new_variable_name_by_old = dict(
        (x, "f{}".format(x[1:])) for x in foyer.columns if regex.match(x))
    foyer.rename(columns = new_variable_name_by_old, inplace = True)
    assert set(foyer.noindiv.values).issubset(set(erf_individus.noindiv.values))
    foyer = foyer.merge(erf_individus, on = 'noindiv')

    years = [year]
    df = denombrements_fiscaux_df_generator(years = years)
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)

    result = pandas.DataFrame()

    variables_name = [
        'salaires',
        'allocations_chomage',
        'pensions_de_retraite',
        ]

    for variable_name in variables_name:
        aggregates, _ = get_or_construct_value(df, variable_name, index_by_variable_name.copy(), years = years)

        dgfip = aggregates.loc[year] / 1e9

        if isinstance(index_by_variable_name[variable_name]['formula'], list):
            for formula_by_key in index_by_variable_name[variable_name]['formula']:
                if formula_by_key['start'] <= year <= formula_by_key['end']:
                    formula = formula_by_key['formula']
            assert formula
        else:
            formula = index_by_variable_name[variable_name]['formula']
        print variable_name
        print formula
        erf = (((foyer.eval(formula)).abs() < 1e9) * foyer.eval(formula) * foyer.wprm).sum() / 1e9

        result_update = pandas.DataFrame(dict(
            erf = erf,
            dgfip = dgfip,
            year = year,
            variable = variable_name,
            ))
        result = pandas.concat((result_update, result))
    print result
    return result

if __name__ == '__main__':

    result = test(year = 2009)
    # data_frame_by_ipp_table_name = build_ipp_tables()
