import streamlit as st
import pandas as pd
from services.db import load


def render():

    # =========================
    # TITLE
    # =========================
    st.markdown("### 📊 Dashboard")

    st.markdown("""
    <style>
        h1 { font-size: 40px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 14px !important; font-weight: 500 !important; }

        .block-container { padding-top: 1rem; }

        .kpi-card {
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 1px 6px rgba(0,0,0,0.12);
        }

        .kpi-title {
            font-size: 13px;
            opacity: 0.8;
            margin-bottom: 4px;
        }

        .kpi-value {
            font-size: 22px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # LOAD DATA
    # =========================
    df = load("records")

    if df is None or df.empty:
        st.warning("No records found")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
    df = df.dropna(axis=1, how="all")

    # ensure status exists
    if "status" not in df.columns:
        df["status"] = "NEW"

    df["status"] = df["status"].astype(str)

    # =========================
    # TOTAL RECORDS (GLOBAL)
    # =========================
    total_records = len(df)

    # =========================
    # LATEST BATCH LOGIC (CORRECT)
    # =========================
    if "BATCH_ID" not in df.columns:
        st.error("BATCH_ID missing. Fix insert logic in Approval page.")
        return

    df["BATCH_ID"] = df["BATCH_ID"].astype(str)

    latest_batch_id = df["BATCH_ID"].max()
    latest_df = df[df["BATCH_ID"] == latest_batch_id]

    latest_count = len(latest_df)

    # =========================
    # KPI CARDS
    # =========================
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="background:#111827;color:white;">
            <div class="kpi-title">Total Records</div>
            <div class="kpi-value">{total_records}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="background:#2563eb;color:white;">
            <div class="kpi-title">Latest Inserted Batch</div>
            <div class="kpi-value">{latest_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # TABLE VIEW
    # =========================
    drop_cols = [c for c in ["ID", "BATCH_ID", "CREATED_AT"] if c in df.columns]
    df = df.drop(columns=drop_cols, errors="ignore")

    df = df.fillna("")

    st.dataframe(df, use_container_width=True)