import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pickle

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

def converting_list(dataframe):
    """
    Convert the imported list in csv which was transform to a string with [] to a python list
    """
    for col in dataframe:
        if isinstance(dataframe[col][0], str) and dataframe[col][0].startswith('['):
            dataframe[col] = dataframe[col].apply(json.loads)
            
def load_data():
    """
    Load data and convert the pandas object to a python type
    """
    interactions = pd.read_csv('data/RAW_interactions.csv')
    recipes = pd.read_csv('data/PP_recipes.csv')
    converting_list(recipes)
    converting_list(interactions)
    interactions["date"]= pd.to_datetime(interactions.date)
    return recipes, interactions

def get_technique_name(l):
    """
    Get from TECHNIQUES_LIST the name of the technique used in the recipe
    1 means the techniques is used 
    0 otherwise
    """
    technique_name = []
    for i in range(0, len(l)):
        if l[i] == 1:
            technique_name.append(TECHNIQUES_LIST[i])
    return technique_name       

def df_techniques(recipes):
    """
    Create a technique dataframe with the recipe id, the techniques used and the number of techniques
    """
    recipes_PP = pd.DataFrame()
    recipes_PP["recipe_id"] = recipes.id
    recipes_PP["techniques"] = recipes.techniques.apply(lambda x:get_technique_name(x))
    recipes_PP["nb_techniques"] = recipes.techniques.apply(lambda x:sum(x))
    return recipes_PP
    
def merge_technique_date(df1,df2):
    """
    Join techniques and interations to have the date of when the techniques were used
    """          
    df_join = pd.merge(df1, df2[['recipe_id', 'date']], on='recipe_id', how='outer')
    df_join.sort_values('date', ascending=True, inplace=True,ignore_index=True)
    df_join['season'] = df_join['date'].apply(get_season)
    return df_join

def get_season(date):
    """
    Return the season associated with the review 
    """
    if date.month in [4,5] or (date.month == 3 and date.day >=20) or (date.month == 6 and date.day <20):
        return "spring"
    elif date.month in [7,8] or (date.month == 6 and date.day >=20) or (date.month == 9 and date.day <20):
        return "summer"
    elif date.month in [10,11] or (date.month == 9 and date.day >=20) or (date.month == 12 and date.day <20) :
        return "autumn"
    else :
        return "winter"

def analyze_correlation(df):
    # Fill NaN values in 'techniques' column with empty lists
    df['techniques'] = df['techniques'].apply(lambda x: x if isinstance(x, list) else [])
    
    # Create dummy variables for techniques
    for technique in TECHNIQUES_LIST:
        df[technique] = df['techniques'].apply(lambda x: 1 if technique in x else 0)
    
    # Create dummy variables for seasons
    season_dummies = pd.get_dummies(df['season'])
    df = pd.concat([df.drop(columns=['season']), season_dummies], axis=1)
    
    # Calculate correlation matrix
    correlation_matrix = df[TECHNIQUES_LIST + list(season_dummies.columns)].corr()
    
    # Extract correlations between techniques and seasons
    season_correlations = correlation_matrix.loc[TECHNIQUES_LIST, season_dummies.columns]
    return season_correlations

if __name__ == "__main__":
    recipes, interactions = load_data()
    techniques = df_techniques(recipes)
    df_tech_by_date = merge_technique_date(techniques,interactions)
    season_correlations = analyze_correlation(df_tech_by_date)
    # Sauvegarder la matrice de corrélation en fichier pickle
    with open("./Frontend/season_correlations.pkl", "wb") as f:
        pickle.dump(season_correlations, f)