import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import cursor as cr



df = pd.read_pickle("../../../data/raw/recipe_filtered.pkl")

df = cr.generate_accurate_df(df)

df = cr.add_intervalle(df) #ajout colonne intervalle

vector,vector_id = cr.get_vectors(df)

dictionnaire_minutes = cr.dictionnaire_minutes(vector,vector_id)

dictionnaire_minutes = cr.filtre_minutes(dictionnaire_minutes)

df_pivot = cr.generate_cursor_dataframe(df)

cr.df_to_pickle(df_pivot,"../webapp_assets/cursor2.pkl")

cr.generate_camemberts_significatifs(df,"../webapp_assets/cursor_significatif.pkl") 


dictionnaire_tops_10 = cr.top_by_interval_season(df)
dictionnaire_final = cr.get_name_top_by_interval_season(dictionnaire_tops_10,df)

print(dictionnaire_final)

with open("../webapp_assets/dictionnaire_tops_10.pkl", "wb") as fichier:
    pickle.dump(dictionnaire_final, fichier) #Etape OK 