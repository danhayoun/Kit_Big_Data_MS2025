import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import sys
import os
import pytest



import src.temps_de_cuisson as cr



def test_generate_accurate_df() :
    df = pd.read_pickle("./data/preprocess/recipe_filtered.pkl")
    assert 'minutes' not in df.columns
    assert 'name' not in df.columns

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    recipe_path = os.path.join(base_dir, "data/raw/RAW_recipes.csv")

    df = cr.Page_temps_de_cuisson.generate_accurate_df(df, recipe_path)
    assert 'minutes','name' in df.columns

def test_add_intervalle() :
    df = pd.read_pickle("./data/preprocess/recipe_filtered.pkl")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    recipe_path = os.path.join(base_dir, "data/raw/RAW_recipes.csv")

    df = cr.Page_temps_de_cuisson.generate_accurate_df(df,recipe_path)
    assert 'intervalle' not in df.columns
    df = cr.Page_temps_de_cuisson.add_intervalle(df)
    assert 'intervalle' in df.columns

def test_get_vectors() :

    tst_df = pd.DataFrame({
        'submitted': [10 for i in range(182)],
        'id': [i for i in range(182)],
        'minutes': [i**2 for i in range(182)],
    })

    tst_df['submitted'] = pd.to_datetime(tst_df['submitted'], errors='coerce')


    vector,vector_id = cr.Page_temps_de_cuisson.get_vectors(tst_df)

    assert np.array_equal(vector, np.array([i**2 for i in range(182)])), "Test échoué pour vector"
    assert np.array_equal(vector_id, np.array([i for i in range(182)])), "Test échoué pour vector_id"




def test_dictionnaire_minutes() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])}
    vector_id = l[:,0]
    vector = l[:,1]
    dictionnaire_obtenu = cr.Page_temps_de_cuisson.dictionnaire_minutes(vector,vector_id)
    assert dictionnaire_verif == dictionnaire_obtenu, "Les deux dictionnaires sont différents"




def test_top_liste() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    top = cr.Page_temps_de_cuisson.top_liste(dictionnaire_verif)
    l_test = [(i,i**2) for i in range(100)]
    l_test = l_test[::-1]
    assert top == l_test , "la liste obtenu est incorrecte "



def test_boxplot() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    cr.Page_temps_de_cuisson.boxplot(dictionnaire_verif)



def test_filtre_minutes() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    dictionnaire = cr.Page_temps_de_cuisson.filtre_minutes(dictionnaire)
    l_verif = np.array([[i,i**2] for i in range(1,32)]) #Jusqu'à 31, x**2 ne dépasse pas 1000
    dictionnaire_verif = {i : j for i,j in zip(l_verif[:,0],l_verif[:,1])}

    assert dictionnaire == dictionnaire_verif, "les deux dictionnaires sont différents"


def test_generate_cursor_dataframe():
    # Dataframe factice
    df = pd.DataFrame({
        'season': ['Spring', 'Winter', 'Summer', 'Fall'] * 50,  # 200 lignes
        'minutes': [i % 181 + 1 for i in range(200)],  # Valeurs de 1 à 181 en boucle
    })
    
    result = cr.Page_temps_de_cuisson.generate_cursor_dataframe(df)
    

    assert isinstance(result, pd.DataFrame), "Le résultat doit être un DataFrame."
    
    expected_columns = ['intervalle', 'Spring', 'Winter', 'Summer', 'Fall', 
                        'Spring_%', 'Winter_%', 'Summer_%', 'Fall_%', 'nb_recettes_total']
    assert list(result.columns) == expected_columns, "Les colonnes du DataFrame ne correspondent pas à celles attendues."
    
    assert result['intervalle'].tolist() == list(range(182)), "La colonne 'intervalle' ne contient pas les valeurs correctes."
    
    for col in ['Spring', 'Winter', 'Summer', 'Fall']:
        assert all(isinstance(x, int) for x in result[col]), f"La colonne '{col}' doit contenir uniquement des entiers."
    
    for saison in ['Spring', 'Winter', 'Summer', 'Fall']:
        assert result[f'{saison}_%'].notna().all(), f"La colonne '{saison}_%' contient des valeurs NaN."

    #assert all(abs(result[['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']].sum(axis=1) - 100) < 1), \
    #    "La somme des pourcentages pour chaque ligne doit être proche de 100."

    # Vérifier la colonne 'nb_recettes_total'
    assert all(result['nb_recettes_total'] == result[['Spring', 'Winter', 'Summer', 'Fall']].sum(axis=1)), \
        "La colonne 'nb_recettes_total' doit être la somme des colonnes de comptage."


