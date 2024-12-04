import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import cursor as cr
from add_minutes_to_df import add_minutes

df = pd.read_pickle("../../data/archive/recipe_filtered.pkl")
df.to_csv("../../data/archive/recipe_filtered.csv", index=False)

add_minutes()

vector,vector_id,df = cr.extraction_csv("../../data/archive/table_cursor.csv")

dictionnaire_minutes = cr.dictionnaire_minutes(vector,vector_id)

dictionnaire_minutes = cr.filtre_minutes(dictionnaire_minutes)

df_pivot = cr.generate_cursor_dataframe(df)

cr.df_to_pickle(df_pivot,"webapp_assets/cursor2.pkl")

cr.generate_camemberts_significatifs(df,"webapp_assets/cursor_significatif.pkl") 