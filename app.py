from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

#page set up

st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

#color template

NAVY = "#172554"
BLUE = "#2563EB"
TEAL = "#0F9D8A"
GOLD = "#E9A23B"
PURPLE = "#7C3AED"
RED = "#DC2626"
GREY = "#64748B"
LIGHT_GREY = "#E2E8F0"

COLORS = [BLUE, TEAL, GOLD, PURPLE, RED, "#0891B2"]


#page outlook

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F9FC;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #172554;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #172554;
    }

    section[data-testid="stSidebar"] {
        background-color: #F0F4FA;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#data loading

DATA_FILE = (
    Path(__file__).parent
    / "travel_analysis_enriched.csv"
)


@st.cache_data
def load_data(file_path, modified_time):
    df = pd.read_csv(file_path)

    required = ["Travel_Reason", "Expenses"]

    missing = [
        column for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df["Expenses"] = pd.to_numeric(
        df["Expenses"],
        errors="coerce",
    )

    df = df.dropna(
        subset=["Expenses", "Travel_Reason"]
    ).copy()

    df = df[df["Expenses"] >= 0].copy()
    df = df.reset_index(drop=True)

    text_columns = [
        "Travel_Reason",
        "City",
        "City_Clean",
        "Destination_State",
        "Accommodation",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
            )

    if "City_Clean" in df.columns:
        df["Destination"] = df["City_Clean"]

        if "City" in df.columns:
            df["Destination"] = (
                df["Destination"].fillna(df["City"])
            )

    elif "City" in df.columns:
        df["Destination"] = df["City"]

    elif "Destination_State" in df.columns:
        df["Destination"] = df["Destination_State"]

    else:
        df["Destination"] = "Unknown"

    df["Destination"] = (
        df["Destination"]
        .fillna("Unknown")
        .astype(str)
    )

    df["Travel_Reason"] = (
        df["Travel_Reason"].astype(str)
    )

    numeric_columns = [
        "Pax",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
        "Regional_Price_Parity",
        "BEA_Reference_Year",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df


if not DATA_FILE.exists():
    st.error(
        "Dataset not found. Place "
        "'travel_analysis_enriched.csv' "
        "in the same folder as app.py."
    )

    st.code(
        "pydata_capstoneproject/\n"
        "├── app.py\n"
        "└── travel_analysis_enriched.csv"
    )

    st.stop()


try:
    df = load_data(
        str(DATA_FILE),
        DATA_FILE.stat().st_mtime,
    )
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()


if df.empty:
    st.error("No valid expenditure records were found.")
    st.stop()



## Helpers


def money(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def p_value(value):
    if pd.isna(value):
        return "N/A"

    if value < 0.001:
        return f"{value:.3e}"

    return f"{value:.4f}"


def style_chart(fig, height=430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=65, b=35),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color=NAVY,
        ),
        title_font=dict(
            size=17,
            color=NAVY,
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_color="white",
            font_size=12,
        ),
        legend_title_text="",
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor=LIGHT_GREY,
        zeroline=False,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF1F7",
        zeroline=False,
    )

    return fig


def money_axis(fig, axis="y"):
    if axis == "y":
        fig.update_yaxes(
            tickprefix="$",
            tickformat=",.0f",
        )
    else:
        fig.update_xaxes(
            tickprefix="$",
            tickformat=",.0f",
        )

    return fig
   
