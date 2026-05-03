import streamlit as st
import sys
import os
from services.db import init

# =========================
# INIT
# =========================
init()

st.set_page_config(
    page_title="Auction WorkSpace",
    layout="wide"
)

# =========================
# HARD REMOVE SIDEBAR (IMPORTANT PART)
# =========================
st.markdown("""
    <style>
        /* Kill entire sidebar container */
        [data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        section[data-testid="stSidebar"] {
            display: none !important;
            width: 0px !important;
        }

        /* Remove collapse button / spacer */
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Expand main content fully */
        .block-container {
            padding-top: 1rem;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# PATH FIX
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =========================
# IMPORT PAGES
# =========================
from pages.dashboard import render as dashboard
from pages.upload import render as upload
from pages.approval import render as approval
from pages.search import render as search
from pages.admin import render as admin
from pages.transformer import render as transformer

# =========================
# TITLE
# =========================
st.title("🏡 Auction WorkSpace")

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"   # ✅ NOT pages.dashboard

pages = {
    "Dashboard": dashboard,
    "Upload": upload,
    "Approval": approval,
    "Search": search,
    "Admin": admin,
    "Transformer": transformer
}
# =========================
# TOP NAV ONLY (YOUR UI)
# =========================
cols = st.columns(len(pages))

for i, (name, func) in enumerate(pages.items()):
    with cols[i]:
        if st.button(name, use_container_width=True):
            st.session_state.page = name

st.divider()

# =========================
# RENDER PAGE
# =========================
pages[st.session_state.page]()