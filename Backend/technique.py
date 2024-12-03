import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pickle
from typing import Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure df option
pd.set_option('display.max_columns', None)

TECHNIQUES_LIST = [
    'bake',
    'barbecue',
    'blanch',
    'blend',
    'boil',
    'braise',
    'brine',
    'broil',
    'caramelize',
    'combine',
    'crock pot',
    'crush',
    'deglaze',
    'devein',
    'dice',
    'distill',
    'drain',
    'emulsify',
    'ferment',
    'freez',
    'fry',
    'grate',
    'griddle',
    'grill',
    'knead',
    'leaven',
    'marinate',
    'mash',
    'melt',
    'microwave',
    'parboil',
    'pickle',
    'poach',
    'pour',
    'pressure cook',
    'puree',
    'refrigerat',
    'roast',
    'saute',
    'scald',
    'scramble',
    'shred',
    'simmer',
    'skillet',
    'slow cook',
    'smoke',
    'smooth',
    'soak',
    'sous-vide',
    'steam',
    'stew',
    'strain',
    'tenderize',
    'thicken',
    'toast',
    'toss',
    'whip',
    'whisk',
]

class DataLoader:
    """Class responsible for loading and converting data"""
    
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """
        Read a csv file into DataFrame
        """
        return pd.read_csv(filepath)

    @staticmethod
    def converting_list_column(dataframe: pd.DataFrame):
        """
        Convert the csv's imported list which was transform wrongly to a string to a python list
        """
        for col in dataframe:
            if isinstance(dataframe[col][0], str) and dataframe[col][0].startswith('['):
                dataframe[col] = dataframe[col].apply(json.loads)

    def load_data(self, csv_path: str, date = None) -> pd.DataFrame:
        """
        Load data from CSV files and convert necessary columns into python type
        """
        try :
            df = self.load_csv(csv_path)
            self.converting_list_column(df)
            if date and date in df.columns:
                df[date] = pd.to_datetime(df[date])
            return df
        except FileNotFoundError:
            logging.error(f"Error: The file at {csv_path} was not found.")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return pd.DataFrame()
    
class TechniqueProcessor:
    """Class responsible for processing recipe techniques."""
    
    def __init__(self, techniques_list: List[str]):
        self.techniques_list = techniques_list

    def get_technique_name(self, techniques_flags: List[int]) -> List[str]:
        """
        Retrieve from techniques_flags (TECHNIQUES_LIST in the usecase here) the name of the technique used in the recipe
        1 means the techniques is used 
        0 otherwise
        """
        return [self.techniques_list[i] for i, flag in enumerate(techniques_flags) if flag == 1]

    def process_techniques(self, recipes: pd.DataFrame) -> pd.DataFrame:
        """
        Create a DataFrame with recipe IDs, the name and the count of techniques.
        """
        recipes_PP = pd.DataFrame()
        recipes_PP["recipe_id"] = recipes["id"]
        recipes_PP["techniques"] = recipes["techniques"].apply(self.get_technique_name)
        recipes_PP["nb_techniques"] = recipes["techniques"].apply(sum)
        return recipes_PP

class DataMerger:
    """Class responsible for merging datasets and adding additional information."""
    
    @staticmethod
    def get_season(date: pd.Timestamp) -> str:
        """
        Determine the season based on the date associated with the review given by a user
        """
        if date.month in [4, 5] or (date.month == 3 and date.day >= 20) or (date.month == 6 and date.day < 20):
            return "Spring"
        elif date.month in [7, 8] or (date.month == 6 and date.day >= 20) or (date.month == 9 and date.day < 20):
            return "Summer"
        elif date.month in [10, 11] or (date.month == 9 and date.day >= 20) or (date.month == 12 and date.day < 20):
            return "Fall"
        else:
            return "Winter"

    def merge_technique_date(self, techniques_df: pd.DataFrame, interactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge techniques data with interaction data to include dates and seasons of when the techniques were used
        """
        df_join = pd.merge(techniques_df, interactions_df[['recipe_id', 'date']], on='recipe_id', how='outer')
        df_join.sort_values("date", ascending=True, inplace=True, ignore_index=True)
        df_join["season"] = df_join["date"].apply(self.get_season)
        return df_join

class CorrelationAnalyzer:
    """Class responsible for analyzing correlations between techniques and seasons."""
    
    def __init__(self, techniques_list: List[str]):
        self.techniques_list = techniques_list

    def analyze_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze the correlation between techniques and seasons.
        """
        # Fill NaN values in 'techniques' column with empty lists
        df["techniques"] = df["techniques"].apply(lambda x: x if isinstance(x, list) else [])

        # Create dummy variables for techniques
        for technique in self.techniques_list:
            df[technique] = df["techniques"].apply(lambda x: 1 if technique in x else 0)

        # Create dummy variables for seasons
        season_dummies = pd.get_dummies(df["season"])
        df = pd.concat([df.drop(columns=["season"]), season_dummies], axis=1)

        # Compute the correlation matrix
        correlation_matrix = df[self.techniques_list + list(season_dummies.columns)].corr()

        # Extract correlations between techniques and seasons
        return correlation_matrix.loc[self.techniques_list, season_dummies.columns]

# Main execution
if __name__ == "__main__":
    data_loader = DataLoader()
    technique_processor = TechniqueProcessor(TECHNIQUES_LIST)
    data_merger = DataMerger()
    correlation_analyzer = CorrelationAnalyzer(TECHNIQUES_LIST)

    # Load data
    recipes = data_loader.load_data('data/raw/PP_recipes.csv')
    interactions = data_loader.load_data('data/raw/RAW_interactions.csv', 'date')

    # Process techniques
    techniques = technique_processor.process_techniques(recipes)

    # Save processed techniques
    with open("./data/preprocess/techniques.pkl", "wb") as f:
        pickle.dump(techniques, f)

    # Merge data and analyze correlations
    df_tech_by_date = data_merger.merge_technique_date(techniques, interactions)
    season_correlations = correlation_analyzer.analyze_correlation(df_tech_by_date)

    # Save correlation analysis results
    with open("./data/preprocess/season_correlations.pkl", "wb") as f:
        pickle.dump(season_correlations, f)