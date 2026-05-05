import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

#  Load cleaned data 
df = pd.read_csv("ev_clean.csv")

#  Design tokens 
COLORS = {
    "bg":        "#0E1117",
    "panel":     "#161A23",
    "panel_2":   "#1F2430",
    "text":      "#E6E8EE",
    "muted":     "#8B92A5",
    "accent":    "#00D4AA",   # signature teal
    "accent_2":  "#FF6B4A",   # warm coral
    "bev":       "#00D4AA",
    "phev":      "#FFB454",
    "border":    "#2A2F3D",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor=COLORS["panel"],
    plot_bgcolor=COLORS["panel"],
    font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"], size=12),
    margin=dict(l=50, r=20, t=50, b=40),
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"]),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"]),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"]),
    hoverlabel=dict(bgcolor=COLORS["panel_2"], font_size=12),
)

# Initialize app 
app = Dash(__name__, title="WA EV Dashboard")
server = app.server  # for deployment

#  Filter options 
year_min, year_max = int(df["Model Year"].min()), int(df["Model Year"].max())
counties = sorted(df["County"].dropna().unique().tolist())


# CHART BUILDERS


def fig_adoption_over_time(dff):
    """Chart 1: EV adoption over time, split by BEV vs PHEV."""
    g = dff.groupby(["Model Year", "EV Type Short"]).size().reset_index(name="count")
    fig = px.area(
        g, x="Model Year", y="count", color="EV Type Short",
        color_discrete_map={"BEV": COLORS["bev"], "PHEV": COLORS["phev"]},
        labels={"count": "Vehicles Registered", "Model Year": "Model Year",
                "EV Type Short": "Type"},
    )
    fig.update_traces(line=dict(width=2), mode="lines",
                      hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,}<extra></extra>")
    fig.update_layout(title="EV Adoption Over Time", **PLOTLY_LAYOUT)
    return fig


def fig_market_share(dff):
    """Chart 2: Top 10 manufacturers by market share."""
    top = dff["Make"].value_counts().head(10).reset_index()
    top.columns = ["Make", "count"]
    total = len(dff)
    top["share"] = (top["count"] / total * 100).round(1)
    top = top.sort_values("count")
    colors = [COLORS["accent"] if m == "TESLA" else COLORS["muted"] for m in top["Make"]]
    fig = go.Figure(go.Bar(
        x=top["count"], y=top["Make"], orientation="h",
        marker=dict(color=colors),
        text=[f"{s}%" for s in top["share"]],
        textposition="outside", textfont=dict(color=COLORS["text"]),
        hovertemplate="<b>%{y}</b><br>Vehicles: %{x:,}<br>Share: %{text}<extra></extra>",
    ))
    fig.update_layout(title="Top 10 Manufacturers by Market Share",
                      xaxis_title="Vehicles Registered", yaxis_title="",
                      **PLOTLY_LAYOUT)
    return fig


def fig_range_evolution(dff):
    """Chart 3: Electric range evolution over time, BEV vs PHEV."""
    valid = dff[dff["Electric Range Reported"].notna()].copy()
    valid["Electric Range Reported"] = valid["Electric Range Reported"].astype(float)
    g = (valid.groupby(["Model Year", "EV Type Short"])["Electric Range Reported"]
         .median().reset_index())
    fig = px.line(
        g, x="Model Year", y="Electric Range Reported", color="EV Type Short",
        markers=True,
        color_discrete_map={"BEV": COLORS["bev"], "PHEV": COLORS["phev"]},
        labels={"Electric Range Reported": "Median Range (miles)",
                "Model Year": "Model Year", "EV Type Short": "Type"},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8),
                      hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.0f} mi<extra></extra>")
    fig.update_layout(title="Electric Range Evolution (Median Miles)", **PLOTLY_LAYOUT)
    return fig


def fig_geography(dff):
    """Chart 4: Top counties by EV count."""
    g = dff["County"].value_counts().head(10).reset_index()
    g.columns = ["County", "count"]
    g = g.sort_values("count")
    fig = go.Figure(go.Bar(
        x=g["count"], y=g["County"], orientation="h",
        marker=dict(
            color=g["count"], colorscale=[[0, COLORS["panel_2"]], [1, COLORS["accent"]]],
            showscale=False,
        ),
        text=[f"{c:,}" for c in g["count"]],
        textposition="outside", textfont=dict(color=COLORS["text"]),
        hovertemplate="<b>%{y} County</b><br>Vehicles: %{x:,}<extra></extra>",
    ))
    fig.update_layout(title="Top 10 Counties by EV Registrations",
                      xaxis_title="Vehicles Registered", yaxis_title="",
                      **PLOTLY_LAYOUT)
    return fig


# LAYOUT


def stat_card(label, value, accent=False):
    return html.Div(
        className="stat-card" + (" stat-card-accent" if accent else ""),
        children=[
            html.Div(label, className="stat-label"),
            html.Div(value, className="stat-value"),
        ],
    )

