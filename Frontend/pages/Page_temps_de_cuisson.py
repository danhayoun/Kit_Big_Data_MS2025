import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle 

import sys
import os

# Ajouter la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))



from Backend.utils.Classe_pickle import Display, CamembertDisplay, DictionnaireDisplay




# Titre de l'application
st.title("Page - Temps de cuisson")

# Introduction
st.write("""
### Bienvenue sur la page interactive du temps de cuisson. Ici, nous étudions les liens entre temps de cuisson et saisons. 
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

st.write("Dans un premier temps, nous avons voulu tracer la répartition des saisons des recettes, pour des valeurs de temps de cuisson fixées. ")
st.write("Point méthode : nous ne comptons pas le nombre de recettes déposées seulement, nous les pondérons par leur nombre de commentaires. Ainsi, plus une recette possède de commentaires, plus elle aura du poids dans le graphique. ")

st.write("\n")
st.write("Il nous a paru important de montrer l'histogramme des recettes par temps de cuisson, car pour certaines valeurs de temps de cuisson choisis, il y a très peu de recettes et les valeurs sont donc moins significatves.")
st.write("Par exemple, pour un temps de 179 minutes, il n'ya même pas de recette associée dans notre jeu de données.")
with open('../../data/preprocess/cursor2.pkl', 'rb') as fichier :
    df = pd.read_pickle(fichier)
    df = df.fillna(0)

    # Création de l'histogramme
    st.title("Histogramme du nombre de recettes par temps de cuisson")
    fig, ax = plt.subplots()
    xticks = list(range(0, 179, 10)) + [181]  # Ajouter des ticks tous les 10 et inclure 181
    xtick_labels = [str(x) if x < 181 else '180+' for x in xticks] 
    ax.bar(df.index, df['nb_recettes_total'], color='blue', alpha=0.7)
    ax.set_title("Distribution de nb_recettes par temps de cuisson")
    ax.set_xlabel("temps de cuisson en minutes")
    ax.set_ylabel("nb_recettes")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation=45, ha="right")  # Rotation pour lisibilité
    
    # Affichage dans Streamlit
    st.pyplot(fig)

################# Camembert interactif ################
data_columns = ['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']
label_names = ['Spring', 'Winter', 'Summer', 'Fall']


pickle = CamembertDisplay('temps_de_cuisson','../../data/preprocess/cursor2.pkl') 

pickle.plot_interactive_pie_chart(
    data_columns=['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%'],
    label_names=['Spring', 'Winter', 'Summer', 'Fall'],
    slider_label="Sélectionner un temps de cuisson (en min)",
    title="Répartition des recettes pour un temps de cuisson de"
)


st.write("nous avons ensuite trouvé que ces graphes n'étaient pas suffisament représentatifs pour tirer des conclusions, par rapport au temps des recettes en fonction des saisons.")

st.write("nous avons donc choisi de regarder 5 autres diagrammes, que nous considérons plus significatifs :")

 
pickle = CamembertDisplay('temps_de_cuisson','../../data/preprocess/cursor_significatif.pkl')

pickle.plot_pie_charts_2(data_columns, label_names, title="Camemberts par intervalle de temps")

st.write("""
### Nous remarquons que l'hiver est plus propice à des recettes à long temps de cuisson (entre 30 min et 1h) tandis que le printemps est plus propice aux recettes rapides. 

Nous remarquons aussi que l'automne est bien plus présents pour des temps de cuisson supérieurs à 1h. Il semble ainsi que les saisons les plus froids soient celles où on réalise les recette les plus longues tandis que les saisons chaudes (printemps, été) sont celles où les recette sont les plus courtes.
""")

st.write("nous vous laissons maintenant avec un top 10, pour chaque saison et chaque intervalle considéré plus haut, afin de vous laisser choisir la recette qui convient le mieux à votre saison ainsi qu'au temps que vous avez devant vous 🙂 ")
dictionnaire = DictionnaireDisplay('temps_de_cuisson','../../data/preprocess/dictionnaire_tops_10.pkl')

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