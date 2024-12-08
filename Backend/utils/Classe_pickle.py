import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import streamlit as st


pages = ['temps_de_cuisson','fun_facts','techniques_cuisine'] #Les 3 pages de l'application 


class Display : 
    """ Classe générique pour tous les .pkl
        attributs : quel page, quel chemin 
    
    """
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

class CamembertDisplay(Display): 
    """ Classe pour les dataframes pour camemberts
    
    """
    def __init__(self, page, pkl_path):
        super().__init__(page, pkl_path)  # Appelle le constructeur de Display
        self.dataframe = self.load_dataframe()  # Charge le DataFrame spécifique


    def load_dataframe(self,enable_fillna = False): #Charge le dataframe, mettre enable_fillna à True si on veut remplacer les Nan par des 0 
        """Charge un DataFrame à partir du fichier .pkl."""
        try:
            df = pd.read_pickle(self.pkl_path)
            if(enable_fillna == True) :
                return df.fillna(0)  # Remplace les valeurs NaN par 0
            else : 
                return df
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du fichier .pkl : {e}")
        

            
    def plot_pie_charts_2(self, data_columns, label_names, title):
            """Trace des camemberts pour chaque ligne du DataFrame.
            Args:
            - data_columns (list): Liste des colonnes à utiliser pour les données (ex: ['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']).
            - label_names (list): Liste des labels correspondants (ex: ['Printemps', 'Hiver', 'Été', 'Automne']).
            - title (str): Titre global pour la section Streamlit."""
         
            intervalle_mapping = {
            '10': "Distribution pour l'intervalle 0-10 min",
            '30': "Distribution pour l'intervalle 10-30 min",
            '1h': "Distribution pour l'intervalle 30-60 min",
            '2h': "Distribution pour l'intervalle 1-2h",
            '+': "Distribution pour + de 2h"
            } 

            if not isinstance(data_columns, list) or not isinstance(label_names, list):
                raise TypeError("Les arguments 'data_columns' et 'label_names' doivent être des listes.")
            if len(data_columns) != len(label_names):
                raise ValueError("Les listes 'data_columns' et 'label_names' doivent avoir la même longueur.")

            st.title(title)
            cols = st.columns(2)  # Divise la ligne en 2 colonnes
            index_col = 0  # Index de la colonne courante

            for index, row in self.dataframe.iterrows():
                # Utiliser le mapping pour obtenir la description
                intervalle_description = intervalle_mapping.get(row['intervalle'], "Intervalle inconnu")

                # Récupérer les données et les labels pour le camembert
                data = row[data_columns]  # Données à tracer
                labels = label_names  # Labels pour le graphique

                # Création du graphique
                fig, ax = plt.subplots()
                ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title(intervalle_description)  # Utiliser directement la description

                # Affichage dans Streamlit
                cols[index_col].pyplot(fig)
                # Alterner entre colonne 0 et 1
                index_col = (index_col + 1) % 2

    def plot_interactive_pie_chart(self, data_columns, label_names, slider_label="Sélectionner un temps de cuisson (en min)", title="Camembert interactif par intervalle"):
        """
        Affiche un camembert interactif en fonction d'une valeur sélectionnée via un curseur.
        Args:
       data_columns (list): Liste des colonnes contenant les données pour le camembert (ex. ['Spring_%', 'Winter_%', ...]).
        label_names (list): Liste des labels correspondants (ex. ['Spring', 'Winter', ...]).
        slider_label (str): Texte affiché pour le curseur.
        title (str): Titre pour le camembert."""

        
        if not isinstance(data_columns, list) or not isinstance(label_names, list):
            raise TypeError("Les arguments 'data_columns' et 'label_names' doivent être des listes.")
        if len(data_columns) != len(label_names):
            raise ValueError("Les listes 'data_columns' et 'label_names' doivent avoir la même longueur.")

        # Curseur pour sélectionner l'intervalle
        intervalle_max = int(self.dataframe['intervalle'].max())
        intervalle_mapping = {i: str(i)+" min" for i in range(1, intervalle_max)}
        intervalle_mapping[181] = '+180 min'
        intervalle = st.slider(slider_label, min_value=1, max_value=intervalle_max, step=1)
        intervalle_label = intervalle_mapping.get(intervalle, intervalle)

        # Filtrer les données pour l'intervalle sélectionné
        if intervalle in self.dataframe['intervalle'].values:
            row = self.dataframe[self.dataframe['intervalle'] == intervalle].iloc[0]

            # Extraire les données pour le camembert
            data = row[data_columns].values.flatten()
            data = [0 if pd.isna(v) else v for v in data]  

            # Vérifier si toutes les valeurs sont 0
            if all(v == 0 for v in data):
                st.warning(f"Aucune donnée significative pour l'intervalle {intervalle_label}.")
                return

            # Créer le graphique du camembert
            fig, ax = plt.subplots()
            ax.pie(data, labels=label_names, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"{title} ({intervalle_label})")

            # Afficher dans Streamlit
            st.pyplot(fig)
        else:
            st.warning(f"Aucun intervalle correspondant à la valeur {intervalle} trouvé.")
    




class DictionnaireDisplay(Display): 
    def __init__(self, page, pkl_path):
        super().__init__(page, pkl_path)  # Appelle le constructeur de Display
        self.dictionnaire = self.load_dictionnaire()  # Charge le DataFrame spécifique
    def load_dictionnaire(self):
        """
        Charge le dictionnaire à partir du fichier pickle spécifié dans self.pkl_path.

        :return: Le dictionnaire chargé.
        """
        try:
            with open(self.pkl_path, 'rb') as f:
                dictionnaire = pickle.load(f)
            return dictionnaire
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier pickle '{self.pkl_path}' est introuvable.")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du dictionnaire : {e}")
        
    def afficher_tops_par_intervalle(self, intervalle_choisi):
        """
        Affiche les tops 10 recettes par saison pour un intervalle donné dans Streamlit.

        :param intervalle_choisi: Intervalle pour lequel afficher les recettes (par exemple : 10, 30, 60, etc.)
        """

        # Vérifie que le dictionnaire est chargé
        if not self.dictionnaire:
            raise ValueError("Le dictionnaire est vide ou non chargé.")

        # Vérifier que l'intervalle existe dans le dictionnaire
        if intervalle_choisi not in [key[1] for key in self.dictionnaire.keys()]:
            st.error(f"L'intervalle {intervalle_choisi} n'existe pas dans les données.")
            return

        # Initialiser une liste pour stocker les données tabulaires
        tableaux = []

        # Parcourir le dictionnaire pour l'intervalle donné
        for (saison, intervalle), recettes in self.dictionnaire.items():
            if intervalle == intervalle_choisi:
                # Ajouter les recettes dans une structure tabulaire
                tableaux.append(pd.DataFrame({
                    'Saison': [saison] * len(recettes[:10]),
                    'Recette': recettes[:10]  # Limiter à 10 recettes
                }))

        # Afficher les tops dans Streamlit
        st.header(f"Tops 10 des recettes par saison ")

        for tableau in tableaux:
            saison = tableau['Saison'].iloc[0]
            st.subheader(f"Saison : {saison}")
            st.table(tableau[['Recette']])




