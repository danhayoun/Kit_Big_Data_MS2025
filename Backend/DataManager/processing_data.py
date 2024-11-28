import numpy as np
from pathlib import Path
import pandas as pd

### Load data ###
def get_next_item(dict_data, index = 1):
    iterator = iter(dict_data.items())
    for i in range(1, index):
        print("ok")
        next(iterator)
    return next(iterator)

# Function to read all CSV files that start with "RAW"
def read_raw_files(csv_files, folder_path):
    raw_files_data = {}
    for file_name in csv_files:
        if file_name.startswith('RAW'):
            raw_files_data[file_name] = read_file(folder_path / file_name)
    
    return raw_files_data

def read_file(file_path):
    return pd.read_csv(file_path)

#---------------------------------------------------------------
def transform_date(date):
    return pd.to_datetime(date)

#---------------------------------------------------------------
### Seasons ###

def create_season(year):
    spring = pd.Timestamp(year=year, month=3, day=21)
    summer = pd.Timestamp(year=year, month=6, day=21)
    fall = pd.Timestamp(year=year, month=9, day=21)
    winter = pd.Timestamp(year=year, month=12, day=21)
    return spring, summer, fall, winter
    
def assign_season_date(date):
    ### assign the seasons for the year
    spring, summer, fall, winter = create_season(date.year)
    
    ### assign 
    if spring <= date < summer:
        return 'Spring'
    elif summer <= date < fall:
        return 'Summer'
    elif fall <= date < winter:
        return 'Fall'
    else:
        return 'Winter'

def modified_frequency(contigency_table):
    number_total_recipe_id = contigency_table.sum(axis=1)
    # numerator = numerator **2
    contigency_table = contigency_table ** 2
    contigency_table['count'] = pd.DataFrame(number_total_recipe_id)
    # numerator / total_nb_recipe
    freq_contigency_table = contigency_table.div(contigency_table['count'], axis=0).drop(columns='count')
    
    # aaply non linear transformation x / (eps + log(1 + x)). log transform to see even more the difference of values (and epsilon to not divide by 0)
    return freq_contigency_table

def filter_data(interaction, columns, i = 5, bool = False):
    recipe_season_count = interaction.groupby(columns).size().reset_index(name='count')
    if bool == True:
        recipe_season_count = recipe_season_count.loc[recipe_season_count[recipe_season_count['count'] >= i].index]
    return recipe_season_count

def contigency_table_(recipe_season_count):
    return pd.crosstab(recipe_season_count['id'], recipe_season_count['season'], values=recipe_season_count['count'], aggfunc='sum').fillna(0)

def determine_max_season(row, tolerance=1e-6):
    #print("This row is ", row)
    max_value = row.max()
    is_close = np.isclose(row, max_value, atol=tolerance)
    max_seasons = row[is_close].index.tolist()
    #print("Max season is: ", max_seasons)
    return np.random.choice(max_seasons)

def assign_season(interaction, recipe, k = 5):
    # assign the season
    interaction_filtered = interaction.copy()
    interaction_filtered['season'] = interaction_filtered['date'].apply(assign_season_date)
    # keep only the recipes with season for i number
    recipe_count = filter_data(interaction_filtered, "id", i = k, bool = True)
    
    # refactor for recipe and interaction of origin
    recipe = recipe[recipe['id'].isin(recipe_count["id"])]
    interaction = interaction[interaction['id'].isin(recipe_count["id"])]
    
    recipe_season_count = filter_data(interaction_filtered, ['id', 'season'])
    #print(recipe_season_count.head())
    contigency_table = contigency_table_(recipe_season_count)
    contigency_table = modified_frequency(contigency_table)  
    
    # assign season
    recipe['season'] = recipe["id"].map(contigency_table.apply(determine_max_season, axis=1))
    return interaction, recipe

# Calcul de la moyenne des ratings pour chaque recipe_id
def average_ratings_recipe(interaction, recipe):
    average_ratings = (
            interaction.groupby('id')['rating']
            .mean()
            .reset_index(name='average_rating')
        )
    return recipe.merge(average_ratings, on='id', how='left')

def save_file_as_csv(file, path):
    file.to_csv(path, index=False)

def preprocess_data(interaction, recipe, path = Path("..") / ".." / "Data" / "recipe_filtrered.csv", k = 5):
    # transform in dates
    interaction['date'] = transform_date(interaction['date'])
    recipe['submitted'] = transform_date(recipe['submitted'])
    
    # to manipulate easier rename the interaction column name 
    interaction = interaction.rename(columns={'recipe_id': 'id'})
    
    interaction, recipe = assign_season(interaction, recipe, k)
    recipe = average_ratings_recipe(interaction, recipe)
    save_file_as_csv(recipe, path)
    
def load_data():
    folder_path = Path('C:\Users\josep\Documents\Telecom Paris\Kit_Big_Data\Kit_Big_Data_MS2025\Backend\DataManager\processing_data.py')
    csv_files = [file.name for file in folder_path.glob('*.csv')]
    print('csv files: ', csv_files)
    raw_data = read_raw_files(csv_files, folder_path)
    file_name1, interaction = get_next_item(raw_data)
    file_name2, recipe = get_next_item(raw_data, index=2)
    preprocess_data(interaction, recipe)
    
if __name__ == "__main__":
    load_data()