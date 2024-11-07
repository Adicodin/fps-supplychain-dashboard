# fps_tab.py
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd

import IPDS_Data_Analysis as analysis

# FPS Tab Layout
def layout():
    return html.Div([

        # # Header
        # html.H1("Data Analysis Dashboard", className="text-center my-4 mb-2"),

        # Section for each figure and table in Bootstrap grid layout
        dbc.Row([  # Row 1
            html.H4("Yearly Analysis", className="text-center mx-auto my-4"),
            dbc.Col(
                dbc.Card([  # Card for Graph 1
                    dbc.CardHeader("Number of Transactions Each Year", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig1))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 2
                    dbc.CardHeader("Number of Unique Ration Card IDs Each Year", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig2))
                ]), width=6
            ),
        ], className="mb-4"),  # Padding between rows

        dbc.Row([  # Row 2
            dbc.Col(
                dbc.Card([  # Card for Table 1
                    dbc.CardHeader("Yearly Usage of Each Ration Card", className="text-center"),
                    dbc.CardBody(dash_table.DataTable(
                        id='rationcard-usage-table',
                        columns=[{'name': 'Ration Card No.', 'id': 'Ration Card No.'}] + [{"name": str(col), "id": str(col)} for col in analysis.rationcard_usage_per_year.columns],
                        data=analysis.rationcard_usage_per_year.reset_index().to_dict('records'),
                        style_table={'overflowX': 'auto', 'width': '100%'},
                        style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '5px'},
                        page_size=8
                    ))
                ]), width=12
            ),
        ], className="mb-4"),

        # Additional rows with graphs
        dbc.Row([  # Row 3
            dbc.Col(width=3),
            dbc.Col(
                dbc.Card([  # Card for Graph 3
                    dbc.CardHeader("Number of times portability is marked as 'Yes' each year", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig4))
                ]), width=6
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 4 - Monthly Analysis
            html.H4("Monthly Analysis", className="text-center mx-auto my-4"),
            dbc.Col(
                dbc.Card([  # Card for Graph 6
                    dbc.CardHeader("Number of transactions each month", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig6))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 7
                    dbc.CardHeader("Number of unique ration card IDs each month", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig7))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 8
                    dbc.CardHeader("Monthly usage of each ration card", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig8))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Table 2
                    dbc.CardHeader("Monthly usage of each ration card", className="text-center"),
                    dbc.CardBody(dash_table.DataTable(
                        id='rationcard-monthly-usage-table',
                        columns=[{'name': 'Ration Card No.', 'id': 'Ration Card No.'}] + [{"name": str(col), "id": str(col)} for col in analysis.rationcard_usage_per_month.columns],
                        data=analysis.rationcard_usage_per_month.reset_index().to_dict('records'),
                        style_table={'overflowX': 'auto', 'width': '100%'},
                        style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '5px'},
                        page_size=8
                    ))
                ]), width=12
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 5
            dbc.Col(
                dbc.Card([  # Card for Graph 9
                    dbc.CardHeader("Number of times portability is marked as 'Yes' each month", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig9))
                ]), width=6
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 6
            dbc.Col(
                dbc.Card([  # Card for Table 3
                    dbc.CardHeader("Monthly analysis of unused ration card", className="text-center"),
                    dbc.CardBody(dash_table.DataTable(
                        style_table={'overflowX': 'auto', 'width': '100%'},
                        style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '5px'},
                        page_size=8
                    ))
                ]), width=12
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 7 - Daily Analysis
            html.H4("Daily Analysis", className="text-center mx-auto my-4"),
            dbc.Col(
                dbc.Card([  # Card for Graph 8
                    dbc.CardHeader("Number of transactions each day", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig11))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 9
                    dbc.CardHeader("Number of unique ration card IDs each day", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig12))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 10
                    dbc.CardHeader("Daily usage of each ration card", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig13))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 11
                    dbc.CardHeader("Number of times portability is marked as 'Yes' each day", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig14))
                ]), width=6
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 7
            
            dbc.Col(
                dbc.Card([  # Card for Graph 12
                    dbc.CardHeader("Another Analysis - Figure 16", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig16))
                ]), width=6
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 8
            dbc.Col(
                dbc.Card([  # Card for Graph 13
                    dbc.CardHeader("Another Analysis - Figure 17", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig17))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 14
                    dbc.CardHeader("Another Analysis - Figure 18", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig18))
                ]), width=6
            ),
        ], className="mb-4"),

        dbc.Row([  # Row 9
            dbc.Col(
                dbc.Card([  # Card for Graph 15
                    dbc.CardHeader("Another Analysis - Figure 19", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig19))
                ]), width=6
            ),
            dbc.Col(
                dbc.Card([  # Card for Graph 16
                    dbc.CardHeader("Another Analysis - Figure 20", className="text-center"),
                    dbc.CardBody(dcc.Graph(figure=analysis.fig20))
                ]), width=6
            ),
        ], className="mb-4"),

    ], className="p-4 bg-light")
