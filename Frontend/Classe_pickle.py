import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import streamlit as st


pages = ['temps_de_cuisson','correlation','techniques_cuisine']

##################CLASSE GENERIQUE POUR TOUS LES PICKLE ####################################

class Display : #Pour tous les .pkl, attributs : quel page, quel chemin 
    def __init__(self,page,pkl_path) :
        if page in pages :
            self.__page = page
        else : 
            raise ValueError(f"La page doit être une chaîne de caractères parmis :{', '.join(pages)}")
        self.pkl_path = pkl_path

    # Méthode publique pour accéder à l'attribut privé
    def get_page(self):
        return self.__page

    # Méthode publique pour modifier l'attribut privé
    def set_page(self, new_page):
        if new_page in pages : 
            self.__page = new_page
        else:
            raise ValueError(f"La page doit être une chaîne de caractères parmis :{', '.join(pages)}")
        

################## CLASSES POUR LES DIFFERENTS TYPES DE PICKLE UTILISES ############################

class DatabaseDisplay(Display):
    def __init__(self, page, pkl_path):
        super().__init__(page, pkl_path)  # Appelle le constructeur de Display
        self.dataframe = self.load_dataframe()  # Charge le DataFrame spécifique

    def load_dataframe(self):
        """Charge un DataFrame à partir du fichier .pkl."""
        try:
            df = pd.read_pickle(self.pkl_path)
            return df.fillna(0)  # Remplace les valeurs NaN par 0
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du fichier .pkl : {e}")
        

            
    def plot_pie_charts_2(self, data_columns, label_names, title):
         #"""Trace des camemberts pour chaque ligne du DataFrame.
         #Args:
        #- data_columns (list): Liste des colonnes à utiliser pour les données (ex: ['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']).
        #- label_names (list): Liste des labels correspondants (ex: ['Printemps', 'Hiver', 'Été', 'Automne']).
        #- title (str): Titre global pour la section Streamlit.

            if not isinstance(data_columns, list) or not isinstance(label_names, list):
                raise TypeError("Les arguments 'data_columns' et 'label_names' doivent être des listes.")
            if len(data_columns) != len(label_names):
                raise ValueError("Les listes 'data_columns' et 'label_names' doivent avoir la même longueur.")

            st.title(title)

            for index, row in self.dataframe.iterrows():
                intervalle = row['intervalle']  # Nom de l'intervalle
                data = row[data_columns]  # Récupération des données à tracer
                labels = label_names  # Récupération des labels

                # Création du graphique
                fig, ax = plt.subplots()
                ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Distribution pour l'intervalle {intervalle}")

                # Affichage du graphique dans Streamlit
                st.pyplot(fig)

    def plot_interactive_pie_chart(self, data_columns, label_names, slider_label="Choisissez un intervalle", title="Camembert interactif par intervalle"):
    #"""
    #Affiche un camembert interactif en fonction d'une valeur sélectionnée via un curseur.
    #rgs:
    #    data_columns (list): Liste des colonnes contenant les données pour le camembert (ex. ['Spring_%', 'Winter_%', ...]).
    #    label_names (list): Liste des labels correspondants (ex. ['Spring', 'Winter', ...]).
    #    slider_label (str): Texte affiché pour le curseur.
    #    title (str): Titre pour le camembert.
        if not isinstance(data_columns, list) or not isinstance(label_names, list):
            raise TypeError("Les arguments 'data_columns' et 'label_names' doivent être des listes.")
        if len(data_columns) != len(label_names):
            raise ValueError("Les listes 'data_columns' et 'label_names' doivent avoir la même longueur.")

        # Curseur pour sélectionner l'intervalle
        intervalle_max = int(self.dataframe['intervalle'].max())
        intervalle = st.slider(slider_label, min_value=1, max_value=intervalle_max, step=1)
        st.write(f"Intervalle sélectionné : {intervalle}")

        # Filtrer les données pour l'intervalle sélectionné
        if intervalle in self.dataframe['intervalle'].values:
            row = self.dataframe[self.dataframe['intervalle'] == intervalle].iloc[0]

            # Extraire les données pour le camembert
            data = row[data_columns].values.flatten()
            data = [0 if pd.isna(v) else v for v in data]  # Remplacer NaN par 0

            # Créer le graphique du camembert
            fig, ax = plt.subplots()
            ax.pie(data, labels=label_names, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"{title} ({intervalle})")

            # Afficher dans Streamlit
            st.pyplot(fig)
        else:
            st.warning(f"Aucun intervalle correspondant à la valeur {intervalle} trouvé.")





