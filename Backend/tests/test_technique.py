import pytest
import pandas as pd
from Backend.technique import CorrelationAnalyzer

@pytest.fixture
def sample_data():
    """
    Create a sample DataFrame to use as test data
    """
    techniques_list = ['bake', 'boil', 'fry']
    df = pd.DataFrame({
        'techniques': [['bake', 'boil'], ['fry'], [], ['bake', 'fry']],
        'season': ['Spring', 'Summer', 'Fall', 'Winter']
    })
    return techniques_list, df

def test_analyze_correlation(sample_data):
    """
    Test the correlation analysis with a valid DataFrame.
    """
    techniques_list, df = sample_data
    analyzer = CorrelationAnalyzer(techniques_list)
    result = analyzer.analyze_correlation(df)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 4)  # 3 techniques x 4 seasons

def test_handle_nan_techniques(sample_data):
    """
    Test the handling of NaN values in the 'techniques' column.
    """
    techniques_list, df = sample_data
    df.loc[2, 'techniques'] = None
    analyzer = CorrelationAnalyzer(techniques_list)
    result = analyzer.analyze_correlation(df)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 4)

def test_dummy_variables_creation(sample_data):
    """
    Test the creation of dummy variables for techniques and seasons.
    """
    techniques_list, df = sample_data
    analyzer = CorrelationAnalyzer(techniques_list)
    result = analyzer.analyze_correlation(df)
    assert 'bake' in result.index
    assert 'boil' in result.index
    assert 'fry' in result.index
    assert 'Spring' in result.columns
    assert 'Summer' in result.columns
    assert 'Fall' in result.columns
    assert 'Winter' in result.columns

'''
def test_correlation_matrix_computation(sample_data):
    """
    Test the computation of the correlation matrix.
    """
    techniques_list, df = sample_data
    analyzer = CorrelationAnalyzer(techniques_list)
    result = analyzer.analyze_correlation(df)
    assert result.loc['bake', 'Spring'] == 1.0
    assert result.loc['boil', 'Spring'] == 1.0
    assert result.loc['fry', 'Summer'] == 1.0
    assert result.loc['bake', 'Winter'] == 1.0
    assert result.loc['fry', 'Winter'] == 1.0
'''