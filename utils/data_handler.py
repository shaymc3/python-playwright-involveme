import pandas as pd


class DataReader:
    def __init__(self, file_path="data/data.xlsx"):
        self.file_path = file_path
        self.sheets = None

    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return df
        except FileNotFoundError:
            raise Exception(f"Excel file not found: {self.file_path}")
        except ValueError:
            raise Exception(f"Sheet not found: {sheet_name}")

    def get_rows_as_dicts(self, sheet_name: str):
        df = self.load_sheet(sheet_name)
        return df.to_dict(orient="records")

    def get_cell(self, sheet_name: str, row: int, column: str):
        df = self.load_sheet(sheet_name)
        return df.loc[row, column]

    def get_column(self, sheet_name: str, column_name: str):
        df = self.load_sheet(sheet_name)
        return df[column_name].tolist()
    

data = DataReader()
users = data.get_rows_as_dicts("users")

print(users)