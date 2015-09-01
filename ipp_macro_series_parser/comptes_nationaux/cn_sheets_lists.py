# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:22:19 2015

@author: sophie.cottet

This script gives the list dictionnaries of the variables needed to recreate the different excel sheets of
'Agrégats IPP - Comptabilité nationale.xls', i.e. the economic / Piketty presentation of the Comptabilité nationale
agregates.
These lists are called by the function cn_output.output_for_sheets.
TODO: a function which calls them all, applies formulas and formats the excel sheet so as to reproduce the actual
formatting.
"""


# CN1

input_CN1 = {
        'Produit_interieur_brut_PIB': {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
        'Produit_interieur_net_PIN': {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'},
        'Revenu_national_brut': {'code': None, 'institution': 'S1', 'ressources': False,
                                 'description': 'revenu national brut en milliards d'},
    # Revenus versés par reste du monde
        'Salaires_verses_au_rdm': {'code': 'D11', 'institution': 'S2', 'ressources': True, 'description': '', 'drop': True},  # salaires reçus par RDM
        'Salaires_verses_par_rdm': {'code': 'D11', 'institution': 'S2', 'ressources': False, 'description': '', 'drop': True},  # salaires versés par RDM
        'Interets_verses_par_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': False, 'description': '', 'drop': True},  # ce qui suit compose les intérêts et dividendes versés par RDM ("provenance")
        'Dividendes_verses_par_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': False, 'description': '', 'drop': True},
        'Dividendes_verses_par_rdm_D43': {'code': 'D43', 'institution': 'S2', 'ressources': False, 'description': '', 'drop': True},
        'Revenus_de_la_propriete_verses_par_rdm': {'code': 'D44', 'institution': 'S2', 'ressources': False, 'description': '', 'drop': True},
        'Interets_verses_au_rdm': {'code': 'D41', 'institution': 'S2', 'ressources': True, 'description': '', 'drop': True},  # ce qui suit compose les intérêts et dividendes versés par RDM
        'Dividendes_verses_au_rdm_D42': {'code': 'D42', 'institution': 'S2', 'ressources': True, 'description': '', 'drop': True},
        'Dividendes_verses_au_rdm_D43': {'code': 'D43', 'institution': 'S2', 'ressources': True, 'description': '', 'drop': True},
        'Revenus_de_la_propriete_verses_au_rdm': {'code': 'D44', 'institution': 'S2', 'ressources': True, 'description': '', 'drop': True},
    # Dépréciation du capital fixe (CCF) : économie nationale, APUs, ISBLSM
        'Consommation_de_capital_fixe_economie_nationale': {'code': 'P51c', 'institution': 'S1', 'ressources': False, 'description': ''},
#        'Consommation_de_capital_fixe _-_APU': {'code': 'P51c', 'institution': 'S13', 'ressources': False, 'description': ''},
#        'Consommation_de_capital_fixe _-_ISBLSM': {'code': 'P51c', 'institution': 'S15', 'ressources': False, 'description': ''},
    # Variables CN2, nécessaires pour reconstruction du Revenu national façon Piketty
        'Sal_verses_SNF': {'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # salaires versés. il nous les faut pour à peu près toutes les institutions
        'Sal_verses_SF': {'code': 'D11', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Sal_verses_par_APU': {'code': 'D11', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'Sal_verses_par_menages': {'code': 'D11', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'Sal_verses_par_ISBLSM': {'code': 'D11', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'ene_menages': {'code': 'B2n', 'institution': 'S14', 'ressources': False, 'description': ''},  # ENE ménages (ie loyers reçus)
        'Revenu_mixte_net_des_menages_non_salaries': {'code': 'B3n', 'institution': 'S1', 'ressources': False, 'description': ''},   # Revenu mixte / non-salariés
        'cs_eff_empl_SNF': {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # cotisations patronales effectives
        'cs_eff_empl_SF': {'code': 'D121', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_APU': {'code': 'D121', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_Menages': {'code': 'D121', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'cs_eff_empl_ISBLSM': {'code': 'D121', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_SNF': {'code': 'D122', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # cotisations patronales imputées
        'cs_imput_empl_SF': {'code': 'D122', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_APU': {'code': 'D122', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_Menages': {'code': 'D122', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'cs_imput_empl_ISBLSM': {'code': 'D122', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
# Excedent_net_d_exploitation_ENE_SNF
        'ene_snf': {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # ENE SNF
        'ene_sf': {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},  # ENE SF
        'Impots_sur_les_produits_ressources_APU': {'code': 'D21', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},  # impôts indirects : impôts nets sur les produits & impôts nets sur la production
        'Subventions_sur_les_produits_ressources_APU': {'code': 'D31', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},
        'Autres_impots_sur_la_production_ressources_APU': {'code': 'D29', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},
        'Autres_subventions_sur_la_production_ressources_APU': {'code': 'D39', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True}  # NB : D39 est aussi dans un autre compte (le compte d'exploitation) pour les APUs, en emplois. donc bien renseigner ressources..
        }

formulas_CN1 = {
    'Profits_des_societes': {
        'formula': 'ene_snf + ene_sf',
        'drop': True},
    'Sal_cs_verses_societes': {
        'formula': 'Sal_verses_SNF + Sal_verses_SF + cs_eff_empl_SNF + cs_eff_empl_SF + cs_imput_empl_SNF + cs_imput_empl_SF',
        'drop': True},
    'VA_Societes': {
        'formula': 'Profits_des_societes + Sal_cs_verses_societes',
        'drop': True},
    'VA_Immobilier_Loyers': {
        'formula': 'ene_menages',
        'drop': True},  # vérifier que ça passe bien.
    'Revenu_d_activite_des_non_salaries': {
        'formula': 'Revenu_mixte_net_des_menages_non_salaries',
        'drop': True},  # vérifier que ça passe bien.
    'Salaires_et_cot_soc_verses_par_les_non_salaries_et_les_menages': {
        'formula': 'Sal_verses_par_menages + cs_eff_empl_Menages + cs_imput_empl_Menages',
        'drop': True},
    'VA_APU_et_ISBLSM': {
        'formula': 'Sal_verses_par_APU + Sal_verses_par_ISBLSM + cs_eff_empl_APU + cs_eff_empl_ISBLSM + cs_imput_empl_APU + cs_imput_empl_ISBLSM',
        'drop': True},
    'Impots_indirects': {
        'formula': 'Impots_sur_les_produits_ressources_APU - Subventions_sur_les_produits_ressources_APU + Autres_impots_sur_la_production_ressources_APU - Autres_subventions_sur_la_production_ressources_APU',
        'drop': True},
    '%_Produit_interieur_net_/_Revenu_national': {
        'formula': 'Produit_interieur_net_PIN / Revenu_national_brut'},
    '%_Revenus_reste_du_monde_/_Revenu_national': {
        'formula': 'Revenus_verses_par_rdm_nets / Revenu_national_brut'},
#    'Depreciation_du_capital_(CCF)': {
#        'formula': 'Consommation_de_capital_fixe _-_APU + Consommation_de_capital_fixe _-_ISBLSM + '},
    'CCF_/_PIB': {
        'formula': 'Consommation_de_capital_fixe_economie_nationale / Produit_interieur_brut_PIB'},  # voir si on utilise la CCF Piketty (à calculer)
# 'Taux_de_croissance_du_PIB_entre_l_annee_N-2_et_l_annee_N-1'
    '%_Revenu_national_/_PIB': {
        'formula': 'Revenu_national_brut / Produit_interieur_brut_PIB'},  # voir si on prend plutôt le RNB Piketty
    'Salaires_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Salaires_verses_par_rdm - Salaires_verses_au_rdm',
        'drop': True},
    'Interets_et_dividendes_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42 + Dividendes_verses_par_rdm_D43 + Revenus_de_la_propriete_verses_par_rdm - Interets_verses_au_rdm - Dividendes_verses_au_rdm_D42 - Dividendes_verses_au_rdm_D43 - Revenus_de_la_propriete_verses_au_rdm',
        'drop': True},
    'Revenus_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Salaires_verses_par_rdm_nets + Interets_et_dividendes_verses_par_rdm_nets',},
    'Revenu_national_Piketty': {
        'formula': 'VA_Societes + VA_Immobilier_Loyers + Revenu_d_activite_des_non_salaries + Salaires_et_cot_soc_verses_par_les_non_salaries_et_les_menages + VA_APU_et_ISBLSM + Impots_indirects + Revenus_verses_par_rdm_nets'},
    }

variables_CN1 = input_CN1.copy()
variables_CN1.update(formulas_CN1)

# CN2

input_CN2 = {
        'Salaires_verses_par_SNF': {'code': 'D11', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # salaires versés. il nous les faut pour à peu près toutes les institutions
        'Salaires_verses_par_SF': {'code': 'D11', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Salaires_verses_par_APU': {'code': 'D11', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'Salaires_verses_par_menages': {'code': 'D11', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'Salaires_verses_par_ISBLSM': {'code': 'D11', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'Excedent_net_d_exploitation_(ENE)_des_menages': {'code': 'B2n', 'institution': 'S14', 'ressources': False, 'description': ''},  # ENE ménages (ie loyers reçus)
        'Revenu_mixte_net_des_menages_(non-salaries)': {'code': 'B3n', 'institution': 'S1', 'ressources': False, 'description': ''},   # Revenu mixte / non-salariés
        'Cot_soc_effectives_employeurs_SNF': {'code': 'D121', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # cotisations patronales effectives
        'Cot_soc_effectives_employeurs_SF': {'code': 'D121', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_effectives_employeurs_APU': {'code': 'D121', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_effectives_employeurs_Menages': {'code': 'D121', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_effectives_employeurs_ISBLSM': {'code': 'D121', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_imputees_employeurs_SNF': {'code': 'D122', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # cotisations patronales imputées
        'Cot_soc_imputees_employeurs_SF': {'code': 'D122', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_imputees_employeurs_APU': {'code': 'D122', 'institution': 'S13', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_imputees_employeurs_Menages': {'code': 'D122', 'institution': 'S14', 'ressources': False, 'description': '', 'drop': True},
        'Cot_soc_imputees_employeurs_ISBLSM': {'code': 'D122', 'institution': 'S15', 'ressources': False, 'description': '', 'drop': True},
        'Excedent_net_d_exploitation_(ENE)_SNF': {'code': 'B2n', 'institution': 'S11', 'ressources': False, 'description': '', 'drop': True},  # ENE SNF
        'Excedent_net_d_exploitation_(ENE)_SF': {'code': 'B2n', 'institution': 'S12', 'ressources': False, 'description': '', 'drop': True},  # ENE SF
        'Impots_sur_les_produits_(ressources_APU)': {'code': 'D21', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},  # impôts indirects : impôts nets sur les produits & impôts nets sur la production
        'Subventions_sur_les_produits_(ressources_APU)': {'code': 'D31', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},
        'Autres_impots_sur_la_production_(ressources_APU)': {'code': 'D29', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True},
        'Autres_subventions_sur_la_production_(ressources_APU)': {'code': 'D39', 'institution': 'S13', 'ressources': True, 'description': '', 'drop': True}  # NB : D39 est aussi dans un autre compte (le compte d'exploitation) pour les APUs, en emplois. donc bien renseigner ressources..
        }

formulas_CN2 = {
    'Profits_des_societes': {
        'formula': 'Excedent_net_d_exploitation_(ENE)_SNF + Excedent_net_d_exploitation_(ENE)_SF'},
    'Salaires_et_cot_soc_verses_par_les_societes': {
        'formula': 'Salaires_verses_par_SNF + Salaires_verses_par_SF + Cot_soc_effectives_employeurs_SNF + Cot_soc_effectives_employeurs_SF + Cot_soc_imputees_employeurs_SNF + Cot_soc_imputees_employeurs_SF'},
    'VA_Societes': {
        'formula': 'Profits_des_societes + Salaires_et_cot_soc_verses_par_les_societes'},
    'VA_Immobilier_(Loyers)': {
        'formula': 'Excedent_net_d_exploitation_(ENE)_des_menages'},  # vérifier que ça passe bien.
    'Revenu_d_activite_des_non_salaries': {
        'formula': 'Revenu_mixte_net_des_menages_(non-salaries)'},  # vérifier que ça passe bien.
    'Salaires_et_cot_soc_verses_par_les_non_salaries_et_les_menages': {
        'formula': 'Salaires_verses_par_menages + Cot_soc_effectives_employeurs_Menages + Cot_soc_imputees_employeurs_Menages'},
    'VA_APU_et_ISBLSM': {
        'formula': 'Salaires_verses_par_APU + Salaires_verses_par_ISBLSM + Cot_soc_effectives_employeurs_APU + Cot_soc_effectives_employeurs_ISBLSM + Cot_soc_imputees_employeurs_APU + Cot_soc_imputees_employeurs_ISBLSM'},
    'Impots_indirects': {
        'formula': 'Impots_sur_les_produits_(ressources_APU) - Subventions_sur_les_produits_(ressources_APU) + Autres_impots_sur_la_production_(ressources_APU) - Autres_subventions_sur_la_production_(ressources_APU)'},
    'Salaires_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Salaires_verses_par_rdm - Salaires_verses_au_rdm',
        'drop': True},
    'Interets_et_dividendes_verses_par_rdm_nets': {
        'code': None,
        'institution': 'S2',
        'ressources': False,
        'formula': 'Interets_verses_par_rdm + Dividendes_verses_par_rdm_D42 + Dividendes_verses_par_rdm_D43 + Revenus_propriete_verses_par_rdm - Interets_verses_au_rdm - Dividendes_verses_au_rdm_D42 - Dividendes_verses_au_rdm_D43 - Revenus_propriete_verses_au_rdm',
        'drop': True},
    'Revenu_national_(Piketty)': {
        'formula': 'VA_Societes + VA_Immobilier_(Loyers) + Revenu_d_activite_des_non_salaries + Salaires_et_cot_soc_verses_par_les_non_salaries_et_les_menages + VA_APU_et_ISBLSM + Impots_indirects + Revenus_verses_par_rdm_nets'},
    }

variables_CN2 = input_CN2.copy()
variables_CN2.update(formulas_CN2)
