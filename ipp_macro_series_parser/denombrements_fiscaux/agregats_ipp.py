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
from ipp_macro_series_parser.denombrements_fiscaux.parsers import (
    create_denombrements_fiscaux_data_frame)
from ipp_macro_series_parser.data_extraction import get_or_construct_value

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )


def update_index_by_variable_name_appearing_in_formula(index_by_variable_name, formula):
    parser_formula = Parser()
    expr = parser_formula.parse(formula)
    formula_variables = expr.variables()
    components = dict(
        (formula_variable, {'code': formula_variable}) for formula_variable in formula_variables
        )
    index_by_variable_name.update(components)
    return index_by_variable_name


def create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name = None):
    index_by_variable_name = dict()
    for variable_name, formula in formula_by_variable_name.iteritems():
        if not formula:
            continue
        index_by_variable_name[variable_name] = {
            'code': None,
            'formula': formula,
            }

        if isinstance(formula, list):
            for single_formula in formula:
                index_by_variable_name = update_index_by_variable_name_appearing_in_formula(
                    index_by_variable_name, single_formula['formula'])
        else:
            index_by_variable_name = update_index_by_variable_name_appearing_in_formula(index_by_variable_name, formula)

    if level_2_formula_by_variable_name is not None:
        level_2_index_by_variable_name = dict()
        for variable_name, formula in level_2_formula_by_variable_name.iteritems():
            level_2_index_by_variable_name[variable_name] = dict(
                formula = formula,
                )

        index_by_variable_name.update(level_2_index_by_variable_name)
    return index_by_variable_name


def build_aggregates(raw_data, formula_by_variable_name, level_2_formula_by_variable_name = None, years = None,
        fill_value = 0):
    assert years is not None
    aggregates = None
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)
    for variable_name in formula_by_variable_name.keys() + level_2_formula_by_variable_name.keys():
        serie, formula = get_or_construct_value(
            raw_data, variable_name, index_by_variable_name, years = years, fill_value = fill_value)
        if aggregates is None:
            aggregates = serie
        else:
            aggregates = pandas.concat([aggregates, serie], axis = 1)
    return aggregates


