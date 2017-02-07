#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import pandas as pd
import os
from slugify import slugify


"""Parse dépenses and bénéficiaires of prestataions sociales to produce the dataframe stored in a HDF5 file or csv files
"""


from ipp_macro_series_parser.config import Config

log = logging.getLogger(__name__)

parser = Config()
prestations_sociales_directory = parser.get('data', 'prestations_sociales_directory')


def build_data_frame(section):
    assert section in ['beneficiaires', 'depenses']

    directory = os.path.join(
        prestations_sociales_directory,
        'raw',
        'caf_data_fr',
        'les-{}-tous-regimes-de-prestations-familiales-et-sociales'.format(
            section
            ),
        )
    prefix = 'DepTR' if section == 'depenses' else 'BenTR'

    filenames = [filename for filename in os.listdir(directory) if filename.startswith(prefix)]

    result_data_frame = None
    for filename in sorted(filenames):
        year = filename[5:5 + 4]
        assert year.startswith('19') or year.startswith('20')
        year = int(year)
        file_path = os.path.join(directory, filename)
        log.info('Parsing {} data from year {} using {}'.format(section, year, file_path))
        data_frame = pd.read_csv(file_path, sep = ';', decimal = ',')
        data_frame.dropna(axis = 1, inplace = True, how = 'all')  # Remove NA columns
        columns_stripped = [
            column.replace(' ', '')
            for column in data_frame.columns
            ]
        new_columns = [
            column[:-5]
            if column.endswith(str(year))
            else column
            for column in columns_stripped
            ]
        data_frame.columns = new_columns
        data_frame['year'] = int(year)
        data_frame = pd.melt(data_frame, id_vars = ['year', 'Prestations'])
        result_data_frame = data_frame if result_data_frame is None else result_data_frame.merge(
            data_frame, how = 'outer')

    result_data_frame.year = result_data_frame.year.astype(int)
    return result_data_frame


def create_prestations_sociales_data_frames():
    # From CAF historical series
    build_historical_amounts_data()
    build_historical_beneficiaries_data()
    # From CNAV
    build_minimum_vieillesse_serie()
    # From data.caf.fr web site
    store = pd.HDFStore(os.path.join(
        prestations_sociales_directory,
        'prestations_sociales.h5'
        ))
    for section in ['beneficiaires', 'depenses']:
        data_frame = build_data_frame(section)
        store[section] = data_frame


