import pandas as pd
import ast
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

interactions = pd.read_csv('data/RAW_interactions.csv')
raw_recipes = pd.read_csv('data/RAW_recipes.csv')

print(interactions)