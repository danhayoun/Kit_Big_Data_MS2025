import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from pathlib import Path
from technique import DataLoader
from pickle_creation import get_histogram_recipe, get_recipes_by_review_count, calculate_season_percentage

import os
ABSOLUTE_PATH = os.path.abspath(__file__)

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
        st.image(path, caption=caption, use_container_width=True)
#-------------------------------------------------------------
class page_plot:
    """
    Class page_plot to call when one want to plot schema directly on the streamlit page.
    """
    @staticmethod
    def plot_season_percentage_pie(data: pd.DataFrame, year: int) -> None:
        """
        Calculates and displays a pie chart of season percentages for a specific year.
        """
        try:
            season_percentage = calculate_season_percentage(data, year)
        except ValueError as ve:
            st.warning(ve)
            return
        fig, ax = plt.subplots(figsize=(3, 3))
        wedges, texts, autotexts = ax.pie(
            season_percentage.values,
            labels=season_percentage.index,
            autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
            startangle=90,
            colors=plt.cm.Paired.colors[:len(season_percentage)],
            wedgeprops=dict(width=0.3)  # Make it a donut chart
        )
        plt.setp(texts, fontsize=8)
        plt.setp(autotexts, fontsize=7, weight="bold")
        ax.set_title(f"Season Percentage for {year}", fontsize=10, weight="bold")
        st.pyplot(plt)

    @staticmethod             
    def plot_histogram_for_recipe(data: pd.DataFrame, recipe_name: str) -> None:
        """
        Plots a histogram for a specific recipe showing the number of reviews by year.
        """
        try:
            count_for_year = get_histogram_recipe(data, recipe_name)
        except ValueError as ve:
            st.warning(ve)
            return    
        if not isinstance(count_for_year, dict) or not count_for_year:
            st.warning(f"No review data available for recipe: {recipe_name}")
            return
    
        plt.figure(figsize=(8, 5))
        plt.bar(count_for_year.keys(), count_for_year.values(), color='lightcoral', edgecolor='black')
        plt.title(f"Review Count Distribution for Recipe: {recipe_name}")
        plt.xlabel("Year")
        plt.ylabel("Number of Reviews")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(plt)
    
class page_review:
    """
    The class page_review manages the Streamlit page for analyzing recipe reviews.

    This class facilitates an interactive dashboard that enables users to explore:
    - The temporal distribution of comments (reviews) for recipes.
    - The relationship between the number of comments and recipe usage across years.
    - Seasonal associations of recipes based on the timing of their reviews.

    It leverages Streamlit functionalities to provide visualizations such as:
    - An annual histogram of reviews.
    - Pie charts showing seasonal distributions.
    - Interactive filters for recipes based on review counts and popularity.
    """
    def __init__(self, dataframe: pd.DataFrame, folder_path: Path) -> None:
        """
        Init the page_review class.
        """
        self.data_path = folder_path
        self.df = dataframe

    def run(self) -> None:
        """
        Runs the fonctions of the page_review class.
        """
        st.title("Analyse des Recettes - Dashboard sur l'analyse des commentaires")
        
        st.write("Nous avons construit notre dataset en considérant que les commentaires sont des indicateurs de:\n" +
                 "- à quelle saison la recette peut être associée. Par exemple: un pot-au-feux, recette hivernale, risque plus facilement d'être utilisée -et donc d'avoir un commentaire sur un site de cuisine- en hiver qu'en été.\n" +
                 "- de son nombre d'utilisation.\n" +
                 "- dans une moindre mesure, de la popularité de la recette.")
        

        # Section 1: Image des interactions
        st.header("1. Analyse temporelle des commentaires")
        page_streamlit.load_image(str(self.data_path / "image" / "image_reviews_per_year.png"), "")
        st.write("Au dessus, un histogramme qui montre le nombre de commentaires par an." + "\nFun fact: Il est intéressant de constater que la plus part des commentaires se font sur des années spécifiques - entre 2006 et 2010.")
        
        # Section 2: 
        st.header("2. Analyse temporelle de l'utilisation des recettes")
        st.write("Nous voulons voir maintenant comment une recette est utilisée dans notre étude. Comme nous considérons que le nombre de commentaires est une bonne représentation, nous regardons la répartition du nombre de commentaire par années.\n"+
                 "\nNotice d'utilisation:\n- Selectionne le nombre maximal de commentaires que peut avoir une recette avec le slider.\n"+
                 "- Puis selectionne la recette que tu souhaites afficher. Les recettes sont données dans l'ordre décroissant de leur popularité.\n"
                 "\nA savoir: Nous avons decider de selectionner dans notre dataset uniquement les recettes avec plus de 5 commentaires (puisque nous avons 4 saisons), et la recette avec le plus de commentaire est 'best banana bread', qui a 1613 commentaires")
        max_count = st.slider("Selectionne le nombre maximal de commentaires que peut avoir une recette.", min_value=5, max_value=1613, step=1, value=5)
        filtered_recipes = get_recipes_by_review_count(self.df, max_count)
        if not filtered_recipes.empty:
            recipe_names = filtered_recipes.tolist()
            selected_recipe = st.selectbox("Selectionne une recette", recipe_names)
        if selected_recipe:
            page_plot.plot_histogram_for_recipe(self.df, selected_recipe)
        else:
            st.write("Aucune recette trouvée avec un nombre de commentaires inférieur ou égal à la valeur sélectionnée.")
        
        # Section 3
        st.header("3. Répartition des saisons en fontion de l'année")
        st.write("Pour interpréter au mieux ce schéma, il faut garder en tête la répartition des commentaires en fonction des années, illustrée au dessus.")
        selected_year = st.selectbox("Selectionne une année", list(range(2001, 2019)), index=0)
        page_plot.plot_season_percentage_pie(df, selected_year)

# Point d'entrée
if __name__ == "__main__":
    # Charger les données
    
    #data_str = "Kit_Big_Data_MS2025\\data\\"
    data_str = Path(ABSOLUTE_PATH) / ".." / ".." / "data" 
    DATA_PATH = data_str / "preprocess" / "recipe_with_years.pkl"
    df = DataLoader.load_pickle(DATA_PATH)
    first_page_review = page_review(df, data_str)
    first_page_review.run()