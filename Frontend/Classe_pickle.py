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
        

    def plot_pie_charts(self, title="Camemberts par intervalle de temps"):
        """Affiche les camemberts pour chaque ligne du DataFrame dans Streamlit."""
        st.title(title)

        for index, row in self.dataframe.iterrows():
            intervalle = row['intervalle']  # Nom de l'intervalle
            data = row[['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']]  # Données des saisons
            labels = ['Printemps', 'Hiver', 'Été', 'Automne']

            # Création du graphique
            fig, ax = plt.subplots()
            ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Distribution pour l'intervalle {intervalle}")

            # Affichage du graphique dans Streamlit
            st.pyplot(fig)
            
    def plot_pie_charts_2(self, data_columns, label_names, title="Camemberts par intervalle de temps"):
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




