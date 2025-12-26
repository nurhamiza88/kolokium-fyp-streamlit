import pandas as pd

def get_juri_from_sheet():
    CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv"
    df = pd.read_csv(CSV_URL)
    return df["NAMA JURI"].dropna().tolist()
