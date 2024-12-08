import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from pathlib import Path
from wordcloud import WordCloud
import seaborn as sns
import time
from technique import DataLoader
from pickle_creation import extract_reviews_for_year, extract_reviews

import os
ABSOLUTE_PATH = os.path.abspath(__file__)

def calculate_season_percentage(data: pd.DataFrame, year: int) -> pd.Series:
    """
    Calcula the pourcentage for every season for a specific year
    """
    data['count_for_year'] = data['review_per_year'].apply(lambda x: extract_reviews_for_year(x, year))
    
    # Calculer la somme totale des reviews pour l'année
    total_count = data['count_for_year'].sum()
    
    if total_count == 0:
        return pd.Series(dtype='float64')  # Retourne une série vide si aucune donnée
    
    # Calculer les pourcentages des saisons
    season_percentage = (
        data.groupby('season')['count_for_year']
        .sum()
        .div(total_count)
        .mul(100)
    )
    
    return season_percentage

#-------------------------------------------------------------
class page_streamlit:
    """
    Class page_streamlit to take care of all the methods related to modifying information on the streamlit page.
    """
    @staticmethod
    def load_image(path: str, caption: str):
        """
        Load the image on the page
        """
        st.image(path, caption=caption, use_column_width=True)
#-------------------------------------------------------------

def filter_and_plot_by_count(data: pd.DataFrame, max_count: int) -> None:
    """
    Filters the DataFrame based on the maximum count of reviews per year
    and simulates an animation by displaying histograms dynamically in Streamlit.
    """
    # Step 1: Filter recipes with count_for_year <= max_count
    filtered_data = data[data['count_for_year'].apply(lambda x: max(x.values()) if isinstance(x, dict) else 0) <= max_count]
    
    # Step 2: Simulate animation by iterating through filtered data
    for _, row in filtered_data.iterrows():
        if isinstance(row['count_for_year'], dict):
            id_year_counts = row['count_for_year']
            
            # Create the plot
            plt.figure(figsize=(8, 5))
            plt.bar(id_year_counts.keys(), id_year_counts.values(), color='lightcoral', edgecolor='black')
            plt.title(f"Review Count Distribution for Recipe ID {row['id']}")
            plt.xlabel("Year")
            plt.ylabel("Number of Reviews")
            plt.xticks(rotation=45)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Display the plot in Streamlit
            st.pyplot(plt)
            
            # Pause for animation effect
            time.sleep(0.5)
            
            # Clear the current plot (important for animations)
            plt.close()
            
class page_review:
    def __init__(self, dataframe: pd.DataFrame, folder_path: Path) -> None:
        """
        Init the page_review class
        """
        self.data_path = folder_path
        self.df = dataframe

    def run(self) -> None:
        # pour chaque id => nombre par an de review. 
        self.df['count_for_year'] = self.df['review_per_year'].apply(lambda x: extract_reviews(x))
        
        st.set_page_config(layout="wide", page_title="Analyse des Recettes - Dashboard Interactif")

        # Section 1 : Image statique et animation
        st.header("1. Analyse temporelle des interactions par recette")
        col1, col2 = st.columns([1.5, 2])
        
        with col1:
            # A voir avec les autres.
            page_streamlit.load_image(str(self.data_path / "image" / "image_reviews_per_year.png"),"Répartition des recettes")
        
        
        with col2:
            st.title("Simulated Animation of Review Counts by Recipe")
            max_count = st.slider("Select Maximum Review Count", min_value=1, max_value=10, step=1, value=5)
            filter_and_plot_by_count(self.df, max_count)
            # Exemple de graphique dynamique pour une année
            #yearly_data = df.copy()
            #yearly_data["interaction_count"] = yearly_data["review_per_year"].apply(lambda x: extract_reviews_for_year(x, year))
            #plot_yearly_interactions(yearly_data)

        '''
        # Section 2 : Répartition des saisons
        st.header("2. Répartition des saisons")
        date_slide = st.slider("Choisir une année pour les pourcentages de saisons", min_value=2001, max_value=2018, step=1, value=2010)
        season_data = calculate_season_percentage(self.df, date_slide)
        plot_season_pie(season_data)

        # Section 3 : Comparaison multi-dimensionnelle
        st.header("3. Analyse multi-dimensionnelle des variables")
        selected_columns = st.multiselect(
            "Choisissez les colonnes à inclure dans le pairplot (ex. rating, season, etc.)",
            options=["rating", "weighted_rating", "season", "review_per_year"],
            default=["rating", "weighted_rating"]
        )
        if selected_columns:
            plot_pairplot(self.df[selected_columns])

        # Section 4 : Nuage de mots
        st.header("4. Recettes les plus populaires")
        generate_wordcloud(self.df, "weighted_rating")
        '''

# Point d'entrée
if __name__ == "__main__":
    # Charger les données
    
    #data_str = "Kit_Big_Data_MS2025\\data\\"
    data_str = Path(ABSOLUTE_PATH) / ".." / ".." / "data" 
    DATA_PATH = data_str / "preprocess" / "recipe_with_years.pkl"
    df = DataLoader.load_pickle(DATA_PATH)
    first_page_review = page_review(df, data_str)
    first_page_review.run()