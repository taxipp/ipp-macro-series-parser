# -*- coding: utf-8 -*-


import logging
import numpy
import os
import pandas
import pkg_resources
import re


from ipp_macro_series_parser.config import Config

config_parser = Config()

xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
hdf_directory = config_parser.get('data', 'denombrements_fiscaux_hdf')


log = logging.getLogger(__name__)


def parse_ipp_denombrements():

    file_path = os.path.join(xls_directory, u'Agrégats IPP - Données fiscales.xls')

    def parse_bloc(name = None, sheetname = '2042-montant', skiprows = 0, parse_cols = None, slice_start = None,
                   slice_end = None, prefix = ''):
        assert name is not None
        df = pandas.read_excel(
            file_path,
            na_values = '-',
            sheetname = sheetname,
            skiprows = skiprows,
            parse_cols = parse_cols).iloc[slice_start:slice_end]
        df.columns = ['year'] + (prefix + df.columns[1:].str.lower()).tolist()
        try:
            df = df.convert_objects(convert_numeric=True)
            df = df.astype(float)
            df.year = df.year.astype(int)
        except Exception, e:
            print e
            return name, df
        return name, df

    # Fiche principale

    # 1 - Traitements, salaire, prime pour l'emploi, pensions et rentes
    traitements_salaires = dict(
        name = 'traitements_salaires',
        sheetname = '2042-montant',
        skiprows = 4,
        parse_cols = 'A:AB',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f1',
        )

    prime_emploi = dict(
        name = 'prime_emploi',
        sheetname = '2042-montant',
        skiprows = 25,
        parse_cols = 'A:K',
        slice_start = 1,
        slice_end = 17,
        prefix = 'f1',
        )

    pension_retraite = dict(
        name = 'pension_retraite',
        sheetname = '2042-montant',
        skiprows = 46,
        parse_cols = 'A:M',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f1',
        )

    rentes_viageres_titre_onereux = dict(
        name = 'rentes_viageres_titre_onereux',
        sheetname = '2042-montant',
        skiprows = 68,
        parse_cols = 'A:E',
        slice_start = 1,
        slice_end = 17,
        prefix = 'f1',
        )

    # 2 - Revenus des valeurs et capitaux mobiliers

    prelevement_forfaitaire_liberatoire = dict(
        name = 'prelevement_forfaitaire_liberatoire',
        sheetname = '2042-montant',
        skiprows = 89,
        parse_cols = 'A:D',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    revenus_avec_abattement = dict(
        name = 'revenus_avec_abattement',
        sheetname = '2042-montant',
        skiprows = 111,
        parse_cols = 'A:E',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    revenus_sans_abattement = dict(
        name = 'revenus_sans_abattement',
        sheetname = '2042-montant',
        skiprows = 133,
        parse_cols = 'A:D',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    autres_revenus_financiers = dict(
        name = 'autres_revenus_financiers',
        sheetname = '2042-montant',
        skiprows = 154,
        parse_cols = 'A:I',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f2',
        )

    # 3 - Plus values et gains taxables à 16% (18% à partir de 2008)

    plus_values = dict(
        name = 'plus_values',
        sheetname = '2042-montant',
        skiprows = 199,
        parse_cols = 'A:C',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f3',
        )

    # 4 - Revenus fonciers
    # TODO: copier coller d'une note
    # Pour les dénombrements de 96 à 2001, on ne connait plus le détail des différents déficits mais seulement total
    # agrégé (case total def)
    # Comme les parts des différents déficits sur le déficit total est pratiquement constant dans le temps, on assume
    # donc que la répartition du déficit total entre les différents déficits est constant entre 96 et 2001 et égal à son
    # niveau de 2003
    # TODO: virer 2012 à 2014 ?
    revenus_fonciers = dict(
        name = 'revenus_foncier',
        sheetname = '2042-montant',
        skiprows = 222,
        parse_cols = 'A:H',
        slice_start = 1,
        slice_end = 20,
        prefix = 'f3',
        )

    contribution_revenus_locatifs = dict(
        name = 'contribution_revenus_locatifs',
        sheetname = '2042-montant',
        skiprows = 246,
        parse_cols = 'A:C',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f4',
        )

    # 5- Revenus exceptionnels ou différés

    revenus_exceptionnels = dict(
        name = 'revenus_exceptionnels',
        sheetname = '2042-montant',
        skiprows = 268,
        parse_cols = 'A:B',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f5',
        )

    # 6- Charges déductibles et imputations diverses

    charges_deductibles = dict(
        name = 'charges_deductibles',
        sheetname = '2042-montant',
        skiprows = 316,
        parse_cols = 'A:I',
        slice_start = 1,
        slice_end = 19,
        prefix = 'f6',
        )

    epargne_retraite = dict(
        name = 'epargne_retraite',
        sheetname = '2042-montant',
        skiprows = 338,
        parse_cols = 'A:O',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f6',
        )

    # 7- Charges ouvrant droit à réduction ou à crédit d'impôt

    reductions_credits_impot = dict(
        name = 'reductions_credits_impot',
        sheetname = '2042-montant',
        skiprows = 360,
        parse_cols = 'A:BH',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f7',
        )

    # 8- Autres imputations, reprises de réductions d'impôt, conventions internationales, divers

    autres_imputations = dict(
        name = 'autres_imputations',
        sheetname = '2042-montant',
        skiprows = 383,
        parse_cols = 'A:L',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f7',
        )

    # Fiche complémentaire

    # 1- Gains de levée d'options

    options = dict(
        name = 'options',
        sheetname = '2042C - montant',
        skiprows = 5,
        parse_cols = 'A:I',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f1',
        )

    name, df = parse_bloc(**options)
    df.dtypes
    df.year

    # salaires exonérés

    salaires_exoneres = dict(
        name = 'salaires_exoneres',
        sheetname = '2042C - montant',
        skiprows = 26,
        parse_cols = 'A:I',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f1',
        )

    # crédit d'impôt mobilité
    # TODO; nothing in agrégats IPP

    # 3- Plus-values et gains divers

    plus_values_complementaire = dict(
        name = 'plus_values_complementaire',
        sheetname = '2042C - montant',
        skiprows = 67,
        parse_cols = 'A:T',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f3',
        )

    # 4- Revenus fonciers

    revenus_fonciers_complementaire = dict(
        name = 'revenus_fonciers_complementaire',
        sheetname = '2042C - montant',
        skiprows = 88,
        parse_cols = 'A:B',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f4',
        )

    # 5- Revenus et plus-values des professions non salariées

    prime_emploi_complementaire = dict(
        name = 'prime_emploi_complementaire',
        sheetname = '2042C - montant',
        skiprows = 111,
        parse_cols = 'A:G',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )

    revenus_agricoles_forfait = dict(
        name = 'revenus_agricoles_forfait',
        sheetname = '2042C - montant',
        skiprows = 167,
        parse_cols = 'A:Q',
        slice_start = 0,
        slice_end = 18,
        prefix = 'f5',
        )

    revenus_agricoles_reel = dict(
        name = 'revenus_agricoles_reel',
        sheetname = '2042C - montant',
        skiprows = 190,
        parse_cols = 'A:Y',
        slice_start = 0,
        slice_end = 18,
        prefix = 'f5',
        )

    revenus_agricoles_deficits = dict(
        name = 'revenus_agricoles_deficits',
        sheetname = '2042C - montant',
        skiprows = 212,
        parse_cols = 'A:M',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f5',
        )
    # TODO: *Avant 2007, les cases HE, IE, JE étaient séparé en deux (cases HE et HK,…,JE et JK) en fonction de
    # l'appartenance ou non à un CGA

    # Revenus industriels et commerciaux professionnels

    bic_pro_micro_entreprise = dict(
        name = 'bic_pro_micro_entreprise',
        sheetname = '2042C - montant',
        skiprows = 237,
        parse_cols = 'A:U',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )

    bic_pro_reel = dict(
        name = 'bic_pro_reel',
        sheetname = '2042C - montant',
        skiprows = 282,
        parse_cols = 'A:AE',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )
    # TODO
    # Pour les revenus de 1997, il n'y a pas de distinction entre les BIC professionnels et les BIC non professionnels.
    # On choisit de mettre les "BIC exonérés" dans cette case (et de ne rien mettre dans la case NB associée aux BIC
    # non professionnels exonérés).

    bic_pro_cga = dict(
        name = 'bic_pro_cga',
        sheetname = '2042C - montant',
        skiprows = 304,
        parse_cols = 'A:G',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )

    bic_non_pro_micro_entreprise = dict(
        name = 'bic_non_pro_micro_entreprise',
        sheetname = '2042C - montant',
        skiprows = 328,
        parse_cols = 'A:T',
        slice_start = 0,
        slice_end = 18,
        prefix = 'f5',
        )

    bic_non_pro_reel = dict(
        name = 'bic_non_pro_reel',
        sheetname = '2042C - montant',
        skiprows = 351,
        parse_cols = 'A:AH',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )
    # Pour l'année 1997, on dispose d'un montant agrégé pour les BIC non professionneles et les BNC non professionnels,
    # sans distinction non plus du régime d'imposition (simplifié, réel). Pour cette année, on met le montant agrégé
    # dans la case NC pour les revenus et dans la case NF pour les déficits. Il s'agit des cases relatives aux BIC non
    # professionnels imposés au régime réel.

    bic_non_pro_deficit_anterieur = dict(
        name = 'bic_non_pro_deficit_anterieur',
        sheetname = '2042C - montant',
        skiprows = 373,
        parse_cols = 'A:G',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )

    # Revenus non commerciaux professionnels

    bnc_pro_micro_vous = dict(
        name = 'bnc_pro_micro_vous',
        sheetname = '2042C - montant',
        skiprows = 396,
        parse_cols = 'A:P',
        slice_start = 0,
        slice_end = 18,
        prefix = 'f5',
        )
    # *Avant 2007, la cases QD était séparé en deux (cases QD et QJ) en fonction de l'appartenance ou non à un AA

    bnc_pro_micro_conj = dict(
        name = 'bnc_pro_micro_conj',
        sheetname = '2042C - montant',
        skiprows = 417,
        parse_cols = 'A:O',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )
    # *Avant 2007, la cases RD était séparé en deux (cases RD et RJ) en fonction de l'appartenance ou non à un AA

    bnc_pro_micro_pac = dict(
        name = 'bnc_pro_micro_pac',
        sheetname = '2042C - montant',
        skiprows = 437,
        parse_cols = 'A:N',
        slice_start = 0,
        slice_end = 17,
        prefix = 'f5',
        )
    # *Avant 2007, la cases SD était séparé en deux (cases SD et SJ) en fonction de l'appartenance ou non à un AA

    # Revenus non commerciaux non professionnels
    bnc_non_pro_vous = dict(
        name = 'bnc_non_pro_vous',
        sheetname = '2042C - montant',
        skiprows = 482,
        parse_cols = 'A:T',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f5',
        )
    # * Avant 2006, l'ensemble des variables de JG à MT ne concerne plus seulement le contribuable mais l'ensemble du
    # foyer. Les cases JK à SW et LK à SX sont donc supprimées.

    bnc_non_pro_conj = dict(
        name = 'bnc_non_pro_conj',
        sheetname = '2042C - montant',
        skiprows = 502,
        parse_cols = 'A:M',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f5',
        )

    bnc_non_pro_pac = dict(
        name = 'bnc_non_pro_pac',
        sheetname = '2042C - montant',
        skiprows = 521,
        parse_cols = 'A:M',
        slice_start = 1,
        slice_end = 18,
        prefix = 'f5',
        )

    # Revenus accessoires
    # TODO

    # Revenus a imposer aux prelevements sociaux

    revenus_prelevements_sociaux = dict(
        name = 'revenus_prelevements_sociaux',
        sheetname = '2042C - montant',
        skiprows = 567,
        parse_cols = 'A:I',
        slice_start = 0,
        prefix = 'f5',
        slice_end = 17,
        )

    # 6- Charges et imputations diverses = charges à déduire du revenu

    charges_imputations_diverses = dict(
        name = 'charges_imputations_diverses',
        sheetname = '2042C - montant',
        skiprows = 587,
        parse_cols = 'A:R',
        slice_start = 2,
        prefix = 'f5',
        slice_end = 19,
        )
    # 3 Cette case EH (investissemencompte épargne co-developpement) n'a rien à voir avec la case EH colonne O
    # (investissement DOM-TOM)
    # 4 : Cette case était dans la déclaration 2042 avant 2007 (case somme à ajouter au revenu imposable)

    # 7- Charges ouvrant droit à réduction ou à crédit d'impôt

    reductions_credits_impot_complementaire = dict(
        name = 'reductions_credits_impot_complementaire',
        sheetname = '2042C - montant',
        skiprows = 613,
        parse_cols = 'A:BA',
        slice_start = 2,
        prefix = 'f5',
        slice_end = 20,
        )
    # 3 : les données brutes sont abérrantes pour l'année 2007, on vait par exemple 113 863 3, il manque donc deux zéros
    # derrères le 3. Et pour UA et UJ, j'ai rajouté 3 zéros derrières les nombres brutes pour avoir le bon rapport de
    # grandeur.
    # * UI = Total réduction d'impôt Outre-mer Avant 2008 : la déclaration détaille les composantes des Ivt Outremer par
    # secteur d'activité

    # 8- Autres imputations, conventions internationales, crédits d'impôt entreprise
    autres_imputations_complementaire = dict(
        name = 'autres_imputations_complementaire',
        sheetname = '2042C - montant',
        skiprows = 639,
        parse_cols = 'A:Z',
        slice_start = 1,
        prefix = 'f5',
        slice_end = 20,
        )

    # name, df = parse_bloc(**autres_imputations_complementaire)
    # print df.dtypes
    # df.year

    # 8- Autres imputations, conventions internationales, crédits d'impôt entreprise

    blocs = [
        traitements_salaires,
        prime_emploi,
        pension_retraite,
        rentes_viageres_titre_onereux,
        prelevement_forfaitaire_liberatoire,
        revenus_avec_abattement,
        revenus_sans_abattement,
        autres_revenus_financiers,
        plus_values,
        revenus_fonciers,
        contribution_revenus_locatifs,
        revenus_exceptionnels,
        charges_deductibles,
        epargne_retraite,
        reductions_credits_impot,
        autres_imputations,
        options,
        salaires_exoneres,
        plus_values_complementaire,
        revenus_fonciers_complementaire,
        prime_emploi_complementaire,
        revenus_agricoles_forfait,
        revenus_agricoles_reel,
        revenus_agricoles_deficits,
        bic_pro_micro_entreprise,
        bic_pro_reel,
        bic_pro_cga,
        bic_non_pro_micro_entreprise,
        bic_non_pro_reel,
        bic_non_pro_deficit_anterieur,
        bnc_pro_micro_vous,
        bnc_pro_micro_conj,
        bnc_pro_micro_pac,
        bnc_non_pro_vous,
        bnc_non_pro_conj,
        bnc_non_pro_pac,
        revenus_prelevements_sociaux,
        charges_imputations_diverses,
        reductions_credits_impot_complementaire,
        autres_imputations_complementaire
        ]

    data_frame_by_bloc_name = dict(parse_bloc(**bloc) for bloc in blocs)

    correct_errors(data_frame_by_bloc_name, show_only = False)

    ipp_denombrements = pandas.DataFrame()
    for data_frame in data_frame_by_bloc_name.values():
        ipp_denombrements = pandas.concat((
            ipp_denombrements,
            pandas.melt(data_frame, id_vars=['year'], var_name = 'code')
            ))
    ipp_denombrements.dropna(inplace = True)
    return ipp_denombrements


def correct_errors(data_frame_by_bloc_name, show_only = False):
    import re
    pattern = re.compile("^f[1-8][a-z][a-z]$")
    note_pattern = re.compile("^f[1-8][a-z][a-z][1-4]$")

    corrected_columns = set()
    problematic_columns = set()
    for bloc_name, data_frame in data_frame_by_bloc_name.items():

        correct_name_by_wrong_name = dict()
        drop_columns = list()

        for column in data_frame.columns:
            if column == 'year':
                assert numpy.issubdtype(data_frame[column].dtype, numpy.integer)
                assert data_frame[column].isin(range(1990, 2015)).all()
                continue
            if not pattern.match(column):
                # print '- ' + str(column)
                # remove trailing spaces
                problematic_columns.add(column)
                if column != column.strip():
                    correct_name_by_wrong_name[column] = column.strip()
                # remove *
                if column.endswith('*') and pattern.match(column[:-1]):
                    correct_name_by_wrong_name[column] = column[:-1]
                # remove unnamed
                if "unnamed" in column or "-" in column or 'total' in column:
                    drop_columns.append(column)
                # remove trailing 1, 2, 3, 4 (notes in excel file)
                if note_pattern.match(column):
                    correct_name_by_wrong_name[column] = column[:-1]

        corrected_columns = corrected_columns.union(set(correct_name_by_wrong_name.keys()))
        corrected_columns = corrected_columns.union(set(drop_columns))

        if not show_only:
            data_frame.drop(labels = drop_columns, axis = 1, inplace = True)
            data_frame.rename(columns = correct_name_by_wrong_name, inplace = True)

    print 'Remaining problematic columns'
    print problematic_columns.difference(corrected_columns)


def parse_openfisca_denombrements():
    openfisca_denombrements = pandas.read_excel(os.path.join(xls_directory, '2042_national.xls'), sheetname = 'montant')
    assert openfisca_denombrements.dtypes.apply(lambda x: numpy.issubdtype(x, numpy.float)).all(), \
        openfisca_denombrements.dtypes
    openfisca_denombrements = openfisca_denombrements.stack().reset_index()
    openfisca_denombrements.rename(columns = {'level_0': 'code', 'level_1': 'year', 0: 'value'}, inplace = True)
    openfisca_denombrements[['year']] = openfisca_denombrements[['year']].astype(int)
    return openfisca_denombrements


def parse_dgfip_denombrements(years = None):

    assert years is not None
    assert min(years) >= 2001
    assert max(years) <= 2013

    dgfip_directory = os.path.join(xls_directory, 'D2042Nat')
    files = os.listdir(dgfip_directory)
    result = pandas.DataFrame()

    for year in years:
        file_regex = re.compile("^R20{}".format(str(year)[2:4]))
        for filename in files:
            if file_regex.match(filename):
                log.info("Using file {} for year {}".format(filename, year))
                break

        print year

        if year in [2001, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]:
            dgfip_denombrements = pandas.read_excel(os.path.join(dgfip_directory, filename))
        if year == 2003:
            dgfip_denombrements = pandas.read_excel(os.path.join(dgfip_directory, filename), skiprows = 4)

        if year in [2001, 2003]:
            regex = re.compile("^[0-9][A-Z]{2}")
            dgfip_denombrements.code.fillna("", inplace = True)
            dgfip_denombrements = dgfip_denombrements.set_index('code').filter(regex = regex, axis = 0)
            new_variable_name_by_old = dict(
                (x, "f{}".format(x.lower())) for x in dgfip_denombrements.index)
            dgfip_denombrements = dgfip_denombrements.rename(index = new_variable_name_by_old)
            dgfip_denombrements['year'] = year
            dgfip_denombrements.rename(columns = {'montant': 'value', 'Nombre': 'nombre'}, inplace = True)
            del dgfip_denombrements['nombre']

        # TODO:
        if year in [2005, 2006, 2007, 2008]:
            # continue
            regex = re.compile("[A-Z]{2}")

            dgfip_denombrements = dgfip_denombrements.set_index('nom').filter(regex = regex, axis = 0)
            dgfip_denombrements.index.name = 'code'
            new_variable_name_by_old = dict(
                (x, "f{}".format(x.lower())) for x in dgfip_denombrements.index)
            dgfip_denombrements = dgfip_denombrements.rename(index = new_variable_name_by_old)
            print dgfip_denombrements
            boum
            # trouver un moyen de renommer les codes pour qu'il y ait le numéro des sections

#            dgfip_denombrements.rename(columns = {'nom': 'code'}, inplace = True)
#            for ind in dgfip_denombrements.index:
#                if re.match("[A-Z][I, J, K, O, P, Q, S, V, W, X]", dgfip_denombrements.ix[ind]['code']):
#                    print dgfip_denombrements.ix[ind]['code']
#                    dgfip_denombrements.rename(
#                        {dgfip_denombrements.ix[ind]['code']: "1{}".format(dgfip_denombrements.ix[ind]['code'])}) # ,inplace = True
#
# or
#            dgfip_denombrements = dgfip_denombrements.filter(items = ['nom'], regex = regex)
#
#            dgfip_denombrements['code'] = dgfip_denombrements['nom']
#            for ind in dgfip_denombrements.index:
#                if re.match("[A-Z][I, J, K, O, P, Q, S, V, W, X]", dgfip_denombrements.ix[ind]['nom']):
#                    print dgfip_denombrements.ix[ind]['nom']
#                    dgfip_denombrements.ix[ind]['code'] = "1{}".format(dgfip_denombrements.ix[ind]['nom'])
#
#            dgfip_denombrements = dgfip_denombrements.set_index('code').filter(regex = regex, axis = 0)

        if year == 2004:
            regex = re.compile("^Z[0-9][A-Z]{2}")
            dgfip_denombrements.case.fillna("", inplace = True)
            dgfip_denombrements.drop_duplicates(['case'], inplace = True)
            dgfip_denombrements = dgfip_denombrements.set_index('case').filter(regex = regex, axis = 0)
            dgfip_denombrements.index.name = 'code'
            new_variable_name_by_old = dict(
                (x, "f{}".format(x[1:].lower())) for x in dgfip_denombrements.index)
            dgfip_denombrements = dgfip_denombrements.rename(index = new_variable_name_by_old)
            dgfip_denombrements.reset_index(inplace = True)

            dgfip_denombrements['year'] = year
            dgfip_denombrements.rename(columns = {'Montant': 'value'}, inplace = True)
            del dgfip_denombrements['Nombre'], dgfip_denombrements[u'libellé'], dgfip_denombrements['nom']

        if year in [2009, 2010, 2011, 2012]:
            regex = re.compile("^Z[0-9][A-Z]{2}")
            dgfip_denombrements = dgfip_denombrements.set_index('nom').filter(regex = regex, axis = 0)
            dgfip_denombrements.index.name = 'code'
            new_variable_name_by_old = dict(
                (x, "f{}".format(x[1:].lower())) for x in dgfip_denombrements.index)
            dgfip_denombrements = dgfip_denombrements.rename(index = new_variable_name_by_old)
            dgfip_denombrements.reset_index(inplace = True)
            dgfip_denombrements['year'] = year

            if year == 2009:
                dgfip_denombrements.rename(columns = {'Montants': 'value', 'Nombre': 'nombre'}, inplace = True)
            else:
                dgfip_denombrements.rename(columns = {'montants': 'value'}, inplace = True)

            del dgfip_denombrements['maximal'], dgfip_denombrements['nombre']

        if year == 2013:
            regex = re.compile("^Z[0-9][A-Z]{2}")
            dgfip_denombrements = dgfip_denombrements.set_index('nom').filter(regex = regex, axis = 0)
            dgfip_denombrements.index.name = 'code'
            new_variable_name_by_old = dict(
                (x, "f{}".format(x[1:].lower())) for x in dgfip_denombrements.index)
            dgfip_denombrements = dgfip_denombrements.rename(index = new_variable_name_by_old)
            dgfip_denombrements.reset_index(inplace = True)
            dgfip_denombrements['year'] = year
            dgfip_denombrements.rename(columns = {'ano': 'value'}, inplace = True)
            del dgfip_denombrements['pas_ano']

        result = pandas.concat((result, dgfip_denombrements))
        result.dropna(subset = ['value'], inplace = True)  # dropping NA's

    return result.loc[result.value != 0].copy()  # excluding 0 values


def create_denombrements_fiscaux_data_frame(year = None, years = None, overwrite = False):
    """
    Generates the table with all the data from Dénombrements Fiscaux .

    Parameters
    ----------
    year : int
        year of DGFIP data (coincides with year of declaration)
    years : list of integers
        list of years of interest. Optional.

    Example
    --------
    >>> table_2013 = denombrements_fiscaux_df_generator(year = 2013)

    Returns the main table of dénombrements fiscaux for the year 2013.
    """
    if year is not None and years is None:
        years = [year]

    log.info('Parsing dénombrements fiscaux raw data for the following years: {}'.format(years))
    # Data coming for openfisca xls file
    openfisca_denombrements = parse_openfisca_denombrements()
    openfisca_denombrements['origin'] = 'OF'

    # Data coming from IPP
    ipp_denombrements = parse_ipp_denombrements()
    ipp_denombrements['origin'] = 'IPP'

    df = pandas.concat([ipp_denombrements, openfisca_denombrements])
    # Drop real duplicates
    df = df.drop_duplicates(subset = ['year', 'code', 'value'])
    df = df.reset_index(drop=True)

    # Problematic duplicates
    dups = df.duplicated(['year', 'code']) | df.duplicated(['year', 'code'], keep = 'last')
    z = df.loc[dups].copy()
    # sum of two columns in IPP for year < 2007
    wrong_before_2007 = ['f5ne', 'f5oe', 'f5rd', 'f5ke', 'f5le', 'f5he', 'f5ie', 'f5qd']
    df = df.loc[~(df.code.isin(wrong_before_2007) & (df.year < 2007))]
    log.info('Remaining roblematic duplicates when merging IPP and OF \n {}'.format(
        z.loc[~(z.code.isin(wrong_before_2007) & (z.year < 2007))]
        ))
    df = df.loc[df.year.isin(years)].copy() if years is not None else df.copy()

    # Data coming from DGFiP
    dgfip_denombrements = parse_dgfip_denombrements(years)
    dgfip_denombrements['origin'] = 'DGFiP'
    df2 = pandas.concat([dgfip_denombrements, df])

    # Drop real duplicates
    df2 = df2.drop_duplicates(subset = ['year', 'code', 'value'])
    df2 = df2.reset_index(drop=True)

    dups2 = df2.duplicated(['year', 'code']) | df2.duplicated(['year', 'code'], keep = 'last')
    errors = df2.loc[dups2].copy()

    wrong_codes = ['f5ne', 'f5oe', 'f5rd', 'f5ke', 'f5le', 'f4tq', 'f5hd',
       'f5id', 'f5he', 'f5ie', 'f5qd', 'f3ve', 'f3vf', 'f3ve', 'f3vf', 'f7tf', 'f7tf', 'f2gr', 'f2ch', 'f2bg', 'f6el',
        'f6st', 'f2bg', 'f7cd', 'f2gr', 'f2ch', 'f7cd', 'f6st', 'f6el']
    wrong_years = [2006, 2005, 2004, 2003]
    log.info('Remaining problematic duplicates when merging with DGFiP data \n {}'.format(
        errors.loc[~(errors.code.isin(wrong_codes) | errors.year.isin(wrong_years))]
        ))
    df2 = df2.loc[~(df2.code.isin(wrong_codes) | (df2.year.isin(wrong_years)))]
    result = df2.loc[df2.year.isin(years)].copy() if years is not None else df2.copy()

    log.info('For now, we keep only DGFiP data')
    result = dgfip_denombrements.copy()  # TODO: recoupement avec data OpenFisca & IPP

    if overwrite:
        save_df_to_hdf(result, 'denombrements_fiscaux.h5', 'montants')

    return result, errors


def build_section_code():
    openfisca_denombrements = parse_openfisca_denombrements()
    ipp_denombrements = parse_ipp_denombrements()
    df = pandas.concat([openfisca_denombrements.code, openfisca_denombrements.code])
    return df.unique()


def get_denombrements_fiscaux_data_frame(year = None, years = None, rebuild = False, overwrite = False,
        fill_value = numpy.nan):
    if year is not None and years is None:
        years = [year]
    if rebuild:
        return create_denombrements_fiscaux_data_frame(years = years, overwrite = overwrite)
    else:
        data_frame = import_from_hdf('denombrements_fiscaux.h5', 'montants')
        return data_frame.loc[data_frame.year.isin(years)].copy()


def save_df_to_hdf(df, hdf_filename, key):
    file_path = os.path.join(hdf_directory, hdf_filename)
    df.to_hdf(file_path, key)


def import_from_hdf(hdf_filename, key):
    file_path = os.path.join(hdf_directory, hdf_filename)
    store = pandas.HDFStore(file_path)
    df = store[key]
    return df


if __name__ == '__main__':
    build_section_code()
    dgfip = parse_dgfip_denombrements(years = range(2008, 2009))
    print dgfip
#    denomb_fisc_all, errors = create_denombrements_fiscaux_data_frame(
#        years = range(2009, 2014),
#        overwrite = True,
#        )
