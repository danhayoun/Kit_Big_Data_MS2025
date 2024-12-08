import pandas as pd
import pickle
from typing import List, Any
import logging
import spacy

from utils.file_manager import DataHandler

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
    
class TechniqueProcessor:
    """Class responsible for processing recipe techniques."""
    
    def __init__(self, techniques_list: List[str]) -> None:
        self.techniques_list = techniques_list
    
    def binarize_step_to_technique(self, steps: Any) -> List[int]:
        """
        Transform steps into a binary list indicating the presence of techniques
        
        Parameters:
        steps (spaCy Doc object): The steps to analyze
        
        Returns:
        List[int]: A binary list indicating the presence of techniques.
        """
        techniques_in_step = [0] * len(self.techniques_list)
        for token in steps:
            if token.lemma_ in self.techniques_list:
                index = self.techniques_list.index(token.lemma_)
                techniques_in_step[index] = 1
        return techniques_in_step
        
    def get_binary_techniques_list(self, raw_recipes_df: pd.DataFrame) -> List[List[int]]:
        """
        Analyze steps using spaCy to detect techniques
        
        Parameters:
        raw_recipes_df (pd.DataFrame): The DataFrame containing the raw recipes data.
        
        Returns:
        List[List[int]]: A list of binary lists indicating the presence of techniques for each recipe.
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
          
class TechniqueAnalyzer:
    """Main class to run the recipe analysis by techniques and season"""
    
    def __init__(self, techniques_list: List[str]) -> None:
        self.data_loader = DataHandler()
        self.technique_processor = TechniqueProcessor(techniques_list)
    
    def run_analysis(self) -> None:
        """Run the main analysis process."""
        recipes = self.data_loader.load_clean_csv('data/raw/RAW_recipes.csv', ['steps'])
        interactions = self.data_loader.load_clean_csv('data/raw/RAW_interactions.csv', date='date')
        filter_recipes = pd.read_pickle('data/preprocess/recipe_filtered.pkl')

        df_steps = pd.merge(recipes[['id', 'name', 'steps']], filter_recipes, on='id', how='right')

        techniques = self.technique_processor.create_technique_df(df_steps)

        with open("data/preprocess/techniques.pkl", "wb") as f:
            pickle.dump(techniques, f)

        season_correlations = self.technique_processor.analyze_correlation(techniques)

        with open("data/preprocess/season_correlations.pkl", "wb") as f:
            pickle.dump(season_correlations, f)

if __name__ == "__main__":
    analyzer = TechniqueAnalyzer(TECHNIQUES_LIST)
    analyzer.run_analysis()