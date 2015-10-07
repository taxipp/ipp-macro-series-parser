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


import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.denombrements_fiscaux.agregats_ipp import build_irpp_tables

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
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

    # Table 3
    slugified_name_by_long_name.update({
        u'Total  Plus-values': 'plus_values',
        u'PV mobilières (régime normal)': 'plus_values_mobilieres_regime_normal',
        # u'PV stock options 1',
        # u'PV stock options 2',  'plus_values_mobilieres_stock_options' sum of both
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

    # Table 4
    slugified_name_by_long_name.update({
        u"Revenus d'activité non salariée": 'revenus_d_activite_non_salariee',
        u'BA': 'benefices_agricoles',
        u'BIC': 'benefices_industriels_commerciaux',
        #        u'BNC',
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

    original_data_frame_by_irpp_table_name = dict(
        irpp_1 = irpp_1,
        irpp_2 = irpp_2,
        irpp_3 = irpp_3,
        irpp_4 = irpp_4,
        )

    return original_data_frame_by_irpp_table_name


data_frame_by_irpp_table_name = build_irpp_tables(years = range(2008, 2013), fill_value = 0)
original_data_frame_by_irpp_table_name = build_original_irpp_tables()


excluded_variables = ['plus_values_mobilieres_stock_options', 'plus_values_mobilieres']

messages = list()
for irpp_table_name, data_frame in data_frame_by_irpp_table_name.iteritems():
    for year in data_frame.index:
        for variable in data_frame.columns:
            if (year >= 2014) or year <= 2008:
                continue
            if variable in excluded_variables:
                continue
            try:
                target = (
                    original_data_frame_by_irpp_table_name[irpp_table_name].loc[year, variable]
                    if irpp_table_name != 'irpp_4'
                    else original_data_frame_by_irpp_table_name[irpp_table_name].loc[year, variable] / 1e9
                    )
            except KeyError:
                print '{} not found for {} in table {}'.format(variable, year, irpp_table_name)
                continue
            actual = data_frame.fillna(value = fill_value).loc[year, variable] / 1e9
            if not abs(target - actual) <= 1e-6:
                messages.append(error_msg(irpp_table_name, variable, year, target, actual))

for message in messages:
    print message
