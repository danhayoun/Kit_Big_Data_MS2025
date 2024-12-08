import pytest
import pandas as pd
import os
from src.pickle_creation import page_review_info, file
from utils.data_processor import DataProcessor

ABSOLUTE_PATH = os.path.abspath(__file__)

@pytest.fixture
def sample_data() -> pd.DataFrame:
    # Create a test DataFrame
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Chocolate Cake', 'Apple Pie', 'Lemon Tart', 'Carrot Cake'],
        'count_for_year': [
            {2020: 3, 2021: 4}, 
            {2020: 5, 2021: 1}, 
            {2020: 2, 2021: 2}, 
            {2020: 17, 2021: 4}
        ],
        'weighted_rating': [4.0, 4.8, 3.8, 4.2]
    })
    
def test_create_review_per_year() -> None:
    # creation du dataset
    df_csv = pd.DataFrame({
        'recipe_id': [1, 1, 2, 2, 3, 3],
        'date': ['2023-01-01', '2023-01-02', '2022-05-01', '2023-06-01', '2023-02-01', '2023-02-02'],
        'count': [3, 5, 20, 15, 8, 12]
    })

    df_pickle = pd.DataFrame({
        'id': [1, 2, 3],
        'rating': [4.5, 3.8, 4.0],
    })
    expanded_df_csv = DataProcessor.expand_rows_by_count(df_csv).drop(columns=['count']).reset_index(drop=True)
    
    # Utilisation de la fonction create_review_per_year
    df_result = page_review_info.create_review_per_year(expanded_df_csv, df_pickle)

    #print(df_result['review_per_year'])
    assert df_result.loc[df_result['id'] == 1, 'review_per_year'].values[0] == {
        pd.Timestamp('2023-01-01'): 3,
        pd.Timestamp('2023-01-02'): 5,
    }, "Les reviews pour l'id 1 sont incorrectes."

    assert df_result.loc[df_result['id'] == 2, 'review_per_year'].values[0] == {
        pd.Timestamp('2022-05-01'): 20,
        pd.Timestamp('2023-06-01'): 15,
    }, "Les reviews pour l'id 2 sont incorrectes."

    assert df_result.loc[df_result['id'] == 3, 'review_per_year'].values[0] == {
        pd.Timestamp('2023-02-01'): 8,
        pd.Timestamp('2023-02-02'): 12,
    }, "Les reviews pour l'id 3 sont incorrectes."
    
def test_extract_reviews_for_year():
    review_dict_1 = {
        pd.Timestamp("2023-01-01"): 5,
        pd.Timestamp("2023-02-15"): 3,
        pd.Timestamp("2022-12-31"): 7,
    }
    year_1 = 2023
    expected_result_1 = {2023:8,2022:7}
    result = page_review_info.extract_reviews(review_dict_1)
    assert result == expected_result_1, (
        f"Test failed. Expected {expected_result_1}, got {result}"
    )
    
    expected_result_2 = 8
    result2 = file.extract_reviews_for_year(result, year_1)
    assert result2 == expected_result_2, (
        f"Test failed for year {year_1}. Expected {expected_result_2}, got {result2}"
    )
    
def test_get_recipes_by_review_count(sample_data: pd.DataFrame):
    # Exemple de données
    test_data = sample_data
    # Test avec max_count = 5
    recipes = page_review_info.get_recipes_by_review_count(test_data, max_count=5)
    assert recipes.tolist() == ['Lemon Tart']

    recipes = page_review_info.get_recipes_by_review_count(test_data, max_count=10)
    assert recipes.tolist() == ['Apple Pie', 'Chocolate Cake', 'Lemon Tart']
    
    # Test avec max_count = 1 (aucune recette ne doit correspondre)
    recipes = page_review_info.get_recipes_by_review_count(test_data, max_count=1)
    assert recipes.empty
    
def test_get_histogram_recipe(sample_data: pd.DataFrame):
    test_data = sample_data
    # Test for a valid recipe
    recipe_name = "Chocolate Cake"
    result = page_review_info.get_histogram_recipe(test_data, recipe_name)
    assert result == {2020: 3, 2021: 4}, f"Expected {{2020: 3, 2021: 4}}, but got {result}"

    # Test for another valid recipe
    recipe_name = "Lemon Tart"
    result = page_review_info.get_histogram_recipe(test_data, recipe_name)
    assert result == {2020: 2, 2021: 2}, f"Expected {{2020: 2, 2021: 2}}, but got {result}"

    # Test for missing recipe
    recipe_name = "Nonexistent Recipe"
    with pytest.raises(ValueError) as exc_info:
        page_review_info.get_histogram_recipe(test_data, recipe_name)
    assert str(exc_info.value) == f"Recipe '{recipe_name}' not found in the dataset."
    
def test_create_review_per_year_empty_df():
    """
    Test create_review_per_year with empty DataFrames.
    """
    empty_df_csv = pd.DataFrame(columns=['recipe_id', 'date', 'count'])
    empty_df_pickle = pd.DataFrame(columns=['id', 'rating'])

    result = page_review_info.create_review_per_year(empty_df_csv, empty_df_pickle)
    assert result.empty, "Expected empty DataFrame, but got data."

def test_extract_reviews_empty_dict():
    """
    Test extract_reviews with an empty dictionary.
    """
    result = page_review_info.extract_reviews({})
    assert result == {}, "Expected an empty dictionary, but got data."