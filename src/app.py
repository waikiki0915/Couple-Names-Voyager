import pandas as pd
df = pd.read_csv("full_data.csv")
df = df.drop(columns = 'Unnamed: 0')
df.columns = ['name','Spouse Name', 'Marriage Year', 'Count']
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['name'].unique(),
                'John',
                id='input_name'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='graphic')
])


@app.callback(
    Output('graphic', 'figure'),
    Input('input_name', 'value'))
def update_graph(column_name):
    dff = df[df['name'] == column_name]
    fig = px.line(dff, x="Marriage Year", y="Count", color = 'Spouse Name', symbol="Spouse Name")
    fig.update_layout(title= column_name + "'s spouse name pattern over time")
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)



