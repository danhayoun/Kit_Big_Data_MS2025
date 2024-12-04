import pandas as pd


def add_minutes() :
    # Chemins des fichiers
    file_path_first = "../../data/archive/recipe_filtered.csv"
    file_path_second = "../../data/archive/RAW_recipes.csv"
    output_path = "../../data/archive/cursor_table.csv"

    # Charger les deux fichiers CSV
    df_first = pd.read_csv(file_path_first)
    df_second = pd.read_csv(file_path_second)

    # Fusionner les deux DataFrames sur la colonne 'id'
    df_merged = df_first.merge(df_second[['id', 'minutes']], on='id', how='left')

    # Sauvegarder le fichier modifié avec la nouvelle colonne "minutes"
    df_merged.to_csv(output_path, index=False)

    print(f"Le fichier modifié a été sauvegardé à : {output_path}")