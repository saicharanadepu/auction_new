
def is_valid(row):
    cols = ["DRIVE_BY","COMP","BID","TAX"]
    return sum(1 for c in cols if str(row.get(c,"")).strip()) >= 2

def make_key(df):
    cols = [c for c in ["ADDRESS","CITY","ZIP"] if c in df.columns]
    return df[cols].astype(str).agg("|".join, axis=1)
