# -*- coding: utf-8 -*-


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
