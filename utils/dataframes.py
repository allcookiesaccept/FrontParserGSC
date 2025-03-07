import pandas as pd
from settings import Config


class DataProcessor:
    def __init__(self):
        self.config = Config()

    def save_to_excel(self, data):
        try:
            df = pd.DataFrame(data)
            df.to_excel(self.config.OUTPUT_FILE, index=False)
            print(f"Data successfully saved to {self.config.OUTPUT_FILE}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            raise