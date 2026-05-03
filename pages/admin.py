
import streamlit as st
from services.db import load, delete_batch

def render():
    st.subheader("⚙️ Admin")
    df = load("records")
    if df.empty: return
    batch = st.selectbox("Batch", df["BATCH_ID"].unique())
    if st.button("Delete"):
        delete_batch(batch)
        st.rerun()
