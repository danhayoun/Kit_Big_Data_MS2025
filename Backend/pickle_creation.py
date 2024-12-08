import pandas as pd
print("pickle creation", pd.__version__)
from pathlib import Path
from Backend.technique import DataLoader
from Backend.utils.data_processor import DataProcessor
from Backend.utils.file_manager import FileManager 
#from technique import DataLoader
#from utils.data_processor import DataProcessor
#from utils.file_manager import FileManager
import os
#from utils.data_processor import DataProcessor
ABSOLUTE_PATH = os.path.abspath(__file__)

class pickle_creation:
    """
    This class is responsible for processing and enriching recipe data with additional features, 
    such as the number of reviews per year and associating recipe names with their IDs. 
    It handles the creation of a modified DataFrame and saves it as a pickle file for further use.
    """
    def __init__(self, folder_path: Path, path_data_csv: Path, path_data_csv_recipe: Path) -> None:
        """
        Init the pickle_creation class.
        """
        self.data_path = folder_path
        self.data_path_csv = path_data_csv
        self.path_data_csv_recipe = path_data_csv_recipe
    
    def create_dataframe(self):
        df_pickle = DataLoader.load_pickle(self.data_path)
        df_csv = DataLoader.load_csv(self.data_path_csv)
        df_csv_recipe = DataLoader.load_csv(self.path_data_csv_recipe)
        df_pickle_modif = page_review_info.create_review_per_year(df_csv, df_pickle)
        df_pickle_modif = df_pickle_modif.merge(df_csv_recipe[['id', 'name']],how='left',on='id')
        df_pickle_modif['count_for_year'] = df_pickle_modif['review_per_year'].apply(lambda x: page_review_info.extract_reviews(x))
        df_pickle_modif = df_pickle_modif.drop(['rating'], axis=1)
        df_pickle_modif = df_pickle_modif.drop(['review_per_year'], axis=1)
        FileManager.save_file_as_pickle(df_pickle_modif, self.data_path / ".." / "recipe_with_years.pkl")

class file:
    def extract_reviews_for_year(review_dict, year):
        """
        Extrait le nombre total de reviews pour une année donnée depuis un dictionnaire de dates.
        """
        return sum(value for key, value in review_dict.items() if key == year)
    
class page_review_info:
    """
    Class page_review_info is just to handle the fonctions for the page_review class
    """
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def get_recipes_by_review_count(data: pd.DataFrame, max_count: int) -> pd.Series:
        """
        Returns a list of recipe names whose total review count is less than or equal to max_count.
        """
        filtered_recipes = data[
            data['count_for_year'].apply(lambda x: sum(x.values()) if isinstance(x, dict) else 0) <= max_count
        ]
        intermediary = filtered_recipes[['name', 'weighted_rating']].reset_index(drop=True).sort_values(by='weighted_rating', ascending=False)
        return intermediary['name']
    @staticmethod
    def get_histogram_recipe(data: pd.DataFrame, recipe_name: str) -> pd.DataFrame:
        """
        For a specific recipe showing the number of reviews by year.
        """
        recipe_data = data[data['name'].str.replace(" ", "").str.lower() == recipe_name.replace(" ", "").lower()]
        
        if recipe_data.empty:
            raise ValueError(f"Recipe '{recipe_name}' not found in the dataset.")
            
        return recipe_data.iloc[0]['count_for_year']
    
    @staticmethod
    def calculate_season_percentage(data: pd.DataFrame, year: int) -> pd.Series:
        """
        Calculate the seasons' pourcentage for a specific year.
        """
        data['count'] = data['count_for_year'].apply(
            lambda x: file.extract_reviews_for_year(x, year)
        )
        # enlever ceux qui ne sont pas pris en compte
        filtered_data = data[data['count'] > 0]
        season_recipe_count = filtered_data['season'].value_counts()
        total_recipes = season_recipe_count.sum()
        
        if total_recipes == 0:
            raise ValueError(f"Il n'y a aucune recette pour l'année {year}")
        
        season_percentage = (season_recipe_count / total_recipes) * 100
        season_percentage.name = "Percentage"
        
        return season_percentage

"""
if __name__ == "__main__":
    # Charger les données
    
    #data_str = "Kit_Big_Data_MS2025\\data\\"
    data_str = Path(ABSOLUTE_PATH) / ".." / ".." / "data" 
    path_data_pickle = data_str / "preprocess" / "recipe_filtered.pkl"
    path_data_csv = data_str / "raw" / "RAW_interactions.csv"
    path_data_csv_recipe = data_str / "raw" / "RAW_recipes.csv"
    pickle_create_object = pickle_creation(path_data_pickle, path_data_csv, path_data_csv_recipe)
    pickle_create_object.create_dataframe()
"""