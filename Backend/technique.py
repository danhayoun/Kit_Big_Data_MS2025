import pandas as pd
import numpy as np
import ast
import pickle
from typing import List
import logging
import spacy

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
    def converting_list_column(df: pd.DataFrame,column_list_to_convert):
        """
        Convert the csv's imported list which was transform wrongly to a string to a python list
        """
        for col in column_list_to_convert:
            if col !='tags': # si on veut traiter la colonne tags, il faudra gérer les erreurs de frappe de l'utilisateur
                if isinstance(df[col][0], str) and df[col][0].startswith('['):
                    df[col] = df[col].apply(ast.literal_eval)

    def load_data(self, csv_path: str,  column_list_to_convert = None, date = None) -> pd.DataFrame:
        """
        Load data from CSV files and convert necessary columns into python type
        """
        try :
            df = self.load_csv(csv_path)
            if column_list_to_convert:
                self.converting_list_column(df, column_list_to_convert= column_list_to_convert)
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
    
    def binarize_step_to_technique(self, steps):
        """
        transform into a binary list 
        """
        techniques_in_step = [0] * len(self.techniques_list)
        for token in steps:
            if token.lemma_ in self.techniques_list:
                index = self.techniques_list.index(token.lemma_)
                techniques_in_step[index] = 1
        return techniques_in_step
        
    def get_binary_techniques_list(self,raw_recipes_df):
        """
        Analyze steps using spaCy to detect techniques
        """    
        # Charge le modèle de langue anglaise de spaCy
        nlp = spacy.load("en_core_web_sm")
        
        # Ensure 'steps' column exists in the dataframe
        if 'steps' in raw_recipes_df.columns:
            # Concaténe les étapes pour chaque recette afin de pouvoir utiliser nlp.pipe
            steps_concat = raw_recipes_df['steps'].apply(lambda steps: " ".join(steps))
        else:
            raise KeyError("'steps' column is missing in the dataframe given")    
            
        # Traiter les données en utilisant nlp.pipe
        lst_techniques = []
        for steps in nlp.pipe(steps_concat, batch_size=1000):
            lst_techniques.append(self.binarize_step_to_technique(steps))
        return lst_techniques

    def get_technique_name(self, techniques_flags: List[int]) -> List[str]:
        """
        Retrieve from techniques_flags (TECHNIQUES_LIST in the usecase here) the name of the technique used in the recipe
        1 means the techniques is used 
        0 otherwise
        """
        return [self.techniques_list[i] for i, flag in enumerate(techniques_flags) if flag == 1]

    def create_technique_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a DataFrame with recipe IDs, the name and the count of techniques.
        """
        lst_techniques = self.get_binary_techniques_list(df)
        techniques_df = pd.DataFrame()
        techniques_df["recipe_id"] = df["id"]
        techniques_df["name"] = df["name"] 
        techniques_df['techniques_binary'] = lst_techniques
        techniques_df["techniques"] = techniques_df["techniques_binary"].apply(self.get_technique_name)
        techniques_df["nb_techniques"] = techniques_df["techniques_binary"].apply(sum)
        techniques_df["season"] = df["season"] 
        techniques_df["weighted_rating"] = df["weighted_rating"] 
        return techniques_df

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
    correlation_analyzer = CorrelationAnalyzer(TECHNIQUES_LIST)
    
    # Load data
    recipes = data_loader.load_data('../data/raw/RAW_recipes.csv',['steps'])
    interactions = data_loader.load_data('../data/raw/RAW_interactions.csv', date = 'date')
    filter_recipes = pd.read_pickle('../data/preprocess/recipe_filtered.pkl')
    #filter_recipes.rename(columns={'id': 'recipe_id'}, inplace=True)

    df_steps = pd.merge(recipes[['id','name','steps']], filter_recipes, on='id', how='right')

    # Process techniques
    techniques = technique_processor.create_technique_df(df_steps)

    # Save processed techniques
    #with open("../data/preprocess/techniques.pkl", "wb") as f:
    #    pickle.dump(techniques, f)

    # Merge data and analyze correlations
    #df_tech_by_date = pd.merge(techniques, interactions[['recipe_id', 'date']],on='recipe_id', how='outer')
    season_correlations = correlation_analyzer.analyze_correlation(techniques)

    # Save correlation analysis results
    #with open("../data/preprocess/season_correlations.pkl", "wb") as f:
    #    pickle.dump(season_correlations, f)