import dash
from dash import html
import dash_cytoscape as cyto

app = dash.Dash(__name__)

elements = [
    {"data": {"id": "Dashboard", "label": "Dashboard"}},
    {"data": {"id": "Reports", "label": "Reports"}},
    {"data": {"id": "Settings", "label": "Settings"}},
    {"data": {"id": "Profile", "label": "Profile"}},
    {"data": {"id": "Security", "label": "Security"}},
    
    {"data": {"source": "Dashboard", "target": "Reports"}},
    {"data": {"source": "Dashboard", "target": "Settings"}},
    {"data": {"source": "Settings", "target": "Profile"}},
    {"data": {"source": "Settings", "target": "Security"}},
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='ia-graph',
        elements=elements,
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '600px'},
    )
])

if __name__ == '__main__':
    app.run(debug=True)
