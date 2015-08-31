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
            result_data_frame = pandas.DataFrame(serie)
        else:
            result_data_frame = pandas.concat([result_data_frame, pandas.DataFrame(serie)], axis = 1)
    return result_data_frame


formula_by_variable_name = dict(
    salaires = 'f1aj + f1bj + f1cj + f1dj + f1ej',
    allocations_chomage = 'f1ap + f1bp + f1cp + f1dp + f1ep + f1fp',
    pensions_de_retraite = 'f1as + f1bs + f1cs + f1ds + f1es + f1fs',
    revenus_fonciers = 'f4be + f4ba',
    dividendes_imposes_au_bareme = 'f2dc + f2fu',
    interest_imposes_au_bareme = 'f2ts + f2go + f2tr',
    assurences_vie_imposes_au_bareme = 'f2ch',
    dividendes_imposes_au_prelevement_liberatoire = 'f2da',
    interets_imposes_au_prelevement_liberatoire = 'f2ee',
    assurences_vie_imposes_au_prelevement_liberatoire = 'f2dh',
    plus_values_mobilieres = 'f3vg + f3vf + f3vi + f3va',  # PV mobilières (régime normal), PV stock options 1, PV stock options 2, PV retraite dirigeant analysis:ignore
    plus_values_professionnelles_regime_normal = 'f5hz + f5iz + f5jz',  # TODO: ceci n'est valable qu'avant 2010
    plus_values_professionnelles_retraite_dirigeant = 'f5hg + f5ig',
    pension_alimentaires_recues = 'f1ao	+ f1bo + f1co + f1do + f1eo + f1fo',
    pensions_alimentaires_versess = 'f6gi + f6gj + f6el + f6em + f6gp + f6gu + f6dd',
    )


level_2_formula_by_variable_name = dict(
    # revenus_d_activite_non_salariee = 'ba + bic + bnc + revenus_activite_non_salariee_exoneres',
    revenus_de_remplacement = 'pensions_de_retraite + allocations_chomage',
    revenus_financiers = 'revenus_imposes_au_bareme + revenus_imposes_au_prelevement_liberatoire + plus_values',
    plus_values = 'plus_values_mobilieres + plus_values_professionnelles',
    plus_values_professionnelles = 'plus_values_professionnelles_regime_normal + plus_values_professionnelles_retraite_dirigeant',  # analysis:ignore
    revenus_imposes_au_bareme = 'dividendes_imposes_au_bareme + interest_imposes_au_bareme + assurences_vie_imposes_au_bareme',  # analysis:ignore
    revenus_imposes_au_prelevement_liberatoire = 'dividendes_imposes_au_prelevement_liberatoire + interets_imposes_au_prelevement_liberatoire + assurences_vie_imposes_au_prelevement_liberatoire',  #analysis:ignore
    )

df = denombrements_fiscaux_df_generator(year)




#serie, formula = get_or_construct_value(df, 'f1aj', index_by_variable = None, years = [year])
#print serie
#print formula

#formula_by_variable_name = create_index_by_variable_name(formula_by_variable_name)
#print formula_by_variable_name
#boum4

result_data_frame = build_aggregates(df, formula_by_variable_name, level_2_formula_by_variable_name).transpose()

print result_data_frame
boum2
