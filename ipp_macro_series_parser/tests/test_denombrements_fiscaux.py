# -*- coding: utf-8 -*-


import logging
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.denombrements_fiscaux.agregats_ipp import build_irpp_tables


log = logging.getLogger(__name__)


config_parser = Config()
xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
file_path = os.path.join(xls_directory, u"Agrégats IPP - Données fiscales.xls")
sheetname = 'calculs calage'


def error_msg(irpp_table_name, variable, year, target, actual):
    msg = '''
In table {} on year {}, error on variable {}:
should be {} instead of {}
'''.format(irpp_table_name, year, variable, target, actual)
    return msg

fill_value = 0


def check_nan_log_msg(table_name, data_frame):

    data_frame = data_frame.reset_index()
    data_frame = data_frame.loc[
        (data_frame.year >= 2008) & (data_frame.year <= 2011)
        ].set_index('year')
    if not data_frame.notnull().all().all():
        log.info('{} has NaN variables:\n {} \n'.format(
            table_name,
            data_frame[
                data_frame.isnull().any(axis=1) & ~data_frame.isnull().all(axis=1)
                ].T
            ))


def build_original_irpp_tables():

    # Table 1
    slugified_name_by_long_name = {
        u"Revenu déclaré total": 'revenu_declare_total',
        u"Salaires": 'salaires',
        u"Revenus d'activité non salariée": 'revenus_d_activite_non_salariee',
        u"dont bénéfices agricoles": 'benefices_agricoles',
        u"dont bénéfices industriels et commerc.": 'bic',
        u"dont bénéfices non commerc. (prof.lib.)": 'bnc',
        u"dont revenus exonérés": 'revenus_activite_non_salariee_exoneres',
        u"Revenus de remplacement": 'revenus_de_remplacement',
        u"dont pensions de retraite": 'pensions_de_retraite',
        u"dont alloc. chômage  ": 'allocations_chomage',
        u"Revenus fonciers (loyers)": 'revenus_fonciers',
        u"dont régime normal": 'revenus_fonciers_regime_normal',
        u"dont régime micro foncier": 'revenus_fonciers_micro_foncier',
        u"Revenus financiers (intérêts, dividendes,  plus-values) ": 'revenus_financiers',
        }

    irpp_1 = pandas.read_excel(
        file_path,
        sheetname,
        index_col = 0,
        skiprows = 22,
        header = 1,
        parse_cols = 'A:O').iloc[1:20]
    irpp_1.rename(columns = slugified_name_by_long_name, inplace = True)
    irpp_1.index.name = 'year'
    check_nan_log_msg('irpp_1', irpp_1)
    irpp_1.loc[2009, 'revenus_financiers'] = 39.334742586

    # Table 2
    slugified_name_by_long_name.update({
        u'Dividendes ': 'dividendes_imposes_au_bareme',
        u'Intérêts': 'interet_imposes_au_bareme',
        u'Revenus AV': 'assurances_vie_imposees_au_bareme',
        u'Total (avant abat.)': 'revenus_imposes_au_bareme',
        # u'Total (après abat.)': None,
        u'Dividendes .1': 'dividendes_imposes_au_prelevement_liberatoire',
        u'Intérêts.1': 'interets_imposes_au_prelevement_liberatoire',
        u'Revenus AV.1': 'assurances_vie_imposees_au_prelevement_liberatoire',
        u'Total*': 'revenus_imposes_au_prelevement_liberatoire',
        u'Unnamed: 10': 'plus_values',
        u'Unnamed: 11': 'revenus_financiers',
        u'Unnamed: 12': 'revenus_financiers_hors_plus_values',
        })

    irpp_2 = pandas.read_excel(
        file_path,
        sheetname,
        index_col = 0,
        skiprows = 54,
        header = 1,
        parse_cols = 'A:M').iloc[1:20]
    irpp_2.rename(columns = slugified_name_by_long_name, inplace = True)
    irpp_2.index.name = 'year'
    del irpp_2[u'Total (après abat.)']
    check_nan_log_msg('irpp_2', irpp_2)
    # Fix issue #34 inversion 2CH et 2GR en 2009
    irpp_2.loc[2009, 'assurances_vie_imposees_au_bareme'] = 1.063726777
    irpp_2.loc[2009, 'revenus_imposes_au_bareme'] = 18.642426901
    irpp_2.loc[2009, 'revenus_financiers'] = 39.334742586
    irpp_2.loc[2009, 'revenus_financiers_hors_plus_values'] = 31.316215196

    # Table 3
    slugified_name_by_long_name.update({
        u'Total  Plus-values': 'plus_values',
        u'PV mobilières (régime normal)': 'plus_values_mobilieres_regime_normal',
        u'PV stock options 1': 'pv_stock_options_1',
        u'PV stock options 2': 'pv_stock_options_2',
        # 'plus_values_mobilieres_stock_options' sum of both see below
        u'PV retraite dirigeant': 'plus_values_mobilieres_retraite_dirigeant',
        u'PV profess. (régime normal)*': 'plus_values_professionnelles_regime_normal',
        u'PV profess. (retraite dirigeant)': 'plus_values_professionnelles_retraite_dirigeant',
        # u'div PEA exo'
        })

    irpp_3 = pandas.read_excel(
        file_path,
        sheetname,
        index_col = 0,
        skiprows = 81,
        header = 0,
        parse_cols = 'A:I').iloc[1:20]
    irpp_3.rename(columns = slugified_name_by_long_name, inplace = True)
    irpp_3.index.name = 'year'
    irpp_3['plus_values_mobilieres_stock_options'] = irpp_3.pv_stock_options_1 + irpp_3.pv_stock_options_2
    check_nan_log_msg('irpp_3', irpp_3)
    # plus_values_professionnelles_regime_normal = 'f5hz + f5iz + f5jz' pas valabe après 2010

    # Table 4
    slugified_name_by_long_name.update({
        u"Revenus d'activité non salariée": 'revenus_d_activite_non_salariee',
        u'BA': 'benefices_agricoles',
        u'BIC': 'benefices_industriels_commerciaux',
        u'BNC': 'benefices_non_commerciaux',
        #        u'Nonsal exo',
        u'BA brut': 'benefices_agricoles_bruts',
        u'BIC brut': 'benefices_industriels_commerciaux_bruts',
        #        u'BNC brut',
        u'BA def': 'deficits_agricoles',
        u'BIC def': 'deficits_industriels_commerciaux',
        #        u'BNC def',
        #        u'txabt_micro',
        #        u'txabt_micro_service',
        #        u'txabt_microbnc'
        })

    irpp_4 = pandas.read_excel(
        file_path,
        sheetname,
        index_col = 0,
        skiprows = 108,
        header = 0,
        parse_cols = 'A:O').iloc[1:20]
    irpp_4.rename(columns = slugified_name_by_long_name, inplace = True)
    irpp_4.index.name = 'year'
    irpp_4 = irpp_4 / 1e9
    del irpp_4['txabt_micro']
    del irpp_4['txabt_micro_service']
    del irpp_4['txabt_microbnc']
    check_nan_log_msg('irpp_4', irpp_4)

    original_data_frame_by_irpp_table_name = dict(
        irpp_1 = irpp_1,
        irpp_2 = irpp_2,
        irpp_3 = irpp_3,
        irpp_4 = irpp_4,
        )

    return original_data_frame_by_irpp_table_name


