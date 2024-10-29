# app.py
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import fps_tab  # Import FPS tab layout
import supply_chain_tab  # Import Supply Chain tab layout

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout with two tabs
app.layout = html.Div([
    html.H1("Project Dashboard"),
    dcc.Tabs(id="tabs",
             value="fps",
             children=[
                 dcc.Tab(label="FPS", value="fps"),
                 dcc.Tab(label="Supply Chain", value="supply_chain")
             ]),
    html.Div(id="tab-content")  # Placeholder for tab content
])


# Callback to control the tab content
@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "fps":
        return fps_tab.layout()
    elif tab == "supply_chain":
        return supply_chain_tab.layout()


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
