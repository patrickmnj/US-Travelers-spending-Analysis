
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats


# Page setup
st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Theme
NAVY = "#450A0A"
RED = "#DC2626"
CORAL = "#EF4444"
PINK = "#F87171"
DARK_RED = "#991B1B"
GREY = "#7F1D1D"
LIGHT_PINK = "#FECACA"
COLORS = [RED, CORAL, PINK, "#B91C1C", DARK_RED, "#FCA5A5"]

st.markdown(
    """
    <style>
    .stApp { background-color: #FEF2F2; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #450A0A; }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #FECACA;
        padding: 14px;
        border-radius: 10px;
    }
    div[data-testid="stMetricLabel"] { color: #7F1D1D; }
    div[data-testid="stMetricValue"] { color: #450A0A; }
    section[data-testid="stSidebar"] { background: #FEF2F2; }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load data
DATA_FILE = Path(__file__).parent / "travel_analysis_enriched.csv"


@st.cache_data
def load_data(file_path, modified_time):
    data = pd.read_csv(file_path)

    required = ["Travel_Reason", "Expenses"]
    missing = [col for col in required if col not in data.columns]

    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    data["Expenses"] = pd.to_numeric(data["Expenses"], errors="coerce")
    data = data.dropna(subset=["Expenses", "Travel_Reason"]).copy()
    data = data[data["Expenses"] >= 0].reset_index(drop=True)

    text_cols = [
        "Travel_Reason",
        "City",
        "City_Clean",
        "Destination_State",
        "Accommodation",
    ]

    for col in text_cols:
        if col in data.columns:
            data[col] = (
                data[col]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
            )

    if "City_Clean" in data.columns:
        data["Destination"] = data["City_Clean"]

        if "City" in data.columns:
            data["Destination"] = data["Destination"].fillna(data["City"])

    elif "City" in data.columns:
        data["Destination"] = data["City"]

    elif "Destination_State" in data.columns:
        data["Destination"] = data["Destination_State"]

    else:
        data["Destination"] = "Unknown"

    data["Destination"] = data["Destination"].fillna("Unknown").astype(str)
    data["Travel_Reason"] = data["Travel_Reason"].astype(str)

    numeric_cols = [
        "Pax",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
        "Regional_Price_Parity",
        "BEA_Reference_Year",
    ]

    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


if not DATA_FILE.exists():
    st.error(
        "Dataset not found. Place travel_analysis_enriched.csv "
        "in the same folder as app.py."
    )
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if df.empty:
    st.error("No valid expenditure records were found.")
    st.stop()


# Helpers
def money(value):
    return "N/A" if pd.isna(value) else f"${value:,.2f}"


def p_value(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.3e}" if value < 0.001 else f"{value:.4f}"


def style_chart(fig, height=430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=65, b=35),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=NAVY),
        title_font=dict(size=17, color=NAVY),
        hoverlabel=dict(bgcolor=NAVY, font_color="white", font_size=12),
    )
    fig.update_xaxes(showgrid=False, linecolor=LIGHT_PINK, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=LIGHT_PINK, zeroline=False)
    return fig


def money_axis(fig, axis="y"):
    if axis == "y":
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    else:
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    return fig


def cohens_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if len(a) < 2 or len(b) < 2:
        return np.nan

    pooled_var = (
        (len(a) - 1) * np.var(a, ddof=1)
        + (len(b) - 1) * np.var(b, ddof=1)
    ) / (len(a) + len(b) - 2)

    if pooled_var <= 0:
        return np.nan

    return (np.mean(a) - np.mean(b)) / np.sqrt(pooled_var)


def mean_difference_ci(a, b, confidence=0.95):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan

    var_a = np.var(a, ddof=1)
    var_b = np.var(b, ddof=1)

    se = np.sqrt(var_a / len(a) + var_b / len(b))

    if se == 0:
        difference = np.mean(a) - np.mean(b)
        return difference, difference

    numerator = (var_a / len(a) + var_b / len(b)) ** 2
    denominator = (
        (var_a / len(a)) ** 2 / (len(a) - 1)
        + (var_b / len(b)) ** 2 / (len(b) - 1)
    )

    degrees_freedom = numerator / denominator
    critical = stats.t.ppf(
        (1 + confidence) / 2,
        degrees_freedom,
    )

    difference = np.mean(a) - np.mean(b)
    return difference - critical * se, difference + critical * se


# Header
st.title("US Travellers Analysis")
st.caption(
    "Travel expenditure, destinations, travel purpose and economic indicators"
)

# Filters
st.sidebar.title("Filters")

reasons = sorted(df["Travel_Reason"].dropna().unique().tolist())
destinations = sorted(df["Destination"].dropna().unique().tolist())

selected_reasons = st.sidebar.multiselect(
    "Travel purpose",
    reasons,
    default=reasons,
)

selected_destinations = st.sidebar.multiselect(
    "Destination",
    destinations,
    default=destinations,
)

min_exp = float(df["Expenses"].min())
max_exp = float(df["Expenses"].max())

if min_exp < max_exp:
    expense_range = st.sidebar.slider(
        "Expenditure ($)",
        min_value=min_exp,
        max_value=max_exp,
        value=(min_exp, max_exp),
        format="$%.2f",
    )
else:
    expense_range = (min_exp, max_exp)

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
    st.warning("No records match the selected filters.")
    st.stop()


# Summary indicators
st.subheader("Key indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Travel records", f"{len(filtered_df):,}")
k2.metric("Average spending", money(filtered_df["Expenses"].mean()))
k3.metric("Median spending", money(filtered_df["Expenses"].median()))
k4.metric("Total spending", money(filtered_df["Expenses"].sum()))

st.divider()


# Tabs
overview, composition, patterns, statistics_tab, economic, explore = st.tabs(
    [
        "Overview",
        "Spending Composition",
        "Spending Patterns",
        "Statistical Tests",
        "Economic Context",
        "Explore Data",
    ]
)


# Overview
with overview:
    st.subheader("Average spending by purpose")

    purpose_summary = (
        filtered_df.groupby("Travel_Reason", as_index=False)
        .agg(
            Average=("Expenses", "mean"),
            Median=("Expenses", "median"),
            Records=("Expenses", "size"),
        )
        .sort_values("Average")
    )

    fig = px.line(
        purpose_summary,
        x="Travel_Reason",
        y="Average",
        markers=True,
        custom_data=["Median", "Records"],
        color_discrete_sequence=[RED],
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10, color=CORAL),
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Mean: $%{y:,.2f}"
            "<br>Median: $%{customdata[0]:,.2f}"
            "<br>Records: %{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        xaxis_title="Travel purpose",
        yaxis_title="Average spending ($)",
    )

    st.plotly_chart(
        money_axis(style_chart(fig)),
        use_container_width=True,
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Destination rankings")

        destination_summary = (
            filtered_df.groupby("Destination", as_index=False)
            .agg(
                Average=("Expenses", "mean"),
                Records=("Expenses", "size"),
            )
        )

        top_destinations = (
            filtered_df["Destination"].value_counts().head(15).index
        )

        ranking = destination_summary[
            destination_summary["Destination"].isin(top_destinations)
        ].sort_values("Average")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=ranking["Average"],
                y=ranking["Destination"],
                mode="lines",
                line=dict(color=LIGHT_PINK, width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=ranking["Average"],
                y=ranking["Destination"],
                mode="markers",
                marker=dict(
                    size=11,
                    color=CORAL,
                    line=dict(color="white", width=2),
                ),
                customdata=ranking[["Records"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b>"
                    "<br>Average: $%{x:,.2f}"
                    "<br>Records: %{customdata[0]:,.0f}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

        fig.update_layout(
            xaxis_title="Average spending ($)",
            yaxis_title=None,
        )

        fig = style_chart(fig, 500)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Records by purpose")

        record_counts = (
            filtered_df["Travel_Reason"]
            .value_counts()
            .rename_axis("Travel_Reason")
            .reset_index(name="Records")
        )

        fig = px.bar(
            record_counts,
            x="Travel_Reason",
            y="Records",
            color="Travel_Reason",
            color_discrete_sequence=COLORS,
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Travel purpose",
            yaxis_title="Records",
        )

        fig = style_chart(fig)
        fig.update_yaxes(tickformat=",")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Spending by state")

    if "Destination_State" in filtered_df.columns:
        state_summary = (
            filtered_df.groupby("Destination_State", as_index=False)
            .agg(
                Total=("Expenses", "sum"),
                Average=("Expenses", "mean"),
                Records=("Expenses", "size"),
            )
        )

        fig = px.choropleth(
            state_summary,
            locations="Destination_State",
            locationmode="USA-states",
            color="Average",
            hover_data={
                "Total": ":$,.2f",
                "Records": True,
                "Destination_State": False,
            },
            color_continuous_scale="Reds",
            scope="usa",
            labels={
                "Average": "Average spending",
                "Destination_State": "State",
                "Total": "Total spending",
            },
        )

        fig.update_layout(
            height=520,
            coloraxis_colorbar=dict(
                title="Average ($)",
                tickprefix="$",
            ),
            geo=dict(
                showlakes=True,
                lakecolor="rgb(235, 235, 235)",
            ),
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("The state column is not available.")


# Spending composition
with composition:
    st.subheader("Spending by purpose and destination")

    top_destinations = (
        filtered_df["Destination"].value_counts().head(12).index
    )

    treemap_data = filtered_df.copy()
    treemap_data["Destination_Group"] = np.where(
        treemap_data["Destination"].isin(top_destinations),
        treemap_data["Destination"],
        "Other",
    )

    treemap_summary = (
        treemap_data.groupby(
            ["Travel_Reason", "Destination_Group"],
            as_index=False,
        )
        .agg(
            Total=("Expenses", "sum"),
            Records=("Expenses", "size"),
            Average=("Expenses", "mean"),
        )
    )

    fig = px.treemap(
        treemap_summary,
        path=["Travel_Reason", "Destination_Group"],
        values="Total",
        color="Average",
        color_continuous_scale="Reds",
        custom_data=["Records", "Average"],
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Total: $%{value:,.2f}"
            "<br>Records: %{customdata[0]:,.0f}"
            "<br>Average: $%{customdata[1]:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=550,
        coloraxis_colorbar=dict(
            title="Average ($)",
            tickprefix="$",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Share of total spending")

        spending_share = (
            filtered_df.groupby("Travel_Reason", as_index=False)
            .agg(
                Total=("Expenses", "sum"),
                Records=("Expenses", "size"),
            )
        )

        spending_share["Share"] = (
            spending_share["Total"]
            / spending_share["Total"].sum()
            * 100
        )

        fig = px.pie(
            spending_share,
            names="Travel_Reason",
            values="Total",
            hole=0.55,
            color_discrete_sequence=COLORS,
            custom_data=["Records", "Share"],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b>"
                "<br>Total: $%{value:,.2f}"
                "<br>Share: %{customdata[1]:.1f}%"
                "<br>Records: %{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(height=460)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Top destination-purpose combinations")

        top_combinations = (
            filtered_df.groupby(
                ["Destination", "Travel_Reason"],
                as_index=False,
            )
            .agg(Total=("Expenses", "sum"))
            .nlargest(10, "Total")
            .sort_values("Total")
        )

        fig = px.bar(
            top_combinations,
            x="Total",
            y="Destination",
            color="Travel_Reason",
            orientation="h",
            color_discrete_sequence=COLORS,
        )

        fig.update_layout(
            xaxis_title="Total spending ($)",
            yaxis_title=None,
            legend_title="Purpose",
        )

        fig = style_chart(fig, 460)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(fig, use_container_width=True)


# Spending patterns
with patterns:
    st.subheader("Expenditure distribution")

    fig = px.histogram(
        filtered_df,
        x="Expenses",
        color="Travel_Reason",
        nbins=40,
        opacity=0.65,
        color_discrete_sequence=COLORS,
    )

    fig.update_layout(
        barmode="overlay",
        xaxis_title="Spending ($)",
        yaxis_title="Frequency",
    )

    fig = style_chart(fig, 450)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True)

    # Log-normal distribution
    st.divider()
    st.subheader("Log-normal distribution")

    log_data = filtered_df.loc[
        filtered_df["Expenses"] > 0,
        "Expenses",
    ].dropna()

    if len(log_data) >= 10 and log_data.nunique() > 1:
        shape, loc, scale = stats.lognorm.fit(log_data, floc=0)

        bin_count = 40
        bin_edges = np.histogram_bin_edges(log_data, bins=bin_count)
        bin_width = bin_edges[1] - bin_edges[0]

        x_values = np.linspace(
            log_data.min(),
            log_data.quantile(0.99),
            300,
        )

        expected_frequency = (
            stats.lognorm.pdf(
                x_values,
                shape,
                loc=loc,
                scale=scale,
            )
            * len(log_data)
            * bin_width
        )

        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=log_data,
                xbins=dict(
                    start=bin_edges[0],
                    end=bin_edges[-1],
                    size=bin_width,
                ),
                name="Observed",
                marker_color=PINK,
                opacity=0.65,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=expected_frequency,
                mode="lines",
                name="Fitted log-normal",
                line=dict(color=NAVY, width=3),
                hovertemplate=(
                    "Spending: $%{x:,.2f}"
                    "<br>Expected frequency: %{y:.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            barmode="overlay",
            xaxis_title="Spending ($)",
            yaxis_title="Frequency",
        )

        fig = style_chart(fig, 470)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(fig, use_container_width=True)

        log_values = np.log(log_data)

        c1, c2, c3 = st.columns(3)
        c1.metric("Positive records", f"{len(log_data):,}")
        c2.metric("Log-scale mean", f"{log_values.mean():.3f}")
        c3.metric("Log-scale SD", f"{log_values.std(ddof=1):.3f}")

        st.caption(
            "The fitted curve is compared with observed spending. "
            "Visual agreement alone does not establish that the data "
            "follow a log-normal distribution."
        )
    else:
        st.info(
            "At least 10 positive expenditure records with variation "
            "are needed."
        )

    # Violin chart
    st.divider()
    st.subheader("Spending by purpose")

    violin_data = filtered_df

    if len(violin_data) > 6000:
        violin_data = violin_data.sample(n=6000, random_state=42)

    fig = px.violin(
        violin_data,
        x="Travel_Reason",
        y="Expenses",
        color="Travel_Reason",
        box=False,
        points=False,
        color_discrete_sequence=COLORS,
    )

    fig.update_traces(meanline_visible=True)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Travel purpose",
        yaxis_title="Spending ($)",
    )

    fig = style_chart(fig, 490)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True)

    # Party size
    if "Pax" in filtered_df.columns:
        party_data = filtered_df.dropna(
            subset=["Pax", "Expenses"]
        ).copy()

        party_data = party_data[party_data["Pax"] > 0]

        if not party_data.empty:
            common_sizes = party_data["Pax"].value_counts().head(20).index
            party_data = party_data[
                party_data["Pax"].isin(common_sizes)
            ].copy()

            st.divider()
            st.subheader("Party size and spending")

            bubble_data = party_data

            if len(bubble_data) > 3500:
                bubble_data = bubble_data.sample(
                    n=3500,
                    random_state=42,
                )

            hover_cols = [
                col
                for col in ["Destination", "Accommodation"]
                if col in bubble_data.columns
            ]

            fig = px.scatter(
                bubble_data,
                x="Pax",
                y="Expenses",
                color="Travel_Reason",
                hover_data=hover_cols,
                opacity=0.65,
                color_discrete_sequence=COLORS,
            )

            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(width=0.5, color="white"),
                )
            )

            fig.update_layout(
                xaxis_title="Party size",
                yaxis_title="Spending ($)",
            )

            fig = style_chart(fig, 480)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")

            st.plotly_chart(fig, use_container_width=True)

            trend_data = party_data[["Pax", "Expenses"]].dropna()

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

                fig = px.scatter(
                    trend_data,
                    x="Pax",
                    y="Expenses",
                    opacity=0.25,
                    color_discrete_sequence=[PINK],
                )

                fig.add_trace(
                    go.Scatter(
                        x=x_line,
                        y=regression.intercept + regression.slope * x_line,
                        mode="lines",
                        name="Trend",
                        line=dict(color=NAVY, width=3),
                    )
                )

                fig.update_layout(
                    xaxis_title="Party size",
                    yaxis_title="Spending ($)",
                )

                fig = style_chart(fig, 460)
                fig.update_yaxes(tickprefix="$", tickformat=",.0f")

                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    f"Correlation: r = {regression.rvalue:.3f} | "
                    f"R² = {regression.rvalue**2:.3f} | "
                    f"Slope = {money(regression.slope)} per additional person"
                )

            party_summary = (
                party_data.groupby(
                    ["Pax", "Travel_Reason"],
                    as_index=False,
                )
                .agg(
                    Average=("Expenses", "mean"),
                    Median=("Expenses", "median"),
                    Records=("Expenses", "size"),
                )
                .sort_values("Pax")
            )

            fig = px.line(
                party_summary,
                x="Pax",
                y="Average",
                color="Travel_Reason",
                markers=True,
                custom_data=["Median", "Records"],
                color_discrete_sequence=COLORS,
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "Party size: %{x}"
                    "<br>Mean: $%{y:,.2f}"
                    "<br>Median: $%{customdata[0]:,.2f}"
                    "<br>Records: %{customdata[1]:,.0f}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Party size",
                yaxis_title="Average spending ($)",
            )

            fig = style_chart(fig, 460)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No valid party-size records are available.")
    else:
        st.info("The dataset has no party-size column.")

    # Cumulative distribution
    st.divider()
    st.subheader("Cumulative spending")

    fig = go.Figure()

    for reason in filtered_df["Travel_Reason"].unique():
        values = np.sort(
            filtered_df.loc[
                filtered_df["Travel_Reason"] == reason,
                "Expenses",
            ].dropna().to_numpy()
        )

        if len(values) < 5:
            continue

        fig.add_trace(
            go.Scatter(
                x=values,
                y=np.arange(1, len(values) + 1) / len(values),
                mode="lines",
                name=reason,
                line=dict(width=2),
            )
        )

    fig.update_layout(
        xaxis_title="Spending ($)",
        yaxis_title="Cumulative proportion",
        yaxis=dict(tickformat=".0%"),
    )

    fig = style_chart(fig, 450)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True)


# Statistical tests
with statistics_tab:
    st.subheader("Business vs Leisure/Vacation")

    business = filtered_df.loc[
        filtered_df["Travel_Reason"] == "Business",
        "Expenses",
    ].dropna().to_numpy()

    leisure = filtered_df.loc[
        filtered_df["Travel_Reason"] == "Leisure/Vacation",
        "Expenses",
    ].dropna().to_numpy()

    if len(business) >= 2 and len(leisure) >= 2:
        business_mean = business.mean()
        leisure_mean = leisure.mean()
        difference = business_mean - leisure_mean

        welch = stats.ttest_ind(
            business,
            leisure,
            equal_var=False,
        )

        effect_size = cohens_d(business, leisure)
        ci_low, ci_high = mean_difference_ci(business, leisure)

        c1, c2, c3 = st.columns(3)
        c1.metric("Business mean", money(business_mean))
        c2.metric("Leisure mean", money(leisure_mean))
        c3.metric("Mean difference", money(difference))

        c4, c5, c6 = st.columns(3)
        c4.metric("Welch p-value", p_value(welch.pvalue))
        c5.metric(
            "Cohen's d",
            f"{effect_size:.3f}" if pd.notna(effect_size) else "N/A",
        )
        c6.metric(
            "Sample sizes",
            f"{len(business):,} / {len(leisure):,}",
        )

        st.write(
            f"95% confidence interval for the mean difference: "
            f"{money(ci_low)} to {money(ci_high)}."
        )

        if welch.pvalue < 0.05:
            st.success(
                "The difference is statistically significant "
                "at the 5% level."
            )
        else:
            st.info(
                "The difference is not statistically significant "
                "at the 5% level."
            )

        st.caption(
            "Results use the current filters. Cohen's d measures the "
            "standardized difference in group means."
        )

        # Mean and confidence intervals
        st.divider()
        st.subheader("Mean spending with 95% confidence intervals")

        ci_data = (
            filtered_df.groupby("Travel_Reason", as_index=False)
            .agg(
                Mean=("Expenses", "mean"),
                SD=("Expenses", "std"),
                N=("Expenses", "count"),
            )
        )

        ci_data["SE"] = ci_data["SD"] / np.sqrt(ci_data["N"])

        ci_data["Margin"] = np.where(
            ci_data["N"] > 1,
            stats.t.ppf(0.975, ci_data["N"] - 1) * ci_data["SE"],
            0,
        )

        ci_data["Lower"] = ci_data["Mean"] - ci_data["Margin"]
        ci_data["Upper"] = ci_data["Mean"] + ci_data["Margin"]

        fig = go.Figure(
            go.Scatter(
                x=ci_data["Travel_Reason"],
                y=ci_data["Mean"],
                mode="lines+markers",
                name="Mean",
                line=dict(color=RED, width=3),
                marker=dict(size=10, color=CORAL),
                error_y=dict(
                    type="data",
                    array=ci_data["Margin"],
                    visible=True,
                    color=GREY,
                    thickness=1.5,
                    width=5,
                ),
                customdata=ci_data[["N", "Lower", "Upper"]].to_numpy(),
                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>Mean: $%{y:,.2f}"
                    "<br>Records: %{customdata[0]:,.0f}"
                    "<br>Lower CI: $%{customdata[1]:,.2f}"
                    "<br>Upper CI: $%{customdata[2]:,.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            xaxis_title="Travel purpose",
            yaxis_title="Mean spending ($)",
        )

        fig = style_chart(fig, 440)
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(fig, use_container_width=True)

        # Mean difference
        st.divider()
        st.subheader("Leisure to business")

        fig = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "total"],
                x=["Leisure mean", "Difference", "Business mean"],
                y=[leisure_mean, difference, 0],
                connector=dict(line=dict(color=LIGHT_PINK)),
                increasing=dict(marker=dict(color=CORAL)),
                decreasing=dict(marker=dict(color=DARK_RED)),
                totals=dict(marker=dict(color=RED)),
                text=[
                    money(leisure_mean),
                    money(difference),
                    money(business_mean),
                ],
                textposition="outside",
            )
        )

        fig.update_layout(
            yaxis_title="Mean spending ($)",
            showlegend=False,
        )

        fig = style_chart(fig, 440)
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(
            "Select Business and Leisure/Vacation, with at least "
            "two records in each group."
        )

    # Purpose profile
    st.divider()
    st.subheader("Purpose  profile")

    profile = (
        filtered_df.groupby("Travel_Reason")
        .agg(
            Mean=("Expenses", "mean"),
            Median=("Expenses", "median"),
            Maximum=("Expenses", "max"),
            Records=("Expenses", "size"),
        )
        .reset_index()
    )

    if len(profile) >= 2:
        measures = ["Mean", "Median", "Maximum", "Records"]

        for col in measures:
            low = profile[col].min()
            high = profile[col].max()

            profile[f"{col}_scaled"] = (
                (profile[col] - low) / (high - low)
                if high > low
                else 0.5
            )

        fig = go.Figure()

        for _, row in profile.iterrows():
            values = [row[f"{col}_scaled"] for col in measures]

            fig.add_trace(
                go.Scatterpolar(
                    r=values + [values[0]],
                    theta=measures + [measures[0]],
                    fill="toself",
                    name=row["Travel_Reason"],
                    opacity=0.4,
                    line=dict(width=2),
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                bgcolor="white",
            ),
            height=480,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        )

        st.plotly_chart(fig, use_container_width=True)


# Economic context
with economic:
    st.subheader("State economic indicators")

    economic_cols = [
        "Destination_State",
        "Per_Capita_Income",
        "Per_Capita_Disposable_Income",
        "Regional_Price_Parity",
    ]

    missing = [
        col for col in economic_cols
        if col not in filtered_df.columns
    ]

    if missing:
        st.info(f"Missing columns: {', '.join(missing)}")

    else:
        state_spending = (
            filtered_df.groupby("Destination_State", as_index=False)
            .agg(
                Average=("Expenses", "mean"),
                Median=("Expenses", "median"),
                Records=("Expenses", "size"),
            )
        )

        source_cols = economic_cols.copy()

        if "BEA_Reference_Year" in filtered_df.columns:
            source_cols.append("BEA_Reference_Year")

        economic_data = (
            filtered_df[source_cols]
            .dropna(subset=["Destination_State"])
            .drop_duplicates()
            .copy()
        )

        if "BEA_Reference_Year" in economic_data.columns:
            latest_year = economic_data["BEA_Reference_Year"].max()

            if pd.notna(latest_year):
                economic_data = economic_data[
                    economic_data["BEA_Reference_Year"] == latest_year
                ]

        economic_data = economic_data.drop_duplicates(
            subset=["Destination_State"]
        )

        merged = state_spending.merge(
            economic_data,
            on="Destination_State",
            how="left",
        )

        merged = merged.dropna(
            subset=["Regional_Price_Parity", "Average"]
        )

        if not merged.empty:
            fig = px.scatter(
                merged,
                x="Regional_Price_Parity",
                y="Average",
                size="Records",
                color="Destination_State",
                hover_name="Destination_State",
                size_max=38,
                custom_data=[
                    "Records",
                    "Median",
                    "Per_Capita_Income",
                    "Per_Capita_Disposable_Income",
                ],
                color_discrete_sequence=COLORS,
            )

            fig.update_traces(
                marker=dict(
                    opacity=0.85,
                    line=dict(color="white", width=1.5),
                ),
                hovertemplate=(
                    "<b>%{hovertext}</b>"
                    "<br>Price parity: %{x:.2f}"
                    "<br>Average spending: $%{y:,.2f}"
                    "<br>Records: %{customdata[0]:,.0f}"
                    "<br>Median: $%{customdata[1]:,.2f}"
                    "<br>Per-capita income: $%{customdata[2]:,.0f}"
                    "<br>Disposable income: $%{customdata[3]:,.0f}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                xaxis_title="Regional price parity",
                yaxis_title="Average spending ($)",
                showlegend=False,
            )

            fig = style_chart(fig, 480)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")

            st.plotly_chart(fig, use_container_width=True)

            # State-level relationship
            st.divider()
            st.subheader("Price parity and average spending")

            correlation_data = merged[
                ["Regional_Price_Parity", "Average"]
            ].dropna()

            if (
                len(correlation_data) >= 3
                and correlation_data["Regional_Price_Parity"].nunique() > 1
                and correlation_data["Average"].nunique() > 1
            ):
                correlation = stats.spearmanr(
                    correlation_data["Regional_Price_Parity"],
                    correlation_data["Average"],
                )

                c1, c2, c3 = st.columns(3)
                c1.metric("Spearman rho", f"{correlation.statistic:.3f}")
                c2.metric("P-value", p_value(correlation.pvalue))
                c3.metric("States", f"{len(correlation_data):,}")

                st.caption(
                    "This is an exploratory state-level relationship. "
                    "It does not establish causation, and a small number "
                    "of states limits the strength of the conclusion."
                )
            else:
                st.info(
                    "At least three states with varying values are needed."
                )

            # Economic table
            st.divider()
            display_data = merged.copy()

            for col in [
                "Average",
                "Median",
                "Per_Capita_Income",
                "Per_Capita_Disposable_Income",
            ]:
                if col in display_data.columns:
                    display_data[col] = display_data[col].map(money)

            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.warning("No matching economic records are available.")


# Explore data
with explore:
    st.subheader("Travel records")
    st.write(f"{len(filtered_df):,} records match the selected filters.")

    available_cols = filtered_df.columns.tolist()

    default_cols = [
        col for col in [
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
        if col in available_cols
    ]

    selected_cols = st.multiselect(
        "Columns to display",
        available_cols,
        default=default_cols,
    )

    if selected_cols:
        st.dataframe(
            filtered_df[selected_cols],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.download_button(
        "Download filtered data",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_travel_data.csv",
        mime="text/csv",
    )

    summary = (
        filtered_df.groupby("Travel_Reason", as_index=False)
        .agg(
            Records=("Expenses", "size"),
            Total=("Expenses", "sum"),
            Average=("Expenses", "mean"),
            Median=("Expenses", "median"),
            SD=("Expenses", "std"),
        )
    )

    st.download_button(
        "Download purpose summary",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="travel_summary.csv",
        mime="text/csv",
    )


st.divider()
st.caption(
    "US Travel Spending Analysis | "
   )