def build_historical_amounts_data():
    directory = os.path.join(
        prestations_sociales_directory,
        'raw',
        'xls',
        )
    depenses_file_path = os.path.join(directory, u"historique_dépenses_depuis 1946.xls")

    # sheetname = u'données histo D'
    sheetname = u'données histo M'
    # sheetname = u'données histo MD'

    data_frame = pd.read_excel(depenses_file_path, sheetname = sheetname, header = 1, inbdex_col = 0)
    table_entry_by_variable = {
        'af': 'Allocations familiales (AF)',
        'af_base': None,
        'af_majoration': None,
        'af_allocation_forfaitaire': None,
        'cf': 'Complément familial (CF)',
        'paje_base': 'PAJE  naissance adoption de base (AB)',
        'paje_naissance': 'PAJE naissance adoption',
        'paje_clca': 'PAJE complément (optionnel) libre choix activité PréPARE',  # contient également le COLCA
        'paje_clmg': 'PAJE complément mode de garde (CMG)',
        'ars': 'Allocation de rentrée scolaire (ARS)',
        'aeeh': 'Allocation d’éducation de l’enfant handicapé de base',
        'asf': 'Allocation de soutien familial (ASF)',
        'aspa': None,
        'aah': ' Allocation adultes handicapés de base',
        'caah': 'Majoration pour la vie autonome (MVA) - Complément AAH',
        'rsa': ' Revenu solidarité active (RSA versé yc prime, créances, indus)',
        'rsa_activite': 'RSA activité (hors RSA Jeunes)',
        'aefa': 'Prime exceptionnelle décembre RSA (Etat)',
        'api': 'Allocation de parent isolé (API)',
        'psa': None,
        'aides_logement': 'Total prestation logement',
        'alf': 'Allocation logement familiale (ALF)',
        'als': 'Allocation logement sociale (ALS)',
        'apl': 'Aide personnalisée au logement (APL)',
        }

    # Sous-total 1 AF, CF, ARS, ASF, AES, APP
    #  Allocations familiales (AF)
    # AF
    # Forfait AF
    #  Complément familial (CF)
    #  Allocation de rentrée scolaire (ARS)
    # ARS de base
    # Majoration d'allocation de rentrée scolaire
    #  Aide à la scolarité (AAS)
    #  Allocation de soutien familial (AO-ASF)
    #  Allocation d’éducation de l’enfant handicapé (AEEH)
    # AEEH de base
    # AEEH complément
    #  Allocation journalière de présence parentale (AJPP)
    #  Sous-total 2 : Prestations jeune enfant
    #  Dont entretien (yc 29 à 30 % de l'Ape = Apje virtuelle)
    #  Dont frais de garde à l'extérieur du foyer
    #  Dont frais de garde à domicile
    #  Dont compensation d'un arrêt de l’activité (- 29 à 30 % Ape)
    #  Prestation d'accueil du jeune enfant (PAJE)
    # PAJE naissance adoption
    # PAJE naissance
    # PAJE adoption
    # PAJE de base naissance adoption (AB)
    # PAJE de base naissance
    # PAJE de base adoption
    # PAJE complément (optionnel) libre choix activité
    # Taux plein
    # Taux partiel
    # PAJE CLCA rang 1
    # Taux plein
    # Taux partiel
    # PAJE CLCA rang 2
    # Taux plein
    # Taux partiel
    # PAJE CLCA rang 3 et plus
    # Taux plein
    # Taux partiel
    # PAJE COLCA rang 3 et plus
    # PAJE CLCA adoption
    # Taux plein
    # Taux partiel
    # PAJE complément mode de garde (CMG)
    # PAJE CMG cotisations prises en charge
    # PAJE CMG rémunérations prises en charge
    # PAJE CMG via association, entreprise
    # PAJE CMG assistantes maternelles
    # Cotisations prises en charge
    # Rémunérations prises en charge
    # Recours association, entreprise
    # PAJE CMG garde à domicile enfant [0 - 3 ans]
    # Cotisations prises en charge
    # Rémunérations prises en charge
    # Recours association, entreprise
    # PAJE CMG garde à domicile enfant ]3 - 6 ans]
    # Cotisations prises en charge
    # Rémunérations prises en charge
    # Recours à une association ou une entreprise
    #  Allocation pour jeune enfant (APJE)
    # APJE courte sans CR jusqu'en janvier 1996
    # APJE longue avec CR
    #  Allocation parentale d'éducation (APE)
    # APE aux familles de 2 enfants
    # APE aux familles de 3 enfants et plus
    #  Allocation de garde d'enfant à domicile (AGED)
    #  Aide à la famille pour l’emploi d’une assistante maternelle agréée
    # AFEAMA de base
    # Majoration d'AFEAMA
    #  Allocation d'adoption (AAD)
    # Sous-total 3 : ASU-AFG, prestations naissance antérieures
    # Sous-total 4 : Autres prestations famille
    #  Prestations hors métropole
    #  Accords CEE
    #  Allocation différentielle
    #  Frais de tutelle
    # Aux prestations sociales
    # Aux prestations familiales
    #  Divers métropole (Algérie...)
    # Sous-total Famille
    # dont sous-total 5 Famille - AF - P. jeune enfant
    # Logement
    #  ALF + APL + ALS + ALT (yc prime, indus)
    # Dont Accession
    # Dont Location (sans foyers, sans ALT)
    #  Allocation logement familiale (ALF)
    # Accession
    # Location
    # Prime de déménagement familiale
    #  Aide personnalisée au logement (APL)
    # Accession
    # Location
    # Foyer
    # Prime de déménagement du FNH
    # Indus, créances,  remises / créances, annulations créances
    #  Allocation logement sociale (ALS)
    # Accession
    # dont étudiant
    # Location
    # dont étudiant
    # Indus, créances,  remises / créances, annulations créances
    # Prime de déménagement sociale
    #  Allocation logement temporaire (ALT1 + ALT2 versées)
    # Aide aux organismes
    # Accueil des gens du voyage
    # Indus, créances,  remises / créances, annulations créances
    #  Prêts amélioration de l'habitat y compris les PAH AM
    #  Prêts amélioration de l'habitat (solde PAH hors AM)
    # Montant des prêts
    # Remboursements
    # Montant des intérêts
    #  PAH assistant(e)s maternel(le)s (solde PAH AM)
    # Montant des prêts
    # Remboursements
    # Montant des intérêts
    #  Prêts aux jeunes ménages (PJM)
    #  Intérêts des prêts jeunes avenir
    #  Allocation d'installation de l'étudiant (ALINE, juillet - décembre)
    # ALINE hors créances
    # Indus, créances,  remises / créances, annulations créances
    # Minima sociaux - Aides à l'emploi
    # Minima sociaux - Aides à l'emploi hors prime ARS
    #  Allocation de parent isolé (API)
    # API hors prime forfaitaire d'intéressement
    # Prime forfaitaire d'intéressement API
    #  Al. aux adultes handicapés (AAH + MVA + GRPH, en EC depuis 2007)
    # AAH de base
    # Majoration pour la vie autonome (MVA) - Complément AAH
    # Garantie de ressources des personnes handicapées (GRPH)
    # Prime avril 2011 (DOM)
    #  Revenu solidarité active (RSA versé yc prime)
    # Dont Etat
    # Dont RSA activité
    # Dont RSA activité hors RSA jeunes
    # Dont département
    # RSA hors primes, divers
    # RSA non majoré
    # RSA socle non majoré (départements)
    # RSA socle hors RSA Jeunes
    # RSA Jeunes socle
    # RSA activité non majoré (Etat)
    # RSA activité hors RSA Jeunes
    # RSA Jeunes activité
    # RSA majoré
    # RSA socle majoré (départements)
    # RSA socle activité majoré (Etat)
    # RSA divers
    # Prime exceptionnelle 2e trimestre 2009 RSA (Etat)
    # Allocation RSA Local (Bonus)
    # Aide personnalisée de retour à l'emploi
    # Prime exceptionnelle décembre RSA (Etat)
    #  Revenu minimum d'insertion (RMI versé yc prime)
    # RMI Etat prime de décembre
    # RMI département
    # Allocations RMI
    # Complément RMI
    # Prime forfaitaire d'intéressement
    # RMI prime département (compta. qd délégation CAF)
    # Frais de tutelle
    # Indus, créances,  remises / créances, annulations créances
    #  Autres (CIRMA, CAV, PRE, RSO, RSA, ASA, SURF...)
    # Supplément de revenu familial (SURF)
    # Allocation spécifique d'attente (ASA)
    # Contrat d'insertion - revenu minimum d'activité (CIRMA)
    # CIRMA versé
    # Indus, créances,  remises / créances, annulations créances
    # Contrat d'avenir (CAV)
    # CAV versé
    # Indus, créances,  remises / créances, annulations créances
    # Prime de retour à l'emploi (PRE, décret et loi)
    # Prime de retour à l'emploi (PRE, décret et loi)
    # Indus, créances,  remises / créances, annulations créances
    # Prime exceptionnelle ARS (Etat)
    # Revenu de solidarité active (RSA expérimental)
    # RSA expérimental hors indus
    # Indus RSA expérimental
    # Revenu de solidarité (RSO versé dans les DOM)
    # RSO hors indus
    # Indus RSO
    #  Prestations légales directes
    #  dont prestations FNPF (hors API, AAH sur toute la période)
    #  dont prestations hors FNPF + API + AAH
    #  dont indus (hors indus RSA en 2010)

    slugified_table_entry_by_variable = dict([
        (variable, slugify(table_entry, separator = "_"))
        for variable, table_entry in table_entry_by_variable.iteritems()
        if table_entry is not None]
        )

    csv_file_path = os.path.join(
        prestations_sociales_directory,
        'clean',
        'historique_depenses.csv'
        )
    variable_by_slugified_table_entry = {
        v: k for k, v in slugified_table_entry_by_variable.iteritems()
        }
    data_frame = (data_frame
        .rename(index = lambda x: slugify(x, separator = "_"))
        .rename(index = variable_by_slugified_table_entry)
        )

    assert 'af' in data_frame.index
    data_frame.to_csv(csv_file_path)


