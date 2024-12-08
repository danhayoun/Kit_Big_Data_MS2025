import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle 

import sys
import os

from utils.Classe_pickle import Display, CamembertDisplay, DictionnaireDisplay


# Titre de l'application
st.title("Analyse des résultats - Mangetamain")

# Introduction
st.write("""
### Bienvenue sur l'application interactive d'analyse des résultats.
Cette application vous permet d'explorer les résultats de notre étude. 
Modifiez les paramètres ci-dessous pour voir comment les résultats changent.
""")




# Charger le dictionnaire depuis le fichier pickle

#ICI ON MANIPULE UN DICTIONNAIRE, PAS UN DF 
#try:
#    with open('../../data/preprocess/recettes_par_saison.pkl', 'rb') as fichier:
#        recettes_par_saison = pickle.load(fichier)

         # Tracer le diagramme camembert
        #labels = list(recettes_par_saison.keys())
        #values = list(recettes_par_saison.values())

        #fig, ax = plt.subplots(figsize=(6, 6))  # Définir la taille du graphique
        #ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        #ax.axis('equal')  # Assure que le camembert est bien rond
        #ax.set_title("Répartition des recettes par saison")

        # Afficher le graphique dans Streamlit
        #st.pyplot(fig)

   # with open('../../data/preprocess/dates_plus_postees.pkl', 'rb') as fichier_liste:
   #     ma_liste = pickle.load(fichier_liste)
   #     st.write("Top des dates avec le plus de posts:")
   #     st.text(", ".join(map(str, ma_liste)))  # Afficher la liste en format texte avec les valeurs qui se suivent



#except FileNotFoundError:
#    st.error("Le fichier 'recettes_par_saison.pkl' est introuvable. Assurez-vous qu'il est bien dans le dossier 'webapp_assets'.")
#except Exception as e:
#    st.error(f"Une erreur est survenue lors du chargement : {e}")




#Ca pourrait être pas mal d'afficher un calendrier averc les fêtes pour qu'on voit quand certaines fêtes sont proches de dates de recettes postées 


# Charger le fichier .pkl

with open('./data/preprocess/cursor2.pkl', 'rb') as fichier :
    df = pd.read_pickle(fichier)
    df = df.fillna(0)

    # Création de l'histogramme
    st.title("Histogramme du nombre de recettes par temps de cuisson")
    fig, ax = plt.subplots()
    ax.bar(df.index, df['nb_recettes_total'], color='blue', alpha=0.7)
    ax.set_title("Distribution de nb_recettes par temps de cuisson")
    ax.set_xlabel("temps de cuisson en minutes")
    ax.set_ylabel("nb_recettes")
    
    # Affichage dans Streamlit
    st.pyplot(fig)

################# Camembert interactif ################
data_columns = ['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']
label_names = ['Spring', 'Winter', 'Summer', 'Fall']


pickle = CamembertDisplay('temps_de_cuisson','./data/preprocess/cursor2.pkl') 

pickle.plot_interactive_pie_chart(
    data_columns=['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%'],
    label_names=['Spring', 'Winter', 'Summer', 'Fall'],
    slider_label="Sélectionnez un intervalle",
    title="Répartition des recettes par intervalle de temps"
)



 
pickle = CamembertDisplay('temps_de_cuisson','./data/preprocess/cursor_significatif.pkl')

pickle.plot_pie_charts_2(data_columns, label_names, title="Camemberts par intervalle de temps")

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