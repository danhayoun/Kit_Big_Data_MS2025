import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle 
from Classe_pickle import Display, DatabaseDisplay

st.title("Analyse des résultats - Mangetamain")

pickle = DatabaseDisplay('temps_de_cuisson','../Backend/src/webapp_assets/cursor2.pkl')

data_columns = ['Printemps_%', 'Hiver_%', 'Ete_%', 'Automne_%']
label_names = ['Printemps', 'Hiver', 'Été', 'Automne']


pickle.plot_interactive_pie_chart(
    data_columns=['Spring_%', 'Winter_%', 'Summer_%', 'Fall_%'],
    label_names=['Printemps', 'Hiver', 'Été', 'Automne'],
    slider_label="Sélectionnez un intervalle",
    title="Répartition des recettes par intervalle de temps"
)