def build_historical_beneficiaries_data():
    directory = os.path.join(
        prestations_sociales_directory,
        'raw',
        'xls',
        )
    beneficiaries_file_path = os.path.join(directory, u"histo_benef_presta.xls")
    sheetname = u'5321TR_M78'  # métropole
    # sheetname = u'5331CAF_MD89'

    data_frame = pd.read_excel(
        beneficiaries_file_path, sheetname = sheetname, header = 3, index_col = 0, engine = 'xlrd')
    variable_by_table_entry = {
        u"Prestation d'accueil du jeune enfant (PAJE)": None,
        u"PAJE naissance adoption (effectifs de décembre)": "paje_naissance",
        u"PAJE de base naissance adoption (AB)": "paje_base",
        u"PAJE complément (optionnel) libre choix activité": "paje_clca",
        u"CLCA taux plein": None,
        u"CLCA autres cas (taux partiel, couple, intéressement)": None,
        u"Complément optionnel libre choix activité (COLCA)": "paje_colca",
        u"PAJE CMG ensemble": "paje_clmg",
        u"PAJE CMG complément assistante maternelle": None,
        u"Nombre d'enfants bénéficiaires de 0 à - 3 ans": None,
        u"Nombre d'enfants bénéficiaires de 3 à - 6 ans": None,
        u"PAJE CMG complément garde à domicile": None,
        u"Famille avec présence d'enfants de moins de 3 ans": None,
        u"F. avec présence d'enfants de 3 à 6 ans (sans E < 3 ans)": None,
        u"PAJE CMG complément structure": None,
        u"Dont CMG micro-crèches": None,
        u"Dont CMG structure garde à domicile": None,
        u"Allocation pour jeune enfant (APJE)": "apje",
        u"dont APJE courte": None,
        u"        APJE longue": None,
        u"Allocation parentale d'éducation (APE)": "ape",
        u"Allocation de garde d'enfant à domicile (AGED)": None,
        u"Aide emploi assistante maternelle (AFEAMA)": None,
        u"Allocation d'adoption": None,
        u"Famille : autres prestations": None,
        u"Allocations familiales (AF)": "af",
        u"Complément familial (CF)": "cf",
        u"Allocation de rentrée scolaire (ARS)": "ars",
        u"Aide à la scolarité": None,
        u"Allocation de soutien familial (ASF)": "asf",
        u"Allocation d’éducation de l’enfant handicapé (AEEH)": "aeeh",
        u"Allocation (journalière) de présence parentale (AJPP)": None,
        u"Dt complément lié à des dépenses l'état de santé de l'E": None,
        u"Salaire unique - frais de garde, majorations": None,
        u"Allocations prénatales": None,
        u"Allocations postnatales": None,
        u"Congé de naissance": None,
        u"Prime de protection de la maternité": None,
        u"Prestations hors métropole": None,
        u"Allocation différentielle": None,
        u"Allocataires sous tutelles": None,
        u"Logement": None,
        u"Allocation logement familiale (ALF)": "alf",
        u"Aide personnalisée au logement (APL)": "apl",
        u"Allocation logement sociale (ALS)": "als",
        u"Allocation d'installation de l'étudiant (ALINE, 31/12)": None,
        u"Prime de déménagement (au cours de l'année)": None,
        u"Minima sociaux et contrats aidés": None,
        u"RSA + RMI + API": None,
        u"Allocation de parent isolé (API)": "api",
        u"Allocation pour adultes handicapés (AAH)": "aah",
        u"Majoration pour vie autonome (MVA), compl. (AFH)": "caah",
        u"Garantie de ressources pour handicapés (GRPH)": None,  # caah ?
        u"Revenu minimum d'insertion (RMI)": "rmi",
        u"Revenu de solidarité active - droit commun (RSA)": "rsa",
        u"Dt RSA socle seulement": "rsa_socle",
        u"Dt RSA socle + activité": None,
        u"Dt RSA activité seulement": None,
        u"Dt RSA jeunes": None,
        u"RSA jeunes socle seulement": None,
        u"RSA jeunes socle + activité": None,
        u"RSA jeunes activité seulement": None,
        u"Dt RSA avec majoration isolement": None,
        u"RSA majoré socle seulement": None,
        u"RSA majoré socle + activité": None,
        u"RSA majoré activité seulement": None,
        u"Dt RSA sans majoration isolement (hors RSA jeunes)": None,
        u"RSA socle seulement": None,
        u"RSA socle + activité": None,
        u"RSA activité seulement": None,
        u"Contrat d'insertion - revenu minimum d'activité (CIRMA)": None,
        u"Supplément de revenu familial (SURF)": None,
        u"Allocation spécifique d'attente (ASA)": None,
        u"Contrat d'avenir (CAV)": None,
        u"Prime de retour à l'emploi (PRE, décret et loi, 1 000 €)": None,
        u"Nouveaux intéressements - loi  retour à l'emploi 10/2006": None,
        u"Revenu de solidarité active expérimental (RSA)": None,
        }

    variable_by_slugified_table_entry = dict([
        (slugify(table_entry, separator = "_"), variable)
        for table_entry, variable in variable_by_table_entry.iteritems()
        if variable is not None]
        )
    csv_file_path = os.path.join(
        prestations_sociales_directory,
        'clean',
        'historique_beneficiaires.csv'
        )
    data_frame = (data_frame
        .rename(index = lambda x: slugify(x.encode('utf-8') if not isinstance(x, float) else str(x), separator = "_"))
        .rename(index = variable_by_slugified_table_entry)
        )

    assert 'af' in data_frame.index
    data_frame.drop([u'nan'], inplace = True)
    assert not(u'nan' in data_frame.index)

    # Adjust paje_adoption to reflect whole year
    data_frame.loc['paje_naissance', data_frame.columns] = 12 * data_frame.loc['paje_naissance', data_frame.columns]
    data_frame.to_csv(csv_file_path, encoding='utf-8')
    print csv_file_path


