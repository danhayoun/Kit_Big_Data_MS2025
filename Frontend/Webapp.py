import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle 
from Classe_pickle import Display, DatabaseDisplay

# Titre de l'application
st.title("Analyse des résultats - Mangetamain")

# Introduction
st.write("""
### Bienvenue sur l'application interactive d'analyse des résultats.
Cette application vous permet d'explorer les résultats de notre étude. 
Modifiez les paramètres ci-dessous pour voir comment les résultats changent.
""")




# Charger le dictionnaire depuis le fichier pickle
try:
    with open('../Backend/src/webapp_assets/recettes_par_saison.pkl', 'rb') as fichier:
        recettes_par_saison = pickle.load(fichier)

         # Tracer le diagramme camembert
        labels = list(recettes_par_saison.keys())
        values = list(recettes_par_saison.values())

        fig, ax = plt.subplots(figsize=(6, 6))  # Définir la taille du graphique
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Assure que le camembert est bien rond
        ax.set_title("Répartition des recettes par saison")

        # Afficher le graphique dans Streamlit
        st.pyplot(fig)

    with open('../Backend/src/webapp_assets/dates_plus_postees.pkl', 'rb') as fichier_liste:
        ma_liste = pickle.load(fichier_liste)
        st.write("Top des dates avec le plus de posts:")
        st.text(", ".join(map(str, ma_liste)))  # Afficher la liste en format texte avec les valeurs qui se suivent



except FileNotFoundError:
    st.error("Le fichier 'recettes_par_saison.pkl' est introuvable. Assurez-vous qu'il est bien dans le dossier 'webapp_assets'.")
except Exception as e:
    st.error(f"Une erreur est survenue lors du chargement : {e}")




#Ca pourrait être pas mal d'afficher un calendrier averc les fêtes pour qu'on voit quand certaines fêtes sont proches de dates de recettes postées 


# Charger le fichier .pkl

with open('../Backend/src/webapp_assets/cursor2.pkl', 'rb') as fichier :
    df = pd.read_pickle(fichier)
    df = df.fillna(0)

    # Création de l'histogramme
    st.title("Histogramme de nb_recettes_total par indice")
    fig, ax = plt.subplots()
    ax.bar(df.index, df['nb_recettes_total'], color='blue', alpha=0.7)
    ax.set_title("Distribution de nb_recettes_total par indice")
    ax.set_xlabel("Indice")
    ax.set_ylabel("nb_recettes_total")
    
    # Affichage dans Streamlit
    st.pyplot(fig)

    saisons = ['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%']
    labels = ['Spring', 'Winter', 'Summer', 'Fall']
# Curseur pour sélectionner le temps de cuisson
    temps_cuisson = st.slider("Choisissez un temps de cuisson (en minutes)", min_value=1, max_value=int(df.index.max()), step=1)
    st.write(f"Temps de cuisson sélectionné : {temps_cuisson} minutes")

# Filtrer les données pour le temps de cuisson sélectionné
if temps_cuisson in df.index:  # Vérifie que l'intervalle existe
    data = df.loc[temps_cuisson]

    # Extraire et nettoyer les pourcentages pour le camembert
    valeurs = data[saisons].values.flatten()
    valeurs = [0 if pd.isna(v) else v for v in valeurs]


# Afficher le camembert
fig, ax = plt.subplots()
ax.pie(valeurs, labels=labels, autopct='%1.1f%%', startangle=90)
ax.set_title(f"Répartition des recettes pour {temps_cuisson} minutes")
st.pyplot(fig)



################################### Code fonctionnel mais sans POO ####################
#with open('../Backend/src/webapp_assets/cursor_significatif.pkl', 'rb') as fichier :
#    df = pd.read_pickle(fichier)
#    df = df.fillna(0)

# Titre de l'application
#st.title("Camemberts par intervalle de temps")

# Création des camemberts pour chaque intervalle
#for index, row in df.iterrows():
#    intervalle = row['intervalle']  # Récupération du nom de l'intervalle
#    data = row[['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']]  # Données des saisons
#   labels = ['Printemps', 'Hiver', 'Été', 'Automne']
#
    # Création du graphique
#    fig, ax = plt.subplots()
#    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
#    ax.set_title(f"Distribution pour l'intervalle {intervalle}")

    # Affichage du graphique dans Streamlit (distinct pour chaque camembert)
#    st.pyplot(fig)


data_columns = ['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']
label_names = ['Printemps', 'Hiver', 'Été', 'Automne']

pickle = DatabaseDisplay('temps_de_cuisson','../Backend/src/webapp_assets/cursor_significatif.pkl')

pickle.plot_pie_charts_2(data_columns, label_names, title="Camemberts par intervalle de temps")