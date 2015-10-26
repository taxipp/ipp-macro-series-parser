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


from ipp_macro_series_parser.demographie.parser import (
    create_demographie_data_frame
    )


def test_demographie():
    data_frame = create_demographie_data_frame()
    years = range(1999, 2015 + 1)

    ensemble_by_year = {
        1999: 60122665,
        2008: 63961859,
        2012: 65241241
        }
    for year in years:
        expr = '(year == {}) & (variable == "Ensemble") & (champ == "France")'.format(year)

        target = ensemble_by_year.get(year, None)
        if target is not None:
            assert data_frame.query(expr)['value'].sum() == target, "Wrong France population in {}".format(year)


if __name__ == "__main__":
    test_demographie()
