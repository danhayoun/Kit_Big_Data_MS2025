import pytest
import pandas as pd
import spacy

from src.technique import TechniqueProcessor, TECHNIQUES_LIST

# Créez des données de test pour les tests unitaires
techniques_list_test = ['bake', 'boil', 'fry']
df_test = pd.DataFrame({
    'techniques': [['bake', 'boil'], ['fry'], [], ['bake', 'fry']],
    'season': ['Spring', 'Summer', 'Fall', 'Winter']
})

@pytest.fixture(scope="module")
def processor():
    """Créez une instance de TechniqueProcessor pour les tests"""
    return TechniqueProcessor(TECHNIQUES_LIST)

def test_binarize_step_to_technique(processor):
    """Test de la méthode binarize_step_to_technique"""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("bake and boil")
    binary_list = processor.binarize_step_to_technique(doc)
    expected_list = [1 if technique in ['bake', 'boil'] else 0 for technique in TECHNIQUES_LIST]
    assert binary_list == expected_list

def test_get_binary_techniques_list(processor):
    """Test de la méthode get_binary_techniques_list"""
    df_test['steps']=[["bake and boil"],["bake"],[],["mix and fry"]]
    binary_techniques = processor.get_binary_techniques_list(df_test)
    assert isinstance(binary_techniques, list)
    assert all(isinstance(item, list) for item in binary_techniques)
    assert len(binary_techniques) == len(df_test)
    # Vérifiez que les listes binaires sont correctes
    for i, steps in enumerate(df_test['steps']):
        if len(steps) > 0:
            expected_list = [1 if technique in steps[0].strip() else 0 for technique in TECHNIQUES_LIST]
        else:
            expected_list = [0] * len(TECHNIQUES_LIST)
        assert binary_techniques[i] == expected_list

def test_get_binary_techniques_list_missing_column(processor):
    """Test de la méthode get_binary_techniques_list avec une colonne manquante"""
    incomplete_data = pd.DataFrame({
        'column2': ['a', 'b', 'c']
    })
    with pytest.raises(KeyError):
        processor.get_binary_techniques_list(incomplete_data)

#CorrelationAnalyzer Test
def test_analyze_correlation():
    """
    Test the correlation analysis with a valid DataFrame.
    """
    analyzer = TechniqueProcessor(techniques_list_test)
    result = analyzer.analyze_correlation(df_test)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 4)  # 3 techniques x 4 seasons

def test_handle_nan_techniques():
    """
    Test the handling of NaN values in the 'techniques' column.
    """
    df_test.loc[2, 'techniques'] = None
    analyzer = TechniqueProcessor(techniques_list_test)
    result = analyzer.analyze_correlation(df_test)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 4)

def test_dummy_variables_creation():
    """
    Test the creation of dummy variables for techniques and seasons.
    """
    analyzer = TechniqueProcessor(techniques_list_test)
    result = analyzer.analyze_correlation(df_test)
    assert 'bake' in result.index
    assert 'boil' in result.index
    assert 'fry' in result.index
    assert 'Spring' in result.columns
    assert 'Summer' in result.columns
    assert 'Fall' in result.columns
    assert 'Winter' in result.columns


def test_correlation_matrix_computation():
    """
    Test the computation of the correlation matrix.
    """
    analyzer = TechniqueProcessor(techniques_list_test)
    result = analyzer.analyze_correlation(df_test)
    assert result.loc['bake', 'Spring'] != 1.0
    assert result.loc['boil', 'Spring'] == 1.0
    assert result.loc['fry', 'Summer'] != 1.0
    assert result.loc['bake', 'Winter'] != 1.0
    assert result.loc['fry', 'Winter'] != 1.0
