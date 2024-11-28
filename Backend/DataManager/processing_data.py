import numpy as np
from pathlib import Path
import pandas as pd
import os

ABSOLUTE_PATH = os.path.abspath(__file__)

#---------------------------------------------------------------
### Create class here just to organise ###
# We should now use the static method for this
#--------------------------
class FileManager:
    @staticmethod
    def get_next_item(dict_data, index = 1):
        iterator = iter(dict_data.items())
        for i in range(1, index):
            next(iterator)
        return next(iterator)

    @staticmethod
    def read_file(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def read_raw_files(csv_files, folder_path):
        raw_files_data = {}
        for file_name in csv_files:
            if file_name.startswith('RAW'):
                raw_files_data[file_name] = FileManager.read_file(folder_path / file_name)
        return raw_files_data

    @staticmethod
    def save_file_as_csv(file, path):
        file.to_csv(path, index=False)

#--------------------------
class SeasonHandler:
    @staticmethod
    def create_season(year):
        spring = pd.Timestamp(year=year, month=3, day=21)
        summer = pd.Timestamp(year=year, month=6, day=21)
        fall = pd.Timestamp(year=year, month=9, day=21)
        winter = pd.Timestamp(year=year, month=12, day=21)
        return spring, summer, fall, winter

    @staticmethod
    def assign_season_date(date):
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
    def modified_frequency(contingency_table):
        number_total_recipe_id = contingency_table.sum(axis=1)
        contingency_table = contingency_table ** 2
        contingency_table['count'] = pd.DataFrame(number_total_recipe_id)
        freq_contingency_table = contingency_table.div(contingency_table['count'], axis=0).drop(columns='count')
        return freq_contingency_table
    
    @staticmethod
    def filter_data(interaction, columns, i=5, filter_count=False):
        recipe_season_count = interaction.groupby(columns).size().reset_index(name='count')
        if filter_count:
            recipe_season_count = recipe_season_count.loc[recipe_season_count[recipe_season_count['count'] >= i].index]
        return recipe_season_count

    @staticmethod
    def contingency_table(recipe_season_count):
        return pd.crosstab(recipe_season_count['id'], recipe_season_count['season'], 
                           values=recipe_season_count['count'], aggfunc='sum').fillna(0)
    
    @staticmethod
    def determine_max_season(row, id_season_dict, id_value, tolerance=1e-6):
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
#--------------------------
class DataProcessor:
    @staticmethod
    def transform_date(date):
        return pd.to_datetime(date)

    @staticmethod
    def average_ratings_recipe(interaction, recipe):
        average_ratings = (
            interaction.groupby('id')['rating']
            .mean()
            .reset_index(name='average_rating')
        )
        return recipe.merge(average_ratings, on='id', how='left')


#---------------------------------------------------------------
### Pipeline ###
#--------------------------
class Pipeline:
    def __init__(self, folder_path, output_path, k=5):
        self.folder_path = folder_path
        self.output_path = output_path
        self.k = k

    def load_data(self):
        csv_files = [file.name for file in self.folder_path.glob('*.csv')]
        raw_data = FileManager.read_raw_files(csv_files, self.folder_path)
        _, interaction = FileManager.get_next_item(raw_data)
        _, recipe = FileManager.get_next_item(raw_data, index=2)
        return interaction, recipe

    def preprocess_data(self, interaction, recipe):
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
        recipe['season'] = recipe['id'].map(contigency_table.apply(
        lambda row: SeasonHandler.determine_max_season(row, id_season_dict, row.name), axis=1
        ))
        # Add average ratings
        recipe = DataProcessor.average_ratings_recipe(interaction, recipe)
        return recipe
    
    def save_processed_data(self, recipe):
        FileManager.save_file_as_csv(recipe, self.output_path)
        print(f"Processed data saved to {self.output_path}")

    def run(self):
        interaction, recipe = self.load_data()
        if interaction is None or recipe is None:
            raise ValueError("Interaction or recipe data is missing.")
           
        processed_recipe = self.preprocess_data(interaction, recipe)
        self.save_processed_data(processed_recipe)

# Utilisation
if __name__ == "__main__":
    folder_path = Path(ABSOLUTE_PATH) / ".." / ".." / ".." / "Data" / "archive"
    output_path = Path(ABSOLUTE_PATH) / ".." / ".." / ".." / "Data" / "recipe_filtered.csv"
    print(folder_path, '\n', output_path)
    pipeline = Pipeline(folder_path, output_path, k=5)
    pipeline.run()