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
from ipp_macro_series_parser.denombrements_fiscaux.test_denombrements import irpp_1


config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
file_path = os.path.join(xls_directory, u"Agrégats IPP - Données fiscales.xls")


def error_msg(variable, year, target, actual):
    msg = '''
On year {}, error on variable {}:
should be {} instead of {}
'''.format(variable, year, target, actual)
    return msg


year = 2008

df = pandas.read_excel(
    file_path,
    'calculs calage',
    index_col = 0,
    skiprows = 22,
    header = 1,
    skip_footer = 40,
    parse_cols = 'A:O').iloc[1:20]

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

df.rename(columns = slugified_name_by_long_name, inplace = True)
df.index.name = 'year'

for year in irpp_1.index:
    for variable in irpp_1.columns:
        target = df.loc[year, variable]
        actual = irpp_1.loc[year, variable] / 1e9
        assert abs(target - actual) <= 1e-6, error_msg(variable, year, target, actual)
