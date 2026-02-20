import pandas as pd
from utils.load import save_to_csv

def test_save_csv_creates_file(tmp_path):
    df=pd.DataFrame({"A":[1]})
    save_to_csv(df)