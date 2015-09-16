# -*- coding: utf-8 -*-


# TaxIPP -- A french microsimulation model
# By: IPP <taxipp@oipp.eu>
#
# Copyright (C) 2012, 2013, 2014, 2015 IPP
# https://github.com/taxipp
#
# This file is part of TaxIPP.
#
# TaxIPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# TaxIPP is distributed in the hope that it will be useful,
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

from ipp_macro_series_parser.comptes_nationaux.parser_main import get_comptes_nationaux_data
from ipp_macro_series_parser.data_extraction import (
    look_many, look_up, get_or_construct_value, get_or_construct_data)
from ipp_macro_series_parser.comptes_nationaux.sheets_lists import variables_CN1, variables_CN2

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')
cn_hdf = parser.get('data', 'cn_hdf_directory')
cn_csv = parser.get('data', 'cn_csv_directory')
tests_directory = parser.get('data', 'tests_directory')

tests_data = os.path.join(
    pkg_resources.get_distribution('ipp-macro-series-parser').location,
    'ipp_macro_series_parser/tests/data')

df = get_comptes_nationaux_data(2013)

values_CN1, formulas_CN1 = get_or_construct_data(df, variables_CN1, range(1949, 2014))
values_CN2, formulas_CN2 = get_or_construct_data(df, variables_CN2, range(1949, 2014))