def test_df_to_pickle() :
    tst_df = pd.DataFrame({
        'submitted': [np.nan for i in range(182)],
        'id': [i for i in range(182)],
        'minutes': [i**2 for i in range(182)],
    })
    df_attendu = pd.DataFrame({
        'submitted': [0 for i in range(182)],
        'id': [i for i in range(182)],
        'minutes': [i**2 for i in range(182)],
    })
    cr.Page_temps_de_cuisson.df_to_pickle(tst_df,"tst_df.pkl")

    df = pd.read_pickle("tst_df.pkl")
    df = df.astype(int) #car le chargement donne des flottants, donc la fonction assert renvoie une erreur : les types des données sont différents. Or on ne se soucie pas de leurs types (ce sont des entiers ou des flottants) donc on force tout à int.
    assert np.nan not in df
    pd.testing.assert_frame_equal(df, df_attendu)

    os.remove("tst_df.pkl")


def test_generate_camemberts_significatifs():
    # Dataframe factice
    df = pd.DataFrame({
        'season': ['Winter', 'Winter', 'Summer', 'Fall', 'Spring', 'Spring'],
        'minutes': [5, 15, 45, 75, 135, 200]
    })
    
    output_path = "df_significatif_test.pkl"
    
    df_significatif = cr.Page_temps_de_cuisson.generate_camemberts_significatifs(df, output_path)
    
    assert os.path.exists(output_path), "Le fichier de sortie n'a pas été cr.Page_temps_de_cuissonéé."
    
    df_significatif_loaded = pd.read_pickle(output_path)
    
    expected_columns = ['intervalle', 'Spring', 'Winter', 'Summer', 'Fall', 
                        'Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']
    assert list(df_significatif.columns) == expected_columns, "Les colonnes du DataFrame généré ne correspondent pas."
    
    # Vérifier que les pourcentages sont bien calculés
    for saison in ['Spring', 'Winter', 'Summer', 'Fall']:
        assert (df_significatif[f'{saison}_%'].notna()).all(), f"La colonne '{saison}_%' contient des NaN."

    assert all(abs(df_significatif[['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']].sum(axis=1) - 100) < 1e-6), \
        "Les pourcentages ne somment pas à 100."

    expected_intervals = ['10', '30', '1h', '2h', '+']
    assert df_significatif['intervalle'].tolist() == expected_intervals, "Les intervalles ne correspondent pas au mapping attendu."
    pd.testing.assert_frame_equal(df_significatif, df_significatif_loaded, check_dtype=False, obj="DataFrame généré et sauvegardé")

    os.remove("df_significatif_test.pkl")


def test_top_by_interval_season():
    # Dataframe factice
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'season': ['Winter', 'Winter', 'Summer', 'Summer', 'Fall', 'Fall', 'Spring', 'Spring', 'Winter', 'Summer'],
        'intervalle': [10, 30, 10, 30, 10, 30, 10, 30, 60, 120],
        'weighted_rating': [4.5, 3.0, 5.0, 4.0, 4.2, 4.8, 3.5, 4.7, 4.6, 5.0]
    })
    
    result = cr.Page_temps_de_cuisson.top_by_interval_season(df)
    
    assert isinstance(result, dict), "Le résultat doit être un dictionnaire."

    expected_keys = [(saison, intervalle) for saison in ['Winter', 'Summer', 'Fall', 'Spring'] for intervalle in [10, 30, 60, 120, 121]]
    assert set(result.keys()) == set(expected_keys), "Les clés du dictionnaire ne correspondent pas à celles attendues."
    

    for key, value in result.items():
        assert isinstance(value, list), f"La valeur pour {key} doit être une liste."
    
    for key, value in result.items():
        assert len(value) <= 10, f"La liste pour {key} ne doit pas contenir plus de 10 éléments."

    for key, value in result.items():
        for id_ in value:
            assert id_ in df['id'].values, f"L'ID {id_} pour {key} n'existe pas dans le DataFrame initial."

    # Vérifier un exemple spécifique (Winter, 10)
    assert result[('Winter', 10)] == [1], "La valeur pour ('Winter', 10) n'est pas correcte."


def test_ids_to_name():
    # DataFrame factice
    df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana']
    })

    # Liste d'IDs à tester
    l = [1, 3, 4]

    # Appeler la fonction
    result = cr.Page_temps_de_cuisson.ids_to_name(l, df)

    # Résultat attendu
    expected = ['Alice', 'Charlie', 'Diana']

    # Vérifier que le résultat correspond
    assert result == expected, f"Résultat attendu : {expected}, mais obtenu : {result}"

def test_get_name_top_by_interval_season():
    # DataFrame factice
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    })

    # Dictionnaire d'entrée
    dictionnaire = {
        ('Winter', 10): [1, 3],
        ('Summer', 30): [2, 5],
        ('Fall', 60): [4],
        ('Spring', 120): []
    }

    # Résultat attendu
    expected = {
        ('Winter', 10): ['Alice', 'Charlie'],
        ('Summer', 30): ['Bob', 'Eve'],
        ('Fall', 60): ['Diana'],
        ('Spring', 120): []
    }

    # Appeler la fonction
    result = cr.Page_temps_de_cuisson.get_name_top_by_interval_season(dictionnaire, df)

    # Vérifier que le résultat correspond au dictionnaire attendu
    assert result == expected, f"Résultat attendu : {expected}, mais obtenu : {result}"


