import pandas as pd
import pickle
import logging
from typing import List, Any
import ast
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class DataHandler:
    """Class responsible for handling data like loading,converting or storing"""
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """
        Read a csv file into DataFrame
        """
        try:
            return pd.read_csv(filepath)
        except FileNotFoundError as e:
            logging.error(f"Error loading CSV file: {e}")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading CSV file: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def load_pickle(filepath: str) -> pd.DataFrame:
        try:
            with open(filepath, "rb") as f:
                df = pickle.load(f)
            return df
        except FileNotFoundError as e:
            logging.error(f"Error loading pickle file: {e}")
            st.error(f"Erreur de chargement des données : {e}")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading pickle file: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def read_raw_files(csv_files: list, folder_path: str) -> dict[str, pd.DataFrame]:
        """
        Reads all raw CSV files from a given folder and stores their data in a dictionary.
        """
        raw_files_data = {}
        for file_name in csv_files:
            if file_name.startswith('RAW'):
                try:
                    raw_files_data[file_name] = DataHandler.load_csv(f"{folder_path}/{file_name}")
                except Exception as e:
                    logging.error(f"Error reading raw file {file_name}: {e}")
        return raw_files_data

    @staticmethod
    def converting_list_column(df: pd.DataFrame,column_list_to_convert: List[str]) -> None:
        """
        Convert the csv's imported list which was transform wrongly to a string back to a python list
        """
        for col in column_list_to_convert:
            if col !='tags': # si on veut traiter la colonne tags, il faudra gérer les erreurs de frappe de l'utilisateur
                try:
                    if isinstance(df[col][0], str) and df[col][0].startswith('['):
                        df[col] = df[col].apply(ast.literal_eval)
                except Exception as e:
                    logging.error(f"Error converting column {col}: {e}")

    @staticmethod
    def load_clean_csv(csv_path: str,  column_list_to_convert = None, date = None) -> pd.DataFrame:
        """
        Load data from CSV files and convert necessary columns into python type
        """
        try :
            df = DataHandler.load_csv(csv_path)
            if column_list_to_convert:
                DataHandler.converting_list_column(df, column_list_to_convert= column_list_to_convert)
            if date and date in df.columns:
                df[date] = pd.to_datetime(df[date])
            return df
        except FileNotFoundError:
            logging.error(f"Error: The file at {csv_path} was not found.")
            return pd.DataFrame()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return pd.DataFrame()
        
    @staticmethod
    def get_next_item(dict_data: dict[any, any], index: int = 1) -> tuple[any, any]:
        """
        Retrieves the nth item from a dictionary.
        Raises ValueError.
        """
        iterator = iter(dict_data.items())
        try:
            for _ in range(1, index):
                next(iterator)
            return next(iterator)
        except StopIteration:
            logging.error(f"Error: Index {index} is out of range for the dictionary.")
            raise ValueError("L'itérateur est vide ou n'a plus d'éléments.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while retrieving the next item: {e}")
            raise

    @staticmethod
    def save_file_as_pickle(obj: any, path: str) -> None:
        """
        Saves Python object using the pickle format.
        """
        with open(path, "wb") as f:
            pickle.dump(obj, f)
    
    