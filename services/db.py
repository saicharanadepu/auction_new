
import sqlite3, json
from datetime import datetime

conn = sqlite3.connect("auction.db", check_same_thread=False)
cur = conn.cursor()

def init():
    cur.execute('''CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        batch_id TEXT,
        created_at TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS staging(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        batch_id TEXT,
        created_at TEXT
    )''')
    conn.commit()

def insert(table, df, batch_id):
    rows = [(json.dumps(r.to_dict()), batch_id, str(datetime.now())) for _, r in df.iterrows()]
    cur.executemany(f"INSERT INTO {table}(data,batch_id,created_at) VALUES(?,?,?)", rows)
    conn.commit()

def load(table):
    import pandas as pd
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    if df.empty: return df
    data = df["data"].apply(json.loads)
    out = pd.json_normalize(data)
    out["ID"] = df["id"]
    out["BATCH_ID"] = df["batch_id"]
    out["CREATED_AT"] = df["created_at"]
    return out

def clear(table):
    cur.execute(f"DELETE FROM {table}")
    conn.commit()

def delete_batch(batch):
    cur.execute("DELETE FROM records WHERE batch_id=?", (batch,))
    conn.commit()
