import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Set option to view all columns when printing DataFrame in terminal

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# Clean the data

df = pd.read_csv("tweets.csv")
df["name"] = pd.Series(df["name"]).str.lower() # lowercase all names
df["date_time"] = pd.to_datetime(df["date_time"], dayfirst=True, format='mixed')
df = (
    df.groupby([df["date_time"].dt.date, "name"])[
        # .dt() is accessor object for Series values’ datetime-like
        # dt.date returns the date part of Timestamps without time and timezone information
        ["number_of_likes", "number_of_shares"]
    ]
    .mean()
    .astype(int)
)
df = df.reset_index()

# PREPARE APP

# Stylesheets
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)

# App layout
app.layout = html.Div(
    [
        html.Div(
          html.H1("My first Dash app", style={"textAlign": "center"}), className="row"
        ),
        html.Div(
          dcc.Graph(id="line-chart", figure={}), className="row"
        ),
        html.Div(
            dcc.Dropdown(
                id="my-dropdown",
                multi=True,
                options=[
                    {"label": x, "value": x}
                    for x in sorted(df["name"].unique())
                ],
                value=["taylorswift13", "cristiano", "jtimberlake"],
            ),
            className="three columns"
        ),
        html.Div(
            html.A(
                id="my-link",
                children="Click here to visit X.com",
                href="https://x.com",
                target="_blank",
            ),
            className="two columns"
        )
    ],
    className="row"
)

# CALLBACKS

@app.callback(
    Output(component_id="line-chart", component_property="figure"),
    Input(component_id="my-dropdown", component_property="value")
)
def update_graph(chosen_value):
    if len(chosen_value) == 0:
        return {}
    else:
        df_filtered = df[df["name"].isin(chosen_value)]
        fig = px.line(
            data_frame=df_filtered,
            x="date_time",
            y="number_of_likes",
            color="name",
            log_y=True,
            labels={
                "number_of_likes": "Likes",
                "date_time": "Date",
                "name": "Celebrity",
            }
        )
        return fig

# Run app

if __name__ == "__main__":
    app.run_server(debug=True) # in production, debug=False