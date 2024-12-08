import pandas as pd

class DataProcessor:
    @staticmethod
    def transform_date(date: pd.Series) -> pd.Series:
        """
        Converts a Pandas Series of dates into datetime objects.
        To note: we could modify to dt.date since the hours, minutes and secondes is not relevant here
        """
        return pd.to_datetime(date)

    @staticmethod
    def average_ratings_recipe(interaction: pd.DataFrame, recipe: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the average rating for each recipe based on interaction data 
        and merges the results into the recipe DataFrame.
        """
        average_ratings = (
            interaction.groupby('id')['rating']
            .mean()
            .reset_index(name='rating')
        )
        return recipe.merge(average_ratings, on='id', how='left')
    
    @staticmethod
    def expand_rows_by_count(df: pd.DataFrame) -> pd.DataFrame:
        """
        Function for test
        """
        expanded_rows = []
        for _, row in df.iterrows():
            expanded_rows.extend([row] * row['count'])
        return pd.DataFrame(expanded_rows)
    
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
    def scale_column_to_range(df: pd.DataFrame, column_name: str, target_max: float = 20) -> pd.DataFrame:
        """
        Scales a column's values to a specified range (can be 20 or 5).
        """
        if column_name not in df.columns:
            raise ValueError(f"La colonne '{column_name}' n'existe pas dans le DataFrame.")
        
        col_max = df[column_name].max()
        
        # Évitez de diviser par 0
        if col_max == 0:
            raise ValueError(f"La colonne '{column_name}' contient uniquement des 0.")
        
        # Calculez le facteur d'échelle
        scaling_factor = target_max / col_max
        
        # Appliquez la transformation
        df[f"{column_name}"] = df[column_name] * scaling_factor
        
        return df