app.layout = html.Div(className="app-shell", children=[
    # Header
    html.Header(className="header", children=[
        html.Div(className="header-inner", children=[
            html.Div(className="brand", children=[
                html.Div("WA·EV", className="brand-logo"),
                html.Div([
                    html.H1("Washington State EV Adoption", className="title"),
                    html.P("An interactive look at 280,000+ registered electric vehicles",
                           className="subtitle"),
                ]),
            ]),
            html.Div(className="header-meta", children=[
                html.Span("DATA STORYTELLING PROJECT", className="kicker"),
                html.Span(f"Years {year_min}–{year_max}", className="kicker-2"),
            ]),
        ]),
    ]),

    # KPI strip
    html.Section(className="kpi-row", children=[
        stat_card("Total Vehicles", f"{len(df):,}", accent=True),
        stat_card("Tesla Market Share",
                  f"{df[df['Make']=='TESLA'].shape[0]/len(df)*100:.1f}%"),
        stat_card("King County Share",
                  f"{df[df['County']=='King'].shape[0]/len(df)*100:.1f}%"),
        stat_card("BEV Share",
                  f"{df[df['EV Type Short']=='BEV'].shape[0]/len(df)*100:.1f}%"),
        stat_card("Unique Makes", f"{df['Make'].nunique()}"),
    ]),

    # Filters
    html.Section(className="filters", children=[
        html.Div(className="filter-group", children=[
            html.Label("Model Year Range", className="filter-label"),
            dcc.RangeSlider(
                id="year-slider",
                min=year_min, max=year_max, step=1,
                value=[year_min, year_max],
                marks={y: str(y) for y in range(year_min, year_max + 1, 2)},
                tooltip={"placement": "bottom", "always_visible": False},
            ),
        ]),
        html.Div(className="filter-row", children=[
            html.Div(className="filter-group-half", children=[
                html.Label("County", className="filter-label"),
                dcc.Dropdown(
                    id="county-dropdown",
                    options=[{"label": "All counties", "value": "ALL"}] +
                            [{"label": c, "value": c} for c in counties],
                    value="ALL", clearable=False, className="dropdown",
                ),
            ]),
            html.Div(className="filter-group-half", children=[
                html.Label("EV Type", className="filter-label"),
                dcc.RadioItems(
                    id="type-radio",
                    options=[
                        {"label": "All", "value": "ALL"},
                        {"label": "BEV only", "value": "BEV"},
                        {"label": "PHEV only", "value": "PHEV"},
                    ],
                    value="ALL", inline=True, className="radio-group",
                ),
            ]),
        ]),
    ]),

    # Story intro
    html.Section(className="narrative", children=[
        html.H2("The Story in Four Charts", className="section-title"),
        html.P(
            "Washington State has become one of America's clearest case studies in EV "
            "adoption: a tenfold rise in a decade, dominated by a single manufacturer, "
            "powered by dramatically improving range, and concentrated almost entirely "
            "in three counties. Use the filters above to explore each part of the story.",
            className="section-lead",
        ),
    ]),

    # Charts grid
    html.Section(className="charts-grid", children=[
        html.Div(className="chart-card", children=[
            html.Div(className="chart-num", children="01"),
            html.H3("Adoption is exploding", className="chart-title"),
            html.P("BEV registrations have outpaced PHEVs since 2018.",
                   className="chart-caption"),
            dcc.Graph(id="chart-adoption", config={"displayModeBar": False}),
        ]),
        html.Div(className="chart-card", children=[
            html.Div(className="chart-num", children="02"),
            html.H3("One brand dominates", className="chart-title"),
            html.P("Tesla holds more share than the next eight makers combined.",
                   className="chart-caption"),
            dcc.Graph(id="chart-market", config={"displayModeBar": False}),
        ]),
        html.Div(className="chart-card", children=[
            html.Div(className="chart-num", children="03"),
            html.H3("Range has tripled", className="chart-title"),
            html.P("Median BEV range climbed from ~75 mi (2013) to 290+ mi (2020).",
                   className="chart-caption"),
            dcc.Graph(id="chart-range", config={"displayModeBar": False}),
        ]),
        html.Div(className="chart-card", children=[
            html.Div(className="chart-num", children="04"),
            html.H3("Geography is concentrated", className="chart-title"),
            html.P("Nearly half of all WA EVs are registered in King County alone.",
                   className="chart-caption"),
            dcc.Graph(id="chart-geo", config={"displayModeBar": False}),
        ]),
    ]),

    # Footer
    html.Footer(className="footer", children=[
        html.Div("Data: Washington State Department of Licensing  ·  "
                 "Built with Dash + Plotly", className="footer-text"),
        html.Div("Data Visualization Project — Part 2: Charts & Dashboard",
                 className="footer-meta"),
    ]),
])


# CALLBACKS


@app.callback(
    [Output("chart-adoption", "figure"),
     Output("chart-market", "figure"),
     Output("chart-range", "figure"),
     Output("chart-geo", "figure")],
    [Input("year-slider", "value"),
     Input("county-dropdown", "value"),
     Input("type-radio", "value")],
)
def update_charts(year_range, county, ev_type):
    dff = df[(df["Model Year"] >= year_range[0]) &
             (df["Model Year"] <= year_range[1])]
    if county != "ALL":
        dff = dff[dff["County"] == county]
    if ev_type != "ALL":
        dff = dff[dff["EV Type Short"] == ev_type]

    if len(dff) == 0:
        empty = go.Figure().update_layout(
            title="No data for current filters", **PLOTLY_LAYOUT)
        return empty, empty, empty, empty

    return (fig_adoption_over_time(dff),
            fig_market_share(dff),
            fig_range_evolution(dff),
            fig_geography(dff))



# RUN

if __name__ == "__main__":
        app.run(debug=False, host="0.0.0.0", port=8050)
