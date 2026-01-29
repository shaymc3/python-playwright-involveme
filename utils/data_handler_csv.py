import pandas as pd
import os


class DataReader:
    def __init__(self, file):
        file_name = "data/" + file + ".csv"
        print(file_name)
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"CSV file not found: {file_name}")
        self.df = pd.read_csv(file_name)

    def get_data(self):
        return self.df.to_dict(orient="records")