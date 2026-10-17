from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

st.set_page_config(
    page_title="US Travellers Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Colors
NAVY = "#450A0A"
BLUE = "#DC2626"
TEAL = "#EF4444"
GOLD = "#F87171"
PURPLE = "#B91C1C"
RED = "#991B1B"
GREY = "#7F1D1D"
LIGHT_GREY = "#FECACA"
COLORS = ["#DC2626", "#EF4444", "#F87171", "#B91C1C", "#991B1B", "#FCA5A5"]

st.markdown("""
<style>
.stApp { background-color: #FEF2F2; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
h1, h2, h3 { color: #450A0A; }
div[data-testid="stMetric"] {
    background-color: white; border: 1px solid #FECACA;
    padding: 16px; border-radius: 10px;
}
div[data-testid="stMetricLabel"] { color: #7F1D1D; }
div[data-testid="stMetricValue"] { color: #450A0A; }
section[data-testid="stSidebar"] { background-color: #FEF2F2; }
</style>
""", unsafe_allow_html=True)

# Data loading
DATA_FILE = Path(__file__).parent / "travel_analysis_enriched.csv"

@st.cache_data
def load_data(file_path, modified_time):
    df = pd.read_csv(file_path)
    required = ["Travel_Reason", "Expenses"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["Expenses"] = pd.to_numeric(df["Expenses"], errors="coerce")
    df = df.dropna(subset=["Expenses", "Travel_Reason"]).copy()
    df = df[df["Expenses"] >= 0].reset_index(drop=True)

    for col in ["Travel_Reason", "City", "City_Clean", "Destination_State", "Accommodation"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().replace("", pd.NA)

    if "City_Clean" in df.columns:
        df["Destination"] = df["City_Clean"]
        if "City" in df.columns:
            df["Destination"] = df["Destination"].fillna(df["City"])
    elif "City" in df.columns:
        df["Destination"] = df["City"]
    elif "Destination_State" in df.columns:
        df["Destination"] = df["Destination_State"]
    else:
        df["Destination"] = "Unknown"

    df["Destination"] = df["Destination"].fillna("Unknown").astype(str)
    df["Travel_Reason"] = df["Travel_Reason"].astype(str)

    for col in ["Pax", "Per_Capita_Income", "Per_Capita_Disposable_Income",
                "Regional_Price_Parity", "BEA_Reference_Year"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

if not DATA_FILE.exists():
    st.error("Dataset not found. Place 'travel_analysis_enriched.csv' in the same folder.")
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

if df.empty:
    st.error("No valid expenditure records found.")
    st.stop()

# Helpers
def money(v):
    return "N/A" if pd.isna(v) else f"${v:,.2f}"

def p_value(v):
    if pd.isna(v): return "N/A"
    return f"{v:.3e}" if v < 0.001 else f"{v:.4f}"

def style_chart(fig, height=430):
    fig.update_layout(
        template="plotly_white", height=height,
        margin=dict(l=20, r=20, t=65, b=35),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=NAVY),
        title_font=dict(size=17, color=NAVY),
        hoverlabel=dict(bgcolor=NAVY, font_color="white", font_size=12),
    )
    fig.update_xaxes(showgrid=False, linecolor=LIGHT_GREY, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#FECACA", zeroline=False)
    return fig

def money_axis(fig, axis="y"):
    if axis == "y":
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    else:
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    return fig

def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2: return np.nan
    pv = ((len(a)-1)*np.var(a,ddof=1) + (len(b)-1)*np.var(b,ddof=1)) / (len(a)+len(b)-2)
    if pv <= 0: return np.nan
    return (np.mean(a) - np.mean(b)) / np.sqrt(pv)

# Header
st.title("US Travellers Analysis in Six States")
st.markdown("Interactive exploration of travel expenditure, purpose, destinations, party size, and economic indicators.")
st.caption("Exploratory data analysis | Interactive charts | Statistical comparisons")

# Sidebar
st.sidebar.title("Dashboard Filters")
reasons = sorted(df["Travel_Reason"].dropna().unique().tolist())
selected_reasons = st.sidebar.multiselect("Travel purpose", reasons, default=reasons)
destinations = sorted(df["Destination"].dropna().unique().tolist())
selected_destinations = st.sidebar.multiselect("Destination", destinations, default=destinations)
min_e, max_e = float(df["Expenses"].min()), float(df["Expenses"].max())
if min_e < max_e:
    expense_range = st.sidebar.slider("Expenditure range ($)", min_e, max_e, (min_e, max_e), format="$%.2f")
else:
    expense_range = (min_e, max_e)
st.sidebar.divider()

# Filter
filtered_df = df[
    df["Travel_Reason"].isin(selected_reasons)
    & df["Destination"].isin(selected_destinations)
    & df["Expenses"].between(expense_range[0], expense_range[1], inclusive="both")
].copy()

if filtered_df.empty:
    st.warning("No records match these filters.")
    st.stop()

# KPIs
st.subheader("Key indicators")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Travel records", f"{len(filtered_df):,}")
k2.metric("Average expenditure", money(filtered_df["Expenses"].mean()))
k3.metric("Median expenditure", money(filtered_df["Expenses"].median()))
k4.metric("Total expenditure", money(filtered_df["Expenses"].sum()))
st.divider()

# Tabs
overview, composition, patterns, statistics_tab, economic, explore = st.tabs(
    ["Overview", "Spending Composition", "Spending Patterns", "Statistical Tests", "Economic Context", "Explore Data"]
)

#  OVERVIEW

with overview:
    st.subheader("Average expenditure by travel purpose")
    purpose_summary = (
        filtered_df.groupby("Travel_Reason", as_index=False)
        .agg(Avg=("Expenses","mean"), Med=("Expenses","median"), N=("Expenses","size"))
        .sort_values("Avg")
    )
    fig = px.line(purpose_summary, x="Travel_Reason", y="Avg", markers=True,
                  custom_data=["Med","N"], title="Average Expenditure by Travel Purpose",
                  color_discrete_sequence=[BLUE])
    fig.update_traces(line=dict(width=3), marker=dict(size=11, color=TEAL),
        hovertemplate="<b>%{x}</b><br>Mean: $%{y:,.2f}<br>Median: $%{customdata[0]:,.2f}<br>Records: %{customdata[1]:,.0f}<extra></extra>")
    fig.update_layout(xaxis_title="Travel purpose", yaxis_title="Average expenditure ($)")
    st.plotly_chart(money_axis(style_chart(fig)), use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Destination rankings")
        dest_summary = filtered_df.groupby("Destination", as_index=False).agg(
            Avg=("Expenses","mean"), N=("Expenses","size"))
        top15 = filtered_df["Destination"].value_counts().head(15).index
        ranking = dest_summary[dest_summary["Destination"].isin(top15)].sort_values("Avg")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ranking["Avg"], y=ranking["Destination"], mode="lines",
            line=dict(color=LIGHT_GREY, width=2), hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=ranking["Avg"], y=ranking["Destination"], mode="markers",
            marker=dict(size=12, color=TEAL, line=dict(color="white", width=2)),
            customdata=ranking[["N"]].to_numpy(),
            text=ranking["Avg"].apply(money), textposition="top center",
            textfont=dict(size=10, color=NAVY),
            hovertemplate="<b>%{y}</b><br>Avg: $%{x:,.2f}<br>Records: %{customdata[0]:,.0f}<extra></extra>",
            showlegend=False))
        fig.update_layout(title="Avg Spending by Destination", xaxis_title="Avg expenditure ($)", yaxis_title=None)
        fig = style_chart(fig, 500)
        fig.update_xaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Record counts by purpose")
        rc = filtered_df["Travel_Reason"].value_counts().rename_axis("Travel_Reason").reset_index(name="N")
        fig = px.bar(rc, x="Travel_Reason", y="N", color="Travel_Reason",
                     color_discrete_sequence=COLORS, title="Records by Travel Purpose")
        fig.update_layout(showlegend=False, xaxis_title="Travel purpose", yaxis_title="Records")
        fig = style_chart(fig)
        fig.update_yaxes(tickformat=",")
        st.plotly_chart(fig, use_container_width=True)

    # Choropleth
    st.divider()
    st.subheader("Geographic distribution")
    if "Destination_State" in filtered_df.columns:
        sa = filtered_df.groupby("Destination_State", as_index=False).agg(
            Total=("Expenses","sum"), Avg=("Expenses","mean"), N=("Expenses","size"))
        fig = px.choropleth(sa, locations="Destination_State", locationmode="USA-states",
            color="Avg", hover_data={"Total":True,"N":True,"Destination_State":False},
            color_continuous_scale="Reds", scope="usa", title="Avg Expenditure by State",
            labels={"Avg":"Avg $","Destination_State":"State"})
        fig.update_layout(height=550, coloraxis_colorbar=dict(title="Avg $", tickprefix="$"),
                          geo=dict(showlakes=True, lakecolor="rgb(220,220,220)"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Destination_State column not available.")
        
        #COMPOSITION

with composition:
    st.subheader("Spending composition")
    ts = filtered_df.copy()
    top12 = ts["Destination"].value_counts().head(12).index
    ts["Dest_Group"] = np.where(ts["Destination"].isin(top12), ts["Destination"], "Other")
    tm = ts.groupby(["Travel_Reason","Dest_Group"], as_index=False).agg(
        Total=("Expenses","sum"), N=("Expenses","size"), Avg=("Expenses","mean"))
    fig = px.treemap(tm, path=["Travel_Reason","Dest_Group"], values="Total",
        color="Avg", color_continuous_scale="Reds", custom_data=["N","Avg"],
        title="Total Expenditure by Purpose & Destination")
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Total: $%{value:,.2f}<br>Records: %{customdata[0]:,.0f}<br>Avg: $%{customdata[1]:,.2f}<extra></extra>")
    fig.update_layout(height=560, coloraxis_colorbar=dict(title="Avg $", tickprefix="$"))
    st.plotly_chart(fig, use_container_width=True)

    sd = filtered_df.groupby("Travel_Reason", as_index=False).agg(Total=("Expenses","sum"), N=("Expenses","size"))
    sd["Share"] = sd["Total"] / sd["Total"].sum() * 100
    fig = px.pie(sd, names="Travel_Reason", values="Total", hole=0.55,
        color_discrete_sequence=COLORS, custom_data=["N","Share"], title="Contribution to Total")
    fig.update_traces(textposition="inside", textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Total: $%{value:,.2f}<br>Share: %{customdata[1]:.1f}%<br>Records: %{customdata[0]:,.0f}<extra></extra>")
    fig.update_layout(height=470)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    stk = filtered_df.groupby(["Destination","Travel_Reason"], as_index=False).agg(
        Total=("Expenses","sum")).sort_values("Total", ascending=False).head(10)
    fig = px.bar(stk, x="Total", y="Destination", color="Travel_Reason", orientation="h",
        color_discrete_sequence=COLORS, title="Top 10 Destinations: Spending by Purpose")
    fig.update_layout(xaxis_title="Total expenditure ($)", yaxis_title=None, legend_title="Purpose")
    fig = style_chart(fig, 500)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: PATTERNS

with patterns:
    # Histogram + KDE
    st.subheader("Expenditure histogram")
    fig = px.histogram(filtered_df, x="Expenses", color="Travel_Reason", nbins=40,
        opacity=0.6, color_discrete_sequence=COLORS, title="Expenditure Distribution")
    for reason in filtered_df["Travel_Reason"].unique():
        sub = filtered_df.loc[filtered_df["Travel_Reason"]==reason, "Expenses"]
        if len(sub) >= 10:
            kde = stats.gaussian_kde(sub)
            xr = np.linspace(sub.min(), sub.max(), 200)
            fig.add_trace(go.Scatter(x=xr, y=kde(xr)*len(sub)*20, mode="lines",
                name=f"{reason} KDE", line=dict(width=2.5), showlegend=False))
    fig.update_layout(barmode="overlay")
    fig = style_chart(fig, 480)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Violin
    st.subheader("Expenditure distribution (violin)")
    vd = filtered_df
    if len(vd) > 6000:
        vd = vd.sample(n=6000, random_state=42)
    fig = px.violin(vd, x="Travel_Reason", y="Expenses", color="Travel_Reason",
        box=False, points=False, color_discrete_sequence=COLORS,
        title="Expenditure Distribution by Purpose")
    fig.update_traces(meanline_visible=True)
    fig.update_layout(showlegend=False, xaxis_title="Travel purpose", yaxis_title="Expenditure ($)")
    fig = style_chart(fig, 520)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Party size
    if "Pax" in filtered_df.columns:
        pd_ = filtered_df.dropna(subset=["Pax","Expenses"]).copy()
        pd_ = pd_[pd_["Pax"] > 0]
        if not pd_.empty:
            cps = pd_["Pax"].value_counts().head(20).index
            pd_ = pd_[pd_["Pax"].isin(cps)].copy()

            # Bubble
            st.subheader("Bubble: party size vs spending")
            bd = pd_
            if len(bd) > 3500:
                bd = bd.sample(n=3500, random_state=42)
            hc = [c for c in ["Destination","Accommodation"] if c in bd.columns]
            fig = px.scatter(bd, x="Pax", y="Expenses", color="Travel_Reason",
                hover_data=hc, opacity=0.65, color_discrete_sequence=COLORS,
                title="Individual Expenditure vs Party Size")
            fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color="white")))
            fig.update_layout(xaxis_title="Party size", yaxis_title="Expenditure ($)")
            fig = style_chart(fig, 520)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")
            st.plotly_chart(fig, use_container_width=True)

            # Trend line
            st.subheader("Trend line")
            td = pd_[["Pax","Expenses"]].dropna()
            fig = px.scatter(td, x="Pax", y="Expenses", opacity=0.3,
                color_discrete_sequence=[BLUE], title="Party Size vs Expenditure")
            if len(td) >= 3 and td["Pax"].nunique() >= 2:
                reg = stats.linregress(td["Pax"], td["Expenses"])
                xl = np.linspace(td["Pax"].min(), td["Pax"].max(), 100)
                fig.add_trace(go.Scatter(x=xl, y=reg.intercept+reg.slope*xl, mode="lines",
                    name="Trend", line=dict(color=RED, width=3)))
                st.caption(f"r = {reg.rvalue:.3f} | R² = {reg.rvalue**2:.3f} | Slope = ${reg.slope:,.2f}/person")
            fig.update_layout(xaxis_title="Party size", yaxis_title="Expenditure ($)")
            fig = style_chart(fig, 500)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")
            st.plotly_chart(fig, use_container_width=True)

            # Avg by party size
            st.subheader("Avg spending by party size")
            ps = pd_.groupby(["Pax","Travel_Reason"], as_index=False).agg(
                Avg=("Expenses","mean"), Med=("Expenses","median"), N=("Expenses","size")).sort_values("Pax")
            fig = px.line(ps, x="Pax", y="Avg", color="Travel_Reason", markers=True,
                custom_data=["Med","N"], color_discrete_sequence=COLORS,
                title="Avg Expenditure by Party Size & Purpose")
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            fig.update_layout(xaxis_title="Party size", yaxis_title="Avg expenditure ($)")
            fig = style_chart(fig, 500)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid party-size data.")
    else:
        st.info("No Pax column in dataset.")

    # ECDF
    st.divider()
    st.subheader("Cumulative distribution (ECDF)")
    fig = go.Figure()
    for reason in filtered_df["Travel_Reason"].unique():
        sub = np.sort(filtered_df.loc[filtered_df["Travel_Reason"]==reason, "Expenses"].dropna().values)
        if len(sub) < 5: continue
        fig.add_trace(go.Scatter(x=sub, y=np.arange(1,len(sub)+1)/len(sub),
            mode="lines", name=reason, line=dict(width=2)))
    fig.update_layout(title="Cumulative Distribution of Expenditure",
        xaxis_title="Expenditure ($)", yaxis_title="Proportion", yaxis=dict(tickformat=".0%"))
    fig = style_chart(fig, 480)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)


#STATISTICAL TESTS

with statistics_tab:
    st.subheader("Business vs Leisure")
    business = filtered_df.loc[filtered_df["Travel_Reason"]=="Business", "Expenses"].dropna()
    leisure = filtered_df.loc[filtered_df["Travel_Reason"]=="Leisure/Vacation", "Expenses"].dropna()

    if len(business) >= 2 and len(leisure) >= 2:
        b_mean, l_mean = business.mean(), leisure.mean()
        diff = b_mean - l_mean
        welch = stats.ttest_ind(business, leisure, equal_var=False)
        d = cohens_d(business, leisure)

        c1, c2, c3 = st.columns(3)
        c1.metric("Business mean", money(b_mean))
        c2.metric("Leisure mean", money(l_mean))
        c3.metric("Difference", money(diff))

        c4, c5, c6 = st.columns(3)
        c4.metric("Welch p-value", p_value(welch.pvalue))
        c5.metric("Cohen's d", f"{d:.3f}" if pd.notna(d) else "N/A")
        c6.metric("Sample size (biz/leisure)", f"{len(business):,} / {len(leisure):,}")

        if welch.pvalue < 0.05:
            if pd.notna(d) and abs(d) >= 0.5:
                st.success(f"Significant and meaningful difference (d = {d:.3f}).")
            else:
                st.info(f"Significant but practically small (d = {d:.3f}).")
        else:
            st.info(f"No significant difference (p = {p_value(welch.pvalue)}).")
    else:
        st.warning("Need both Business and Leisure/Vacation with ≥ 2 records each.")

    # CI chart
    st.divider()
    st.subheader("Mean with 95% CI")
    ci = filtered_df.groupby("Travel_Reason", as_index=False).agg(
        Mean=("Expenses","mean"), SD=("Expenses","std"), N=("Expenses","count"))
    ci["SE"] = ci["SD"] / np.sqrt(ci["N"])
    ci["Margin"] = 0.0
    v = ci["N"] > 1
    ci.loc[v, "Margin"] = stats.t.ppf(0.975, ci.loc[v, "N"]-1) * ci.loc[v, "SE"]
    ci["Lower"] = ci["Mean"] - ci["Margin"]
    ci["Upper"] = ci["Mean"] + ci["Margin"]

    fig = go.Figure(go.Scatter(
        x=ci["Travel_Reason"], y=ci["Mean"], mode="lines+markers", name="Mean",
        line=dict(color=BLUE, width=3), marker=dict(size=10, color=TEAL),
        error_y=dict(type="data", array=ci["Margin"], visible=True, color=GREY, thickness=1.5, width=5),
        customdata=ci[["N","Lower","Upper"]].to_numpy(),
        hovertemplate="<b>%{x}</b><br>Mean: $%{y:,.2f}<br>N: %{customdata[0]:,.0f}<br>CI: $%{customdata[1]:,.2f}–$%{customdata[2]:,.2f}<extra></extra>"))
    fig.update_layout(title="Avg Expenditure & 95% CI", xaxis_title="Purpose", yaxis_title="Mean ($)")
    fig = style_chart(fig, 470)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

    # Waterfall
    st.divider()
    st.subheader("Waterfall: leisure → business")
    if len(business) >= 2 and len(leisure) >= 2:
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=["absolute","relative","total"],
            x=["Leisure mean","Difference","Business mean"],
            y=[leisure.mean(), business.mean()-leisure.mean(), 0],
            connector=dict(line=dict(color=LIGHT_GREY)),
            increasing=dict(marker=dict(color=TEAL)),
            decreasing=dict(marker=dict(color=RED)),
            totals=dict(marker=dict(color=BLUE)),
            text=[money(leisure.mean()), money(business.mean()-leisure.mean()), money(business.mean())],
            textposition="outside"))
        fig.update_layout(title="Leisure → Business", yaxis_title="Mean ($)", showlegend=False)
        fig = style_chart(fig, 470)
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)

    # Radar
    st.divider()
    st.subheader("Radar: purpose profile")
    rd = filtered_df.groupby("Travel_Reason").agg(
        Mean=("Expenses","mean"), Median=("Expenses","median"),
        Max=("Expenses","max"), Records=("Expenses","size")).reset_index()
    if len(rd) >= 2:
        for col in ["Mean","Median","Max","Records"]:
            mn, mx = rd[col].min(), rd[col].max()
            rd[f"{col}_n"] = (rd[col]-mn)/(mx-mn) if mx > mn else 0.5
        cats = ["Mean","Median","Max","Records"]
        fig = go.Figure()
        for _, row in rd.iterrows():
            vals = [row[f"{c}_n"] for c in cats] + [row[f"{cats[0]}_n"]]
            fig.add_trace(go.Scatterpolar(r=vals, theta=cats+[cats[0]], fill="toself",
                name=row["Travel_Reason"], opacity=0.35, line=dict(width=2)))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1]), bgcolor="white"),
            height=500, title="Normalized Profile by Purpose",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need ≥ 2 purposes for radar.")


