import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("world_cup_winners.csv")

winning_countries = df["Winners"].unique()

win_counts = df["Winners"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup Dashboard", style={"textAlign": "center"}),

    dcc.Graph(id="world_map"),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country_dropdown",
        options=[{"label": country, "value": country} for country in win_counts["Country"]],
        placeholder="Select a country...",
    ),

    html.Div(id="win_count_display", style={"fontSize": "20px", "marginTop": "10px"}),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        id="year_dropdown",
        options=[{"label": year, "value": year} for year in df["Year"].unique()],
        placeholder="Select a year...",
    ),

    html.Div(id="match_result", style={"fontSize": "20px", "marginTop": "10px"}),
])

@app.callback(
    Output("world_map", "figure"),
    Input("country_dropdown", "value")
)

def update_choropleth(selected_country):
    fig = px.choropleth(
        win_counts,
        locations="Country",
        locationmode="country names",
        color="Wins",
        title="World Cup Winners by Country",
        color_continuous_scale="greens"
    )
    return fig

@app.callback(
    Output("win_count_display", "children"),
    Input("country_dropdown", "value")
)

def update_win_count(selected_country):
    if selected_country:
        wins = win_counts[win_counts["Country"] == selected_country]["Wins"].values[0]
        return f"{selected_country} has won {wins} times."
    return ""

@app.callback(
    Output("match_result", "children"),
    Input("year_dropdown", "value")
)

def update_match_result(selected_year):
    if selected_year:
        match = df[df["Year"] == selected_year]
        if not match.empty:
            winner, runner_up = match.iloc[0]["Winners"], match.iloc[0]["Runners-up"]
            return f"In {selected_year}, {winner} won and {runner_up} was runner-up."
    return ""


if __name__ == "__main__":
    app.run_server(debug=True)
