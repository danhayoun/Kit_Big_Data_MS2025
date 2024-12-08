import pandas as pd
print("file manager", pd.__version__)
import pickle

class FileManager:
    @staticmethod
    def get_next_item(dict_data: dict[any, any], index: int = 1) -> tuple[any, any]:
        """
        Retrieves the nth item from a dictionary.
        Raises ValueError.
        """
        iterator = iter(dict_data.items())
        try:
            for i in range(1, index):
                next(iterator)
            return next(iterator)
        except StopIteration:
            raise ValueError("L'itérateur est vide ou n'a plus d'éléments.")

    @staticmethod
    def read_file(file_path: str) -> pd.DataFrame:
        """
        Reads a CSV file
        """
        return pd.read_csv(file_path)

    @staticmethod
    def read_raw_files(csv_files: list, folder_path: str) -> dict[str, pd.DataFrame]:
        """
        Reads all raw CSV files from a given folder and stores their data in a dictionary.
        """
        raw_files_data = {}
        for file_name in csv_files:
            if file_name.startswith('RAW'):
                raw_files_data[file_name] = FileManager.read_file(folder_path / file_name)
        return raw_files_data

    @staticmethod
    def save_file_as_pickle(file: any, path: str) -> None:
        """
        Saves Python object using the pickle format.
        """
        with open(path, "wb") as f:
            pickle.dump(file, f)

if __name__ == "__main__":
    print("Dani")