import pandas as pd
import pytest
import os
from utils.file_manager import DataHandler

# Créez des données de test pour les tests unitaires
TEST_CSV_FILE = "test_data.csv"
TEST_PICKLE_FILE = "test_data.pkl"

# Créez des données de test pour les tests unitaires
df_test = pd.DataFrame({
    'techniques': [['bake', 'boil'], ['fry'], [], ['bake', 'fry']],
    'season': ['Spring', 'Summer', 'Fall', 'Winter']
})

# DataLoader Test
@pytest.fixture(scope="module", autouse=True)
#pour être exécutée automatiquement une fois par module de test
def setup_test_files():
    """
    Create a csv and a pickle to test the function in DataLoader
    """
    # Créez un fichier CSV de test
    df_test.to_csv(TEST_CSV_FILE, index=False)
    # Créez un fichier pickle de test
    df_test.to_pickle(TEST_PICKLE_FILE)
    yield
    # Supprimez les fichiers de test après les tests
    os.remove(TEST_CSV_FILE)
    os.remove(TEST_PICKLE_FILE)

def test_load_csv():
    """
    Test de la méthode load_csv
    """
    df = DataHandler.load_csv(TEST_CSV_FILE)
    DataHandler.converting_list_column(df,['techniques'])
    pd.testing.assert_frame_equal(df, df_test)

def test_load_pickle():
    """
    Test de la méthode load_pickle
    """
    df = DataHandler.load_pickle(TEST_PICKLE_FILE)
    pd.testing.assert_frame_equal(df, df_test)
