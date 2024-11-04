import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Analyse des résultats - Mangetamain")

# Introduction
st.write("""
### Bienvenue sur l'application interactive d'analyse des résultats.
Cette application vous permet d'explorer les résultats de notre étude. 
Modifiez les paramètres ci-dessous pour voir comment les résultats changent.
""")

# Chargement des données
# Remplace avec tes propres données ou une méthode d'import des données
@st.cache
def load_data():
    data = pd.read_csv("data/archive/RAW_recipes.csv")  # Remplace par tes données
    return data

data = load_data()

data['submitted'] = pd.to_datetime(data['submitted'], errors='coerce')
st.write(data.dtypes)

# Sidebar pour l'interactivité
st.sidebar.header("Options d'analyse")
selected_month = st.sidebar.selectbox("Choisissez un mois", data['submitted'].dt.month.unique())

# Filtrage des données
filtered_data = data[data['submitted'].dt.month == selected_month]

# Affichage des données filtrées
st.write(f"### Données pour le mois sélectionné : {selected_month}")
st.dataframe(filtered_data)

# Graphique interactif
st.write("### Graphique des résultats")
fig, ax = plt.subplots()
filtered_data.groupby('variable_a_plotter').size().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Conclusion avec storytelling
st.write("""
## Conclusion
Nous espérons que cette analyse vous a aidé à comprendre les enjeux de cette étude. 
N'hésitez pas à utiliser les options sur la gauche pour explorer les résultats par vous-même.
""")