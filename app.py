import streamlit as st
import pandas as pd

# ----------------------------
# 1. App configuration (minimal look)
# ----------------------------
st.set_page_config(page_title="Indicator Register Search", layout="wide")

# Custom CSS for the minimalist style
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Helvetica Neue', sans-serif;
        color: #333;
    }
    
    .css-1d391kg {  /* Customizing background of sidebar */
        background-color: #f9f9f9;
    }
    
    .sidebar .sidebar-content {
        background-color: #f4f4f4;
    }

    .css-18e3th9 {
        background-color: #f4f4f4;
    }

    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: #2196f3;
    }
    
    .stMarkdown>div {
        font-size: 18px;
        line-height: 1.5;
    }

    .stSelectbox, .stMultiselect {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 12px;
        font-size: 14px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }

    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 2. Page Title
# ----------------------------
st.title("Indicator Register Explorer")

# ----------------------------
# 3. Load data
# ----------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data("indicator_register_clean_wide.csv")

# ----------------------------
# 4. Sidebar filters (Minimalist style)
# ----------------------------
st.sidebar.header("Filters")
domain_filter = st.sidebar.multiselect(
    "Domain",
    options=sorted(df["domain"].dropna().unique()),
    key="domain_filter"
)

type_filter = st.sidebar.multiselect(
    "Type (Outcome / Process)",
    options=sorted(df["type"].dropna().unique()),
    key="type_filter"
)

tier_filter = st.sidebar.multiselect(
    "Tier(s) (select one or more)",
    options=["T1", "T2", "T3", "T4"],
    key="tier_filter"
)

role_filter = st.sidebar.multiselect(
    "Primary Role",
    options=["Rangers", "Scientists"],
    key="role_filter"
)

# Text search
query = st.sidebar.text_input("Search (text)", key="search_query")

# ----------------------------
# 5. Apply filters
# ----------------------------
filtered = df.copy()

if domain_filter:
    filtered = filtered[filtered["domain"].isin(domain_filter)]

if type_filter:
    filtered = filtered[filtered["type"].isin(type_filter)]

if tier_filter:
    for t in tier_filter:
        filtered = filtered[filtered[f"has_{t}"] == 1]

if role_filter:
    if "Rangers" in role_filter:
        filtered = filtered[filtered["role_rangers"] == True]
    if "Scientists" in role_filter:
        filtered = filtered[filtered["role_scientists"] == True]

if query:
    filtered = filtered[
        filtered.apply(
            lambda row: query.lower() in " ".join(row.astype(str).tolist()).lower(),
            axis=1,
        )
    ]

# ----------------------------
# 6. Display results with clean design
# ----------------------------
st.write(f"Showing **{len(filtered)}** results")
st.dataframe(filtered, use_container_width=True)

# ----------------------------
# 7. Export button (Sleek with rounded corners)
# ----------------------------
if len(filtered) > 0:
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data",
        data=csv,
        file_name="filtered_indicators.csv",
        key="download_button"
    )
