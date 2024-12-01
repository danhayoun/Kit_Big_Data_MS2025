import streamlit as st
import pickle
import pandas as pd

def load_data():
    # Charger la matrice de corrélations
    with open("./data/preprocess/season_correlations.pkl", "rb") as f:
        season_correlations = pickle.load(f)
        
    with open("./data/preprocess/techniques.pkl", "rb") as f:
        techniques = pickle.load(f)
    
    # Charger les données des recettes et avis
    recipes_data = pd.read_csv("../data/preprocess/recipe_filtered.csv") 
    return season_correlations,techniques, recipes_data

def get_season_for_technique(technique, season_correlations, threshold=0.01):
    # Find the season with the highest correlation for the given technique
    if technique in season_correlations.index:
        max_corr = season_correlations.loc[technique].max()
        min_corr = season_correlations.loc[technique].min()
        if max_corr - min_corr < threshold:
            return "No specific season", None
        else:
            season = season_correlations.loc[technique].idxmax()
            return season, max_corr
    else:
        return None, None

def get_top_recipes_by_season(recipes,techniques, technique, season, top_n=10):
    clean_recipe = recipes[['name', 'id', 'season', 'average_rating']]
    clean_recipe = clean_recipe.rename(columns={'id': 'recipe_id'})
    
    # Filtrer les recettes par saison et trier par avis
    recipes_with_technique = techniques[techniques['techniques'].apply(lambda x: technique in x)]
    
    # Merge with interactions to get ratings
    merged_df = pd.merge(recipes_with_technique, clean_recipe, on='recipe_id')
    
    # Filter recipes by the given season
    recipes_in_season = merged_df[merged_df['season'] == season]
    
    # Get the top N recipes with the highest average rating
    top_recipes = recipes_in_season.sort_values(by='average_rating', ascending=False).head(top_n)
    
    return top_recipes[['name', 'techniques', 'average_rating']]

def main():
    # Initialisation de l'état persistant
    if "selected_technique" not in st.session_state: # Variable pour stocker la technique sélectionnée
        st.session_state.selected_technique = None

    if "selected_season" not in st.session_state: # Variable pour stocker la saison sélectionnée
        st.session_state.selected_season = None
        
    st.set_page_config(layout="wide")  # Mode large pour plus d'espace
    st.title("Corrélations Techniques - Saisons et Recettes")
    st.write("""
        Cliquez sur une technique pour découvrir la saison avec laquelle elle est la plus corrélée 
        et les 10 recettes les mieux notées de cette saison.
    """)

    # Charger les données
    season_correlations, techniques, recipes_data = load_data()

    # Liste des techniques
    techniques_list = list(season_correlations.index)
    seasons_list = ['Winter','Summer','Spring','Fall'] #list(season_correlations.columns)

    # Organisation des boutons dans une grille
    cols = st.columns(8)  # Créer 8 colonnes pour organiser les boutons
    for idx, technique in enumerate(techniques_list):
        with cols[idx % 8]:  # Répartir les boutons sur les colonnes
            if st.button(technique):  # Créer un bouton pour chaque technique
                st.session_state.selected_technique = technique

    # Section des résultats en bas de la page
    result_container = st.container()
    with result_container:
        if st.session_state.selected_technique:
            # Récupérer la technique sélectionnée
            selected_technique = st.session_state.selected_technique
            # Trouver la saison la plus corrélée
            most_correlated_season, correlation_value = get_season_for_technique(selected_technique,season_correlations)

            # Afficher la saison la plus corrélée
            if correlation_value is None:
                st.subheader(f"La technique {selected_technique} n'est pas caractéristique d'une saison propre .")
            else :
                st.subheader(f"La saison la plus corrélée avec la technique {selected_technique} est **{most_correlated_season}** avec une corrélation de {correlation_value:.4f}.")

            # Ajouter un séparateur
            st.divider()
            st.write(f"### Choisissez une saison pour afficher les 10 recettes les mieux notées pour la technique {selected_technique}:")
            selected_season = st.radio("Saisons disponibles :", seasons_list)
            
            if selected_season:
                st.session_state.selected_season = selected_season
                # Récupérer les 10 recettes les mieux notées pour cette saison
                top_recipes = get_top_recipes_by_season(recipes_data,techniques,selected_technique,selected_season)
                st.write("### Les 10 recettes les mieux notées sont pour la saison {selected_season} sont :")
                st.table(top_recipes)

if __name__ == "__main__":
    main()