def test():
    data_frame_by_irpp_table_name = build_irpp_tables(years = range(2009, 2013), fill_value = 0)
    original_data_frame_by_irpp_table_name = build_original_irpp_tables()

    excluded_variables = [
        'salaires_imposables',
        'heures_supplementaires',
        'frais_reels',
        'pensions_alimentaires_percues',
        'plus_values_mobilieres_stock_options',
        'plus_values_mobilieres',
        'plus_values_professionnelles',
        ]

    messages = list()
    for irpp_table_name, data_frame in data_frame_by_irpp_table_name.iteritems():
        for year in data_frame.index:
            for variable in data_frame.columns:
                if not (2008 <= year <= 2011):
                    continue
                if variable in excluded_variables:
                    continue
                try:
                    target = (
                        original_data_frame_by_irpp_table_name[irpp_table_name].loc[year, variable]
                        )
                except KeyError:
                    print '{} not found for {} in table {}'.format(variable, year, irpp_table_name)
                    continue
                actual = data_frame.fillna(value = fill_value).loc[year, variable] / 1e9
                if not abs(target - actual) / abs(target) <= 1e-3:
                    messages.append(error_msg(irpp_table_name, variable, year, target, actual))

    assert len(messages) == 0, "\nThere are {} errors.".format(len(messages)) + "\n".join(messages)
