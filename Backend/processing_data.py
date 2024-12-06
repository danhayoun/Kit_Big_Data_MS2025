import numpy as np
from pathlib import Path
import pandas as pd
import os
import sys

# Ajouter le répertoire parent de 'utils' au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#---------------------------------------------------------------
# import classes from utils
from Backend.utils.file_manager import FileManager
from Backend.utils.data_processor import DataProcessor

ABSOLUTE_PATH = os.path.abspath(__file__)

#---------------------------------------------------------------
### Create class here just to organise ###
# We should now use the static method for this
#--------------------------
#--------------------------
class SeasonHandler:
    @staticmethod
    def create_season(year: int) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
        """
        Create seasonal boundaries based on the year.
        Returns:
            tuple: A tuple containing the start dates of Spring, Summer, Fall, and Winter.
        """
        spring = pd.Timestamp(year=year, month=3, day=21)
        summer = pd.Timestamp(year=year, month=6, day=21)
        fall = pd.Timestamp(year=year, month=9, day=21)
        winter = pd.Timestamp(year=year, month=12, day=21)
        return spring, summer, fall, winter

    @staticmethod
    def assign_season_date(date: pd.Timestamp) -> str:
        """
        Assign a season to a specific date.
        Returns:
            str: The season corresponding to the date.
        """
        spring, summer, fall, winter = SeasonHandler.create_season(date.year)
        if spring <= date < summer:
            return 'Spring'
        elif summer <= date < fall:
            return 'Summer'
        elif fall <= date < winter:
            return 'Fall'
        else:
            return 'Winter'

    @staticmethod
    def modified_frequency(contingency_table: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the frequency table by squaring values and normalizing them.
        Returns:
            pd.DataFrame: Modified contingency table with normalized values.
        """
        number_total_recipe_id = contingency_table.sum(axis=1)
        contingency_table = contingency_table ** 2
        contingency_table['count'] = pd.DataFrame(number_total_recipe_id)
        freq_contingency_table = contingency_table.div(contingency_table['count'], axis=0).drop(columns='count')
        return freq_contingency_table
    
    @staticmethod
    def filter_data(interaction: pd.DataFrame, columns: list[str], i: int = 5, filter_count: bool = False) -> pd.DataFrame:
        """
        Filter interaction data based on column values and count threshold.
        Returns:
            pd.DataFrame: Filtered interaction data.
        """
        recipe_season_count = interaction.groupby(columns).size().reset_index(name='count')
        if filter_count:
            recipe_season_count = recipe_season_count.loc[recipe_season_count[recipe_season_count['count'] >= i].index]
        return recipe_season_count

    @staticmethod
    def contingency_table(recipe_season_count: pd.DataFrame) -> pd.DataFrame:
        """
        Create a contingency table from recipe season counts.
        Returns:
            pd.DataFrame: Contingency table.
        """
        return pd.crosstab(recipe_season_count['id'], recipe_season_count['season'], 
                           values=recipe_season_count['count'], aggfunc='sum').fillna(0)
    
    @staticmethod
    def determine_max_season(row: pd.Series, id_season_dict: dict[int, str], id_value: int, tolerance: float = 1e-6) -> str:
        """
        Determine the most likely season for a row based on maximum value,
        and if their are multiple maximum values take the season corresponding to submitted recipe.
        Returns:
            str: The determined season.
        """
        max_value = row.max()
        is_close = np.isclose(row, max_value, atol=tolerance)
        max_seasons = row[is_close].index.tolist()
        if len(max_seasons) > 1: 
            # get id season
            id_season = id_season_dict.get(id_value, None)
            # Compare with weither in max_season. If not random.
            if id_season in max_seasons:
                return id_season
            else:
                return np.random.choice(max_seasons)
        return max_seasons[0]
    
#--------------------------
class DataProcess:
    @staticmethod
    def weigthed_ratings_recipe(interaction: pd.DataFrame, recipe: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate weighted ratings for recipes based on the log(number of comments for a recipe).
        Returns:
            pd.DataFrame: Recipe data with weighted ratings added.
        """
        # création of column weigth
        interaction_counts = (
            interaction.groupby('id')
            .size()
            .reset_index(name='count')
        )
        interaction_counts['weight'] = np.log1p(interaction_counts['count'])
        # Multiplier directement rating par weight lors du mappage
        var = 'weighted_rating'
        recipe[var] = recipe['rating'] * recipe['id'].map(interaction_counts.set_index('id')['weight'])
        # Remmetre ça sur 5 pour que ce soit des notations que l'on connaisse.
        return DataProcessor.scale_column_to_range(recipe, var, target_max=5)
    
    @staticmethod
    def calculate_weighted_rating(contigency_table: pd.DataFrame, id_season_dict: dict[int, str], recipe: pd.DataFrame) -> pd.Series:
        """ 
        Same as weigthed_ratings_recipe but for ratings, a.k.a the ratings mean value.
        """
        # Crée une colonne pondérée
        return recipe['id'].map(contigency_table.apply(
        lambda row: SeasonHandler.determine_max_season(row, id_season_dict, row.name), axis=1
        ))

#---------------------------------------------------------------
### Pipeline of Preprocessing the Data ###
#--------------------------
class PreprocessingData:
    def __init__(self, folder_path: Path, output_path: Path, k: int = 5) -> None:
        """
        Initializes the PreprocessingData class
        """
        self.folder_path = folder_path
        self.output_path = output_path
        self.k = k

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loads interaction and recipe data from raw CSV files.
        Returns:
            tuple[pd.DataFrame, pd.DataFrame]
        """
        csv_files = [file.name for file in self.folder_path.glob('*.csv')]
        raw_data = FileManager.read_raw_files(csv_files, self.folder_path)
        _, interaction = FileManager.get_next_item(raw_data)
        _, recipe = FileManager.get_next_item(raw_data, index=2)
        return interaction, recipe

    def preprocess_data(self, interaction: pd.DataFrame, recipe: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the interaction and recipe data:
        - Transforms dates.
        - Filters and assigns seasons.
        - Calculates ratings and weighted ratings.

        Returns:
            Processed recipe DataFrame with additional columns.
        """
        # Transform dates
        interaction['date'] = DataProcessor.transform_date(interaction['date'])
        recipe['submitted'] = DataProcessor.transform_date(recipe['submitted'])

        # Rename interaction column
        interaction = interaction.rename(columns={'recipe_id': 'id'})

        # Assign seasons and Filter data
        interaction['season'] = interaction['date'].apply(SeasonHandler.assign_season_date)
        recipe_count = SeasonHandler.filter_data(interaction, "id", i = self.k, filter_count = True)
        
        # refactor for recipe and interaction of origin
        recipe = recipe[recipe['id'].isin(recipe_count["id"])]
        interaction = interaction[interaction['id'].isin(recipe_count["id"])]
    
        recipe_season_count = SeasonHandler.filter_data(interaction, ['id', 'season'])
        contigency_table = SeasonHandler.contingency_table(recipe_season_count)
        contigency_table = SeasonHandler.modified_frequency(contigency_table)

        # To keep track of publication date
        id_date_df = recipe[['id', 'submitted']].copy()
        id_date_df['submitted'] = id_date_df['submitted'].apply(SeasonHandler.assign_season_date)
        id_season_dict = id_date_df.set_index('id')['submitted'].to_dict()
        
        # Assign max season
        recipe['season'] = DataProcess.calculate_weighted_rating(contigency_table, id_season_dict, recipe)
        # Add average ratings
        recipe = DataProcessor.average_ratings_recipe(interaction, recipe)
        
        # Add weighted ratings
        recipe = DataProcess.weigthed_ratings_recipe(interaction, recipe)
        return recipe
    
    def save_processed_data(self, recipe: pd.DataFrame) -> None:
        """
        Saves the processed recipe data to the specified output path as a pickle file.
        """
        FileManager.save_file_as_pickle(recipe, self.output_path)
        print(f"Processed data saved to {self.output_path}")

    def run(self) -> None:
        """
        Executes the pipeline:
        - Loads data.
        - Processes the data.
        - Saves only the added colonnes of the processed data as a pickle.
        """
        interaction, recipe = self.load_data()
        if interaction is None or recipe is None:
            raise ValueError("Interaction or recipe data is missing.")
        
        processed_recipe = self.preprocess_data(interaction, recipe)
        processed_recipe = processed_recipe.filter(items=['id', 'season', 'rating', 'weighted_rating'])
        self.save_processed_data(processed_recipe)

if __name__ == "__main__":
    folder_path = Path(ABSOLUTE_PATH) / ".." / ".." / "data" / "raw"
    output_path = Path(ABSOLUTE_PATH) / ".." / ".." / "data" / "preprocess" / "recipe_filtered.pkl"
    print(folder_path, '\n', output_path)
    pipeline = PreprocessingData(folder_path, output_path, k=5)
    pipeline.run()
    
