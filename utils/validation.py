
# def is_valid(row):
#     cols = ["DRIVE_BY","COMP","BID","TAX"]
#     return sum(1 for c in cols if str(row.get(c,"")).strip()) >= 2

# def make_key(df):
#     cols = [c for c in ["ADDRESS","CITY","ZIP"] if c in df.columns]
#     return df[cols].astype(str).agg("|".join, axis=1)
import pandas as pd


# =========================
# VALIDATION LOGIC
# =========================
def is_valid(row):

    required_cols = [
        "ADDRESS",
        "ZIP",
        "YEAR",
        "VOLUME",
        "PAGE"
    ]

    for c in required_cols:

        if c not in row.index:
            return False

        val = str(row[c]).strip()

        if val == "" or val.lower() == "nan":
            return False

    return True


# =========================
# DUPLICATE KEY LOGIC
# =========================
# def make_key(df):

#     cols = [
#         "ADDRESS",
#         "ZIP",
#         "YEAR",
#         "VOLUME",
#         "PAGE"
#     ]

#     # Create missing columns safely
#     for c in cols:

#         if c not in df.columns:
#             df[c] = ""

#     return (
#         df["ADDRESS"]
#         .astype(str)
#         .str.strip()
#         .str.upper()

#         + "|"

#         + df["ZIP"]
#         .astype(str)
#         .str.strip()

#         + "|"

#         + df["YEAR"]
#         .astype(str)
#         .str.strip()

#         + "|"

#         + df["VOLUME"]
#         .astype(str)
#         .str.strip()

#         + "|"

#         + df["PAGE"]
#         .astype(str)
#         .str.strip()
#     )

def make_key(df):

    def find_col(possible_names):

        for col in df.columns:

            col_upper = str(col).upper().replace(" ", "_")

            for p in possible_names:

                if p in col_upper:
                    return col

        return None

    address_col = find_col(["ADDRESS"])
    zip_col = find_col(["ZIP"])
    year_col = find_col(["YEAR"])
    volume_col = find_col(["VOLUME"])
    page_col = find_col(["PAGE"])

    return (
        df[address_col].astype(str).str.strip().str.upper()
        + "|"
        + df[zip_col].astype(str).str.strip()
        + "|"
        + df[year_col].astype(str).str.strip()
        + "|"
        + df[volume_col].astype(str).str.strip()
        + "|"
        + df[page_col].astype(str).str.strip()
    )
