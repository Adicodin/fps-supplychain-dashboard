# fps_tab.py
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample Data for FPS (Replace with actual analytics data)
df_fps = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 20, 30, 40]
})


# FPS Tab Layout
def layout():
    return html.Div([
        html.H3("FPS Analysis"),
        dcc.Graph(id="fps-graph",
                  figure=px.bar(df_fps,
                                x="Category",
                                y="Value",
                                title="FPS Data"))
    ])
