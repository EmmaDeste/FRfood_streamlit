import pandas as pd

# because I had a FileNotFound error
import os
repertoire_actuel = os.getcwd()
fichiers = os.listdir(repertoire_actuel)
print("Fichiers dans le répertoire actuel:")
for fichier in fichiers:
    print(fichier)

# read the database
conso = pd.read_csv("conso-compo-alim-vf-mad-datagouv2021.csv", delimiter=";", low_memory=False)

# DATA TRANSFORMATION

# Only 'Pop3' in the POPULATION column, and only '1' in the aliment_marque_enrichi column, so I delete these column.
conso = conso.drop('POPULATION', axis=1)
conso = conso.drop('aliment_marque_enrichi', axis=1)

# Many columns are not consistent for my analysis.
columns1 = ['NUM_LIGNE', 'R24_num', 'R24_nombre', 'R24_pond', 'occ_lieu', 'aliment_code_INCA3', 'aliment_code_FX']
columns2 = ['occ_type', 'occ_alim_num', 'qte_conso_pond', 'occ_alim_num_seq', 'gpe_INCA3', 'aliment_libelle_FX']
columns3 = ['polyols', 'ag_16_0', 'ag_18_0', 'ag_14_0', 'ag_12_0', 'ag_10_0', 'ag_04_0', 'ag_06_0', 'ag_08_0']
columns4 = ['agmi', 'ag_18_1_ole', 'agpi', 'ag_18_2_lino', 'ag_18_3_a_lino', 'ag_20_4_ara', 'ag_20_5_epa', 'ag_20_6_dha']
columns5 = ['facette_01', 'facette_02', 'facette_03', 'facette_04', 'facette_05', 'facette_06', 'facette_07']
columns6 = ['facette_08', 'facette_09', 'facette_10', 'facette_12', 'facette_13', 'facette_14', 'facette_19']
columns7 = ['facette_20', 'facette_25', 'facette_27', 'facette_27_libelle']
columns8 = ['facette_06_libelle', 'facette_12_libelle', 'facette_13_libelle', 'facette_14_libelle', 'facette_25_libelle']
columns9 = ['vitamine_b1', 'vitamine_b2', 'vitamine_b3', 'vitamine_b5', 'vitamine_b6', 'vitamine_b9', 'vitamine_b12']
columns10 = ['aesa', 'manganese', 'acides_organiques', 'retinol', 'beta_carotene', 'selenium']
columns_to_delete = columns1 + columns2 + columns3 + columns4 + columns5 + columns6 + columns7 + columns8 + columns9 + columns10

conso = conso.drop(columns=columns_to_delete)

# Some columns have more than 75% of the information missing. So I delete these columns.
columns1 = ['facette_01_libelle', 'facette_02_libelle', 'facette_03_libelle', 'facette_04_libelle']
columns2 = ['facette_05_libelle', 'facette_07_libelle', 'facette_08_libelle', 'facette_19_libelle', 'facette_20_libelle']
columns_null = columns1 + columns2

conso = conso.drop(columns=columns_null)

# The same way, deleting the lines with some empty cells.
conso = conso.dropna(subset=['occ_alim_libelle'])

# Normalize all the textual data, to avoid separation of same data because of the case.
conso = conso.apply(lambda col: col.str.lower() if col.dtype == 'O' else col)

# Convertir l'heure en format datetime, pour une bonne visualisation.
conso['occ_hdeb'] = pd.to_datetime(conso['occ_hdeb'], format='%H:%M')


# add new column for delivery ways

conso['preparation_style'] = conso['facette_10_libelle']

# drop columns having no details
non_renseigne_columns = conso[conso['facette_10_libelle'] == 'non renseigné'].index
conso['preparation_style'] = conso['preparation_style'].drop(non_renseigne_columns)
conso['preparation_style'] = conso['preparation_style'].drop(conso[conso['facette_10_libelle'] == 'ne connait pas le mode de préparation ou de production de l’aliment'].index)
conso['preparation_style'] = conso['preparation_style'].drop(conso[conso['facette_10_libelle'] == 'non préparé maison sans précision'].index)


# Garder que les aliments principaux des plats, et pas le descriptif complet.

# - Boissons
# eau plate (TOP)
condition = conso['occ_alim_libelle'].str.contains(r'\beau\b', case=False)
        # syntaxe pour obtenir le mot 'eau' seulement et éviter les mots comme gateau, veau ou poireau

