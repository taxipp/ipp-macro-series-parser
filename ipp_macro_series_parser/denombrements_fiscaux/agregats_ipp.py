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

import collections
import os
import pandas
import pkg_resources


from py_expression_eval import Parser


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_fiscaux_parser import (
    denombrements_fiscaux_df_generator)
from ipp_macro_series_parser.data_extraction import get_or_construct_value

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )


def create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name = None):
    index_by_variable_name = dict()
    for variable_name, formula in formula_by_variable_name.iteritems():
        parser_formula = Parser()
        if not formula:
            continue
        expr = parser_formula.parse(formula)
        formula_variables = expr.variables()
        components = dict(
            (formula_variable, {'code': formula_variable}) for formula_variable in formula_variables
            )
        index_by_variable_name[variable_name] = {
            'code': None,
            'formula': formula,
            }
        index_by_variable_name.update(components)

    if level_2_formula_by_variable_name is not None:
        level_2_index_by_variable_name = dict()
        for variable_name, formula in level_2_formula_by_variable_name.iteritems():
            level_2_index_by_variable_name[variable_name] = dict(
                formula = formula,
                )

        index_by_variable_name.update(level_2_index_by_variable_name)
    return index_by_variable_name


def build_aggregates(raw_data, formula_by_variable_name, level_2_formula_by_variable_name = None, fill_value = 0):
    aggregates = None
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)
    for variable_name in formula_by_variable_name.keys() + level_2_formula_by_variable_name.keys():
        # raw_data1 = look_many(raw_data, index_by_variable_name.values())
        serie, formula = get_or_construct_value(
            raw_data, variable_name, index_by_variable_name, years = years, fill_value = fill_value)
        if aggregates is None:
            aggregates = serie
        else:
            aggregates = pandas.concat([aggregates, serie], axis = 1)
    return aggregates


formula_by_variable_name = dict(
    salaires = 'f1aj + f1bj + f1cj + f1dj + f1ej + f1au + f1bu + f1cu + f1du',
    benefices_agricoles_forfait_exoneres = 'f5hn + f5in + f5jn',  # frag_exon
    benefices_agricoles_forfait_imposables = 'f5ho + f5io + f5jo',  # frag_impo
    benefices_agricoles_reels_exoneres = 'f5hb + f5ib + f5jb',  # arag_exon
    benefices_agricoles_reels_imposables = 'f5hc + f5ic + f5jc + f5hd + f5id + f5jd',  # arag_impg TODO: check last values in openfisca
    benefices_agricoles_reels_deficits = 'f5hf + f5if + f5jf',  # arag_defi
    benefices_agricoles_reels_sans_cga_exoneres = 'f5hh + f5ih + f5jh',  # nrag_exon
    benefices_agricoles_reels_sans_cga_imposables = 'f5hi + f5ii + f5ji + f5hj + f5ij + f5jj',  # nrag_impg TODO: check last values in openfisca
    # TODO voir années antérieurs à 2006
    benefices_agricoles_reels_sans_cga_deficits = 'f5hl + f5il + f5jl',  # nrag_defi
    # benefices_agricoles_  = 'f5hm + f5im + f5jm',  # nrag_ajag
    revenus_fonciers_regime_normal = 'f4ba',
    revenus_fonciers_micro_foncier = 'f4be',
    allocations_chomage = 'f1ap + f1bp + f1cp + f1dp + f1ep + f1fp',
    pensions_de_retraite = 'f1as + f1bs + f1cs + f1ds + f1es + f1fs',
    dividendes_imposes_au_bareme = 'f2dc + f2fu',
    interet_imposes_au_bareme = 'f2ts + f2go + f2tr',
    assurances_vie_imposees_au_bareme = 'f2ch',
    dividendes_imposes_au_prelevement_liberatoire = 'f2da',
    interets_imposes_au_prelevement_liberatoire = 'f2ee',
    assurances_vie_imposees_au_prelevement_liberatoire = 'f2dh',
    plus_values_mobilieres_regime_normal = 'f3vg',
    plus_values_mobilieres_stock_options = 'f3vf + f3vi',  # PV stock options 1, stock options 2, TODO Différencier ?
    plus_values_mobilieres_retraite_dirigeant = 'f3va',  # TODO f3vb ?
    plus_values_professionnelles_regime_normal = 'f5hz + f5iz + f5jz',  # TODO: ceci n'est valable qu'avant 2010
    plus_values_professionnelles_retraite_dirigeant = 'f5hg + f5ig',
    revenus_distribues_pea_exoneres = 'f2gr',
    pension_alimentaires_recues = 'f1ao	+ f1bo + f1co + f1do + f1eo + f1fo',
    pensions_alimentaires_versess = 'f6gi + f6gj + f6el + f6em + f6gp + f6gu + f6dd',
    )


