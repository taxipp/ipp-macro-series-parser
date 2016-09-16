# -*- coding: utf-8 -*-


from ipp_macro_series_parser.denombrements_fiscaux.agregats_ipp import (
    create_index_by_variable_name,
    formula_by_variable_name,
    level_2_formula_by_variable_name
    )
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_parsers import (
    get_denombrements_fiscaux_data_frame
    )
from ipp_macro_series_parser.data_extraction import get_or_construct_value


def test_run_through():
    years = [2006, 2007, 2008, 2009, 2010, 2011]
    df = get_denombrements_fiscaux_data_frame(years = years)
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
    variable_name = u'f5he'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = range(2010, 2012))
    variable_name = u'f5jr'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = range(2007, 2012), fill_value = 0)
    variable_name = 'plus_values_professionnelles_regime_normal'
    get_or_construct_value(df, variable_name, index_by_variable_name, years = range(2007, 2012), fill_value = 0)


def test_corrections():
    years = range(2006, 2013)
    df = get_denombrements_fiscaux_data_frame(years = years)
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
        benefices_agricoles_reels_imposables_sans_cga = [
            {'year': 2006, 'target': 165830038},
            ],
        benefices_agricoles_reels_deficits = [
            {'year': 2006, 'target': 519217942},
            ],
        benefices_agricoles_reels_sans_cga_deficits = [
            {'year': 2006, 'target': 208934263},
            ],
        deficits_industriels_commerciaux_professionnels = [
            {'year': 2006, 'target': 1427052021},
            ],
        deficits_industriels_commerciaux_non_professionnels = [
            {'year': 2006, 'target': 301194784},
            ],
        plus_values_mobilieres_stock_options = [
            {'year': 2008, 'target': 228873359},
            # {'year': 2010, 'target': 690459289}, TODO: check dénombremenst DGFIP vs IPP
            ],
        revenus_imposes_au_bareme = [
            {'year': 2010, 'target': 18907148239},
            ],
        plus_values_mobilieres_regime_normal = [
            {'year': 2010, 'target': 5393808406},
            ],
        plus_values_professionnelles_regime_normal = [
            {'year': 2011, 'target': 1101248065},
            {'year': 2010, 'target': 1083102431},
            ],
        # Inversion 2ch et 2gr dans dénombrements fiscax (Agrégats IPP et en ligne)
        assurances_vie_imposees_au_bareme = [
            {'year': 2009, 'target': 1063726777},
            ],
        # Test revenus exonérés
        benefices_agricoles_forfait_exoneres = [
            {'year': 2011, 'target': (5826752 + 466632 + 467)},
            ],
        benefices_agricoles_reels_exoneres = [
            {'year': 2011, 'target': (64880784 + 15074222 + 3733)},
            ],
        benefices_agricoles_reels_exoneres_sans_cga = [
            {'year': 2011, 'target': (10214497 + 2275427 + 171787)},
            ],
        
        )

    def assert_value_construction(variable_name, test):
        year = test['year']
        target = test['target']
        value = get_or_construct_value(
            df, variable_name, index_by_variable_name, years = years, fill_value = 0)[0].loc[year]
        if year >= 2009:
            assert all(value == target), "{} for {}: got {} instead of {}".format(
                variable_name, year, value.values, target)

    for variable_name, tests in test_by_variable.iteritems():
        for test in tests:
            yield assert_value_construction, variable_name, test
