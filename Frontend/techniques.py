import streamlit as st
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(layout="wide")  # Met la page en mode large
    st.title("Analyse des Corrélations entre Techniques et Saisons")
    st.write("""
        Cette application charge une matrice de corrélation pré-calculée
        et affiche une visualisation interactive.
    """)

    # Chargement de la matrice de corrélation depuis un fichier pickle
    try:
        with open("season_correlations.pkl", "rb") as f:
            season_correlations = pickle.load(f)
        
        st.success("Matrice de corrélation chargée avec succès !")

        # Affichage de la matrice sous forme de tableau
        st.subheader("Matrice de Corrélation")
        st.dataframe(season_correlations)
        
        st.subheader("Heatmap Interactive des Corrélations")
        
        fig = go.Figure(
            data=go.Heatmap(
                z=season_correlations.values[::-1],
                x=season_correlations.columns,
                y=season_correlations.index[::-1],
                colorscale="Balance",#Rdbu
                colorbar=dict(title="Corrélation"),
            )
        )

        # Ajouter les annotations (valeurs dans les cellules)
        annotations = []
        for i, row in enumerate(season_correlations.index):
            for j, col in enumerate(season_correlations.columns):
                value = season_correlations.iloc[i, j]
                annotations.append(
                    dict(
                        x=col,
                        y=row,
                        text=f"{value:.4f}",  # Formater avec deux décimales
                        showarrow=False,
                        font=dict(color="black" if abs(value) < 0.025 else "white"),  # Contraste selon la valeur
                    )
                )
         
        
        fig.update_layout(
            annotations=annotations,
            autosize=False,
            height=1000,  # Hauteur personnalisée
            margin=dict(l=0, r=0, t=50, b=50),  # Marges réduites
            coloraxis_colorbar=dict(title="Corrélation"),
        )
        
        # Afficher la heatmap interactive sur toute la largeur
        st.plotly_chart(fig, use_container_width=True)  

        
    except FileNotFoundError:
        st.error("Le fichier 'season_correlations.pkl' est introuvable. Assurez-vous de l'avoir généré et placé dans le répertoire de l'application.")

if __name__ == "__main__":
    main()
