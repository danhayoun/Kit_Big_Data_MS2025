#Ce fichier définit les fonctions utilisées pour créer la page des curseurs 


import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
#################### Fonction qui extrait le csv et renvoie les 2 vecteurs ids et temps de cuisson (vector = vecteur temps de cuisson, vector_id = vecteur des ids)  ######################
def extraction_csv(path) :
    df = pd.read_csv(path)

    times = df['minutes']

    ids = df['id']
    vector_id = ids.to_numpy()
    vector = times.to_numpy()
    return vector,vector_id,df




############### Fonction qui créé le dictionnaire_minutes #######################################
def dictionnaire_minutes(vector,vector_id) :
    #dictionnaire_minutes = {} #clé = id, valeur = temps de cuisson
    dictionnaire_minutes =  {}

    j=0
    for i in vector_id :
        #dictionnaire_minutes[i] = df[df['id'] == i ]['minutes'].iloc[0]
        dictionnaire_minutes[i] = vector[j]
        j+=1
    return dictionnaire_minutes


############### Fonction qui créé le top des ids par temps de cuisson  #######################################

def top_liste(dictionnaire) : #Prend en entrée un dictionnaire_minutes, et renvoie la liste des ids triée, le temps de cuisson le plus élevé à son id en première position 

    top = sorted(dictionnaire.items(),key =lambda x : x[1], reverse = True) #Liste des mots les plus utilisés
    return top 




############### Fonction qui trace le boxplot des temps de cuisson #######################################

def boxplot(dictionnaire_minutes) : #Reçoit le dictionaire {id : temps de cuisson} et plot le boxplot répartition des temps de cuisson 

    occurrences_values = list(dictionnaire_minutes.values())
    mots = list(dictionnaire_minutes.keys())

# Créer le diagramme en boîte (boxplot)
    fig, ax = plt.subplots()
    fig.set_size_inches(1, 4)
    ax.boxplot(occurrences_values)

# Calculer la position des points extrêmes
    outliers = ax.lines[5].get_ydata()

# Afficher les mots associés aux outliers (valeurs extrêmes)
    for outlier in outliers:
    # Trouver le mot correspondant à la valeur d'occurrence
        mot_associe = [mot for mot, count in dictionnaire_minutes.items() if count == outlier]

# Ajouter un titre et des labels
    plt.title('Diagramme moustache des occurrences des temps de cuisson')
    plt.ylabel('Nombre d\'occurrences')

# Afficher le diagramme
    plt.show()



############### Fonction qui filtre le dictionnaire pour enlever les valeurs extrêmes #######################################
def filtre_minutes(dictionnaire_minutes) :
    #On enlève au dessus de  1000 min on garde toutes les recettes de moins de 24h (mijotage) et = à 0 min 
    l = [] #liste des ids à enlever 
    for i in dictionnaire_minutes.keys() :
        if dictionnaire_minutes[i] > 1000 :
            l.append(i)
        if dictionnaire_minutes[i] == 0 : #On supprime aussi les valeurs à 0 min
            l.append(i)

    for i in l :
        del dictionnaire_minutes[i]

    return dictionnaire_minutes


