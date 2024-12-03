import pandas as pd
import pickle

class FileManager:
    @staticmethod
    def get_next_item(dict_data, index = 1):
        iterator = iter(dict_data.items())
        for i in range(1, index):
            next(iterator)
        return next(iterator)

    @staticmethod
    def read_file(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def read_raw_files(csv_files, folder_path):
        raw_files_data = {}
        for file_name in csv_files:
            if file_name.startswith('RAW'):
                raw_files_data[file_name] = FileManager.read_file(folder_path / file_name)
        return raw_files_data

    @staticmethod
    def save_file_as_pickle(file, path):
        with open(path, "wb") as f:
            pickle.dump(file, f)