conso.loc[condition, 'occ_alim_libelle'] = 'eau'

conso.loc[conso['occ_alim_libelle'].str.contains('cristaline', case=False), 'occ_alim_libelle'] = 'eau'
conso.loc[conso['occ_alim_libelle'].str.contains('hépar', case=False), 'occ_alim_libelle'] = 'eau'

# eau gazeuse
conso.loc[conso['occ_alim_libelle'].str.contains('eau minérale gazeuse', case=False), 'occ_alim_libelle'] = 'eau pétillante'

# soda
conso.loc[conso['occ_alim_libelle'].str.contains('gazeu', case=False), 'occ_alim_libelle'] = 'soda'
conso.loc[conso['occ_alim_libelle'].str.contains('soda', case=False), 'occ_alim_libelle'] = 'soda'

# coca
conso.loc[conso['occ_alim_libelle'].str.contains('coca', case=False), 'occ_alim_libelle'] = 'coca cola'

# chocolat chaud
condition = conso['occ_alim_libelle'].str.contains('chocolat chaud|lait+chocolat', case=False)

conso.loc[condition, 'occ_alim_libelle'] = 'chocolat chaud'

# café (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('café', case=False), 'occ_alim_libelle'] = 'café'
conso.loc[conso['occ_alim_libelle'].str.contains('déca', case=False), 'occ_alim_libelle'] = 'café'

# tisane (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('tisane', case=False), 'occ_alim_libelle'] = 'tisane'
conso.loc[conso['occ_alim_libelle'].str.contains('infusion', case=False), 'occ_alim_libelle'] = 'tisane'

# thé (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('thé', case=False), 'occ_alim_libelle'] = 'thé'
conso.loc[conso['occ_alim_libelle'].str.contains('the', case=False), 'occ_alim_libelle'] = 'thé'

# cocktail
conso.loc[conso['occ_alim_libelle'].str.contains('cocktail', case=False), 'occ_alim_libelle'] = 'cocktail'

# alcool forts = digestifs
condition = conso['occ_alim_libelle'].str.contains('rhum|wisky', case=False)

conso.loc[condition, 'occ_alim_libelle'] = 'alcool fort'

# alcool vin (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains(r'\bvin\b', case=False), 'occ_alim_libelle'] = 'vin'

# jus de fruits (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('jus', case=False), 'occ_alim_libelle'] = 'jus de fruits'

# - Apero
# pain (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('pain', case=False), 'occ_alim_libelle'] = 'pain'
conso.loc[conso['occ_alim_libelle'].str.contains('baguette', case=False), 'occ_alim_libelle'] = 'pain'

# fromage (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('fromage', case=False), 'occ_alim_libelle'] = 'fromage'

# chips
conso.loc[conso['occ_alim_libelle'].str.contains('chips', case=False), 'occ_alim_libelle'] = 'chips'

# saucisson
condition = conso['occ_alim_libelle'].str.contains('saucisson|bridou', case=False) & conso['occ_alim_libelle'].str.contains('morceau', case=False)
conso.loc[condition, 'occ_alim_libelle'] = 'saucisson'

# - Plats
# salade verte (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('^salade mache$', case=False), 'occ_alim_libelle'] = 'salade verte'

# salade composée (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('salade', case=False), 'occ_alim_libelle'] = 'salade composée'

# sandwich
conso.loc[conso['occ_alim_libelle'].str.contains('sandwich', case=False), 'occ_alim_libelle'] = 'sandwich'

# porc
conso.loc[conso['occ_alim_libelle'].str.contains('porc', case=False), 'occ_alim_libelle'] = 'porc'

# veau (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('porc', case=False), 'occ_alim_libelle'] = 'veau'

# canard
conso.loc[conso['occ_alim_libelle'].str.contains('canard', case=False), 'occ_alim_libelle'] = 'canard'

# saumon
conso.loc[conso['occ_alim_libelle'].str.contains('saumon', case=False), 'occ_alim_libelle'] = 'saumon'

# frites (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('frite', case=False), 'occ_alim_libelle'] = 'frites'

# pomme de terre (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('patat', case=False), 'occ_alim_libelle'] = 'pomme de terre'

# pates (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('pâte', case=False), 'occ_alim_libelle'] = 'plats de pâtes'
conso.loc[conso['occ_alim_libelle'].str.contains('pate', case=False), 'occ_alim_libelle'] = 'plats de pâtes'
conso.loc[conso['occ_alim_libelle'].str.contains('patte', case=False), 'occ_alim_libelle'] = 'plats de pâtes'