################## Fonction pour créer le camembert interactif, avec le curseur ####################################################
def generate_cursor_dataframe(df) :
    df_pivot = pd.DataFrame({
        'intervalle': [i for i in range(182)],
        'Spring': [0 for i in range(182)],
        'Winter': [0 for i in range(182)],
        'Summer': [0 for i in range(182)],
        'Fall': [0 for i in range(182)],
    }) #On initialise avec des valeurs aléatoires 

    Liste_saisons = ['Spring','Winter','Summer','Fall']
    liste_cook_times = [i for i in range(1,182)] #Un peu mal dit mais bon 

    #Maintenant l'étape difficile

    for i in Liste_saisons :
        for j in range(len(liste_cook_times)) :
            if(j==0) :
                count = df[(df['season'] == i) & (df['minutes'] <= liste_cook_times[j])]
            elif j < len(liste_cook_times)-1:
                count = df[(df['season'] == i) & (liste_cook_times[j-1]<= df['minutes'] ) & (df['minutes'] <= liste_cook_times[j])]
            else : 
                count = df[(df['season'] == i) & (df['minutes'] >= liste_cook_times[-1] )]
                print(f"[DEBUG] Saison: {i}, Intervalle: >= {liste_cook_times[-1]}, Lignes trouvées: {count.shape[0]}")

            df_pivot.loc[df_pivot['intervalle'] == liste_cook_times[j], i] = count.shape[0]


    #Pourcentages 

    # Pour chaque saison, calcule le pourcentage des recettes dans chaque intervalle
    for saison in ['Spring', 'Winter', 'Summer', 'Fall']:
        # Ajoute une nouvelle colonne pour les pourcentages
        df_pivot[f'{saison}_%'] = (df_pivot[saison] / df_pivot[['Spring', 'Winter', 'Summer', 'Fall']].sum(axis=1)) * 100

    df_pivot['nb_recettes_total'] = (df_pivot['Summer']+df_pivot['Winter']+df_pivot['Spring']+df_pivot['Fall'])
    # Affiche le résultat
    return df_pivot





#################### Fonction pour envoyer le dataframe réduit, utilisé pour le camembert interactif, vers un .pkl ################################
def df_to_pickle(df_pivot,path_pickle) :
    df_pivot = df_pivot.fillna(0)
    df_pivot.to_pickle(path_pickle)
    return 1 



################### Fonction pour les camemberts significatifs #######################################

def generate_camemberts_significatifs(df,path) : #Mettre le df et le path de sortie du .pkl
    df_significatif = pd.DataFrame({
        'intervalle': [10,30,60,120,121],
        'Printemps': [0 for i in range(5)],
        'Hiver': [0 for i in range(5)],
        'Ete': [0 for i in range(5)],
        'Automne': [0 for i in range(5)],
    }) #On initialise 

    Liste_saisons = ['Hiver','Ete','Automne','Printemps']
    liste_cook_times = [10,30,60,120,121] #Un peu mal dit mais bon 

    #Maintenant l'étape difficile

    for i in Liste_saisons :
        for j in range(5) :
            if(j==0) :
                count = df[(df['saison'] == i) & (df['minutes'] <= 10)]
            elif j < 4:
                count = df[(df['saison'] == i) & (liste_cook_times[j-1] < df['minutes'] ) & (df['minutes'] <= liste_cook_times[j])]
            else : 
                count = df[(df['saison'] == i) & (df['minutes'] > liste_cook_times[-1] )]
                print(f"[DEBUG] Saison: {i}, Intervalle: >= {liste_cook_times[-1]}, Lignes trouvées: {count.shape[0]}")

            df_significatif.loc[df_significatif['intervalle'] == liste_cook_times[j], i] = count.shape[0]



    print(df_significatif)

    #Pourcentages 

    # Pour chaque saison, calcule le pourcentage des recettes dans chaque intervalle
    for saison in ['Printemps', 'Hiver', 'Ete', 'Automne']:
        # Ajoute une nouvelle colonne pour les pourcentages
        df_significatif[f'{saison}_%'] = (df_significatif[saison] / df_significatif[['Printemps', 'Hiver', 'Ete', 'Automne']].sum(axis=1)) * 100

    # Affiche le résultat
    print(df_significatif)

    intervalle_mapping = {
        10: "10",
        30: "30",
        60: "1h",
        120: "2h",
        121: "+"
    }

    df_significatif['intervalle'] = df_significatif['intervalle'].replace(intervalle_mapping)

    # Affichage du DataFrame
    print(df_significatif)

    df_significatif = df_significatif.fillna(0)

    df_significatif.to_pickle(path)