from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats


## Page set up

st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


## Color template

NAVY = "#450A0A"
BLUE = "#DC2626"
TEAL = "#EF4444"
GOLD = "#F87171"
PURPLE = "#B91C1C"
RED = "#991B1B"
GREY = "#7F1D1D"
LIGHT_GREY = "#FECACA"

COLORS = ["#DC2626", "#EF4444", "#F87171", "#B91C1C", "#991B1B", "#FCA5A5"]


## Page outlook

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



Here's the full corrected c    h1, h2, h3 {
ode with the indentation         color: #450A0A;
fixed in the Statistical Tests tab and the CSS updated     }

    div[data-testid="stMetric"] {
        backgrounto match your red palette:

```python
from pathlid-color: white;
        border: 1px solid #FECACA;
        paddinb import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objectg: 16px;
        border-radius: 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: s as go
import streamlit as st
from scipy import stats


## Page set up

st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
#7F1D1D;
    }

    div[data-testid="stMetricValue"] {
        color: #450A0A;
    }

    section[data-testid="stSidebar"] {
        background-color: #FEF2F2;
    }
        initial_sidebar_state="expanded",
)

# Color template

NAVY = "#450A0A"
BLUE = "#DC2626"
TEAL = "#EF4444"
GOLD = "#F87171"
PURPLE = "#B91C1C"
RED = "</style>
    """,
    unsafe_allow_html=True,
)


## Data Loading

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
        if column not in df#991B1B"
GREY = "#7F1D1D"
LIGHT_GREY = "#FECACA"

COLORS = ["#DC2626", "#EF4444", "#F87171", "#B91C1C", "#991B1B", "#FCA5A5"]

# Page outlook

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FEF2F2;
    }

    .block-container {
        padding-top: 1.5rem;
        padding.columns
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

    df =-bottom: 2rem;
    }

 df[df["Expenses"] >=    h1, h2, h3 {
 0].copy()
    df = df.res        cet_index(drop=True)

olor: #450A0A;
    text_columns = [
        "Travel_    }

    div[data-testid="stMetric"] {
        backgrounReason",
        "City",
        "City_Clean",
        "Desd-color: white;
        border: 1px solid #tination_State",
        "Accommodation",
    ]

    for column in text_FECACA;
        padding: 16px;
        border-radius: 10px;
    }

    div[data-tecolumns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .sstid="stMetricLabel"] {
        color: tr.strip()
         #7F1D1D;
    }

    div[dat       .replace("", pd.NA)
   a-testid="stMet         )

ricValue"] {
        c    if "City_Clean" in dfolor.columns:
  : #450A0A;
    }

         df["Destination"] = df section[data-te["City_Clean"]

stid="stSide        ibar"] {
        backgrounf "City" in df.d-colocolumns:
        r: #    df["DestinatiFEF2F2;
    }
    on"] = (
                df["Destination"].f</style>
    """,
    unsaillna(df["City"])
            )

fe_allow_html=True,
)


## Data Loading

D    elif "City" in df.columns:
        df["Destination"] = df["City"]

    elif "DesATA_FILE = (
    Path(__file__).parent
    / "travel_analysis_enriched.csv"
)


@st.cactination_State" in df.columns:
        df["Destination"] = df["Destination_State"]

    else:
        df["Destination"] = "he_data
def load_data(file_path, modified_time):
    df = pd.read_csv(file_path)

    required = ["Travel_Reason", "Expenses"]

    missing = [
        column for column in Unknown"

    df["Destination"] = (
        df["Destination"]
        .fillna("Unknown")
        .astype(str)
    )

    df["Travel_Reason"] = (
        df["Travel_Reason"].astype(str)
    )

required
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

    numeric_columns = [
        "Pax",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
        "Regional_Price_    df = df.dropna(
        sParity",
        "BEA_Refereubset=["Expence_Year",
nses", "Travel_Reason"]
      ]

    for column in numeric_  ).copy()

    df = df[df["Expencolumns:
        if column in df.columns:
            df[column] = pd.to_numeric(
       ses"] >= 0].copy()
    df = df.reset_index(drop=True)

    text_c         df[column],
                errors="coerce",
            )

    return df


if not DATA_FILolumns = [
        "Travel_Reason",
        "City",
        "City_Clean",
        "Destination_State",
        "Accommodation",
    ]

    foE.exists():
    st.error(
        "Dataset not found. Place "
        "'travel_analysis_enriched.csv' "
        "in the same folder as app.py."
    )

    st.code(
        "pydata_r column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
            )

    if "City_Clean" in df.columns:
        df["Destinacapstoneproject/\n"
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
    st.error(f"Unable to load thetion"] = df["City_Clean"]

        if "City" in df.columns:
            df["Destination"] = (
                df["Destination"].fillna(df["City"])
            )

    elif "City" in df.columns:
        df["Destination"] = df["City"]

    elif "Destination_State" in df.columns:
        df["Destination"] = df["Destination_State"]

    else:
        df["Desti dataset: {error}")
    st.stop()


if df.empty:
    st.error("No valid expenditure records were found.")
    st.stop()


## Helpers

def money(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def p_value(nation"] = "Unknown"

    df["Destination"] = (
        df["Destination"]
        .fillna(value):
    if pd.isna("Unknown")
 value):
        r       .astyeturn "N/A"

pe(str)
    )

    if     df[valu"Travel_Rease < 0.001:
on"] = (
            return     df["Travel_Rf"{valeason"].astyue:.3e}"

    pe(str)
    )

    numeric_colreturn f"{value:.4f}"


umns = [
  def style_ch      "Pax",
art(fig, h        eight=430):
"Per_Capita_    fig.updateIncome",
    _layout(
        te    "Per_Capita_Disposable_mplate="plotly_white",
       Income",
        " height=height,
Regional_Price_Parity",
           margin=dict     "BEA_Reference_Year",
(l=20, r=20, t    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column]=65, b=35),
        paper_bgcolor="white",
        plot_bgcolor="white",
        fon = pd.to_numeric(
                df[column],
                errors="coerce",
            )

  t=dict(
            family="Arial, sans-serif",
            size=12,
            color=NAVY,
        ),
        title_fon  return df


if not DATA_FILE.exists():
    st.error(
        "Dataset not found. Place "
        "'travel_analysis_enriched.csv' "
t=dict(
            size=17,
            color=NAVY,
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_color="white",
            font_size=12,
           "in the same folder as app.py."
    )

    st.code(
        "pydata_capstoneproject/\n"
        "├── app.py\n"
        "└── travel_analysis_enriched.csv"
    )

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
        gridcolor=    st.stop()


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
"#FECACA",
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


    st.stop()


# Helpers

def money(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def p_value(value):
    if pd.isna(value):
        return "N/A"

    if value < 0.001:
        return f"{value:.3e}"

    return f"{def cohens_d(group_a, group_b):
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)

    if value:.4f}"


def style_chlen(a) < 2 or len(b) < 2:
        return np.nan

    pooled_variance = (
 art(fig, height=430):
    fig.update_layout(
        template="plotly       (len(a) - 1) * np.var(a_white",
        height=height,
        margin=dict(l=2, ddof=1)
        + (len(b) - 1) * 0, r=20, t=65, b=35),
        paper_bgcolor="white",
np.var(b, ddof=1)
    ) / (len(a) + l        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
         en(b) - 2)

    if pooled_variance <= 0:
        return np.nan

    return (
        np.mean   size=12,
            color=NAVY,
        ),
        title_font=dict(
            size=17,
            color=NAVY,
        ),
        ho(a) - np.mean(b)
    ) / np.sqrt(pooled_variance)


def line_chart(
    data,
    x,
verlabel=dict(
            bgco    y,
    title,
lor=NAVY,
            font_color=    color,
    custom_da"white",
            fta=None,
   ont_ x_title=None,
size=12,
       y_tit     ),
        legend_tile=None,
):
tle_text="",
    fig =    )

    fi px.line(
    g.update_xaxes(
        showgr    data,
        x=x,
id=False,
             linecolor=L   y=y,
        markeIGHT_GREY,
rs=True,
        tit        zeroline=False,
    )

le=title,
        custom_data=custom_data,
    fig.update_yaxes(
        showgrid=True,
        g    )

    fig.update_traces(
        line=dict(color=color, width=3),
ridcolor="#FECACA",
        zeroline=False,
    )

    return fig


def money_axis(fig, axis="y"):
    if axis == "y":
        fig.update        marker=dict(
            size=9,
            color=color,
            line=dict(color="white", width=1.5),
        ),
        hovertemplate=(
       _yaxes(
            tickprefix="$",
            tickformat=",.0f",
        )
    else:
        fig.update_xaxes(
            tickprefix="$",
            tickfo     "<b>%{x}</b><br>"
            "Average expenditure: $%{y:,.2f}"
            "<extra></extra>"
        ),
    )

    firmat=",.0f",
        )

    return fig


def cohens_d(group_a, group_b):
    a = np.asarray(group_a, dtype=float)
g.update_layout(
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
    )

    return money_axis(style_chart(fig))


## Header

st.title("✈️ Travel Spend Analytics")

st.    b = np.asarray(group_b, dtype=float)

    if len(a) < 2 or len(b) < 2:
        return np.nan

    pooled_variance = (
        (len(a) - 1) * np.var(a, ddof=1)
        + (lenmarkdown(
    """
    An interactive exploration of travel expenditure,
    travel purpose, destinations, party size, and
    destination-level economic indicators.
    """
)

st.caption(
    "Exploratory data analysis | "
    "Interactive charts | Statistical comparisons"
)


## Sidebar filters

st.sidebar.title("Dashboard Filters")
st.sidebar.capt(b) - 1) * np.var(b, ddof=1)
    ) / (len(a) + len(b) - 2)

    if pooled_variance <= 0:
        return np.nan

    return (
        np.mean(a) - np.mean(b)
    ) / np.sqrt(pooled_variance)


def line_chart(
    data,
    x,
    y,
ion("Use the filters to explore the records.")

reasons = sorted(
    df["Travel_Reason"].dropna().unique().tolist()
)

selected_reasons = st.sidebar.multiselect(
    "Travel purpose",
    reasons,
    default=reasons,
)

destinations = sorted(
    df["Destination"].dropna().unique().tolist()
)

selected_destinations = st.sidebar.multiselect(
    "Destination",
    destinations,
    defa    title,
    color,
    custom_data=None,
    x_title=None,
    y_title=None,
):
    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        title=title,
        custom_data=custom_data,
    )

    fig.update_traces(
        line=dict(color=color, width=3),
        marker=dict(
            size=9,
            color=color,
            line=dict(color="white", width=1.5),
   ult=destinations,
)

min_expense = float(df["Expenses"].min())
max_expense = float(df["Expenses"].max())

if min_expense < max_expense:
    expense_range = st.sidebar.slider(
        "Expenditure range ($)",
        min_value=min_expense,
        max_value=max_expense,
        value=(min_expense, max_expense),
        format="$%.2f",
    )
else:
    expense_range = (min_expense, max_expense)

st.sidebar.divider()

st.sidebar.caption(
     ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average expenditure: $%{y:,.2f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title=x_title or x,
        yaxis_title=y_title or y,
    )

    return money_axis(style_chart(fig))


## Header

st.title("✈️ Travel Spend Analytics")

st.markdown(
    """
    An interactive exploration of travel expenditure,
    travel purpose, destinations, party size, and
    destination-level economic indicators.
    """
)

st.caption(
    "Exploratory data     "All charts and statistical tests update "
    "when you change the filters."
)


## Record filters

filtered_df = df[
    df["Travel_Reason"].isin(selected_reasons)
    & df["Destination"].isin(selected_destinations)
    & df["Expenses"].between(
        expense_range[0],
        expense_range[1],
        inclusive="both",
    )
].copy()

if filtered_df.empty:
    st.warning(
        "No records match these filters. "
        "Adjust your selections in the sidebar."
    )
    st.stop()


## KPIs

st.subheader("Key indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Travel records",
    f"{len(filteranalysis | "
    "Interactive charts | Statistical comparisons"
)


# Sidebar filter

st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Use the filters to explore the records.")

reasons = sorted(
    df["Travel_Reason"].dropna().unique().tolist()
)

selected_reasons = st.sidebar.multiselect(
    "Travel purpose",
    reasons,
    default=reasons,
)

destinations = sorted(
    df["Destination"].dropna().unique().tolist()
)

selected_destinations = st.sidebar.multiselect(
    "Destination",
    destinations,
    default=destinations,
)

min_expense = float(df["Expenses"].min())
max_expense = float(df["Expenses"].max())

if min_expense < max_expense:
    expense_range = st.sidebar.slider(
        "Expenditure range ($)",
        min_value=min_expense,
        max_value=max_expense,
        value=ed_df):,}",
)

k2.metric(
    "Average expenditure",
    money(filtered_df["Expenses"].mean()),
)

k3.metric(
    "Median expenditure",
    money(filtered_df["Expenses"].median()),
)

k4.metric(
    "Total recorded expenditure",
    money(filtered_df["Expenses"].sum()),
)

st.caption(
    "Currency is displayed as dollars; confirm the source "
    "dataset's currency definition before publishing results."
)

st.divider()


## Tabs

overview, composition, patterns, statistics_tab, economic, explore = (
    st.tabs(
        [
            "Overview",
            "Spending Composition",
            "Spending Patterns",
            "Statistical Tests",
            "Economic Context",
            "Explore Data",
        ]
    )
)


## Overview

with overview:

    st.subheader("Average expenditure by travel purpose")

    purpose_summary = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Average_Expenses=("Expenses", "mean"),
            Median_Expenses=("Expenses", "median"),
            Records=("(min_expense, max_expense),
        format="$%.2f",
    )
else:
    expense_range = (min_expense, max_expense)

st.sidebar.divider()

st.sidebar.caption(
    "All charts and statistical tests update "
    "when you change the filters."
)


## Record filters

filtered_df = df[
    df["Travel_Reason"].isin(selected_reasons)
    & df["Destination"].isin(selected_destinations)
    & df["Expenses"].between(
        expense_range[0],
        expense_range[1],
        inclusive="both",
    )
].copy()

if filtered_df.empty:
    st.warning(
        "No records match these filters. "
        "Adjust your selections in the sidebar."
    )
    st.stop()

## KPIs

st.subheader("Key indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Travel records",
    f"{len(filtered_df):,}",
)

k2.metric(
    "Average expenditure",
    money(filtered_df["Expenses"].mean()),
)

k3.metric(
    "Median expenditure",
    money(filtered_df["Expenses"].median()),
)

k4.metric(
    "Total recorded expenditure",
    money(filtered_df["Expenses"].sum()),
)

st.caption(
    "Currency is displayed as dollars; confirm the source "
    "dExpenses", "size"),
        )
        .sort_values("Average_Expenses")
    )

    fig = px.line(
        purpose_summary,
        x="Travel_Reason",
        y="Average_Expenses",
        markers=True,
        custom_data=[
            "Median_Expenses",
            "Records",
        ],
        title="Average Expenditure by Travel Purpose",
        color_discrete_sequence=[BLUE],
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=11, color=TEAL),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Mean: $%{y:,.2f}<br>"
            "Median: $%{customdata[0]:,.2f}<br>"
            "Records: %{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="Travel purpose",
        yaxis_title="Average expenditure ($)",
    )

    st.plotly_chart(
        money_axis(style_chart(fig)),
        use_container_width=True,
    )

    st.caption(
        "The connecting line compares categories; it does "
        "not represent a change over time."
    )

 ataset's currency definition before publishing results."
)

st.divider()

# Tabs

overview, composition, patterns, statistics_tab, economic, explore = (
    st.tabs(
        [
            "Overview",
            "Spending Composition",
            "Spending Patterns",
            "Statistical Tests",
            "Economic Context",
            "Explore Data",
        ]
    )
)


## Overview

with overview:

    st.subheader("Average expenditure by travel purpose")

    purpose_summary = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Average_Expenses=("Expenses", "mean"),
            Median_Expenses=("Expenses", "median"),
            Records=("Expenses",    left, right = st.columns(2)

    with left:

        st.subheader("Destination rankings")

        destination_summary = (
            filtered_df.groupby(
                "Destination",
                as_index=False,
            )
            .agg(
                Average_Expenses=("Expenses", "mean"),
               "size"),
        )
        .sort_values("Ave Records=("Expenses", "rage_Expenses")
size"),
            )
        )

          )

    fig = px.line(
        purpose_summary,
   common_destinations = (
            filtered_df["Destination"]
            .value_counts()
            x="Travel_Reason",
        y="Average_Expenses",
        marker       .head(15)
            .index
        )

        ranking = destination_ss=True,
        custom_data=[
            "Median_Expenses",
            "Records",
        ],
        title="Average Expummary[
            destination_summary["Destination"].isin(
                common_destinations
            )
        ].sort_values("Average_Expenses")

        enditure by Travel Purpose",
        color_discrete_sequence=[BLUE],
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dfig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=ranking["Average_Expenses"],
                y=ranking["Destination"],
                mode="lines",
                lict(size=11, color=TEAL),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Mean: $%{y:,.2f}<br>"
            "Median: $%{cuine=dict(color=LIGHT_GREY, width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=ranking["Average_Expstomdata[0]:,.2f}<br>"
            "Records: %{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="Travel purpose",
     enses"],
                y=ranking["Destination"],
                mode="markers",
                marker=dict(
                    size=12,
                    color=TEAL,
                    line=dict(color="white", width=2),
                ),
                customdata=ranking[["Records"]].to_numpy(),
          yaxis_title="Average expenditure ($)",
    )

    st.plotly_chart(
        money_axis(style_chart(fig)),
        use_container_width=True,
    )

    st.caption(
        "The connecting line compares categories; it does "
        "not represent a change over time."
         text=ranking["Average_Expenses"].apply(money),
                textposition="top center",
                textfont=dict(size=10, color=NAVY),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Average: $%{x:,.2f}<br>"
                 )

    left, right = st.columns(2)

    with left:

        st.subheader("Destination rankings")

        destination_summary = (
            filtered_df.groupby(
                "Destination",
              "Records: %{custom         as_index=False,
      data[0]:,.0f}"
                         )
            .agg(
                 "<extra></extra>"
                ),
       Average_Expenses=("Expenses         showlegend=False,
      ", "mean"),
                Records=("Ex      )
        )

        fig.updatepenses", "size"),
            )
        )

        common_destinat_layout(
            title="Average Spending by Destination (Lollipop)",
            xaxis_title="Average expenditure ($)",
            yaxis_tiions = (
            filtered_df["Destination"]
            .value_counts()
            .head(15)
            .index
        )

        rtle=None,
        )

        fig = style_chanking = destination_summary[
            destination_summary["Destination"].isin(
                common_destinations
            )
        ].sort_values("Average_Expenses")

art(fig, 500)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(
            fig,
            use_container_width=True,
           fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=ranking["Average_Expenses"],
                y=ranking["Destination"],
                mode=     )

    with right:

        st.subheader("Travel-purpose record counts")

        reason_counts = (
            filtered_df["Travel_Reason"]
            .value_counts()
     "lines",
                line=dict(color=L       .rename_axis("Travel_RIGHT_GREYeason")
            .res, width=2),
       et_index(name="R         hoverinecords")
        )

fo="skip",
                showlegend        fig = px.bar(
            reason_=False,
            )
        )

        fig.addcounts,
            x="Travel_Reason",
            y="Records",
            color="Trave_trace(
            go.Scatter(
                x=ranking["Average_Expenses"],
                y=ranking["Destinl_Reason",
            color_discrete_sequence=COLORS,
            title="Number of Records by Travel Purpose",
ation"],
                mode="markers",
                marker=dict(
                    size=12,
                    color=TEAL,
                        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
             line=dict(color="white", width=2),
                ),
                customdata=ranking[["Records"]].to_numpy(),
                text=ranking["Average_       "Records: %{y:,.0f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            showlegend=False,
            xaxisExpenses"].apply(money),
                textposition="top center",
                textfont=dict(size=10, color=NAVY),
                hovertemplate=(
                   _title="Travel purpose",
            yaxis_title="Number of records",
        )

        fig = style_chart(fig)
        fig.update_yaxes(tickformat=",")

        st.plotly_chart(
    "<b>%{y}</b><br>"
                    "Average: $%{x:,.2f}<br>"
                    "Records: %{customdata[0]:,.0f}"
                    "<extra></extra>"
                ),
                showlegend=False,
               fig,
            use_container_width=True,
        )

    ## Map

    st.divider()
    st.subheader("Geographic distribution of spending")

    if "Des      )
        )

        fig.update_layout(
           tination_State" in filtered_df.c title="Average Spending by Destination (Lololumns:
        state_agg = (
            lipop)",
            xaxis_title="Average expenditure ($)",
   filtered_df.groupby("Destination_State", as_index=False)
                   yaxis_title=None,
        )

        fig = style_ch  .agg(
                Total_Expenses=("Expenses", "sum"),
                Average_Expensart(fig, 500)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

es=("Expenses", "mean"),
                Records=("Expenses", "size"),
            )
        )

        fig =        st.plotly_chart(
            fig,
            use_container_wi px.chordth=True,
 opleth(
            st       )

    wiate_agg,
            locth right:

  ations="Destination_      st.subheaderState",
            locati("Travel-purpose record onmode="USA-scounts")

        reasotates",
            color=n_counts = (
   "Average_Ex         filtered_df["Travel_Rpenses",
            hover_data={
                "Total_eason"]
            .value_counts()
            .rename_axisExpenses": True,
                "Records": True,
                "Destination("Travel_Reason")
            .reset_index(name="Records")
        )

        _State": False,
            },
            color_continuous_scale="Reds",
            scopfig = px.bar(
            reason_counts,
            x="Travel_Reason",
            y=e="usa",
            title="Average Expenditure by State",
            labels={
                ""Records",
            color="Travel_Reason",
            color_discrete_sequence=COLORS,
            titleAverage_Expenses": "Avg expenditure ($)",
                "Destination_State": "State",
      ="Number of Records by Travel Purpose",
        )

        fig.update_traces(
            hover      },
        )

        fig.update_layout(
            height=550,
            coloraxis_colorbar=dict(title="Avg $", tickptemplate=(
                "<b>%{x}</b><br>"
                "Records: refix="$"),
            geo=dict(s%{y:,.0f}"
          howlakes=True, l      "<extra><akecolo/extra>"
      r="r      )
        )

gb(2        fig.update_layout(
            sh20,220,220)"),
        )

        sowlegend=False,
            xaxist.plotly_chart(_title="Travel pufig, use_container_widrpose",
            yaxth=True)
 is_title="Number of   else:
        records",
  st.info("Destination_Stat       )

        fig = style_che column not available for map.")


## art(fig)
        fig.update_yaSpending composition

with composition:

xes(tickformat=",")

        st.plotly_chart(
       st.subheader("How total spending is distributed")

    st.markdown("### Treemap: spending composition")

    treemap_source = filtered_df.copy()

    top_destinati         fig,
            use_container_width=True,
        )

    # Map

    st.divider()
    st.subheader("Geographic distribution of spending")

    if "Destination_State" in filtered_df.columns:
        state_agg = (
            filons = (
        treemap_source["Destination"]
        .value_counts()
        .head(12)
        .index
    )

    treemap_source["Destination_Group"] = np.where(
        treemap_source["Destination"].isin(
            top_destinations
        ),
        treemap_source["Destination"],
        "Other desttered_df.groupby("Destination_State", as_index=False)
            .agg(
                Total_Expenses=("Expenses", "sum"),
                Average_Expenses=("Expenses", "mean"),
                Records=("Expenses", "size"),
            )
        )

        fig = px.choropleth(
            state_agg,
            locations="Destination_State",
            locationminations",
    )

    treemap_data = (
        treemap_source.groupby(
            ["Travel_Reason", "Destination_Group"],
            as_index=False,
        )
        .agg(
            Total_Expenses=("Expenses", "sum"),
            Records=("Expenses", "size"),
            Average_Expenses=("Expenses", "mean"),
        )
    )

    fig ode="USA-states",
            color="Average_Expenses",
            hover_data={
                "Total_Expenses": True,
                "Records": True,
                "Destination_State": False,
            },
            color_continuous_scale="Reds",
            scope="usa",
            title="Average Expenditure by State",
            labels={
                "Average_Expenses": "Avg expenditure ($)",
                "Destination_State": = px.treemap(
        treemap_data,
        path=[
            "Travel_Reason",
            "Destination_Group",
        ],
        values="Total_Expenses",
        color="Average_Expenses",
        color_continuous_scale="Reds",
        custom_data=[
            "Records",
            "Average_Expenses",
        ],
        title="Total Expenditure by Purpose and Destination",
    )

    fig.update_traces(
        hoverte"State",
            },
        )

        fig.update_layout(
            height=550,
            coloraxis_colorbar=dict(title="Avg $", tickprefix="$"),
            geo=dict(showlakes=True, lakecolor="rgb(220,220,220)"),
        )

mplate=(
            "<b>%{        st.plotlabel}<ly_chart(fig, use_c/b><br>"
          ontainer_widt  "Total expendih=True)
  ture: $%{  else:
        svalue:t.info("Destination_State co,.2f}<br>"
     lumn not available for map.")


## Spending com       "Records: %{customdata[0]:,.0f}<br>"
   position

with composition:

    st.subheader("How total spending is distributed")

    # Treemap
    st.markd         "Average expenditure: $%{customdata[1]:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        heigown("### Treemap: spending composition")

    treemap_source = filtered_df.copy()

    top_destinations = (
        treemap_source["Destination"]
        .value_counts()
        .head(12)
        .index
    )

   ht=560,
        coloraxis_colorbar=dict(
            title="Average<br>expenditure",
            tickprefix="$",
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "Rectangle area represents total recorded expendi treemap_source["Destination_Group"] = np.where(
        treemap_source["Destination"].isin(
            top_destinations
        ),
        treemap_source["Destination"],
        "Other destinations",
    )

    treemap_data = (
        treemap_source.groupby(
            ["Travel_Reason", "Destination_Group"],
            as_index=False,
        )
        .agg(
            Tture. "
        "The treemap groups less common destinations into "
        "'Other destinations' to keep it readable."
    )

    st.markdown("### Share of recorded expenditure")

    share_data = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Total_Expenses=("Expenses", "sum"),
            Records=("Expenses", "size"),
 otal_Expenses=("Expenses", "sum"),
            Records=("Expenses", "size"),
            Average_Expenses=("Expenses", "mean"),
        )
    )

    fig = px.treemap(
        treemap_data,
        path=[
            "Travel_Reason",
            "Destination_Group",
        ],
        values="Total_Expenses",
        color="Average_Expenses",
        color_continuous_scale="Reds",
        custom_data=[
                   )
    )

    share_data["Spending_Share"] = (
        share_data["Total_Expenses"]
        / share_data["Total_Expenses"].sum()
        * 100
    )

    fig = px.pie(
        share_data,
        names="Travel_Reason",
        values="Total_Expenses",
        hole=0.55,
        color_discrete_sequence=COLORS,
        custom_data=["Records", "Spending_Share"],
        title="Cont"Records",
            "Average_Expenses",
        ],
        title="Total Expenditure by Purpose and Destination",
    )

    fig.update_traces(
        hoverteribution to Total Expenditure",
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Total expenditure: $%{value:,.2f}<br>"
            "Share: %{customdata[1]:.1f}%<br>"
            "Records: %{customdata[0]:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(height=470)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()
    st.markdownmplate=(
            "<b>%{label}</b><br>"
            "Total expenditure: $%{value:,.2f}<br>"
            "Records: %{customdata[0]:,.0f}<br>"
            "Average expenditure: $%{customdata[1]:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=560,
        coloraxis_colorbar=dict(
            title="Average<br>expenditure",
            tickprefix="$",
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "Rectangle area represents total recorded expenditure. "
        "The treemap groups less common destinations("### Stacked: spending by purpose within destination")

    stack_data = (
        filtered_df. into "
        "'Other destinations' to keep it readable."
    )

    # Purpose share
    st.markdown("### Share of recorded expenditure")

    share_data = (
        filgroupby(
            ["Destination", "Travel_Reason"], as_index=False
        )
        .agg(Total_Expenses=("Expenses", "sum"))
        .sort_values("Total_Expenses", atered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Total_Expenses=("Expenses", "sum"),
            Records=("Expenses", "size"),
        )
scending=False)
        .head(10)
    )

    fig = px.bar(
        stack_data,
        x="Total_Expenses",
        y="Destination",
        color="Travel_Reason",
        orientation="h",
    )

    share_data["Spending_Share"] = (
        share_data["Total_Expenses"]
        / share_data["Total_Expenses"].sum()
        * 100
    )

    fig = px.pie(
        share_data,
        names=        color_discrete_sequence=COLORS,
        title="Top 10 Destinations: Spending by Purpose",
    )

    fig.update_layout(
        xaxis_title="Total expenditure ($)",
        yaxis_title=None,
        legend_title="Travel purpose",
    )

 "Travel_Reason",
        values="Total_Expenses",
        hole=0.55,
        color_discrete_sequence=COLORS,
        custom_data=["Records", "Spending_Share"],
        title="Contribution to Total Expenditure",
    )

    fig.update_traces(
        textposition="inside",
           fig = style_chart(fig, 500)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)


## Spending patterns

with patterns:

    st.subheader("0. Expenditure histogram")

    fig = px.histogram(
        filtered_df,
 textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Total expenditure: $%{value:,.2f}<br>"
            "Share: %{customdata[1]:.1f}%<br>"
            "Records: %{customdata[0]:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(h       x="Expenses",
        color="Travel_Reason",
        nbins=40,
        opacity=0.6,
        color_discrete_sequence=COLORS,
        title="Expenditure Distribution (Histogram + KDE)",
    )

    for reason in filtered_df["Travel_Reason"].ueight=470)

    st.plotnique():
        subset = filteredly_chart(
   _df.loc[
            fil     fig,
        use_container_widtered_df["Traveth=True,
    )

    # Stacked bar
    st.divider()
    st.markdown("###l_Reason"] == reason, "Expenses"
        ]
        if len(subset) >= 10:
            kde = stats.gaus Stacked: spending by purpose within destination")

    stack_data = (
        filtered_df.groupby(
            ["Destination", "Travesian_kde(subset)
            x_range = np.linspace(subset.min(), subset.ml_Reason"], as_index=False
        )
        .agg(Total_Expenses=("Expenses", "sum"))
        .sort_values("Total_Expenses", ascendiax(), 200)
            fig.add_trace(go.Scatter(
                x=x_range,
                y=kde(x_range) * len(subset) * 20,
                mode="lines",
            ng=False)
        .head(10)
    )

    fig = px.bar(
        stack_data,
        x="Total_Expenses",
        y="Destination",
        color    name=f"{reason} KDE",
                line=dict(width=2.5),
                showlegend=False,
            ))

    fig.update_layout(barmode="overlay")
    fig = style_chart(fig, 480)
    fig.update_yaxes(tickformat=",")
    st.plotly_ch="Travel_Reason",
        orientation="h",
        color_discrete_sequence=COLORS,
        title="Top 10 Destinations: Spending by Purpose",
    )

    fig.update_layout(
        xaxis_title="Total expenditure ($)",
        yaxis_title=None,
        legend_title="Travel part(fig, use_container_width=True)

    st.divider()

    st.subheader("1. Expenditure distribution")

    st.write(
        "A violin plot shows where expenditure values are "
        "concentrated within each travel-purpose group."
    )

    violin_data = filtered_df

    if len(violurpose",
    )

    fig = style_chart(fig, 500)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)


## Spending patterns

with patterns:

    # Histogram + KDE
    st.subheader("0. Expenditure histogram")

    fig = px.histogram(
        filtered_df,
        x="Expenses",
       in_data) > 6000:
        violin_data = violin_data.sample(
            n=6000,
            random_ color="Travel_Reason",
        nbins=40,
        opacity=0.6,
        color_discrete_sequence=COLORS,
        title="Expenditure Distribution (Histogram + KDE)",
    )

    for reason in filtered_df["Travel_Reason"].unique():
        subset = filtered_df.loc[
            filtered_df["Travel_Reason"] == reason, "Expenses"
        ]
        if len(subset) >= 10:
            kde = stats.gaussian_kde(subset)
            x_range = np.linspace(subset.min(), subset.max(), 200)
            fig.add_trace(go.Scatter(
                x=x_range,
                y=kde(x_range) * len(subset) * 20,
                mode="lines",
            state=42,
        )

     name=f"{reason} KDE",
                line=dic   fig = px.violin(
        violin_data,
        x="Travel_Reason",
        y="Expenses",
        color="Travel_Reason",
        box=False,
        points=False,
        color_discrete_sequence=COLORS,
        title="Expenditure Distribution by Travel Purpose",
    )

    fig.update_traces(
        meanline_visible=True,
        hovertemplate=(
            "Travel purpose: %{x}<br>"
            "Expenditure: $%{y:,.2f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Travel purpose",
        yaxis_title="Expenditure ($)",
    )

    fig = style_chart(fig, 520)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    if len(filtered_df) > len(violin_data):
        st.caption(
     t(width=2.5),
                showlegend=False,
            ))

    fig.update_layout(barmode="overlay")
    fig = style_chart(fig, 480)
    fig.update_yaxes(tickformat=",")
          "The violin chart uses a reproducible sample of "
            f"{len(violin_data):,} records for rendering speed. "
            "Other analyses use all filtered records."
        )

 st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Violin plot
    st.subheader("1. Expenditure distribution")

    st.write(
        "A violin plot shows where expenditure value    st.divider()

    if "Pax" in filtered_df.columns:

        party_data = filtered_df.dropna(
            subset=["Pax", "Expenses"]
        ).copy()

        party_data = party_data[
            party_data["Pax"] > 0
        ]

        if not party_data.empty:

s are "
        "concentrated within each travel-purpose group."
    )

    violin_data = filtered_df

    if len(violin_data) > 6000:
        violin_data = violin_data.sample(
            n=6000,
            random_state=42,
        )

    fig = px.violin(
        violin_data,
        x="Travel_Reason",
        y="Exp            common_party_sizes = (
                party_data["Pax"]
                .value_counts()
                .head(20)
                .index
            )

            party_data = party_data[
                party_data["Pax"].isin(
                    common_party_sizes
                )
            ].copy()

            st.subheader("2. Bubble scatter: party size and spending")

            st.write(
                "Eaenses",
        color="Travel_Reason",
        box=False,
        points=False,
        color_discrete_sequence=COLORS,
        title="Expenditure Distribution by Travel Puch point represents a travel record. "
       rpose",
    )

         "Th    fig.update x-axis shows pare_traces(
    ty size, the y-ax    meanline_visibis shows "
         le=True,
        hover       "expetemplate=(
     nditure, and colour represent       "Travel purs travel purpose."
   pose: %         )

            bubble_data = pa{x}<br>"
            "Expenditure: $%{rty_data

            if len(bubble_data) > 3500:
                bubbly:,.2f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegee_data = bubble_data.sample(
              nd=False,
        xaxis_title="Travel purpose",
        yaxis_title="Expenditure ($)",
    )

    fig = style_chart(fig, 520)
      n=3500,
                    random_state=42,
                )

            hover_columns = [
                column
                for column in [
                    "Destination",
                    "Accommodation",
                ]
           fig.update         if column i_yaxes(tickpren bubble_data.columns
   fix="$", tickfo         ]

       rmat=",.0f")

    st.plotly_chart(
     fig = px.scatter(
                bubble_data,
                 fig,
               use_container_wix="Pax",
           dth=True,
     y="Exp    )

    if len(filtered_df) > leenses",
                color="Travel_Reason",
                hovn(violin_data):
        st.caption(
            "Ther_data=hover_columns,
                opacity=0.65,
                color_discrete_sequene violin chart uses a reproducible sample of "
            f"{len(violin_ce=COLORS,
                title="Individual Expenditure vs Party Size",
            )

            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(wdata):,} records for rendering speed. "
            "Other analyses use all filtered records."
        )

    st.divider()

    # Party size data
    if "Pax" in idth=0.5, color="white"),
                ),
                hovertemplate=(
                    "Party size: %{x}<br>"
                    "Expenditure: $%{filtered_df.columns:

        party_data = filtered_df.dropna(
            subset=["Pax", "Expenses"]
        ).copy()

        party_data = party_data[
            party_data["Pax"] > 0
        ]

        if not party_data.empty:

            common_pary:,.2f}<br>"
                    "<extra>%{fullData.name}</extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Travel party size",
                yaxis_title="Expenditure ($)",
            )

            fig = style_chart(fig, 520)
            fig.update_yaxes(
                tickprety_sizes = (
                party_data["Pax"]
                .value_counts()
                .head(20)
                .index
            )

            party_data = party_data[
                party_data["Pax"].isin(
                    common_party_sizes
                )
            ].copy()

            # Bubble scatter
            st.subheader("2. Bubble scatter: party size and spending")

            st.write(
             fix="$",
                tickformat=",.0f",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            if len(party_data) > len(bubble_data):
                st.caption(
                    "A reproducible sample is displayed to keep "
                    "the scatter plot responsive."
                )

            st.subheader("3. Scatter plot with trend line")

            "Each point represents a travel record. "
                "The x-axis shows party size, the y-axis shows "
                "expenditure, and colour represents travel purpose."
            )

            bubble_data = party_data

            if len(bubble_d   trend_data = party_data[
                [ata)"Pax", "Exp > 3500:
                bubble_data = bubble_datenses"]
            ].dropna()

       a.sample(
                    n=3500,
                    random     fig = px.scatter(
                trend_data,
                x="Pax",
           _state=42,
                )

            hover_columns = [
                column
                for col     y="Expenses",
                opacity=0.3,
                color_discrete_sequence=[BLUE],
               umn in [
                    "Destination",
                    "Accommodation",
                ]
                if column in bubble_data. title="Relationship Between Party Size and Expenditure",
            )

            if (
                len(trend_data) >= 3
       columns
            ]

            fig = px.scatter(
                bubble_data,
                x="Pax",
                y="Expenses",
                        and trend_data["Pax"].nunique() >= 2
            ):

                regression = stats.linregress(
                    trend_data["Pax"],
                  color="Travel_Reason",
                hover_data=hover_columns,
                opacity=0.65,
                color_discrete_sequence=COLORS,
                title="Individual Expend   trend_data["Expenses"],
                )

                x_line = np.linspace(
                    trend_data["Pax"].min(),
                    trend_data["Pax"].max(),
             iture vs Party Size",
            )

            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(width=0.5, color="white"),
                ),
                hovertemplate=(
                    "Par       100,
                )

                y_line = (
                    regression.intercept
                    + regression.slope * x_line
                )

                fig.add_trace(
                    goty size: %{x}<br>"
                    "Expe.Scatter(
                        x=nditux_line,
                        re: $%{y:,.2y=y_line,
                        mode="lines",
                        namef}<br>"
                    "<extra>%{fullData.name}</="Linear trend",
                        line=dict(
                            color=RED,
                         extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Travel pa   width=3,
                        ),
                        hovertemplate=(
                            "Party size: %{xrty size",
                yaxis_title="Expenditure ($)",
            )

            fig = style_chart(f:.1f}<br>"
                            "Fitted expenditure: $%{y:,.2f}"
                            "<extra>Linear trend</extra>"
                        ),
           ig, 520)
            fig.update_yaxes(
                tickprefix="$",
                tickfor         )
         mat=",.0f",
          )

                st         )

            st.plotly_chart(
            .caption(
                    f"Linear correlation: r = "
                    f"{regression.    fig,
                use_container_width=True,
            )

            if len(party_data) > len(bubblrvalue:.3f} | "
                    f"R² = {regression.rvalue ** 2:.3f} | "
           e_data):
                st.caption(
                    "A reproducible sample is displayed         f to keep "
             "Slope = ${regr       "the scatter plot reession.ssponsive."
                )

            #lope:,.2f} "
                    "per ad Scatter with treditional party mnd line
            st.subheader("3.ember."
                )

            fig.update_layout(
              Scatter plot with trend line")

            trend_data = party_data[
             xaxis_title="Travel party size",
                yaxis_title="Expenditure ($)",
            )

            fig = style_ch      ["Pax", "Expenses"]
            ].dropna()

            fig = px.scatter(
                trend_data,
                x="Pax",
                y="Expart(fig, 500)
            fig.update_yaxes(
                tickprefix="$",
                tickformat=",.0f",
            )

   enses",
                opacity=0.3,
                color_discrete_sequence         st.plotly_chart(
           =[BLUE],
                    fig,
                use_container_wid title="Relationship Between Party Size and Expenditure",
     th=True,
            )

            st.caption(
                "The trend line summarize       )

            if (
                len(trend_data) >= 3
                and trens linear association; "
                "it does not establish thd_data["Pax"].nunique() >= 2
            ):

                regression = stats.liat party size causes "
                "higher or lower expenditure."
            )

            st.subheader("4. Average spending by party size")

            party_summary = (
       nregress(
                    trend_data["Pax"],
                    trend_data["Expenses"],
                )

                x_line = np.l         party_data.groupby(
                    ["Pax",inspace(
                    tr "Travel_Reend_dataason"],
                    as_index=False,
         ["Pax"].min(),
                    trend_data["Pax"       )
                .agg(
                    Average_Exp].max(),
                    100,
                )

                y_enses=("Expenses", "mean"),
                    Median_Expenses=("Expenses", "median"),
                    Recorline = (
                    regression.intercept
                    + regression.slope * x_line
                )

                fig.addds=("Expenses", "size"),
                )
                .sort_values("Pax")
            )

            fig = p_trace(
                    go.Scatter(
                        x=x_line,
                        y=y_line,
                        mode="lines",
                        name="Linear trend",
                        line=dict(
                            cx.line(
                party_summary,
                x="Pax",
                y="Average_Expenses",
                color="Travel_Reason",
                markers=True,
                custom_data=[
                    "Meolor=RED,
                            width=3,
                        ),
                        hovertemplate=(
                            "Party size: %{x:.1f}<br>"
                            "Fitted expenditure: $dian_Expenses",
                    "Records",
                ],
                color_discrete_sequence=COLORS,
                title="Average Expenditure by Party Size and Purpose",
            )

            fig.update%{y:,.2f}"
                            "<extra>Linear trend</extra>"
                        ),
                    )
                )

                st.caption(
                    f"Linear corr_traces(
                line=dict(width=3),
                marelationker=dict(: r = "
                  size=8),
                hover  f"{regression.template=(
             rvalu       "Party e:.3f} | "
             size: %     {x}<br>"
                      f"R² = {regression.rva"Average: lue ** 2:.3f} | "
           $%{y:,.2f}<br>"
                            f"Slope = ${regression.s "Median: $%{customdatalope:,.2f} "
                    "per additional party member."
                )

   [0]:,.2f}<br>"
                    "Records: %{customdata[1]:,.0f}"
                    "<         fig.update_layout(
                xaxis_title="Travel party size",
                yaxis_title="Expendextra>%{fullData.name}</extra>"
                ),
            )

            fig.update_layout(
                xaxisiture ($)",
            )

            fig = style_chart(fig, 500)
            fig.update_yaxes(
                tickprefix="$",
       _title="Party size",
                yaxis_title="Average expenditure ($)",
            )

            fig = style_chart(fig, 500)
            fig.update_yaxes(
                tickprefix="$",
                tickformat=",.0f",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            st.caption(
                "The trend line summarizes linear association; "
                         tickformat=",.0f",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:
            st.info(
                "No valid party-size data is available "
                "under the current filters."
            )

"it does not establish that party size causes "
                "higher or lower expenditure."
            )

            # Average expenditure by party size
            st.subheader("4. Average spending by party size")

            party_summary = (
                party_data.groupby(
                    ["Pax", "Travel_Reason"],
                    as_index=False,
                )
                .agg(
               else:
        st.info(
            "The dataset does not contain a Pax column."
        )

    st.divider()
    st.subheader("5. Cumulative distribution (ECDF)")

    fig = go.Figure()

    for reason in filtered_df["Travel_Reason"].unique():
        subset = np.sort(
            filtered_df.loc[
                filtered_df["Travel_Reason"] == reason, "Expenses"
            ].d         Average_Expenses=("Expenses", "mean"),
                    Median_Expenses=("Expenses", "median"),
                    Records=("Expenses", "size"),
                )
                .sort_values("Pax")
            )

            fig = px.line(
                party_summary,
                x="Pax",
                y="Average_Expenses",
                color="Traveropna().values
        )
        if len(subset) < 5:
            continue
        ecdf = np.arange(1, lenl_Reason",
               (subs markers=True,
       et) + 1) / le         custom_data=[
                    n(subset)
        fig.add_trace(go.Scatter(
   "Median_Expenses",
                    "Records",
                ],
                color_         x=subset,
            y=ecdf,
            moddiscrete_sequence=COLORS,
                title="Average Expenditure by Party Size and Pue="lines",
            name=reason,
            line=dict(width=2),
        ))

    fig.updaterpose",
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=(
           _layout(
        title="Cumulative Distribution of Expenditure",
        xaxis_title="Expenditure ($)",
        yaxis_title="Proportion of records",
        yaxis=dict(tickformat=".0%"),
         "Party size: %{x}<br>"
                    "Average: $%{y:,.2f}<br>"
                    "Me    )

    fig = style_cdian: $%{customdathart(fig, 480)
a[0]:,.2f}<br>"
                    "Records: %{cu    fig.update_xaxes(tickprefix="$", tickformatstomdata[1]=",.0f")
    st.plotly_chart(fig, use_container_width=True)


## Sta:,.0f}"
                    "<extra>%{fullData.name}</extra>"
                ),
            )

       tistical tests

with statistics_tab:

     fig.update_layout(
                xax    st.subheader("Business versus leisure expenditure")

    is_title="Party size",
                yaxis_title="Average expenditure ($)",
            )

       business_name = "Business"
    leisure_name = "Leisure/Vacation"

    business = filtered_df.loc[
        filtered_df[     fig = style_chart(fig, 500)
            fig.update_yaxes(
                tickprefix="$",
                tickformat=",.0f",
            )

            s"Travel_Reason"] == business_name,
        "Expenses",
    ].dropna()

    leisure = filtered_df.loc[
        filtered_df["Travel_Reason"] == leisure_name,
        "t.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:
            st.info(
                "No valid party-size data is available "
                "under the current filters."
            )

    else:
        Expenses",
    ].dropna()

    if len(business) >= 2 and len(leisure) >= 2:

        business_mean = business.mean()
        leisure_mean = leisure.mean()
        difference = business_mean - leisure_mean

        welch = stats.ttest_ind(
            st.info(
            "The dataset does not contain a Pax column."
        )

    # ECDF
    st.divider()
    st.subheader("5. Cumulative distribution (ECDF)")

    fig = go.Figure()

    for reason in filtered_df["Travel_Reason"].unbusiness,
            leisure,
            equal_var=False,
        )

        effect_size = cohens_d(business, leisure)

        c1, c2, c3 = st.columns(3)

ique():
        subset = np.sort(
            filtered_df.loc[
                filtered_df["Travel_Reason"] ==        c1.metric(
            "Business mean",
            money( reason, "Expenses"
            ].dropna().values
        )
business_mean),
        )

        c2.metric(
            "Leisure mean",
           if len(subset) < 5:
                     money(leisure_mean),
 continue
           )

      ecdf = np      c3.metric(
   .arange(1,         "Difference ( len(subusiness − leibset) + sure)",
            money(di1) / len(fference),
 subset)
        fig.a       )

       dd_trace(go.Scatter(
            x=subset,
    st.markdown("### Statistical results")

        c1, c2, c3 = st.         y=ecdf,
            mode="lines",
            name=reason,
            line=dict(width=2),
  columns(3)

        c1.metric(
            "Welch p-value",
            p_value      ))

    fig.update_layout(
        title="Cumulative Distribution of Expenditure",
        xaxis_title="Expenditure ($)",
 (welch.pvalue),
        )

        c2.metric(
            "Cohen's d",
            f       yaxis_ti"{effect_tle="Proportion of rsize:.3f}" iecords",
     f pd.notna(effe   yaxis=dict(tict_size) eckformat=".0%"),
    )

lse "N/A",
        )

        c3.metric(
                fig = style_chart(fig, 480)
    fig.update_xaxes(tickprefix=""Records (business / leisure)",
            f"{len(business):,} / {len(le$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)


## Statistical tests

isure):,}",
        )

        if welch.pvalue < 0.05:
            if pd.notna(effect_size) and abs(effect_size) >= 0.5:
       with statistics_tab:

    st.subheader("Business versus leisure expenditure")

    business_name = "Business"
    leisure_name = "Leisure/Vacation"

    business = filtered_df.loc[
        filtered_df["Travel_Reason"] == busines         st.success(
                    f"Significant and meaningful difference "
                    f"(d = {effect_size:.3f})."
                )
            else:
                st.info(
                    "Statistically significant but practically small "
                    f"(d = {effect_sizs_name,
        "Expenses",
    ].dropna()

    leisure = filtered_df.loc[
        filtered_df["Travel_Reason"] == leisure_name,
        "Expenses",
    ].dropna()

    if len(business) >= 2 and len(leisure) >= 2:

        business_mean = businesse:.3f})."
                )
        else:
            st.info(
                f"No statistically significant difference "
                f"(p = {p_value(welch.pvalue)})."
            )

        st.caption(
            "Welch's t-test compares group means; Cohen's d "
            "measures the standardized effect size. "
            "Statistical significance does not establish caus.mean()
        leisure_mean = leisure.mean()
        difference = business_mean - leisure_mean

        welch = stats.ttest_ind(
            business,
            leisure,
            equal_var=False,
        )

        effect_size = cohens_d(business, leisure)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Business mean",
            money(business_mean),
        )

        c2.metric(
            "Leisuration."
        )

    else:
        st.warning(
            "Select both Business and Leisure/Vacation in the "
            "sidebar and ensure each has at least two records."
        )

    st.divider()
    st.subheader("Mean expenditure with 95% confidence intervals")

    ci_se mean",
            money(leisure_mean),
        )

        c3.metric(
            "Diummary = (
        filtered_df.gfference (business −roupby(
             leisure)",
         "Travel_Reason",
      money(diffe         as_inderence),
        )

       x=False,
        )
      st.markdown("### Sta   .agg(
           tistical results")

 Mean=("Expe       nses", "mean"),
            SD=(" c4, c5, c6 = st.columns(3)

  Expenses", "std"),
            N=("Expenses", "count"),
        )
    )

    ci_summary      c4.metric(
            "Welch p-value",
            p_value(welch.pvalue),
        )

        c5.metric(
            "Cohen's d",
     ["SE"] = (
        ci_summary["SD"] / np.sqrt(ci_summary["N"])
    )

    ci_summary["Margin"] = 0.0

    valid_ci = ci_su       f"{effect_size:.3f}" if pd.notna(effect_size) else "N/A",
        )

        c6mmary["N"] > 1

    ci.metric(
            "Sample size (biz / leisure)",
          _summary.loc[valid_ci, "Margin"] = (
        stats.t.ppf(
          f"{len(bus    0.975,
   iness):,         ci_summ} / {len(leary.loc[valisure):,}",
 id_ci, "N"] - 1,
       )

        # Verdict
        if welch.pva        )
        * ci_summary.loc[valid_ci, "SE"]
    )

    ci_summary[lue < 0.05:
            if pd.notna(effect_size) and abs(effect_size) >= 0.5:
                st.success(
                    f"Significant and me"Lower"] = (
        ci_summary["Mean"] - ci_summary["Margin"]
    )

    ci_summary["Upper"] = (
        ci_summary["aningful difference "
                    f"(d = {effect_size:.3f})."
                )
            else:
                st.info(
                    "Statistically significant but practically small "
                Mean"] + ci_summary["Margin"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ci_summary["Travel_Reason"],
            y=ci_summary["Mean"],
              f"(d = {effect_size:.3f})."
                )
        else:
            st.info(
                f"No statistically significant difference "
                f"(p = {p_value(welch.pvalue)})."
            )

    else:
        st.warning(
       mode="lines+markers",
            name="Mean",
            line=dict(
                color=BLUE,
                width=3,
            ),
            marker=dict(
                size=10,
                color=TEAL,
            ),
            error_y=dict(
                type="data",
                array=ci_summary["Margin"],
                      "Select both Business and Leisure/Vacation in the "
            "sidebar and ensure each has at least two records."
        )

    # Mean with 95% CI
    st.divider()
    st.subheader("Mean expenditure with 95% confidence intervals")

    ci_summary = (
        filtered_df.groupby(
            "Travel_Reason",
    visible=True,
                color=GREY,
                thickness=1.5,
                width=5,
            ),
            customdata=ci_summary[
                ["N", "Lower", "Upper"]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Mean: $%{y:,.         as_index=False,
        )
        .agg(
            Mean=("Expenses", "mean"),
            SD=("Expenses", "std"),
            N=("Expenses", "count"),
        )
    )

    ci_summary["SE"] = (
        ci_summary["SD"] / np2f}<br>"
                "Records: %{customdata[0]:,.0f}<br>"
                "95% CI lower: $%{customdata[1]:,.2f}<br>"
                "95% CI upper: $%{customdata[2]:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_.sqrt(ci_summary["N"])
    )

    ci_summary["Margin"] = 0.0

    valid_ci = ci_summary["N"] > 1

    ci_summary.loc[valid_ci, "Margin"] = (
        stats.t.ppf(
            0.975,
            ci_summary.loc[valid_ci, "N"] - 1,
        )
        * ci_summary.loc[valid_ci, "SE"]
    )

    ci_summary["Lower"] = (
layout(
        title="Average Expenditure and Uncertainty",
        xaxis_title="Travel purpose",
        yaxis_title="Mean expenditure ($)",
    )

    fig = style_chart(fig, 470)
    fig.update_yaxes(
        tickprefix="$",
        tickformat=",.0f",
    )

        ci_summary["Mean"] - ci_summary["Margin"]
    )

    ci_summary["Upper"] = (
        ci_s    st.plotly_chart(
ummary["Mea        fig,
n"] + ci_summary["        use_container_wiMargin"]
    )

    fig = go.Figure()

    fig.adth=True,
    )

    st.caption(
        "Error bars represent 95% codd_trace(
        go.Scatter(
            x=ci_summary["Travel_Reason"],
            y=ci_summary["Mean"],
            modnfidence intervals for group means, "
        "not the range of individual expenditures."
    )

    st.divider()
    st.subheader("Waterfall: business versus leisure mean")

e="lines+markers",
            name="Mean",
            line=dict(
                color=BLUE,
                width=3,
            ),
            marker=dict(
                size=10,
                col    if len(business) >= 2 and len(leisure) >= 2:

        fig = go.Figure(
            go.Waterfall(
            or=TEAL,
           name="Mean expen     ),
            error_y=dict(
                type="data",
                array=ci_summary["Margin"],
                visiditure",
                orientation="v",
                measure=[
                    "absolute",
                    "relative",
                    "total",
          ble=True,
                color=GREY,
                thickn      ],
                x=[
                    "Leisureess=1.5,
                width=5,
    mean",
                    "Difference to business mean",
                    "Busin         ),
            customdata=ci_summary[
                ["N"ess mean",
                ],
                y=[
                    leisure.mean(),
                    business.mean() -, "Lower", "Upper"]
            ].to_numpy(),
    leisure.mean(),
                    hovertem    plate=(
                  0,
                ],
          "<b         connecto>%{x}</r=dict(
                    line=dib><br>"
              ct(color=LI  "MeGHT_GREY)
                ),
                increasan: $%{y:,.2ing=dict(
                    marker=dict(color=TEAL)
       f}<br>"
                "Records: %{customdata[0]:,.         ),
                decreasing=dict(
                    marker=dict(color=RED)
       0f}<br>"
                "95% CI lower: $%{cust         ),
                totals=dict(
                    marker=dict(color=BLUE)
       omdata[1]:,.2f}<br>"
                "95% CI upper: $%{custom         ),
                text=[
                    money(leisure.mean()),
                    money(business.mean() - leisure.mean()),
                    money(data[2]:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    fibusiness.mean()),
                ],
                textposition="outside",
                hovertemplate=(
                    "%{x}<br>"
                    "Vg.update_layout(
        title="Average Expenditure and Uncertainty",
        xaxis_title="Travel purpose",
        yaxis_title="Mean expenditure ($)",
    )

    fig = style_chart(alue: $%{y:,.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="From Leisure Average to Business Average",
            yaxis_title="Mean expenditure ($)",
   fig, 470)
    fig.update_yaxes(
        tickprefix="$",
        tickformat=",.0f",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        "Error bars rep         showlegend=False,
        )

        fig = style_chart(fig, 470)
        fig.update_yaxes(
            tickprefix="$",
            tickformat=",.0f",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.cresent 95% confidence intervals for group means, "
        "not the range of individual expenditures."
    )

    # Waterfall
    st.divider()
    st.subheader("Waterfall: business versus leisure mean")

    if len(business) >= 2 and len(leisure) >= 2:

        fig = go.Figure(
            go.Waterfall(
                name="Mean expenaption(
            "This waterfall compares the two group means; it does "
            "not decompose individual spending or explain causation."
        )

    st.divider()
    st.subheader("Radar: purpose profile comparison")

    radar_data = (
        filtered_df.groupby("Travel_Reason")
        .agg(
            Mean=("Expenses", "diture",
                orientation="v",
                measure=[
                    "absolute",
                    "relative",
                    "total",
                ],
                x=[
                    "Leisure mean",
                    "Difference to business mean",
                    "Business mean",
                ],
                y=[
                    leisure.mean(),
                    business.mean() - leisure.mean(),
               mean"),
            Median=("Expenses", "median"),
            Max=("Expenses", "max"),
            Records=("Expenses", "size"),
        )
        .reset_index()
    )

    if len(radar_data) >= 2:
        for col in ["Mean", "Median", "Max", "Records"]:
            col_min = radar_data[col].min()
            0,
                ],
                connector=dict(
                    line=dict(color=LIGHT_GREY)
                ),
                increasing=dict(
                    marker=dict(color=TEAL)
                ),
                decreasing=dict(
                    marker=dict(color=RED)
                ),
                totals=dict(
                    marker=dict(color=BLUE)
                ),
                text=[
                    money(leisure.     col_max = radar_data[col].max()
            if col_max > col_min:
                radar_data[f"{col}_norm"] = (
                    (radar_data[col] - col_min)
                    / (col_max - col_min)
                )
            else:
                radar_data[f"{col}_norm"] = 0.5

        camean()),
                    money(business.mean() - leisure.mean()),
                    money(business.mean()),
                ],
                textposition="outside",
                hovertemplate=(
              tegories =       ["Mean", "Me"%{x}<br>"
                    "Value: $%{ydian", "Max", "Records"]
        fig = go.Figure()

        for i, reason in enumerate(radar_data["Trave:,.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="From Leisure Average to Business Average",
         l_Reason"]):
            row = radar_data[
                radar_data["Travel_Reason"] == reason
            ].iloc[0]
            values = [row[f"{c}_norm"] for c in categories]
            values.append(values[0])
             yaxis_title="Mean expenditure ($)",
            showlegend=False,
        )

        fig = style_chart(fig, 470)
        fig.update_yaxes(
            tickp  cats = categories + [categories[0]]

            fig.add_trace(go.Scatterpolar(
       refix="$",
            tickformat=",.0f",
        )

           r=values,
                     st.plotly_chart(
         theta=cats,
                fill    fig,
            use_container_width=True,
        )

        st.c="toself",
                name=reason,
                opacity=0.35,
                line=dict(waption(
            "This waterfall compares the two group means; it does "
            "not decompose individual spending or explain causation."
idth=2),
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                bgcolor="white",
            ),
           )

    # Radar
    st.divider()
    st.subheader("Radar: purpose profile comparison")

    radar_data = (
        filtered_df.groupby("Travel_Reason")
        .agg(
            Me         height=500,
            title="Normalized Metric Profile by Travel Purpose",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        )

        st.plotly_chart(fig, use_container_width=True)
an=("Expenses", "mean"),
            Median=("Expenses", "median"),
            Max=("Expenses", "max"),
               else:
   Records=("Ex      st.info("penses", "size"),
        )
At least two travel purp        .resetoses are needed for the radar chart.")


_index()
    )

## Economic context

    with economic:

if len(radar_    st.subdata) >= 2:
        foheader("Destination economics and travel spending")

    economic_colr col in ["Mean", "Median", "Max", "Records"]:
            col_min = radar_umns = [
        "Destination_State",
        "Per_Capita_Income",
        "Per_Capita_Disposable_data[col].min()
            col_max = radar_data[col].max()
            if col_max > col_min:
                radar_data[f"{cIncome",
        "Regional_Price_Parity",
    ]

    missing_economic = [
        column
        for column in economic_columns
        if column not in filol}_norm"] = (
                    (radar_data[col] - col_min)
                    / (col_max - col_min)
                )
            else:
                ratered_df.columns
    ]

    if missing_economic:

        st.info(
      dar_data[      "Economic analysis neef"{col}_nds these colorm"] = 0.5

umns: "
                   categor + ", ".join(mies = ["Mean",issing_economic)
 "Median"        )

, "Max", "Records"]
        fig = go.Figure()

          else:

       for i, reason in enumerate(radar_data["Travel_Reason"]):
            row = radar_data[
                radar_data["Travel_Reason"] == reason
            ].iloc[0]
             state_spending = (
            filtered_df.groupby(
                "Destination_State",
                as_index=False,
            )
            .agg(
                Average_Expenses=("Expenses", "mean"),
                Median_Expenses=("  values = [row[f"{c}_norm"] for c in categories]
            values.append(values[0])
            cats = categories + [categories[0]]

       Expenses", "median"),
                Travel_Records=("Expenses", "size"),
            )
        )

        economic_fields = economic_columns.copy()

        if "BEA_Reference_Year" in filtered_df.columns:
            economic_fields.append("BEA_Reference_Year")

     fig.add_trace(go.Scatterpolar(
                r=values,
                theta=cats,
                fill="toself",
                name=reason,
                opacity=0.35,
                line=dict(width=2),
            ))

        fig.update_layout(
            polar=dict(
                ra        economic_source = (
            filtered_df[economic_fields]
            .dropna(subset=["Destination_State"])
            .drop_duplicates()
            .copy()
        )

        if "BEA_Reference_Year" in economic_source.columns:

            latest_year = economic_source[
                "BEA_Reference_Year"
            ].max()

            if pd.notna(latesdialaxis=dict(visible=True, range=[0, 1]),
                bgcolor="white",
            ),
            height=500,
            title="Normalized Metric Profile by Travel Purpose",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        )

        st.plotly_chart(fig, use_container_width=True)
  t_year):
                economic_source = economic_source[
                    economic_source["BEA_Reference_Year"]
                    == latest_year
                ]

        economic_source = economic_source.drop_duplicates(
            else:
        st.info("At least tw  subset=["Destination_State"]
        )

o travel purposes are needed for the radar         economic_summary = state_spendichart.")


## Economic context

with economic:

  ng.merge(
            economic_source,
            on="Destination_State",
            how="left",
        )

        economic_summary = economic_summary  st.subheader("Destination economics and travel spending")

    economic_columns = [
        "Destination_State",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
.dropna(
            subset=[
                "        "Regional_Price_Parity",
    ]

    missing_economic = [
        column
        for column in economic_columns
        if column not in filtered_df.columns
    ]

    if missing_economic:

        st.info(
            "Economic analysis needs these columns: "
            + ", ".join(missing_economic)
        )

    else:

        state_spending = (
            filtered_df.groupby(
                "Destination_State",
                as_index=False,
            )
            .agg(
                Average_Expenses=("ExpensesRegional_Price_Parity",
                "Average_Expenses",
            ]
        )

        if len(economic_summary) >= 1:

            st.markdown("### Regional price parity vs expenditure")

            fig = px.scatter(
                economic_summary,
                x="Regional_Price_Parity",
                y="Average_Expenses",
                size="Travel_Records",
                color="Destination_State",
                hover_name="Destination_State",
                size_max=38,
                custom_data=[
                    "Travel_Records",
                    "Median_Expenses",
                    "Per_Capita_Income",
                    "Per_Capita_Dispo", "mean"),
                Median_Expenses=("Expenses", "median"),
       sable_Income",
                ],
                color_discrete_s         Travel_Reequence=cords=("ExpeCOLORS,
                title="Desnses", "size"),
   tination-Level Economic C         )
 ontext",
            )

       )

        economi            fig.uc_fields = economic_colupdate_traces(
       mns.copy()

           marke      if "BEA_Rr=dict(
                    oeference_Year" in filtered_df.pacity=0.85,
                    lcolumns:
            economiine=dict(
                     c_fields.app   color="white",
                       end("BEA_Reference_Year")

        economic_source = (
            filtered_df[ width=1.5,
                    ),
                ),
                hovertemplate=(
                    "<b>%{hovereconomic_fields]
            .dropna(subset=["Destination_State"])
            .drop_duplicates()
            .copy()
        )

        if "BEA_Referetext}</b><br>"
                    "Regional price parity: %{x:.2f}<br>"
                    "Average expenditure: $%{y:,.2f}<br>"
                    "Travelnce_Year" in economic_source.columns:

            latest_year = economic_source[
                "BEA_Reference_Year"
            ].max()

            if pd.notn records: %{customdata[0]:,.0f}<br>"
                    "Median expenditure: $%{customdata[1]:,.2f}<br>"
                    "Per-capita income: $%{custa(latest_year):
                economic_source = economic_source[
                    economic_source["BEA_Reference_Year"]
                    == latest_year
                ]

        economic_source = economic_source.drop_duplicates(
            subset=["Destination_State"]
        )

        economic_summary = omdata[2]:,.0f}<br>"
                    "Disposable income: $%{customdata[3]:,.0f}"
              state_spending.merge(
            economic      "<extra></extra>"
           _source,
             ),
            )

       on="Destination_         fig.updateState",
            h_layout(
             ow="left",
    xaxis_title="Region       )

        economical price parity",
       _summary = economic_summ         yaxisary.dropna(
   _title="Average travel expend         subset=[
                "Regional_Price_Parity",
                "Aveiture ($)",
                showlegend=False,
            )

            fig = style_charrage_Expenses",
            ]
        )

        if len(economic_summary) >= 1:

            # Bubble scatter
            st.markdt(fig, 510)
            fig.update_yaxes(
                tickprefix="$",
                tickformat=",.0f",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
   own("### Regional price parity vs expenditure")

            fig = px.scatter(
                economic_summary,
                x="Regional_Price_Parity",
                y="Average_Expenses",
                size="Travel_Records",
                        )

            st.divider()
            st.markdown("### Correlation heatmap")

            correlation_candidates = [
                "Expenses",
                "Pax",
                "Per_Capita_Income",
                 color="Destination_State",
                hover_name="Destination_State",
                size_max=38,
                custom_data=[
                    "Travel_Records",
                    "Median_Expenses",
                    "Per_Capita_Income",
                    "Per_Capita_Disposable_Income",
          "Per_Capita_Disposable_Income",
                "Regional_Price_Parity",
            ]

            available_numeric = [
                column
                for column in correlation_candidates
                if column in filtered_df.columns
                and filtered_df[column].notna().sum() > 1
            ]

      ],
                color_discrete_sequence=COLORS,
                title="Destination-Level Economic Context",
            )

            fig.update_traces(
                marker=dict(
                    opacity=0.85,
                    line=dict(
                        color="white",
                           correlation_data = filtered_df[
                available_numeric
            ].copy()

            if len(available_numeric) >= 2:

                correlation_matrix = (
                    correlation_data.corr(
                        method="spearman"
                    )
                )

                fig = px.imshow(
                    correlation_         width=1.5,
                    ),
                ),
                hovertemplate=(
                    "<b>%{hovertext}</b><br>"
                    "Regional price parity: %{x:.2f}<br>"
                    "Average expenditure: $%{y:,.2f}<br>"
                    "Travel records: %{customdata[0]:,.0f}<br>"
                   matrix,
                    text_auto=".2f",
                    color_continuous_scale="RdBu",
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                    title="Spearman Correlation Between Numeric Variables",
                )

                fig.update_layout(
                    height=520,
                    coloraxis_colorbar=dict(
                        title=" "Median expenditure: $%{customdata[1]:,.2f}<br>"
                    "Per-capita income: $%{customdata[2]:,.0f}<br>"
                    "Disposable income: $%{customdata[3]:,.0f}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Regional price parity",
         Spearman<br>rho",
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                st.caption(
                    "Spearman correlation measures monotonic association. "
                    "Correlations do not prove causation. Economic indicators "
                    "are destination-level data and are not individual "
                    "traveller incomes."
                )

            else:
                st.info(
                    "At least two usable numeric v       yaxis_title="Average travel expenditure ($)",
                showlegend=False,
            )

            fig = style_chart(fig, 510)
            fig.update_yaxes(
                tickprefix="$",
                tickformat=",.0f",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            # Correlation heatmap
            st.divider()
            st.markdown("### Correlation heatmap")

            correlation_candidates = [
                "Expenses",
                "Pax",
         ariables are needed "
                    "to calculate a correlation matrix."
                )

            st.divider()
            st.markdown(
                "### Destination-level correlation test"
            )

            corr_data = economic_summary[
                [
                    "Regional_Price_Parity",
                    "Average_Expenses",
                ]
            ].dropna()

            if (
                len(corr_data) >= 3
                and corr_data["Regional_Price_Parity"].nunique() > 1
                and corr_data["Average_Expenses"].nunique() > 1
            ):

                result = stats.spearmanr(
                    corr_data["Region       "Per_Capita_Income",
                "Per_Capita_Disposable_Income",
                "Regional_Price_Parity",
            ]

            available_numeric = [
                column
                for column in correlation_candidates
                if column in filtered_df.columns
                and filtered_df[column].notna().sum() > 1
            ]

            correlation_data = filtered_df[
                available_numeric
            ].copy()

            if len(available_numeric) >= 2:

                correlation_matrix = (
                    correlation_data.corr(
                        method="spearman"
                    )
                )

                fig = px.imshow(
                    correlation_matrix,
                    text_autal_Price_Parity"],
                    corr_data["Average_Expenses"],
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Spearman rho",
                    f"{result.statistic:.3f}",
                )

                c2.metric(
                    "P-value",
                    p_value(result.pvalue),
                )

                c3.metric(
                    "Destinations",
                    f"{len(corr_data):,}",
                )

                st.caption(
                    "The destination is the unit of analysis, "
                    "not the individual traveller. "
                    "A small N produces uncertain estimates."
                )

            else:
                st.info(
             o=".2f",
                    color_continuous_scale="RdBu",
                    zmin=-1,
                    zmax=1,
                    aspect="auto",
                    title="Spearman Correlation Between Numeric Variables",
                )

                fig.update_layout(
                    height=520,
                    coloraxis_colorbar=dict(
                        title="Spearman<br>rho",
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                st.caption(
                    "Spearman correlation measures monotonic association. "
                    "Correlations do not prove causation. Economic indicators "
                    "are destination-level data and are not individual "
                    "traveller incomes."
                )

            else:
                st.info(
                    "At least two usable numeric varia       "A minimum of three destinations with "
                    "varying price parity and average spending "
                    "is required."
                )

            st.divider()
            st.markdown("### Summary of the Economy")

            economic_display = economic_summary.copy()

            for column in [
                "Average_Expenses",
                "Median_Expenses",
                "Per_Capita_Income",
                "Per_Capita_Disposable_Income",
            ]:
                if column in economic_display.columns:
                    economic_display[column] = (
                        economic_display[column].map(money)
                    )

            st.dataframe(
                economic_display,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.warning(
                "Destinations have no matching economic data "
                "under the current filters."
            )

bles are needed "
                    "to calculate a correlation matrix."
                )

            # Spearman: destination price parity
            st.divider()
            st.markdown(
                "### Destination-level correlation test"
            )

            corr_data = economic_summary[
                [
                    "Regional_Price_Parity",
                    "Average_Expenses",
                ]
            ].dropna()

            if (
                len(corr_data) >= 3
                and corr_data["Regional_Price_Parity"].nunique() > 1
                and corr_data["Average_Expenses"].nunique() > 1
            ):

                result = stats.spearmanr(
                    corr_data["Regional_Price_Parity"],
                    corr_data["Average_Expenses"],
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Spearman rho",
                    f"{result.statistic:.3f}",
                )

                c2.
## Data exploring

with explore:

    st.subheader("Explore filtered travel records")

    st.write(
        f"**{len(filtered_df):,} records** match the current filters."
    )

    available_columns = filtered_df.columns.tolist()

    default_columns = [
        column
        for column in [
            "Respondent",
            "Travel_Reason",
            "Expenses",
            "Destination",
            "Destination_State",
            "Accommodation",
            "Pax",
            "Per_Capita_Income",
            "Per_Capita_Disposable_Income",
            "Regional_Price_Parity",
            "BEA_Reference_Year",
        ]
        if column in available_columns
    ]

    chosenmetric(
                    "P-value",
                    p_value(result.pvalue),
                )

                c3.metric(
                    "Destinations",
                    f"{len(corr_data):,}",
                )

                st.caption(
                    "The destination is the_columns = st.multiselect(
        "Columns to d unit of analisplay",
        ysis, "
                    options=available_c"not the individual traveller. "
              olumns,
        default=default_columns,
    )

    i      "A small N produces uncertain estimates."
                )

            else:
                st.info(
                    "A mif chosen_columns:
        st.dataframe(
            filtered_df[chosen_columns],
            use_container_width=True,
            hide_index=True,
        )
    else:
       nimum of three destinations with "
                    "varying price parity and average spending "
                    "is required."
                )

            # Economic data table
            st.divider()
            st.markdown("### Summary of the E st.info("Select at least one column.")

    st.divider()

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download filtered records",
        data=conomy")

            economic_display = economic_summary.copy()

            for column in [
                "Average_Expenses",
                "Median_Expenses",
                "Per_Capita_Income",
                "Per_Capita_Disposable_Income",
            ]:
                if column in economic_display.columns:
                    economic_display[column] = (
                        economic_displacsv_data,
        file_name="travel_spend_filtered.csv",
        mime="text/csv",
    )

y[column].map(money)
                    )

            st.dataframe(
                economic_d    purpose_export = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Recorisplay,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.warning(
                "Destinations have no ds=("Expenses", "size"),
            Total_Expenses=("Expenses", "sum"),
            Average_Expenses=("Expenses", "mean"),
            Median_Expenses=("Expenses", "median"),
            Standard_Deviatimatching economic data "
                "under the current filters."
            )


## Data exploring

with explore:

    st.subheader("Explore filtered travel records")

on=("Expenses", "std"),
        )
    )

    st.download_button(
        label="Download travel-purpose summary",
    st.write(
                data=purpose_export.to_csv(indf"**{len(filtered_df):,} recordsex=False).encode("utf-8"),
        fil** match the current filters."
    )

    available_columns = filtered_df.columne_name="travel_spend_summary.csv",
        mime="text/csv",
    )


## Footer

st.ds.tolist()

    default_columns = [
        column
        for column in [
            "Respondent",
            "Travel_Reason",
            "Expenses",
            "Destination",
            "Desivider()

st.caption(
    "Travel Spend Analytics | Interactive exploratory analysis. "
    "Results describe the filtered dataset and should not "
    "automatically be generalized to all travellers."
)   
