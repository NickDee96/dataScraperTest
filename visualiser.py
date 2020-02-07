import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

df=pd.read_csv("data/output.csv")


def getPlot():
    df["Date"]=pd.to_datetime(df["Date"],format="%b %d %Y")
    fig = px.line(df, x='Date', y='Price')
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
## Setting up the DashBoard layout

app.layout = html.Div([
    html.H1(
        children="Henry Hub Natural Gas Spot Price (Dollars per Million Btu)",
        style={"justify":"center"}
    ),
    dcc.Graph(
        figure=getPlot()
    )
])
app.run_server(host="127.0.0.1",port=8050)