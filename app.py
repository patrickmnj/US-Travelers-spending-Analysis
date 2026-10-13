
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. COLOUR PALETTE
# =========================================================

NAVY = "#172554"
BLUE = "#2563EB"
TEAL = "#0F9D8A"
GOLD = "#E9A23B"
PURPLE = "#7C3AED"
RED = "#DC2626"
GREY = "#64748B"
LIGHT_GREY = "#E2E8F0"

COLORS = [BLUE, TEAL, GOLD, PURPLE, RED, "#0891B2"]


# =========================================================
# 3. PAGE STYLING
# =========================================================

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


# =========================================================
# 4. LOAD AND PREPARE DATA
# =========================================================

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

    # Clean text fields.
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

    # Prefer cleaned city names for destination analysis.
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


# =========================================================
# 5. HELPER FUNCTIONS
# =========================================================

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


def cohens_d(group_a, group_b):
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)

    if len(a) < 2 or len(b) < 2:
        return np.nan

    pooled_variance = (
        (len(a) - 1) * np.var(a, ddof=1)
        + (len(b) - 1) * np.var(b, ddof=1)
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
    title,
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


# =========================================================
# 6. HEADER
# =========================================================

st.title("✈️ Travel Spend Analytics")

st.markdown(
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


# =========================================================
# 7. SIDEBAR FILTERS
# =========================================================

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
        value=(min_expense, max_expense),
        format="$%.2f",
    )
else:
    expense_range = (min_expense, max_expense)

st.sidebar.divider()

st.sidebar.caption(
    "All charts and statistical tests update "
    "when you change the filters."
)


# =========================================================
# 8. FILTER RECORDS
# =========================================================

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


# =========================================================
# 9. KEY PERFORMANCE INDICATORS
# =========================================================

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
    "dataset's currency definition before publishing results."
)

st.divider()


# =========================================================
# 10. TABS
# =========================================================

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


