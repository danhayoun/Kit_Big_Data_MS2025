import streamlit as st
import sys
from typing import Tuple, Optional
import pandas as pd
import plotly.graph_objects as go
import os 

# Ajouter le répertoire racine au chemin de recherche des modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.technique import DataLoader
class SeasonCorrelationAnalyzer:
    """Class for analyzing season correlations."""
    def __init__(self, season_correlations: pd.DataFrame) -> None:
        self.season_correlations = season_correlations

    def get_season_for_technique(self, technique: str, threshold: float = 0.01) -> Tuple[Optional[str], Optional[float]]:
        """
        Give the season correlated to the class with the value.
        If the difference for the maximum value and the minimum value for the technique are less than the given threshold (0.01 by default), we decide to say that the technique has no specific season.

        Parameters:
        technique (str): The technique to analyze.
        threshold (float): The threshold to determine if a technique has a specific season.

        Returns:
        Tuple[Optional[str], Optional[float]]: The season and the correlation value, or (None, None) if no specific season is found.
        """
        if technique in self.season_correlations.index:
            max_corr = self.season_correlations.loc[technique].max()
            min_corr = self.season_correlations.loc[technique].min()
            if max_corr - min_corr < threshold:
                return "No specific season", None
            season = self.season_correlations.loc[technique].idxmax()
            return season, max_corr
        return None, None

    def plot_heatmap(self) -> None:
        """
        Plot an interactive heatmap of the season correlations.
        """
        fig = go.Figure(
            data=go.Heatmap(
                z=self.season_correlations.values[::-1],
                x=self.season_correlations.columns,
                y=self.season_correlations.index[::-1],
                colorscale="Balance",
                colorbar=dict(title="Corrélation"),
            )
        )
        annotations = [
            dict(
                x=col,
                y=row,
                text=f"{value:.4f}",
                showarrow=False,
                font=dict(color="black" if abs(value) < 0.025 else "white"),
            )
            for i, row in enumerate(self.season_correlations.index)
            for j, col in enumerate(self.season_correlations.columns)
            if (value := self.season_correlations.iloc[i, j])
        ]
        fig.update_layout(
            annotations=annotations,
            autosize=False,
            height=1000,
            margin=dict(l=0, r=0, t=50, b=50),
            coloraxis_colorbar=dict(title="Corrélation"),
        )
        return fig


class RecipeRecommender:
    """Class for recommending recipes"""
    
    @staticmethod
    def get_top_recipes_by_season(techniques : pd.DataFrame, technique: str, season: str, top_n : int = 10) -> pd.DataFrame:
        """
        Return the TOP 10 recipes for the selected season for this technique by weighted rating
        Parameters:
        techniques (pd.DataFrame): The DataFrame containing the techniques and recipes data.
        technique (str): The technique to filter recipes by.
        season (str): The season to filter recipes by.
        top_n (int): The number of top recipes to return. Default is 10.

        Returns:
        pd.DataFrame: A DataFrame containing the top recipes for the selected season and technique.
        """
        recipes_with_technique = techniques[techniques['techniques'].apply(lambda x: technique in x)]
        clean_recipe = recipes_with_technique[['recipe_id', 'name', 'techniques','season', 'weighted_rating']]
        recipes_in_season = clean_recipe[clean_recipe['season'] == season]
        return recipes_in_season.sort_values(by='weighted_rating', ascending=False).head(top_n)[['name', 'techniques', 'weighted_rating']]


class TechniquePage:
    """
    Main application class for Technique
    """
    def __init__(self) -> None:
        self.season_correlations = None
        self.techniques = None
        self.analyzer = None

    def load_datas(self) -> None:
        """
        Load all the needed pickle for the technique page (season_correlations & techniques)
        """
        data_loader = DataLoader()
        self.season_correlations = data_loader.load_pickle("./data/preprocess/season_correlations.pkl")
        self.techniques = data_loader.load_pickle("./data/preprocess/techniques.pkl")
        if self.season_correlations is not None:
            self.analyzer = SeasonCorrelationAnalyzer(self.season_correlations)

    def run(self) -> None:
        """
        Method to run the Streamlit Technique Page
        """
        st.set_page_config(layout="wide")
        st.title("Analyse des Corrélations entre Techniques et Saisons")
        self.load_datas()

        if self.season_correlations is not None:
            st.subheader("Heatmap Interactive des Corrélations")
            fig = self.analyzer.plot_heatmap()
            st.plotly_chart(fig, use_container_width=True)

            if "selected_technique" not in st.session_state:
                st.session_state.selected_technique = None

            st.write("### Sélectionnez une technique pour découvrir les corrélations")
            techniques_list = list(self.season_correlations.index)
            cols = st.columns(8)
            for idx, technique in enumerate(techniques_list):
                with cols[idx % 8]:
                    if st.button(technique):
                        st.session_state.selected_technique = technique

            if st.session_state.selected_technique:
                selected_technique = st.session_state.selected_technique
                season, correlation_value = self.analyzer.get_season_for_technique(selected_technique)

                if correlation_value is None:
                    st.subheader(f"La technique {selected_technique} n'est pas caractéristique d'une saison propre.")
                else:
                    st.subheader(
                        f"La saison la plus corrélée avec la technique {selected_technique} est **{season}** "
                        f"avec une corrélation de {correlation_value:.4f}."
                    )
                    st.divider()
                    st.write(f"### Choisissez une saison pour voir les recettes pour la technique {selected_technique}:")
                    seasons_list = ['Winter', 'Summer', 'Spring', 'Fall']
                    selected_season = st.radio("Saisons disponibles :", seasons_list)

                    if selected_season:
                        top_recipes = RecipeRecommender.get_top_recipes_by_season(
                            self.techniques, selected_technique, selected_season
                        )
                        st.write(f"### Les 10 recettes les mieux notées pour {selected_season} sont :")
                        st.table(top_recipes)


if __name__ == "__main__":
    app = TechniquePage()
    app.run()
