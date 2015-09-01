# -*- coding: utf-8 -*-


from py_expression_eval import Parser
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config

from ipp_macro_series_parser.denombrements_fiscaux.denombrements_fiscaux_parser import (
    denombrements_fiscaux_df_generator)
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import look_many, get_or_construct_value

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )


# inputs
year = 2008


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


def build_aggregates(df, formula_by_variable_name, level_2_formula_by_variable_name = None):
    result_data_frame = None
    index_by_variable_name = create_index_by_variable_name(formula_by_variable_name, level_2_formula_by_variable_name)
    for variable_name in formula_by_variable_name.keys() + level_2_formula_by_variable_name.keys():
        # df1 = look_many(df, index_by_variable_name.values())
        serie, formula = get_or_construct_value(df, variable_name, index_by_variable_name, years = [year])
        if result_data_frame is None:
            result_data_frame = serie
        else:
            result_data_frame = pandas.concat([result_data_frame, serie], axis = 1)
    return result_data_frame


formula_by_variable_name = dict(
    salaires = 'f1aj + f1bj + f1cj + f1dj + f1ej + f1au + f1bu + f1cu + f1du',
    benefices_agricoles_forfait_exoneres = 'f5hn + f5in + f5jn',  # frag_exon
    benefices_agricoles_forfait_imposables = 'f5ho + f5io + f5jo',  # frag_impo
    benefices_agricoles_reels_exoneres = 'f5hb + f5ib + f5jb',  # arag_exon
    benefices_agricoles_reels_imposables = 'f5hc + f5ic + f5jc',  # arag_impg
    benefices_agricoles_reels_deficits = 'f5hf + f5if + f5jf',  # arag_defi
    benefices_agricoles_reels_sans_cga_exoneres = 'f5hh + f5ih + f5jh',  # nrag_exon
    benefices_agricoles_reels_sans_cga_imposables = 'f5hi + f5ii + f5ji',  # nrag_impg
    # TODO voir années antérieurs à 2006
    benefices_agricoles_reels_sans_cga_deficits = 'f5hl + f5il + f5jl',  # nrag_defi
    # benefices_agricoles_  = 'f5hm + f5im + f5jm',  # nrag_ajag
    revenus_fonciers_regime_normal = 'f4ba',
    revenus_fonciers_micro_foncier = 'f4be',
    allocations_chomage = 'f1ap + f1bp + f1cp + f1dp + f1ep + f1fp',
    pensions_de_retraite = 'f1as + f1bs + f1cs + f1ds + f1es + f1fs',
    dividendes_imposes_au_bareme = 'f2dc + f2fu',
    interest_imposes_au_bareme = 'f2ts + f2go + f2tr',
    assurences_vie_imposees_au_bareme = 'f2ch',
    dividendes_imposes_au_prelevement_liberatoire = 'f2da',
    interets_imposes_au_prelevement_liberatoire = 'f2ee',
    assurences_vie_imposees_au_prelevement_liberatoire = 'f2dh',
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
    revenus_imposes_au_bareme = 'dividendes_imposes_au_bareme + interest_imposes_au_bareme + assurences_vie_imposees_au_bareme',  # analysis:ignore
    revenus_imposes_au_prelevement_liberatoire = 'dividendes_imposes_au_prelevement_liberatoire + interets_imposes_au_prelevement_liberatoire + assurences_vie_imposees_au_prelevement_liberatoire',  #analysis:ignore
    )

df = denombrements_fiscaux_df_generator(year)


result_data_frame = build_aggregates(df, formula_by_variable_name, level_2_formula_by_variable_name)

print result_data_frame

# 1. Tableau IRPP1: Les revenus figurant dans les déclarations de revenus
irrp_1 = result_data_frame[[
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
    ]]

# 2. Tableau IRPP2: Détails des revenus financiers (intérêts, dividendes, plus-values) figurant dans les
# déclations de revenus (imposition au barème, imposition au prélèvement forfaitaire libératoire (PL), et plus-values)

irrp_2 = result_data_frame[[
    'revenus_imposes_au_bareme',
    'dividendes_imposes_au_bareme',
    'interest_imposes_au_bareme',
    'assurences_vie_imposees_au_bareme',
    'revenus_imposes_au_prelevement_liberatoire',
    'dividendes_imposes_au_prelevement_liberatoire',
    'interets_imposes_au_prelevement_liberatoire',
    'assurences_vie_imposees_au_prelevement_liberatoire',
    'plus_values',
    'revenus_financiers',
    'revenus_financiers_hors_plus_values'
    ]]


# 3. Tableau IRPP3: Plus-values mobilières et professionnelles
irrp_3 = result_data_frame[[
    'plus_values',
    'plus_values_mobilieres',
    'plus_values_mobilieres_regime_normal',
    'plus_values_mobilieres_stock_options',
    'plus_values_mobilieres_retraite_dirigeant',
    'plus_values_professionnelles',
    'plus_values_professionnelles_regime_normal',
    'plus_values_professionnelles_retraite_dirigeant',
    ]]


irpp_4 = result_data_frame[[
    'revenus_d_activite_non_salariee',
    'benefices_agricoles',
    'benefices_agricoles_bruts',
    'deficits_agricoles',
    #    'bic',
    #    'bnc',
    #    'revenus_activite_non_salariee_exoneres',
    ]]

irrp_5_ba = result_data_frame[[
    'benefices_agricoles',
    'benefices_agricoles_forfait_exoneres',
    'benefices_agricoles_forfait_imposables',
    'benefices_agricoles_reels_exoneres',
    'benefices_agricoles_reels_imposables',
    'benefices_agricoles_reels_deficits',
    'benefices_agricoles_reels_sans_cga_exoneres',
    'benefices_agricoles_reels_sans_cga_imposables',
    'benefices_agricoles_reels_sans_cga_deficits',
    ]]
boum2