formula_by_variable_name = dict(
    ## Salaires
    salaires = [
        dict(
            start = 1990,
            end = 2004,
            formula = 'f1aj + f1bj + f1cj + f1dj + f1ej',
            ),
        dict(
            start = 2005,
            end = 2006,
            formula = 'f1aj + f1bj + f1cj + f1dj',
            ),
        dict(
            start = 2007,
            end = 2010,
            formula = 'f1aj + f1bj + f1cj + f1au + f1bu + f1cu + f1du',
            ),
        ],
    ## Bénéfices agricoles
    benefices_agricoles_forfait_exoneres = 'f5hn + f5in + f5jn',  # frag_exon
    benefices_agricoles_forfait_imposables = 'f5ho + f5io + f5jo',  # frag_impo
    benefices_agricoles_reels_exoneres = 'f5hb + f5ib + f5jb',  # arag_exon
    benefices_agricoles_reels_imposables = [
        dict(
            start = 1990,
            end = 2005,
            formula = 'f5hc + f5ic + f5jc + f5hd + f5id + f5jd'
            ),
        dict(
            start = 2006,
            end = 2015,
            formula = 'f5hc + f5ic + f5jc'
            ),
        ],  # arag_impg TODO: check last values in openfisca
    benefices_agricoles_reels_deficits = 'f5hf + f5if + f5jf',  # arag_defi
    benefices_agricoles_reels_sans_cga_exoneres = 'f5hh + f5ih + f5jh',  # nrag_exon
    benefices_agricoles_reels_sans_cga_imposables = [
        dict(
            start = 1990,
            end = 2005,
            formula = 'f5hi + f5ii + f5ji + f5hj + f5ij + f5jj',
            ),
        dict(
            start = 2006,
            end = 2015,
            formula = 'f5hi + f5ii + f5ji',
            ),
        ],  # nrag_impg TODO: check last values in openfisca
    # TODO voir années antérieurs à 2006
    benefices_agricoles_reels_sans_cga_deficits = 'f5hl + f5il + f5jl',  # nrag_defi
    # TODO: benefices_agricoles_  = 'f5hm + f5im + f5jm',  # nrag_ajag
    ## Bénéfices industriels et commerciaux professionnels (déclaration complémentaire, cadres 5B)
    benefices_industriels_commerciaux_professionnels_micro_entreprise_vente = 'f5ko + f5lo + f5mo',
    benefices_industriels_commerciaux_professionnels_micro_entreprise_services = 'f5kp + f5lp + f5mp',
    benefices_industriels_commerciaux_professionnels_reels_exoneres = 'f5kb + f5lb + f5mb',
    benefices_industriels_commerciaux_professionnels_reels_imposables_normal = 'f5kc + f5lc + f5mc',
    benefices_industriels_commerciaux_professionnels_reels_imposables_simplifie = 'f5kd + f5ld + f5md',
    benefices_industriels_commerciaux_professionnels_reels_exoneres_sans_cga = 'f5kh + f5lh + f5mh',
    benefices_industriels_commerciaux_professionnels_reels_imposables_normal_sans_cga = 'f5ki + f5li + f5mi',
    benefices_industriels_commerciaux_professionnels_reels_imposables_simplifie_sans_cga = 'f5kj + f5lj + f5mj',
    deficits_industriels_commerciaux_professionnels_normal = 'f5kf + f5lf + f5mf',
    deficits_industriels_commerciaux_professionnels_simplifie = 'f5kg + f5lg + f5mg',
    deficits_industriels_commerciaux_professionnels_sans_cga = 'f5kl + f5ll + f5ml',
    deficits_industriels_commerciaux_professionnels_locations = [
        dict(
            start = 1990,
            end = 2008,
            formula = 'f5km + f5lm + f5mm',
            ),
        ],
    ## Bénéfices industriels et commerciaux non professionnels (déclaration complémentaire, cadres 5C)
    benefices_industriels_commerciaux_non_professionnels_micro_entreprise_exoneres = 'f5nn + f5on + f5pn',
    benefices_industriels_commerciaux_non_professionnels_micro_entreprise_vente = 'f5no + f5oo + f5po',
    benefices_industriels_commerciaux_non_professionnels_micro_entreprise_services = 'f5np + f5op + f5op',
    benefices_industriels_commerciaux_non_professionnels_reels_exoneres = 'f5nb + f5ob + f5pb',
    benefices_industriels_commerciaux_non_professionnels_reels_imposables_normal = 'f5nc + f5nc + f5nc',
    benefices_industriels_commerciaux_non_professionnels_reels_imposables_simplifie = 'f5nd + f5nd + f5nd',  # TODO: ceci avant 2010 mais après locations meublées pro,
    benefices_industriels_commerciaux_non_professionnels_reels_exoneres_sans_cga = 'f5nh + f5oh + f5ph',
    benefices_industriels_commerciaux_non_professionnels_reels_imposables_normal_sans_cga = 'f5ni + f5ni + f5ni',
    benefices_industriels_commerciaux_non_professionnels_reels_imposables_simplifie_sans_cga = 'f5nj + f5nj + f5nj',  # TODO: ceci avant 2012 mais après locations déjà soumises aux prélèvements sociaux,
    deficits_industriels_commerciaux_non_professionnels_normal = 'f5nf + f5of + f5pf',
    deficits_industriels_commerciaux_non_professionnels_simplifie = 'f5og + f5og + f5pg',
    deficits_industriels_commerciaux_non_professionnels_sans_cga = 'f5nl + f5ol + f5pl',
    # TODO: Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)

    # - Détails Bénéfices non commerciaux professionnels (déclaration complémentaire, cadres 5D)

    benefices_non_commerciaux_professionnels_micro_entreprise_imposables = 'f5hq + f5iq + f5jq',
    benefices_non_commerciaux_professionnels_declaration_controlee = 'f5qc + f5rc + f5sc',
    benefices_non_commerciaux_professionnels_declaration_controlee_sans_cga = 'f5qi + f5ri + f5si',
    deficits_non_commerciaux_professionnels_declaration_controlee = 'f5qe + f5re + f5se',
    deficits_non_commerciaux_professionnels_declaration_controlee_sans_cga = 'f5qk + f5rk + f5sk',

    # - Détails Bénéfices non commerciaux non professionnels (déclaration complémentaire, cadres 5E)
    benefices_non_commerciaux_non_professionnels_micro_entreprise_imposables = 'f5ku + f5lu + f5mu',
    benefices_non_commerciaux_non_professionnels_declaration_controlee = 'f5jg + f5rf + f5sf',
    benefices_non_commerciaux_non_professionnels_declaration_controlee_sans_cga = 'f5sn + f5ns + f5os',
    deficits_non_commerciaux_non_professionnels_declaration_controlee = 'f5jj + f5rg + f5sg',
    deficits_non_commerciaux_non_professionnels_declaration_controlee_sans_cga = 'f5sp + f5nu + f5ou',

    revenus_fonciers_regime_normal = 'f4ba',
    revenus_fonciers_micro_foncier = 'f4be',
    allocations_chomage = [
        dict(
            start = 2007,
            end = 2009,
            formula = 'f1ap + f1bp + f1cp + f1dp',
            ),
        dict(
            start = 2005,
            end = 2006,
            formula = 'f1ap + f1bp + f1cp + f1dp + f1ep',
            ),
        dict(
            start = 2000,
            end = 2004,
            formula = 'f1ap + f1bp + f1cp + f1dp + f1ep + f1fp',
            ),
        ],
    pensions_de_retraite = [
        dict(
            start = 2007,
            end = 2009,
            formula = 'f1as + f1bs + f1cs + f1ds',
            ),
        dict(
            start = 2005,
            end = 2006,
            formula = 'f1as + f1bs + f1cs + f1ds + f1es',
            ),
        dict(
            start = 2000,
            end = 2004,
            formula = 'f1as + f1bs + f1cs + f1ds + f1es + f1fs',
            ),
        ],
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
    revenus_d_activite_non_salariee = 'benefices_agricoles + benefices_industriels_commerciaux + benefices_non_commerciaux', # + revenus_activite_non_salariee_exoneres',
    # TODO get parameters form openfisca legislation
    benefices_agricoles = 'benefices_agricoles_bruts - 0.5 * deficits_agricoles',
    benefices_agricoles_bruts = 'benefices_agricoles_forfait_imposables + benefices_agricoles_reels_imposables + 1.25 * benefices_agricoles_reels_sans_cga_imposables',  # TODO get parameters form openfisca legislation
    deficits_agricoles = 'benefices_agricoles_reels_deficits + benefices_agricoles_reels_sans_cga_deficits',

    # Bénéfices industriels et commerciaux
    benefices_industriels_commerciaux =  'benefices_industriels_commerciaux_professionnels + benefices_industriels_commerciaux_non_professionnels',
    benefices_industriels_commerciaux_bruts = 'benefices_industriels_commerciaux_professionnels_bruts + benefices_industriels_commerciaux_non_professionnels_bruts',
    deficits_industriels_commerciaux = 'deficits_industriels_commerciaux_professionnels + deficits_industriels_commerciaux_non_professionnels',
    # - Bénéfices industriels et commerciaux professionnels
    benefices_industriels_commerciaux_professionnels = 'benefices_industriels_commerciaux_professionnels_bruts  - 0.5 * deficits_industriels_commerciaux_professionnels',
    benefices_industriels_commerciaux_professionnels_bruts = 'benefices_industriels_commerciaux_professionnels_micro_entreprise + benefices_industriels_commerciaux_professionnels_reels',
    benefices_industriels_commerciaux_professionnels_micro_entreprise = '(1 - 0.71) * benefices_industriels_commerciaux_professionnels_micro_entreprise_vente + (1 - 0.5) * benefices_industriels_commerciaux_professionnels_micro_entreprise_services',  # TODO check and use legislation parameters
    benefices_industriels_commerciaux_professionnels_reels = 'benefices_industriels_commerciaux_professionnels_reels_avec_cga + benefices_industriels_commerciaux_professionnels_reels_sans_cga',
    benefices_industriels_commerciaux_professionnels_reels_avec_cga = 'benefices_industriels_commerciaux_professionnels_reels_imposables_normal + benefices_industriels_commerciaux_professionnels_reels_imposables_simplifie',
    benefices_industriels_commerciaux_professionnels_reels_sans_cga = '1.25 * (benefices_industriels_commerciaux_professionnels_reels_imposables_normal_sans_cga + benefices_industriels_commerciaux_professionnels_reels_imposables_simplifie_sans_cga)', # TODO check and use legislation
    deficits_industriels_commerciaux_professionnels = 'deficits_industriels_commerciaux_professionnels_normal + deficits_industriels_commerciaux_professionnels_simplifie + deficits_industriels_commerciaux_professionnels_sans_cga + deficits_industriels_commerciaux_professionnels_locations',

    # - Bénéfices industriels et commerciaux non professionnels (déclaration complémentaire, cadres 5C)
    benefices_industriels_commerciaux_non_professionnels = 'benefices_industriels_commerciaux_non_professionnels_bruts  - 0.5 * deficits_industriels_commerciaux_non_professionnels',
    benefices_industriels_commerciaux_non_professionnels_bruts = 'benefices_industriels_commerciaux_non_professionnels_micro_entreprise + benefices_industriels_commerciaux_non_professionnels_reels',
    benefices_industriels_commerciaux_non_professionnels_micro_entreprise = '(1 - 0.71) * benefices_industriels_commerciaux_non_professionnels_micro_entreprise_vente + (1 - 0.5) * benefices_industriels_commerciaux_non_professionnels_micro_entreprise_services',  # TODO check and use legislation parameters
    benefices_industriels_commerciaux_non_professionnels_reels = 'benefices_industriels_commerciaux_non_professionnels_reels_avec_cga + benefices_industriels_commerciaux_non_professionnels_reels_sans_cga',
    benefices_industriels_commerciaux_non_professionnels_reels_avec_cga = 'benefices_industriels_commerciaux_non_professionnels_reels_imposables_normal + benefices_industriels_commerciaux_non_professionnels_reels_imposables_simplifie',
    benefices_industriels_commerciaux_non_professionnels_reels_sans_cga = '1.25 * (benefices_industriels_commerciaux_non_professionnels_reels_imposables_normal_sans_cga + benefices_industriels_commerciaux_non_professionnels_reels_imposables_simplifie_sans_cga)', # TODO check and use legislation

    # Bénéfices non commerciaux
    benefices_non_commerciaux = 'benefices_non_commerciaux_professionnels + benefices_non_commerciaux_non_professionnels',
    benefices_non_commerciaux_bruts = 'benefices_non_commerciaux_professionnels_bruts + benefices_non_commerciaux_non_professionnels_bruts',
    deficits_non_commerciaux = 'deficits_non_commerciaux_professionnels + deficits_non_commerciaux_non_professionnels',
    deficits_industriels_commerciaux_non_professionnels = 'deficits_industriels_commerciaux_non_professionnels_normal + deficits_industriels_commerciaux_non_professionnels_simplifie + deficits_industriels_commerciaux_non_professionnels_sans_cga',

    # - Bénéfices non commerciaux professionnels (déclaration complémentaire, cadres 5D)
    benefices_non_commerciaux_professionnels = 'benefices_non_commerciaux_professionnels_bruts  - 0.5 * deficits_non_commerciaux_professionnels',
    benefices_non_commerciaux_professionnels_bruts = '(1 - 0.34) * benefices_non_commerciaux_professionnels_micro_entreprise_imposables + benefices_non_commerciaux_professionnels_declaration_controlee + 1.25 * benefices_non_commerciaux_professionnels_declaration_controlee_sans_cga',
    deficits_non_commerciaux_professionnels = 'deficits_non_commerciaux_professionnels_declaration_controlee + deficits_non_commerciaux_professionnels_declaration_controlee_sans_cga',

    # - Bénéfices non commerciaux non professionnels (déclaration complémentaire, cadres 5E)
    benefices_non_commerciaux_non_professionnels = 'benefices_non_commerciaux_non_professionnels_bruts  - 0.5 * deficits_non_commerciaux_non_professionnels',
    benefices_non_commerciaux_non_professionnels_bruts = '(1 - 0.34) * benefices_non_commerciaux_non_professionnels_micro_entreprise_imposables + benefices_non_commerciaux_non_professionnels_declaration_controlee + 1.25 * benefices_non_commerciaux_non_professionnels_declaration_controlee_sans_cga',
    deficits_non_commerciaux_non_professionnels = 'deficits_non_commerciaux_non_professionnels_declaration_controlee + deficits_non_commerciaux_non_professionnels_declaration_controlee_sans_cga',

    # Revenus Fonciers
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


def build_ipp_tables(years = [2006, 2007, 2008, 2009]):
    raw_data = create_denombrements_fiscaux_data_frame(years = years)
    aggregates = build_aggregates(
        raw_data,
        formula_by_variable_name,
        level_2_formula_by_variable_name = level_2_formula_by_variable_name,
        years = years)
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
            'benefices_industriels_commerciaux',
            'benefices_industriels_commerciaux_bruts',
            'deficits_industriels_commerciaux',
            #    'bnc',
            #    'revenus_activite_non_salariee_exoneres',
            ]]),
        #        ('irpp_5_a', aggregates[[
        #            'benefices_agricoles',
        #            'benefices_agricoles_forfait_exoneres',
        #            'benefices_agricoles_forfait_imposables',
        #            'benefices_agricoles_reels_exoneres',
        #            'benefices_agricoles_reels_imposables',
        #            'benefices_agricoles_reels_deficits',
        #            'benefices_agricoles_reels_sans_cga_exoneres',
        #            'benefices_agricoles_reels_sans_cga_imposables',
        #            'benefices_agricoles_reels_sans_cga_deficits',
        #            ]])
        ])
    return data_frame_by_ipp_table_name
