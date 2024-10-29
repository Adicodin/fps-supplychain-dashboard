# supply_chain_tab.py
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample Data for Supply Chain (Replace with actual analytics data)
df_supply_chain = pd.DataFrame({
    "Stage": ["Procurement", "Production", "Distribution", "Retail"],
    "Cost": [500, 800, 300, 700]
})


# Supply Chain Tab Layout
def layout():
    return html.Div([
        html.H3("Supply Chain Analysis"),
        dcc.Graph(id="supply-chain-graph",
                  figure=px.line(df_supply_chain,
                                 x="Stage",
                                 y="Cost",
                                 title="Supply Chain Costs"))
    ])
