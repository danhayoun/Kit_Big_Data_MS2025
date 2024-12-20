import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime, date
import matplotlib.dates as mdates
import pickle
import bisect
from typing import List, Tuple, Dict


def generate_accurate_df(df: pd.DataFrame, path: str = "data/raw/RAW_recipes.csv") -> pd.DataFrame:
    """ 
    Fonction qui rajoute les colonnes 'minutes', 'name' et 'intervalle au df
        en entrée : - un dataframe pandas
    """
    recipes = pd.read_csv(path)  # ICI
    df = pd.merge(recipes[['id', 'name', 'minutes']], df, on='id', how='right')
    liste_cook_times = [10, 30, 60, 120, 121]  # Un peu mal dit mais bon
    df['intervalle'] = 0  # Rajoute la colonne intervalle
    for i in range(len(df)):
        minutes = df.at[i, "minutes"]  # manière de remplacer une valeur dans une ligne du df
        position = bisect.bisect_left(liste_cook_times, minutes)
        if position < len(liste_cook_times):
            df.at[i, 'intervalle'] = liste_cook_times[position]
        else:
            df.at[i, 'intervalle'] = 121
    return df


class Page_temps_de_cuisson:
    """ Classe pour définir la page temps de cuisson
        pas d'attributs
    """

    @staticmethod
    def get_vectors(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """  
        Fonction qui extrait le dataframe pandas et renvoie les 2 vecteurs ids et temps de cuisson (vector = vecteur temps de cuisson, vector_id = vecteur des ids)
            en entrée : - un dataframe pandas

        """
        times = df['minutes']
        ids = df['id']
        vector_id = ids.to_numpy()
        vector = times.to_numpy()
        return vector, vector_id

    @staticmethod
    def dictionnaire_minutes(vector: np.ndarray, vector_id: np.ndarray) -> Dict[int, int]:
        """ 
        Fonction qui créé le dictionnaire_minutes
            en entrée : - un vecteur des temps de cuisson
                        - un vecteur des ids correspondants
        """
        dictionnaire_minutes = {}
        j = 0
        for i in vector_id:
            dictionnaire_minutes[i] = vector[j]
            j += 1
        return dictionnaire_minutes

    @staticmethod
    def top_liste(dictionnaire: Dict[int, int]) -> List[Tuple[int, int]]:
        """ 
        Fonction qui créé le top des ids par temps de cuisson
            Prend en entrée un dictionnaire_minutes, et renvoie la liste des ids triée, le temps de cuisson le plus élevé à son id en première position 
        """
        top = sorted(dictionnaire.items(), key=lambda x: x[1], reverse=True)  # Liste des mots les plus utilisés
        return top

    @staticmethod
    def boxplot(dictionnaire_minutes: Dict[int, int]) -> None:
        """ 
        Fonction qui trace le boxplot des temps de cuisson

        Reçoit le dictionnaire {id : temps de cuisson} et plot le boxplot répartition des temps de cuisson 
        """
        occurrences_values = list(dictionnaire_minutes.values())
        mots = list(dictionnaire_minutes.keys())
        fig, ax = plt.subplots()
        fig.set_size_inches(1, 4)
        ax.boxplot(occurrences_values)
        outliers = ax.lines[5].get_ydata()
        for outlier in outliers:
            mot_associe = [mot for mot, count in dictionnaire_minutes.items() if count == outlier]
        plt.title('Diagramme moustache des occurrences des temps de cuisson')
        plt.ylabel('Nombre d\'occurrences')
        plt.show()

    @staticmethod
    def filtre_minutes(dictionnaire_minutes: Dict[int, int]) -> Dict[int, int]:
        """ 
        Fonction qui filtre le dictionnaire pour enlever les valeurs extrêmes
            reçoit en entrée : - un dictionnaire dictionnaire_minutes
        
        """
        l = []  # liste des ids à enlever
        for i in dictionnaire_minutes.keys():
            if dictionnaire_minutes[i] > 1000:
                l.append(i)
            if dictionnaire_minutes[i] == 0:  # On supprime aussi les valeurs à 0 min
                l.append(i)
        for i in l:
            del dictionnaire_minutes[i]
        return dictionnaire_minutes

    @staticmethod
    def generate_cursor_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """ 
        Fonction pour créer le camembert interactif, avec le curseur
            reçoit en entrée : un dataframe pandas
        """
        df_pivot = pd.DataFrame({
            'intervalle': [i for i in range(182)],
            'Spring': [0 for i in range(182)],
            'Winter': [0 for i in range(182)],
            'Summer': [0 for i in range(182)],
            'Fall': [0 for i in range(182)],
        })  # On initialise avec des valeurs à 0
        Liste_saisons = ['Spring', 'Winter', 'Summer', 'Fall']
        liste_cook_times = [i for i in range(1, 182)]
        for i in Liste_saisons:
            for j in range(len(liste_cook_times)):
                if j == 0:
                    count = df[(df['season'] == i) & (df['minutes'] <= liste_cook_times[j])]
                elif j < len(liste_cook_times) - 1:
                    count = df[(df['season'] == i) & (liste_cook_times[j - 1] <= df['minutes']) & (df['minutes'] <= liste_cook_times[j])]
                else:
                    count = df[(df['season'] == i) & (df['minutes'] >= liste_cook_times[-1])]
                df_pivot.loc[df_pivot['intervalle'] == liste_cook_times[j], i] = count.shape[0]
        for saison in ['Spring', 'Winter', 'Summer', 'Fall']:
            df_pivot[f'{saison}_%'] = (df_pivot[saison] / df_pivot[['Spring', 'Winter', 'Summer', 'Fall']].sum(axis=1)) * 100
        df_pivot['nb_recettes_total'] = (df_pivot['Summer'] + df_pivot['Winter'] + df_pivot['Spring'] + df_pivot['Fall'])
        df_pivot = df_pivot.fillna(0)
        return df_pivot

    @staticmethod
    def df_to_pickle(df_pivot: pd.DataFrame, path_pickle: str) -> int:
        """
        Fonction pour envoyer le dataframe réduit, utilisé pour le camembert interactif, vers un .pkl 
        reçoit en entrée : un dataframe et un chemin vers le pickle où sauvegarder le df
        """
        df_pivot = df_pivot.fillna(0)
        df_pivot.to_pickle(path_pickle)


    @staticmethod
    def generate_camemberts_significatifs(df : pd.DataFrame, path : str) -> pd.DataFrame: 
        """ 
        Fonction pour générer les 5 camemberts significatifs
        reçoit en entrée : un dataframe et un chemin vers la sortie .pkl
        """
        df_significatif = pd.DataFrame({
            'intervalle': [10,30,60,120,121],
            'Spring': [0 for i in range(5)],
            'Winter': [0 for i in range(5)],
            'Summer': [0 for i in range(5)],
            'Fall': [0 for i in range(5)],
        }) #On initialise 

        Liste_saisons = ['Winter','Summer','Fall','Spring']
        liste_cook_times = [10,30,60,120,121] 

        #Maintenant l'étape difficile

        for i in Liste_saisons :
            for j in range(5) :
                if(j==0) :
                    count = df[(df['season'] == i) & (df['minutes'] <= 10)]
                elif j < 4:
                    count = df[(df['season'] == i) & (liste_cook_times[j-1] < df['minutes'] ) & (df['minutes'] <= liste_cook_times[j])]
                else : 
                    count = df[(df['season'] == i) & (df['minutes'] > liste_cook_times[-1] )]
                    print(f"[DEBUG] season: {i}, Intervalle: >= {liste_cook_times[-1]}, Lignes trouvées: {count.shape[0]}")

                df_significatif.loc[df_significatif['intervalle'] == liste_cook_times[j], i] = count.shape[0]
        #Pourcentages 
        # Pour chaque saison, calcule le pourcentage des recettes dans chaque intervalle
        for saison in ['Spring', 'Winter', 'Summer', 'Fall']:
            # Ajoute une nouvelle colonne pour les pourcentages
            df_significatif[f'{saison}_%'] = (df_significatif[saison] / df_significatif[['Spring', 'Winter', 'Summer', 'Fall']].sum(axis=1)) * 100

        # Affiche le résultat
        intervalle_mapping = {
            10: "10",
            30: "30",
            60: "1h",
            120: "2h",
            121: "+"
        }

        df_significatif['intervalle'] = df_significatif['intervalle'].replace(intervalle_mapping)

        df_significatif = df_significatif.fillna(0)

        df_significatif.to_pickle(path)

        return df_significatif

    @staticmethod
    def top_by_interval_season(df: pd.DataFrame) -> Dict[Tuple[str, int], List[int]] :
        """ 
        Fonction qui créé un dictionnaire, regroupant les top 10 des recettes par saison et par intervalle
        reçoit en entrée : - un dataframe
        """
        Liste_saisons = ['Winter','Summer','Fall','Spring']
        liste_cook_times = [10,30,60,120,121] 

        dictionnaire = {(saison, intervalle): 0 for saison in Liste_saisons for intervalle in liste_cook_times}

        for i in Liste_saisons :
            for j in liste_cook_times :
                index_value = df.loc[(df['season'] == i) & (df['intervalle'] == j),'weighted_rating'].nlargest(10).index
                value = df.loc[index_value,'id']
                value = value.to_list()
                dictionnaire[(i,j)] = value 
        
        return dictionnaire



    @staticmethod
    def ids_to_name(l: List[int],df: pd.DataFrame) -> List[str] : 
        """ 
        Fonction qui prend en entrée la liste des ids des recettes et renvoit la liste des recettes
        reçoit en entrée : une liste et un dataframe
        """
        l_names = []

        for i in l :    
            value =  df.loc[df['id']==i,'name'].iloc[0]
            l_names.append(value)
        return l_names

    @staticmethod
    def get_name_top_by_interval_season(dictionnaire: Dict[Tuple[str, int], List[int]],df: pd.DataFrame) -> Dict[Tuple[str, int], List[str]] :
        """ 
        Fonction qui prend en entrée notre dictionnaire conçu à top_by_interval_season, 
        et qui renvoie le dictionnaire avec comme values les noms des recettes

        reçoit en entrée : - un dictionnaire
                        - un dataframe 
        """
        for i in dictionnaire.keys() :
            dictionnaire[i] = Page_temps_de_cuisson.ids_to_name(dictionnaire[i],df)
        return dictionnaire
    



    @staticmethod
    def generate_pickles_temps_de_cuisson() -> None:
        """
        Génère les pickles de temps de cuisson
        """
        df = pd.read_pickle("./data/preprocess/temps_de_cuisson.pkl")
        vector, vector_id = Page_temps_de_cuisson.get_vectors(df)
        dictionnaire_minutes = Page_temps_de_cuisson.dictionnaire_minutes(vector, vector_id)
        dictionnaire_minutes = Page_temps_de_cuisson.filtre_minutes(dictionnaire_minutes)
        df_pivot = Page_temps_de_cuisson.generate_cursor_dataframe(df)
        Page_temps_de_cuisson.df_to_pickle(df_pivot, "./data/preprocess/cursor2.pkl")
        Page_temps_de_cuisson.generate_camemberts_significatifs(df,"./data/preprocess/cursor_significatif.pkl") 
        dictionnaire_tops_10 = Page_temps_de_cuisson.top_by_interval_season(df)
        dictionnaire_final = Page_temps_de_cuisson.get_name_top_by_interval_season(dictionnaire_tops_10,df)
        with open("./data/preprocess/dictionnaire_tops_10.pkl", "wb") as fichier:
            pickle.dump(dictionnaire_final, fichier) #Etape OK 


    #Lancement du script 
if __name__ == "__main__": 
    Page_temps_de_cuisson.generate_pickles_temps_de_cuisson()