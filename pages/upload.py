
import streamlit as st, pandas as pd, uuid
from services.db import insert
from utils.helpers import clean

def render():
    st.subheader("📤 Upload")
    f = st.file_uploader("Excel", type=["xlsx"])
    if f:
        df = clean(pd.read_excel(f))
        st.dataframe(df)
        if st.button("Send to Approval"):
            insert("staging", df, str(uuid.uuid4()))
            st.session_state["page"] = "Approval"
            st.rerun()