#ECONOMIC CONTEXT

with economic:
    st.subheader("Destination economics")
    econ_cols = ["Destination_State","Per_Capita_Income","Per_Capita_Disposable_Income","Regional_Price_Parity"]
    missing = [c for c in econ_cols if c not in filtered_df.columns]
    if missing:
        st.info(f"Missing: {', '.join(missing)}")
    else:
        ss = filtered_df.groupby("Destination_State", as_index=False).agg(
            Avg=("Expenses","mean"), Med=("Expenses","median"), N=("Expenses","size"))
        ef = econ_cols.copy()
        if "BEA_Reference_Year" in filtered_df.columns:
            ef.append("BEA_Reference_Year")
        es = filtered_df[ef].dropna(subset=["Destination_State"]).drop_duplicates().copy()
        if "BEA_Reference_Year" in es.columns:
            ly = es["BEA_Reference_Year"].max()
            if pd.notna(ly):
                es = es[es["BEA_Reference_Year"]==ly]
        es = es.drop_duplicates(subset=["Destination_State"])
        em = ss.merge(es, on="Destination_State", how="left").dropna(
            subset=["Regional_Price_Parity","Avg"])

        if len(em) >= 1:
            fig = px.scatter(em, x="Regional_Price_Parity", y="Avg", size="N",
                color="Destination_State", hover_name="Destination_State", size_max=38,
                custom_data=["N","Med","Per_Capita_Income","Per_Capita_Disposable_Income"],
                color_discrete_sequence=COLORS, title="Economic Context")
            fig.update_traces(marker=dict(opacity=0.85, line=dict(color="white", width=1.5)))
            fig.update_layout(xaxis_title="Price parity", yaxis_title="Avg expenditure ($)", showlegend=False)
            fig = style_chart(fig, 510)
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")
            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            corr_cands = ["Expenses","Pax","Per_Capita_Income","Per_Capita_Disposable_Income","Regional_Price_Parity"]
            avail = [c for c in corr_cands if c in filtered_df.columns and filtered_df[c].notna().sum() > 1]
            if len(avail) >= 2:
                cm = filtered_df[avail].corr(method="spearman")
                fig = px.imshow(cm, text_auto=".2f", color_continuous_scale="RdBu",
                    zmin=-1, zmax=1, aspect="auto", title="Spearman Correlation")
                fig.update_layout(height=520, coloraxis_colorbar=dict(title="rho"))
                st.plotly_chart(fig, use_container_width=True)

            st.divider()
            cd = em[["Regional_Price_Parity","Avg"]].dropna()
            if len(cd) >= 3 and cd["Regional_Price_Parity"].nunique() > 1:
                r = stats.spearmanr(cd["Regional_Price_Parity"], cd["Avg"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Spearman rho", f"{r.statistic:.3f}")
                c2.metric("P-value", p_value(r.pvalue))
                c3.metric("Destinations", f"{len(cd):,}")
            else:
                st.info("Need ≥ 3 destinations for correlation test.")

            st.divider()
            ed = em.copy()
            for c in ["Avg","Med","Per_Capita_Income","Per_Capita_Disposable_Income"]:
                if c in ed.columns:
                    ed[c] = ed[c].map(money)
            st.dataframe(ed, use_container_width=True, hide_index=True)
        else:
            st.warning("No matching economic data under current filters.")


# EXPLORE

with explore:
    st.subheader("Explore records")
    st.write(f"**{len(filtered_df):,} records** match current filters.")
    avail_cols = filtered_df.columns.tolist()
    defaults = [c for c in ["Respondent","Travel_Reason","Expenses","Destination",
        "Destination_State","Accommodation","Pax","Per_Capita_Income",
        "Per_Capita_Disposable_Income","Regional_Price_Parity","BEA_Reference_Year"] if c in avail_cols]
    chosen = st.multiselect("Columns", avail_cols, default=defaults)
    if chosen:
        st.dataframe(filtered_df[chosen], use_container_width=True, hide_index=True)

    st.divider()
    st.download_button("Download filtered CSV",
        filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered.csv", mime="text/csv")
    pe = filtered_df.groupby("Travel_Reason", as_index=False).agg(
        N=("Expenses","size"), Total=("Expenses","sum"), Avg=("Expenses","mean"),
        Med=("Expenses","median"), SD=("Expenses","std"))
    st.download_button("Download summary CSV",
        pe.to_csv(index=False).encode("utf-8"),
        file_name="summary.csv", mime="text/csv")

st.divider()
st.caption("Travel Spend Analytics | Results describe the filtered dataset only.")   