level_2_formula_by_variable_name = dict(
    revenus_d_activite_non_salariee = 'benefices_agricoles',  # + bic + bnc + revenus_activite_non_salariee_exoneres',
    # TODO get parameters form openfisca legislation
    benefices_agricoles = 'benefices_agricoles_bruts - 0.5 * deficits_agricoles',
    benefices_agricoles_bruts = 'benefices_agricoles_forfait_imposables + benefices_agricoles_reels_imposables + 1.25 * benefices_agricoles_reels_sans_cga_imposables',  # TODO get parameters form openfisca legislation
    deficits_agricoles = 'benefices_agricoles_reels_deficits + benefices_agricoles_reels_sans_cga_deficits',
    revenus_fonciers = 'revenus_fonciers_regime_normal + revenus_fonciers_micro_foncier',
    revenus_de_remplacement = 'pensions_de_retraite + allocations_chomage',
    revenus_financiers_hors_plus_values = 'revenus_imposes_au_bareme + revenus_imposes_au_prelevement_liberatoire',
    revenus_financiers = 'revenus_imposes_au_bareme + revenus_imposes_au_prelevement_liberatoire + plus_values',
    plus_values = 'plus_values_mobilieres + plus_values_professionnelles',
    plus_values_mobilieres = 'plus_values_mobilieres_regime_normal + plus_values_mobilieres_stock_options + plus_values_mobilieres_retraite_dirigeant', # analysis:ignore
    plus_values_professionnelles = 'plus_values_professionnelles_regime_normal + plus_values_professionnelles_retraite_dirigeant',  # analysis:ignore
    revenus_imposes_au_bareme = 'dividendes_imposes_au_bareme + interet_imposes_au_bareme + assurances_vie_imposees_au_bareme',  # analysis:ignore
    revenus_imposes_au_prelevement_liberatoire = 'dividendes_imposes_au_prelevement_liberatoire + interets_imposes_au_prelevement_liberatoire + assurances_vie_imposees_au_prelevement_liberatoire',  #analysis:ignore
    )



def build_ipp_tables(years = [2006, 2007, 2008]):
    raw_data = denombrements_fiscaux_df_generator(years = years)
    aggregates = build_aggregates(raw_data, formula_by_variable_name, level_2_formula_by_variable_name)
    data_frame_by_ipp_table_name = collections.OrderedDict([
        # 1. Tableau IRPP1: Les revenus figurant dans les déclarations de revenus
        ('irpp_1', aggregates[[
            'salaires',
            # TODO
            #    'revenus_d_activite_non_salariee'
            #    'ba',
            #    'bic',
            #    'bnc',
            #    'revenus_activite_non_salariee_exoneres',
            'revenus_de_remplacement',
            'pensions_de_retraite',
            'allocations_chomage',
            'revenus_fonciers',
            'revenus_fonciers_regime_normal',
            'revenus_fonciers_micro_foncier',
            'revenus_financiers'
            ]]),
        # 2. Tableau IRPP2: Détails des revenus financiers (intérêts, dividendes, plus-values) figurant dans les
        # déclations de revenus (imposition au barème, imposition au prélèvement forfaitaire libératoire (PL) et
        # plus-values)
        ('irpp_2', aggregates[[
            'revenus_imposes_au_bareme',
            'dividendes_imposes_au_bareme',
            'interet_imposes_au_bareme',
            'assurances_vie_imposees_au_bareme',
            'revenus_imposes_au_prelevement_liberatoire',
            'dividendes_imposes_au_prelevement_liberatoire',
            'interets_imposes_au_prelevement_liberatoire',
            'assurances_vie_imposees_au_prelevement_liberatoire',
            'plus_values',
            'revenus_financiers',
            'revenus_financiers_hors_plus_values'
            ]]),
        # 3. Tableau IRPP3: Plus-values mobilières et professionnelles
        ('irpp_3', aggregates[[
            'plus_values',
            'plus_values_mobilieres',
            'plus_values_mobilieres_regime_normal',
            'plus_values_mobilieres_stock_options',
            'plus_values_mobilieres_retraite_dirigeant',
            'plus_values_professionnelles',
            'plus_values_professionnelles_regime_normal',
            'plus_values_professionnelles_retraite_dirigeant',
            ]]),
        ('irpp_4', aggregates[[
            'revenus_d_activite_non_salariee',
            'benefices_agricoles',
            'benefices_agricoles_bruts',
            'deficits_agricoles',
            #    'bic',
            #    'bnc',
            #    'revenus_activite_non_salariee_exoneres',
            ]]),
        ('irpp_5_ba', aggregates[[
            'benefices_agricoles',
            'benefices_agricoles_forfait_exoneres',
            'benefices_agricoles_forfait_imposables',
            'benefices_agricoles_reels_exoneres',
            'benefices_agricoles_reels_imposables',
            'benefices_agricoles_reels_deficits',
            'benefices_agricoles_reels_sans_cga_exoneres',
            'benefices_agricoles_reels_sans_cga_imposables',
            'benefices_agricoles_reels_sans_cga_deficits',
            ]])
        ])
    return data_frame_by_ipp_table_name
