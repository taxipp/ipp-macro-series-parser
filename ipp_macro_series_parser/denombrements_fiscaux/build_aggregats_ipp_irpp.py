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


# Revenu déclaré total
# Salaires
# Revenus d'activité non salariée	dont bénéfices agricoles	dont bénéfices industriels et commerc.	dont bénéfices non commerc. (prof.lib.)	dont revenus exonérés
# Revenus de remplacement	dont pensions de retraite	dont alloc. chômage
# Revenus fonciers (loyers)	dont régime normal	dont régime micro foncier
# Revenus financiers (intérêts, dividendes,  plus-values)

variables = [
    'salaires',
    'revenus_d_activite_non_salariee',
    'revenus_de_remplacement',
    'pensions_de_retraite',
    'allocations_chomage',
    'revenus_fonciers',
    'revenus_financiers',
    'pension_alimentaires_recues',
    'pensions_alimentaires_versess',
    ]
