import pandas as pd
from pathlib import Path
#from Backend.utils.data_processor import DataProcessor
from utils.data_processor import DataProcessor

def create_review_per_year(df_csv: pd.DataFrame, df_pickle: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column with a dictionnary of the number of review per date.
    """
    df_csv['date'] = DataProcessor.transform_date(df_csv['date'])
    reviews_per_year = DataProcessor.filter_data(df_csv, ['recipe_id', 'date'], filter_count=False)
    
    # Create a dictionary for each recipe_id with years as keys and review counts as values
    reviews_dict = (
        reviews_per_year.groupby('recipe_id')
        .apply(lambda x: dict(zip(x['date'], x['count'])))
        .to_dict()
    )
  
    # Map the dictionary to the id column in df_pickle to create the new column
    df_pickle['review_per_year'] = df_pickle['id'].map(reviews_dict)
    
    return df_pickle

def extract_reviews(review_dict):
    """
    Extracts a dictionary containing the total number of reviews per year 
    from a dictionary with dates as keys and counts as values.
    """
    if not isinstance(review_dict, dict):
        return {}

    year_review_counts = {}
    for date, count in review_dict.items():
        year = date.year
        year_review_counts[year] = year_review_counts.get(year, 0) + count

    return year_review_counts

def extract_reviews_for_year(review_dict, year):
    """
    Extrait le nombre total de reviews pour une année donnée depuis un dictionnaire de dates.
    """
    return sum(value for key, value in review_dict.items() if key == year)