# =========================================================
# TAB 1: OVERVIEW
# =========================================================

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
            Records=("Expenses", "size"),
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

    left, right = st.columns(2)

    with left:

        st.subheader("Destination rankings")

        destination_summary = (
            filtered_df.groupby(
                "Destination",
                as_index=False,
            )
            .agg(
                Average_Expenses=("Expenses", "mean"),
                Records=("Expenses", "size"),
            )
        )

        # Limit the chart to the 15 destinations with the
        # most records, then rank them by average expenditure.
        common_destinations = (
            filtered_df["Destination"]
            .value_counts()
            .head(15)
            .index
        )

        ranking = destination_summary[
            destination_summary["Destination"].isin(
                common_destinations
            )
        ].sort_values("Average_Expenses")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=ranking["Average_Expenses"],
                y=ranking["Destination"],
                mode="lines",
                line=dict(color=LIGHT_GREY, width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=ranking["Average_Expenses"],
                y=ranking["Destination"],
                mode="markers",
                marker=dict(
                    size=10,
                    color=TEAL,
                ),
                customdata=ranking[["Records"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Average: $%{x:,.2f}<br>"
                    "Records: %{customdata[0]:,.0f}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

        fig.update_layout(
            title="Average Spending by Destination",
            xaxis_title="Average expenditure ($)",
            yaxis_title="Destination",
        )

        fig = style_chart(fig, 500)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        st.subheader("Travel-purpose record counts")

        reason_counts = (
            filtered_df["Travel_Reason"]
            .value_counts()
            .rename_axis("Travel_Reason")
            .reset_index(name="Records")
        )

        fig = px.bar(
            reason_counts,
            x="Travel_Reason",
            y="Records",
            color="Travel_Reason",
            color_discrete_sequence=COLORS,
            title="Number of Records by Travel Purpose",
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Records: %{y:,.0f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Travel purpose",
            yaxis_title="Number of records",
        )

        fig = style_chart(fig)
        fig.update_yaxes(tickformat=",")

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# =========================================================
# TAB 2: SPENDING COMPOSITION
# =========================================================

with composition:

    st.subheader("How total spending is distributed")

    # -----------------------------------------------------
    # TREEMAP
    # -----------------------------------------------------

    st.markdown("### Treemap: spending composition")

    treemap_source = filtered_df.copy()

    top_destinations = (
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
        "Other destinations",
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

    fig = px.treemap(
        treemap_data,
        path=[
            "Travel_Reason",
            "Destination_Group",
        ],
        values="Total_Expenses",
        color="Average_Expenses",
        color_continuous_scale="Teal",
        custom_data=[
            "Records",
            "Average_Expenses",
        ],
        title="Total Expenditure by Purpose and Destination",
    )

    fig.update_traces(
        hovertemplate=(
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
        "The treemap groups less common destinations into "
        "'Other destinations' to keep it readable."
    )

    # -----------------------------------------------------
    # PURPOSE SHARE
    # -----------------------------------------------------

    st.markdown("### Share of recorded expenditure")

    share_data = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Total_Expenses=("Expenses", "sum"),
            Records=("Expenses", "size"),
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
        title="Contribution to Total Expenditure",
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


# =========================================================
# TAB 3: SPENDING PATTERNS
# =========================================================

with patterns:

    # -----------------------------------------------------
    # VIOLIN PLOT
    # -----------------------------------------------------

    st.subheader("1. Expenditure distribution")

    st.write(
        "A violin plot shows where expenditure values are "
        "concentrated within each travel-purpose group."
    )

    # Use a reproducible sample for responsive rendering
    # when the filtered dataset is large.
    violin_data = filtered_df

    if len(violin_data) > 6000:
        violin_data = violin_data.sample(
            n=6000,
            random_state=42,
        )

    fig = px.violin(
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
            "The violin chart uses a reproducible sample of "
            f"{len(violin_data):,} records for rendering speed. "
            "Other analyses use all filtered records."
        )

    st.divider()

    # -----------------------------------------------------
    # PARTY SIZE DATA
    # -----------------------------------------------------

    if "Pax" in filtered_df.columns:

        party_data = filtered_df.dropna(
            subset=["Pax", "Expenses"]
        ).copy()

        party_data = party_data[
            party_data["Pax"] > 0
        ]

        if not party_data.empty:

            # Limit very unusual party sizes for readability.
            common_party_sizes = (
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

            # -------------------------------------------------
            # BUBBLE SCATTER
            # -------------------------------------------------

            st.subheader("2. Bubble scatter: party size and spending")

            st.write(
                "Each point represents a travel record. "
                "The x-axis shows party size, the y-axis shows "
                "expenditure, and colour represents travel purpose."
            )

            bubble_data = party_data

            if len(bubble_data) > 3500:
                bubble_data = bubble_data.sample(
                    n=3500,
                    random_state=42,
                )

            hover_columns = [
                column
                for column in [
                    "Destination",
                    "Accommodation",
                ]
                if column in bubble_data.columns
            ]

            fig = px.scatter(
                bubble_data,
                x="Pax",
                y="Expenses",
                color="Travel_Reason",
                hover_data=hover_columns,
                opacity=0.65,
                color_discrete_sequence=COLORS,
                title="Individual Expenditure vs Party Size",
            )

            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(width=0.5, color="white"),
                ),
                hovertemplate=(
                    "Party size: %{x}<br>"
                    "Expenditure: $%{y:,.2f}<br>"
                    "<extra>%{fullData.name}</extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Travel party size",
                yaxis_title="Expenditure ($)",
            )

            fig = style_chart(fig, 520)
            fig.update_yaxes(
                tickprefix="$",
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

            # -------------------------------------------------
            # SCATTER WITH TREND LINE
            # -------------------------------------------------

            st.subheader("3. Scatter plot with trend line")

            trend_data = party_data[
                ["Pax", "Expenses"]
            ].dropna()

            fig = px.scatter(
                trend_data,
                x="Pax",
                y="Expenses",
                opacity=0.3,
                color_discrete_sequence=[BLUE],
                title="Relationship Between Party Size and Expenditure",
            )

            if (
                len(trend_data) >= 3
                and trend_data["Pax"].nunique() >= 2
            ):

                regression = stats.linregress(
                    trend_data["Pax"],
                    trend_data["Expenses"],
                )

                x_line = np.linspace(
                    trend_data["Pax"].min(),
                    trend_data["Pax"].max(),
                    100,
                )

                y_line = (
                    regression.intercept
                    + regression.slope * x_line
                )

                fig.add_trace(
                    go.Scatter(
                        x=x_line,
                        y=y_line,
                        mode="lines",
                        name="Linear trend",
                        line=dict(
                            color=RED,
                            width=3,
                        ),
                        hovertemplate=(
                            "Party size: %{x:.1f}<br>"
                            "Fitted expenditure: $%{y:,.2f}"
                            "<extra>Linear trend</extra>"
                        ),
                    )
                )

                st.caption(
                    f"Linear correlation: r = "
                    f"{regression.rvalue:.3f} | "
                    f"R² = {regression.rvalue ** 2:.3f} | "
                    f"Slope = ${regression.slope:,.2f} "
                    "per additional party member."
                )

            fig.update_layout(
                xaxis_title="Travel party size",
                yaxis_title="Expenditure ($)",
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
                "it does not establish that party size causes "
                "higher or lower expenditure."
            )

            # -------------------------------------------------
            # AVERAGE EXPENDITURE BY PARTY SIZE
            # -------------------------------------------------

            st.subheader("4. Average spending by party size")

            party_summary = (
                party_data.groupby(
                    ["Pax", "Travel_Reason"],
                    as_index=False,
                )
                .agg(
                    Average_Expenses=("Expenses", "mean"),
                    Median_Expenses=("Expenses", "median"),
                    Records=("Expenses", "size"),
                )
                .sort_values("Pax")
            )

            fig = px.line(
                party_summary,
                x="Pax",
                y="Average_Expenses",
                color="Travel_Reason",
                markers=True,
                custom_data=[
                    "Median_Expenses",
                    "Records",
                ],
                color_discrete_sequence=COLORS,
                title="Average Expenditure by Party Size and Purpose",
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "Party size: %{x}<br>"
                    "Average: $%{y:,.2f}<br>"
                    "Median: $%{customdata[0]:,.2f}<br>"
                    "Records: %{customdata[1]:,.0f}"
                    "<extra>%{fullData.name}</extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Party size",
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

        else:
            st.info(
                "No valid party-size data is available "
                "under the current filters."
            )

    else:
        st.info(
            "The dataset does not contain a Pax column."
        )


# =========================================================
# TAB 4: STATISTICAL TESTS
# =========================================================

with statistics_tab:

    st.subheader("Business versus leisure expenditure")

    business_name = "Business"
    leisure_name = "Leisure/Vacation"

    business = filtered_df.loc[
        filtered_df["Travel_Reason"] == business_name,
        "Expenses",
    ].dropna()

    leisure = filtered_df.loc[
        filtered_df["Travel_Reason"] == leisure_name,
        "Expenses",
    ].dropna()

    if len(business) >= 2 and len(leisure) >= 2:

        business_mean = business.mean()
        leisure_mean = leisure.mean()
        difference = business_mean - leisure_mean

        # Welch's t-test does not assume equal group variances.
        welch = stats.ttest_ind(
            business,
            leisure,
            equal_var=False,
        )

        # Confidence interval for the difference in means.
        term_b = business.var(ddof=1) / len(business)
        term_l = leisure.var(ddof=1) / len(leisure)

        standard_error = np.sqrt(term_b + term_l)

        denominator = (
            term_b ** 2 / (len(business) - 1)
            + term_l ** 2 / (len(leisure) - 1)
        )

        degrees_freedom = (
            (term_b + term_l) ** 2 / denominator
            if denominator > 0
            else np.nan
        )

        if pd.notna(degrees_freedom) and standard_error > 0:

            critical = stats.t.ppf(
                0.975,
                degrees_freedom,
            )

            ci_low = difference - critical * standard_error
            ci_high = difference + critical * standard_error

        else:
            ci_low = np.nan
            ci_high = np.nan

        mann = stats.mannwhitneyu(
            business,
            leisure,
            alternative="two-sided",
        )

        effect_size = cohens_d(business, leisure)

        superiority = (
            mann.statistic
            / (len(business) * len(leisure))
        )

        rank_biserial = 2 * superiority - 1

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Business mean",
            money(business_mean),
        )

        c2.metric(
            "Leisure mean",
            money(leisure_mean),
        )

        c3.metric(
            "Difference (business − leisure)",
            money(difference),
        )

        results = pd.DataFrame(
            {
                "Statistical measure": [
                    "Business sample size",
                    "Leisure sample size",
                    "Welch t-statistic",
                    "Welch degrees of freedom",
                    "Welch t-test p-value",
                    "95% CI lower bound",
                    "95% CI upper bound",
                    "Mann–Whitney U statistic",
                    "Mann–Whitney p-value",
                    "Cohen's d",
                    "Probability of superiority",
                    "Rank-biserial correlation",
                ],
                "Result": [
                    f"{len(business):,}",
                    f"{len(leisure):,}",
                    f"{welch.statistic:.4f}",
                    f"{degrees_freedom:.2f}",
                    p_value(welch.pvalue),
                    money(ci_low),
                    money(ci_high),
                    f"{mann.statistic:,.0f}",
                    p_value(mann.pvalue),
                    (
                        f"{effect_size:.3f}"
                        if pd.notna(effect_size)
                        else "N/A"
                    ),
                    f"{superiority:.3f}",
                    f"{rank_biserial:.3f}",
                ],
            }
        )

        st.markdown("### Statistical results")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True,
        )

        if welch.pvalue < 0.05:
            st.success(
                "The difference in mean expenditure is "
                "statistically significant at the 5% level."
            )
        else:
            st.info(
                "The difference in mean expenditure is not "
                "statistically significant at the 5% level."
            )

        if pd.notna(effect_size):
            magnitude = abs(effect_size)

            if magnitude < 0.2:
                effect_label = "negligible"
            elif magnitude < 0.5:
                effect_label = "small"
            elif magnitude < 0.8:
                effect_label = "medium"
            else:
                effect_label = "large"

            st.write(
                f"Cohen's d = {effect_size:.3f}, indicating "
                f"a {effect_label} standardized difference."
            )

        st.caption(
            "Mann–Whitney compares rank distributions and is not "
            "automatically a test of medians. Statistical "
            "significance does not establish causation."
        )

    else:
        st.warning(
            "Select both Business and Leisure/Vacation in the "
            "sidebar and ensure each has at least two records."
        )

    # -----------------------------------------------------
    # MEAN WITH 95% CONFIDENCE INTERVALS
    # -----------------------------------------------------

    st.divider()
    st.subheader("Mean expenditure with 95% confidence intervals")

    ci_summary = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Mean=("Expenses", "mean"),
            SD=("Expenses", "std"),
            N=("Expenses", "count"),
        )
    )

    ci_summary["SE"] = (
        ci_summary["SD"] / np.sqrt(ci_summary["N"])
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
        ci_summary["Mean"] - ci_summary["Margin"]
    )

    ci_summary["Upper"] = (
        ci_summary["Mean"] + ci_summary["Margin"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ci_summary["Travel_Reason"],
            y=ci_summary["Mean"],
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
                "Mean: $%{y:,.2f}<br>"
                "Records: %{customdata[0]:,.0f}<br>"
                "95% CI lower: $%{customdata[1]:,.2f}<br>"
                "95% CI upper: $%{customdata[2]:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="Average Expenditure and Uncertainty",
        xaxis_title="Travel purpose",
        yaxis_title="Mean expenditure ($)",
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

    st.caption(
        "Error bars represent 95% confidence intervals for group means, "
        "not the range of individual expenditures."
    )

    # -----------------------------------------------------
    # WATERFALL: BUSINESS VS LEISURE
    # -----------------------------------------------------

    st.divider()
    st.subheader("Waterfall: business versus leisure mean")

    if len(business) >= 2 and len(leisure) >= 2:

        fig = go.Figure(
            go.Waterfall(
                name="Mean expenditure",
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
                    money(leisure.mean()),
                    money(business.mean() - leisure.mean()),
                    money(business.mean()),
                ],
                textposition="outside",
                hovertemplate=(
                    "%{x}<br>"
                    "Value: $%{y:,.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="From Leisure Average to Business Average",
            yaxis_title="Mean expenditure ($)",
            showlegend=False,
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

        st.caption(
            "This waterfall compares the two group means; it does "
            "not decompose individual spending or explain causation."
        )


# =========================================================
# TAB 5: ECONOMIC CONTEXT
# =========================================================

with economic:

    st.subheader("Destination economics and travel spending")

    economic_columns = [
        "Destination_State",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
        "Regional_Price_Parity",
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
                Average_Expenses=("Expenses", "mean"),
                Median_Expenses=("Expenses", "median"),
                Travel_Records=("Expenses", "size"),
            )
        )

        economic_fields = economic_columns.copy()

        if "BEA_Reference_Year" in filtered_df.columns:
            economic_fields.append("BEA_Reference_Year")

        economic_source = (
            filtered_df[economic_fields]
            .dropna(subset=["Destination_State"])
            .drop_duplicates()
            .copy()
        )

        if "BEA_Reference_Year" in economic_source.columns:

            latest_year = economic_source[
                "BEA_Reference_Year"
            ].max()

            if pd.notna(latest_year):
                economic_source = economic_source[
                    economic_source["BEA_Reference_Year"]
                    == latest_year
                ]

        economic_source = economic_source.drop_duplicates(
            subset=["Destination_State"]
        )

        economic_summary = state_spending.merge(
            economic_source,
            on="Destination_State",
            how="left",
        )

        economic_summary = economic_summary.dropna(
            subset=[
                "Regional_Price_Parity",
                "Average_Expenses",
            ]
        )

        if len(economic_summary) >= 1:

            # ---------------------------------------------
            # BUBBLE SCATTER: PRICE PARITY VS SPENDING
            # ---------------------------------------------

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
                    "Per_Capita_Disposable_Income",
                ],
                color_discrete_sequence=COLORS,
                title="Destination-Level Economic Context",
            )

            fig.update_traces(
                marker=dict(
                    opacity=0.85,
                    line=dict(
                        color="white",
                        width=1.5,
                    ),
                ),
                hovertemplate=(
                    "<b>%{hovertext}</b><br>"
                    "Regional price parity: %{x:.2f}<br>"
                    "Average expenditure: $%{y:,.2f}<br>"
                    "Travel records: %{customdata[0]:,.0f}<br>"
                    "Median expenditure: $%{customdata[1]:,.2f}<br>"
                    "Per-capita income: $%{customdata[2]:,.0f}<br>"
                    "Disposable income: $%{customdata[3]:,.0f}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Regional price parity",
                yaxis_title="Average travel expenditure ($)",
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

            # ---------------------------------------------
            # CORRELATION HEATMAP
            # ---------------------------------------------

            st.divider()
            st.markdown("### Correlation heatmap")

            correlation_candidates = [
                "Expenses",
                "Pax",
                "Per_Capita_Income",
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
                    "At least two usable numeric variables are needed "
                    "to calculate a correlation matrix."
                )

        
            # SPEARMAN: DESTINATION PRICE PARITY
           

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

                c2.metric(
                    "P-value",
                    p_value(result.pvalue),
                )

                c3.metric(
                    "Destinations",
                    f"{len(corr_data):,}",
                )

                st.caption(
                    "The destination is the unit of analysisn not the individual traveller"
                    "A small Pa poduces uncertain estimates."
                )

            else:
                st.info(
                    "Minimum of three destination are required for price parity"
                    "an average spending is required."
                )

        
            # ECONOMIC DATA TABLE
            st.divider()
            st.markdown("###  Summary of the Economy")

            economic_display = economic_summary.copy()

            for column in [
                "Average_Expenses",
                "Median_Expenses",
                "Per_Capita_Income",
                "Per_Capita_Disposable_Income",
            ]:
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
                "Destination has no economic data for matching"
                "Using current filters"
            )



## Data Exploration


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

    chosen_columns = st.multiselect(
        "Columns to display",
        options=available_columns,
        default=default_columns,
    )

    if chosen_columns:
        st.dataframe(
            filtered_df[chosen_columns],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Select at least one column.")

    st.divider()

    # Download filtered data.
    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download filtered records",
        data=csv_data,
        file_name="travel_spend_filtered.csv",
        mime="text/csv",
    )

    # Download purpose-level summary.
    purpose_export = (
        filtered_df.groupby(
            "Travel_Reason",
            as_index=False,
        )
        .agg(
            Records=("Expenses", "size"),
            Total_Expenses=("Expenses", "sum"),
            Average_Expenses=("Expenses", "mean"),
            Median_Expenses=("Expenses", "median"),
            Standard_Deviation=("Expenses", "std"),
        )
    )

    st.download_button(
        label="Download travel-purpose summary",
        data=purpose_export.to_csv(index=False).encode("utf-8"),
        file_name="travel_spend_summary.csv",
        mime="text/csv",
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Travel Spend Analytics | Interactive exploratory analysis. "
    "Results describe the filtered dataset and should not "
    "automatically be generalized to all travellers."
)
