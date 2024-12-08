import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from datetime import datetime, date 
import matplotlib.dates as mdates
import pickle
import src.cursor as cr
import pytest
import os

"""
def test_extraction_csv() :

    tst_df = pd.DataFrame({
        'submitted': [10 for i in range(182)],
        'id': [i for i in range(182)],
        'minutes': [i**2 for i in range(182)],
    })

    tst_df['submitted'] = pd.to_datetime(tst_df['submitted'], errors='coerce')

    tst_df.to_csv('csv_test',index=False)

    vector,vector_id,df = cr.extraction_csv('csv_test')

    assert np.array_equal(vector, np.array([i**2 for i in range(182)])), "Test échoué pour vector"
    assert np.array_equal(vector_id, np.array([i for i in range(182)])), "Test échoué pour vector_id"

    try:
        pd.testing.assert_frame_equal(df, tst_df)
        print("Test réussi pour DataFrame")
    except AssertionError as e:
        print(f"Test échoué pour DataFrame : {e}")

    os.remove("csv_test")


    return 1

"""

def test_dictionnaire_minutes() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])}
    vector_id = l[:,0]
    vector = l[:,1]
    dictionnaire_obtenu = cr.dictionnaire_minutes(vector,vector_id)
    assert dictionnaire_verif == dictionnaire_obtenu, "Les deux dictionnaires sont différents"




def test_top_liste() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    top = cr.top_liste(dictionnaire_verif)
    l_test = [(i,i**2) for i in range(100)]
    l_test = l_test[::-1]
    assert top == l_test , "la liste obtenu est incorrecte "



def test_boxplot() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire_verif = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    cr.boxplot(dictionnaire_verif)



def test_filtre_minutes() :
    l = np.array([[i,i**2] for i in range(100)])
    dictionnaire = {i : j for i,j in zip(l[:,0],l[:,1])} #On réutilise des mêmes dictionnaires car on les connait mieux 
    dictionnaire = cr.filtre_minutes(dictionnaire)
    l_verif = np.array([[i,i**2] for i in range(1,32)]) #Jusqu'à 31, x**2 ne dépasse pas 1000
    dictionnaire_verif = {i : j for i,j in zip(l_verif[:,0],l_verif[:,1])}

    assert dictionnaire == dictionnaire_verif, "les deux dictionnaires sont différents"


def test_generate_cursor_dataframe() :
        #TODO
    return 1


def test_df_to_pickle() :
    #TODO
    return 1


def test_generate_camemberts_significatifs() :
    #TODO
    return 1 

def test_top_by_interval_season() :
    #TODO
    return 1 


def test_ids_to_name() :
    #TODO
    return 1

def test_get_name_top_by_interval_season() :
    #TODO
    return 1