def build_minimum_vieillesse_serie():
    directory = os.path.join(
        prestations_sociales_directory,
        'raw',
        'statistiques_recherches_cnav_fr',
        )

    minimum_vieillesse = pd.read_excel(
        os.path.join(
            directory,
            'Les%20allocataires%20du%20minimum%20vieillesse%20en%20stock%20depuis%201994.xls',
            ),
        header = [1, 2],
        index_col = 0,
        skip_footer = 3,
        parse_cols= 'A:M',
        ).stack().unstack(level = 0)
    minimum_vieillesse = (
        minimum_vieillesse.loc[[row for row in minimum_vieillesse.index if row.startswith("Nombre de prestataires")]]
        ).copy()
    # \n\nNombre total de retraités\n\n (b)    Inutile
    # \n%\n de prestataires\n\n(a/b)           Inutile
    # Nombre d'allocataires du minimum vieillesse(2)   On compte 2 pour des aspa couples (bniveau individuel)
    # Nombre de prestataires bénéficiaires d'un minim  On compte 1 pour un couple
    minimum_vieillesse.index = ['minimum_vieillesse']
    csv_file_path = os.path.join(
        prestations_sociales_directory,
        'clean',
        'historique_beneficiaires_minimum_vieillesse.csv'
        )
    minimum_vieillesse = minimum_vieillesse / 1000
    minimum_vieillesse[u'Métropole'].to_csv(csv_file_path, encoding='utf-8')


if __name__ == '__main__':
    build_historical_amounts_data()
    build_historical_beneficiaries_data()
    build_minimum_vieillesse_serie()
