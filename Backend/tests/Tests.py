
import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

df = pd.read_csv("data/PP_recipes.csv")

recipe_name = pd.read_pickle("data/archive/ingr_map.pkl")

#print(df.columns)

#print(max(recipe_name[recipe_name.columns[-1]]))

x = list(range(1,8023))


dictionnaire = {}
for i in range(len(df[df.columns[-1]])) :
    l = df[df.columns[-1]][i]
    l = l.strip('[]').replace(' ','')
    l_string = l.split(',')
    l_valeurs = [int(l_string[k]) for k in range(len(l_string))]
    for j in range(len(l_valeurs)) :
        if (l_valeurs[j] in dictionnaire) :
            dictionnaire[l_valeurs[j]] += 1 
        else :
            dictionnaire[l_valeurs[j]] = 1





ids_manquants = []

for i in range(1,8023) :
    if i not in dictionnaire.keys() :
        ids_manquants.append(i)

for i in range(len(ids_manquants)) :
    dictionnaire[ids_manquants[i]] = 0

y = [dictionnaire[k] for k in range(1,8023)]


#plt.figure(figsize=(15, 6))
#plt.hist(y, bins=100, color='blue', alpha=0.7, edgecolor='black')  # Ajuste 'bins' pour contrôler le niveau de détail
#plt.xlim(1,8023)
#plt.xlabel('ID de l\'ingrédient')
#plt.ylabel('Nombre d\'apparitions')
#plt.title('Nombre d\'apparitions de chaque ID d\'ingrédient')
#plt.show()

x = np.array(x)
y = np.array(y)

x_smooth = np.linspace(x.min(), x.max(), 2000)  # Augmente le nombre de points pour lisser la courbe
y_smooth = make_interp_spline(x, y)(x_smooth)
y_smooth = np.maximum(y_smooth, 0)  # Remplace toutes les valeurs négatives par 0

plt.figure(figsize=(15, 6))
plt.plot(x_smooth, y_smooth, color='blue', linewidth=2)  # Tracer la courbe lissée

plt.xlim(1, 8023)

plt.xlabel('ID de l\'ingrédient')
plt.ylabel('Nombre d\'apparitions')
plt.title('Spectre lissé du nombre d\'apparitions des IDs')
plt.show()


print(max(dictionnaire, key =dictionnaire.get))

derniere_ligne = recipe_name[recipe_name[recipe_name.columns[-1]] == 6270]

print(derniere_ligne.iloc[:,5])
