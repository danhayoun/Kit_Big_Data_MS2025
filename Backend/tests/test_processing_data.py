import pytest
import pandas as pd
from pathlib import Path
import os
import numpy as np
import sys
from Backend.processing_data import SeasonHandler, DataProcess#, PreprocessingData

ABSOLUTE_PATH = os.path.abspath(__file__)

# TO NOTE: I am using here some make up data so that I can check the functions.
@pytest.fixture # éviter répétitionquand utiliser dans plusieurs tests 
def sample_data():
    # Données factices pour les tests
    interaction_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'date': ['2023-03-15', '2023-06-15', '2023-09-15', '2023-12-15', '2023-02-15'],
        'rating': [4, 5, 3, 4, 2],
        'count': [5, 10, 3, 9, 8]
    })

    recipe_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'submitted': ['2023-03-10', '2023-06-10', '2023-09-10', '2023-12-10', '2023-02-10'],
        'rating': [3.5, 4.5, 3, 3.8, 2.5]
    })

    return interaction_data, recipe_data
  

def test_assign_season_date():
    # Tester la détection des saisons
    date = pd.Timestamp("2023-06-15")
    season = SeasonHandler.assign_season_date(date)
    assert season == 'Spring'

    date = pd.Timestamp("2023-12-15")
    season = SeasonHandler.assign_season_date(date)
    assert season == 'Fall'

def test_reassign_season(sample_data):
    _, recipe = sample_data
     # Étape 1 : Créer un contigency_table factice
    contigency_table = pd.DataFrame({
    'Spring': [10.0, 1.3, 0.3, 2.0, 1.8],
    'Summer': [1.1, 1.3, 0.4, 0.2, 1.2],
    'Fall':   [0.9, 0.8, 1.3, 1.0, 1.8],
    'Winter': [1.2, 0.5, 0.8, 1.4, 0.6]
}, index=[1, 2, 3, 4, 5])   

    # expect 0: sum or win; 1: spring, or sum; 2: 
    # Étape 2 : Créer un id_season_dict factice
    id_season_dict = {
        1: 'Summer',
        2: 'Spring',
        3: 'Summer',
        4: 'Spring',
        5: 'Winter'
    }
    
    # Index 0 : 'Spring' est un maximum clair sans besoin de id_season_dict.
    # Index 1 : 'Summer' et 'Spring' max mais 'Spring' est défini dans id_season_dict, donc résultat attendu : 'Spring'.
    # Index 2 : 'Fall' est le maximum sans ambiguïté, pas besoin de id_season_dict, donc résultat attendu : 'Fall'.
    # Index 3 : 'Spring' est le maximum sans ambiguïté, pas besoin de id_season_dict, donc résultat attendu : 'Spring'.
    # Index 4 : id_season_dict est vérifié, et n'est pas dedans, donc choix aléatoire dans max_seasons attendu entre Spring et Fall.
    expected_seasons = ['Spring', 'Spring', 'Fall', 'Spring', ['Spring', 'Fall']]
    
    recipe['season'] = DataProcess.calculate_weighted_rating(
            contigency_table,
            id_season_dict,
            recipe
        )

    
    assert recipe['season'][:4].tolist() == expected_seasons[:4], f"Expected {expected_seasons}, but got {recipe['season'].tolist()}"
    
    index_4_season = recipe.loc[recipe['id'] == 4, 'season'].values[0]
    assert index_4_season in ['Spring', 'Fall'], (
        f"Expected one of ['Spring', 'Fall'] for index 4, but got {index_4_season}"
    )