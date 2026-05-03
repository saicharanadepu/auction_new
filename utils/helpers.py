
def clean(df):
    df = df.copy()
    df.columns = [c.strip().upper().replace(" ","_") for c in df.columns]
    return df.fillna("")
