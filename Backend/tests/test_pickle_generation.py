import pytest
import pandas as pd
import os
from Backend.pickle_creation import create_review_per_year, extract_reviews, extract_reviews_for_year
from Backend.utils.data_processor import DataProcessor

ABSOLUTE_PATH = os.path.abspath(__file__)

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
    df_result = create_review_per_year(expanded_df_csv, df_pickle)

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
    result = extract_reviews(review_dict_1)
    assert result == expected_result_1, (
        f"Test failed. Expected {expected_result_1}, got {result}"
    )
    
    expected_result_2 = 8
    result2 = extract_reviews_for_year(result, year_1)
    assert result2 == expected_result_2, (
        f"Test failed for year {year_1}. Expected {expected_result_2}, got {result2}"
    )