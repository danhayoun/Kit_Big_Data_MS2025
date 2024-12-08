import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle 

import sys
import os

from utils.Classe_pickle import Display, CamembertDisplay, DictionnaireDisplay, HistogramDisplay


# Titre de l'application
st.title("Page - Temps de cuisson")

# Introduction
st.write("""
### Bienvenue sur la page interactive du temps de cuisson. Ici, nous étudions les liens entre temps de cuisson et saisons. 
""")





st.write("Dans un premier temps, nous avons voulu tracer la répartition des saisons des recettes, pour des valeurs de temps de cuisson fixées. ")
st.write("Point méthode : nous ne comptons pas le nombre de recettes déposées seulement, nous les pondérons par leur nombre de commentaires. Ainsi, plus une recette possède de commentaires, plus elle aura du poids dans le graphique. ")

st.write("\n")
st.write("Il nous a paru important de montrer l'histogramme des recettes par temps de cuisson, car pour certaines valeurs de temps de cuisson choisis, il y a très peu de recettes et les valeurs sont donc moins significatves.")
st.write("Par exemple, pour un temps de 179 minutes, il n'ya même pas de recette associée dans notre jeu de données.")

f = HistogramDisplay('temps_de_cuisson','./data/preprocess/cursor2.pkl')
f.afficher_histogram()

################# Camembert interactif ################
data_columns = ['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']
label_names = ['Spring', 'Winter', 'Summer', 'Fall']


pickle = CamembertDisplay('temps_de_cuisson','./data/preprocess/cursor2.pkl') 

pickle.plot_interactive_pie_chart(
    data_columns=['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%'],
    label_names=['Spring', 'Winter', 'Summer', 'Fall'],
    slider_label="Sélectionner un temps de cuisson (en min)",
    title="Répartition des recettes pour un temps de cuisson de"
)


st.write("nous avons ensuite trouvé que ces graphes n'étaient pas suffisament représentatifs pour tirer des conclusions, par rapport au temps des recettes en fonction des saisons.")

st.write("nous avons donc choisi de regarder 5 autres diagrammes, que nous considérons plus significatifs :")

 
pickle = CamembertDisplay('temps_de_cuisson','./data/preprocess/cursor_significatif.pkl')

pickle.plot_pie_charts_2(data_columns, label_names, title="Camemberts par intervalle de temps")

st.write("""
### Nous remarquons que l'hiver est plus propice à des recettes à long temps de cuisson (entre 30 min et 1h) tandis que le printemps est plus propice aux recettes rapides. 

Nous remarquons aussi que l'automne est bien plus présents pour des temps de cuisson supérieurs à 1h. Il semble ainsi que les saisons les plus froids soient celles où on réalise les recette les plus longues tandis que les saisons chaudes (printemps, été) sont celles où les recette sont les plus courtes.
""")

st.write("nous vous laissons maintenant avec un top 10, pour chaque saison et chaque intervalle considéré plus haut, afin de vous laisser choisir la recette qui convient le mieux à votre saison ainsi qu'au temps que vous avez devant vous 🙂 ")
dictionnaire = DictionnaireDisplay('temps_de_cuisson','./data/preprocess/dictionnaire_tops_10.pkl')


intervalle_mapping = {
    '0-10 min': 10,
    '10-30 min': 30,
    '30-60 min': 60,
    '1-2h': 120,
    'plus de 2h': 121
}
option_choisie = st.selectbox("Choisissez un intervalle :", options=list(intervalle_mapping.keys()))
intervalle_choisi = intervalle_mapping[option_choisie]

dictionnaire.afficher_tops_par_intervalle(intervalle_choisi)