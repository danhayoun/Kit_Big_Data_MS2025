import pandas as pd

class DataProcessor:
    @staticmethod
    def transform_date(date):
        return pd.to_datetime(date)

    @staticmethod
    def average_ratings_recipe(interaction, recipe):
        average_ratings = (
            interaction.groupby('id')['rating']
            .mean()
            .reset_index(name='rating')
        )
        return recipe.merge(average_ratings, on='id', how='left')
    
    @staticmethod
    def scale_column_to_range(df, column_name, target_max=20):
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