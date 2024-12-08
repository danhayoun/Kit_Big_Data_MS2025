import pytest
import pandas as pd
from pathlib import Path
import os
import numpy as np
import sys

from src.processing_data import SeasonHandler, DataProcess#, PreprocessingData
from utils.data_processor import DataProcessor

ABSOLUTE_PATH = os.path.abspath(__file__)

# TO NOTE: I am using here some make up data so that I can check the functions.
@pytest.fixture # éviter répétition quand utiliser dans plusieurs tests 
def sample_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Provide fictive sample data for testing purposes.
    """
    # Données factices pour les tests
    interaction_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'date': ['2023-03-15', '2023-06-15', '2023-09-15', '2023-12-15', '2023-02-15'],
        'counts': [5, 10, 3, 9, 8],
        'rating': [4.0, 5.0, 3.0, 4.0, 2.0]
    })

    recipe_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'submitted': ['2023-03-10', '2023-06-10', '2023-09-10', '2023-12-10', '2023-02-10'],
        'rating': [4.0, 5.0, 3.0, 4.0, 2.0]
    })

    contigency_table = pd.DataFrame({
    'Spring': [10.0, 1.3, 0.3, 2.0, 1.8],
    'Summer': [1.1, 1.3, 0.4, 0.2, 1.2],
    'Fall':   [0.9, 0.8, 1.3, 1.0, 1.8],
    'Winter': [1.2, 0.5, 0.8, 1.4, 0.6]
}, index=[1, 2, 3, 4, 5])
    
    interaction = interaction_data.loc[
        interaction_data.index.repeat(interaction_data['counts'])
    ].reset_index(drop=True)

    return interaction_data, recipe_data, contigency_table, interaction
  

def test_assign_season_date() -> None:
    """
    Test the assignment of seasons based on dates.
    """
    # Tester la détection des saisons
    date = pd.Timestamp("2023-06-15")
    season = SeasonHandler.assign_season_date(date)
    assert season == 'Spring'

    date = pd.Timestamp("2023-12-15")
    season = SeasonHandler.assign_season_date(date)
    assert season == 'Fall'
    
def test_average_ratings_recipe(sample_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    """
    Verify that average ratings are correctly calculated and merged into the recipe DataFrame.
    """
    _, recipe, _, interaction_data = sample_data
    
    average_recipe = recipe['rating'].copy()
    updated_recipe = DataProcessor.average_ratings_recipe(interaction_data, recipe.drop(columns=['rating']))
    #le drop ici car sinon confusion avec deux colonnes rating dans recipe.
    assert average_recipe.equals(updated_recipe['rating'])


def test_filter_data(sample_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    """
    Verify that filtering works correctly based on interaction counts.
    """
    # On va tester pour supérieur strictement à 5. 
    _, _, _, interaction_data = sample_data   

    expected_filtered_ids = [2, 4, 5] ## la solution
    
    filtered_data = DataProcessor.filter_data(interaction_data, "id", i=6, filter_count=True)
    filtered_ids = filtered_data['id'].unique().tolist()

    assert set(filtered_ids) == set(expected_filtered_ids), (
        f"Expected IDs: {expected_filtered_ids}, but got: {filtered_ids}"
    ) ## ici je veux une comparaison des id

def test_reassign_season(sample_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    """
    Test the assignment of seasons
    """
    _, recipe, contigency_table, _= sample_data
    
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
    
    recipe['season'] = DataProcess.calculate_seasons(
        contigency_table,
        id_season_dict,
        recipe
    )
    
    assert recipe['season'][:4].tolist() == expected_seasons[:4], f"Expected {expected_seasons}, but got {recipe['season'].tolist()}"
    
    index_4_season = recipe.loc[recipe['id'] == 4, 'season'].values[0]
    assert index_4_season in ['Spring', 'Fall'], (
        f"Expected one of ['Spring', 'Fall'] for index 4, but got {index_4_season}"
    )
    
def test_specific_weighted_rating(sample_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    """
    Verify the weighted rating for a specific recipe ID.
    We test 2 functions: weigthed_ratings_recipe and scale_column_to_range
    """
    target_max=5
    specific_id = 2 # car c'est la max value pour weight * rating
    interaction, recipe, _, interaction_data = sample_data
    
    #on calcule le weight
    interaction['weight'] = np.log1p(interaction['counts'])
    
    # et on récupère les données pour tester manuellement pour le maximum value pour id = 2
    rating = recipe.loc[recipe['id'] == specific_id, 'rating'].values[0]
    weight = interaction.loc[interaction['id'] == specific_id, 'weight'].values[0]
    manual_weighted_rating = (target_max / (rating * weight)) * rating * weight ## comme max value elle est forcément égale à 5. 

    # calculation avec la fonction
    updated_recipe = DataProcess.weigthed_ratings_recipe(interaction_data, recipe)
    # Ne pas oublier qu'on rescale a la fin avec DataProcessor.scale_column_to_range(recipe, var, )
    calculated_weighted_rating = updated_recipe.loc[updated_recipe['id'] == specific_id, 'weighted_rating'].values[0]
    assert pytest.approx(manual_weighted_rating, rel=1e-6) == pytest.approx(calculated_weighted_rating, rel=1e-6)
    
def test_filter_data_no_match(sample_data):
    """
    Test filter_data when no records match the threshold.
    """
    _, _, _, interaction_data = sample_data
    filtered_data = DataProcessor.filter_data(interaction_data, "id", i=20, filter_count=True)
    assert filtered_data.empty, "Expected no data to match the threshold, but found some records."

def test_scale_column_to_range():
    """
    Test scaling a column to a specific range.
    """
    test_data = pd.DataFrame({'rating': [1, 2, 3, 4, 5]})
    scaled_data = DataProcessor.scale_column_to_range(test_data, "rating", target_max=10)
    expected_scaled_values = [2, 4, 6, 8, 10]
    assert scaled_data['rating'].tolist() == expected_scaled_values, "Scaling did not produce expected results."