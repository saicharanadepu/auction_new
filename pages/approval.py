import streamlit as st
import pandas as pd
import time
from services.db import load, insert, clear
from utils.validation import is_valid, make_key


# =========================
# RESET STATE
# =========================
def reset_selection():
    st.session_state["sel_new"] = set()
    st.session_state["sel_dup"] = set()


# =========================
# TABLE COMPONENT
# =========================
def table(df, key):

    if df is None or df.empty:
        return df

    state_key = f"sel_{key}"

    if state_key not in st.session_state:
        st.session_state[state_key] = set()

    df = df.copy().reset_index(drop=True)

    # Ensure ID
    if "ID" not in df.columns:
        df["ID"] = df.index.astype(str) + f"_{key}"

    # =========================
    # COLUMN ORDER FIX
    # =========================
    priority = ["DRIVE_BY", "COMP", "BID", "TAX"]
    priority_cols = [c for c in priority if c in df.columns]
    other_cols = [c for c in df.columns if c not in priority_cols + ["ID"]]

    df = df[["ID"] + priority_cols + other_cols]

    # =========================
    # SELECT FIRST COLUMN
    # =========================
    df.insert(0, "SELECT", df["ID"].isin(st.session_state[state_key]))

    edited = st.data_editor(
        df,
        use_container_width=True,
        key=f"editor_{key}",
        hide_index=True
    )

    if "SELECT" in edited.columns:
        st.session_state[state_key] = set(
            edited.loc[edited["SELECT"] == True, "ID"]
        )

    return df


# =========================
# MAIN PAGE
# =========================
def render():

    st.subheader("✅ Approval Center")

    # =========================
    # LOAD DATA
    # =========================
    s = load("staging")
    r = load("records")

    if s is None or s.empty:
        st.warning("No staging data")
        return

    s = s.copy()
    s["KEY"] = make_key(s)

    if r is not None and not r.empty:
        r = r.copy()
        r["KEY"] = make_key(r)
        dup_keys = set(r["KEY"])
    else:
        dup_keys = set()

    s["IS_DUP"] = s["KEY"].isin(dup_keys)

    valid = s[s.apply(is_valid, axis=1)]
    new = valid[~valid["IS_DUP"]]
    dups = valid[valid["IS_DUP"]]

    # =========================
    # METRICS
    # =========================
    c1, c2, c3 = st.columns(3)

    c1.metric("Pending Records", len(valid))
    c2.metric("New Records", len(new))
    c3.metric("Duplicate Records", len(dups))

    st.divider()

    # =========================
    # NEW RECORDS
    # =========================
    st.markdown("### 🆕 New Records")

    c1, c2 = st.columns(2)

    if c1.button("Select All New"):
        st.session_state["sel_new"] = set(new["ID"]) if "ID" in new.columns else set()

    if c2.button("Clear New"):
        st.session_state["sel_new"] = set()

    table(new, "new")

    st.divider()

    # =========================
    # DUPLICATES
    # =========================
    st.markdown("### 🔁 Duplicate Records")

    c1, c2 = st.columns(2)

    if c1.button("Select All Duplicates"):
        st.session_state["sel_dup"] = set(dups["ID"]) if "ID" in dups.columns else set()

    if c2.button("Clear Duplicates"):
        st.session_state["sel_dup"] = set()

    table(dups, "dup")

    st.divider()

    # =========================
    # ACTIONS
    # =========================
    c1, c2, c3 = st.columns(3)

    sel_new_ids = st.session_state.get("sel_new", set())
    sel_dup_ids = st.session_state.get("sel_dup", set())
    selected_ids = sel_new_ids.union(sel_dup_ids)

    # =========================
    # APPROVE
    # =========================
    if c1.button("✅ Approve"):

        if not selected_ids:
            st.warning("Nothing selected")
            return

        all_data = pd.concat([new, dups], ignore_index=True)
        approved = all_data[all_data["ID"].isin(selected_ids)]

        # =========================
        # ADD BATCH ID (IMPORTANT FIX)
        # =========================
        batch_id = str(int(time.time()))
        approved["BATCH_ID"] = batch_id

        insert("records", approved, "approved")

        remaining = s[~s["ID"].isin(selected_ids)]
        clear("staging")
        insert("staging", remaining, "staging")

        reset_selection()

        st.success("Approved successfully")
        st.rerun()

    # =========================
    # REJECT
    # =========================
    if c2.button("❌ Reject"):

        if not selected_ids:
            st.warning("Nothing selected")
            return

        remaining = s[~s["ID"].isin(selected_ids)]

        clear("staging")
        insert("staging", remaining, "staging")

        reset_selection()

        st.success("Rejected successfully")
        st.rerun()

    # =========================
    # CANCEL
    # =========================
    if c3.button("↩ Cancel"):

        reset_selection()
        st.session_state["page"] = "Upload"
        st.rerun()