# - Desserts
# dessert saveur chocolat (TOP)
condition = conso['occ_alim_libelle'].str.contains('chocolat|choclat', case=False)
conso.loc[condition, 'occ_alim_libelle'] = 'dessert chocolat'

# gateau (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('gateau', case=False), 'occ_alim_libelle'] = 'gateau'

# yaourt (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('yaourt', case=False), 'occ_alim_libelle'] = 'yaourt'

# compote (TOP)
conso.loc[conso['occ_alim_libelle'].str.contains('compte', case=False), 'occ_alim_libelle'] = 'compote'
conso.loc[conso['occ_alim_libelle'].str.contains('compote', case=False), 'occ_alim_libelle'] = 'compote'

# (pour les habitudes matinales)
conso.loc[conso['occ_alim_libelle'].str.contains('cereale', case=False), 'occ_alim_libelle'] = 'céréales'
conso.loc[conso['occ_alim_libelle'].str.contains('céréale', case=False), 'occ_alim_libelle'] = 'céréales'

conso.loc[conso['occ_alim_libelle'].str.contains('brioche', case=False), 'occ_alim_libelle'] = 'brioche'

conso.loc[conso['occ_alim_libelle'].str.contains('lait', case=False), 'occ_alim_libelle'] = 'lait'

conso.loc[conso['occ_alim_libelle'].str.contains('ricoré', case=False), 'occ_alim_libelle'] = 'café'

conso.loc[conso['occ_alim_libelle'].str.contains('biscotte', case=False), 'occ_alim_libelle'] = 'biscottes'


# 1, 2, 3, 5. Enregistrer les consommations habituelles
conso.to_csv('consommation_fr.csv', index=False)


# 4. Histogram: Enregistrer par tranche horaire précise
conso4 = conso.copy()

conso4 = conso4[conso4['occ_alim_libelle'] != 'dessert chocolat']
conso4.loc[conso4['occ_alim_libelle'].str.contains('fromage', case=False), 'occ_alim_libelle'] = 'fromage blanc'
conso4.loc[conso4['occ_alim_libelle'].str.contains('pain', case=False), 'occ_alim_libelle'] = 'tartines'
conso4.loc[conso4['occ_alim_libelle'].str.contains('tartine', case=False), 'occ_alim_libelle'] = 'tartines'

conso4.to_csv('morning_conso.csv', index=False)


# 6. Heatmap: ou pas
# warning called "value is trying to be set on a copy of a slice from a DataFrame"
style = conso.copy()
style = style.dropna(subset=['preparation_style'])

# replace names for easier lisibility while visualizing
style.loc[style['preparation_style'].str.contains('rapide', case=False), 'preparation_style'] = 'restauration rapide'
style.loc[style['preparation_style'].str.contains(' classique', case=False), 'preparation_style'] = 'restaurant'
style.loc[style['preparation_style'].str.contains('industriel', case=False), 'preparation_style'] = 'industriel'
style.loc[style['preparation_style'].str.contains('artisan', case=False), 'preparation_style'] = 'artisan'
style.loc[style['preparation_style'].str.contains('fait maison', case=False), 'preparation_style'] = 'fait maison'
style.loc[style['preparation_style'].str.contains('cantine', case=False), 'preparation_style'] = 'cantine'
style.loc[style['preparation_style'].str.contains('automatique', case=False), 'preparation_style'] = 'distributeur'
style.loc[style['preparation_style'].str.contains('artisan', case=False), 'preparation_style'] = 'artisan'

# extract the hour for the visu
style['occ_hdeb'] = pd.to_datetime(style['occ_hdeb'], format='%Y-%m-%d %H:%M:%S')
style.loc[:, 'hour'] = style['occ_hdeb'].dt.hour

style.to_csv('prep_style.csv', index=False)

# Conserver que les colonnes concernant les heures et la santé
columns1 = ['NOIND', 'occ_alim_libelle', 'aliment_libelle_INCA3', 'qte_conso', 'facette_09_libelle', 'facette_10_libelle']
columns2 = ['aliment_marque_bio']
columns_to_delete = columns1 + columns2
conso = conso.drop(columns=columns_to_delete)

conso.to_csv('sante_fr.csv', index=False)
