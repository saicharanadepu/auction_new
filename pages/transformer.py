
import streamlit as st, pandas as pd
from utils.helpers import clean

def render():
    st.subheader("🧪 Transformer")
    f = st.file_uploader("Excel", type=["xlsx"])
    if f:
        df = clean(pd.read_excel(f))
        for c in ["DRIVE_BY","COMP","BID","TAX","STUDY"]:
            if c not in df.columns:
                df[c] = ""
        st.dataframe(df)
        st.download_button("Download CSV", df.to_csv(index=False), "output.csv")
