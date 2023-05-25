import pandas as pd
df = pd.read_csv("full_data.csv")
df = df.drop(columns = 'Unnamed: 0')
df.columns = ['name','Spouse Name', 'Marriage Year', 'Count']
top15 = pd.read_csv("top15.csv")
top15.columns = ['name','Spouse Name', 'Count']
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server = app.server

app.layout = html.Div([
  html.H1(children='Couple Names Voyager'),

    html.Div(children='''
        Enter a first name, and discover the evolving pattern of their spouse's name over time! 
    '''),  
  html.Div([

        html.Div([
            dcc.Dropdown(
                df['name'].unique(),
                'John',
                id='input_name'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='pie'),
    dcc.Graph(id='graphic')
])


@app.callback(
    Output('pie', 'figure'),
    Input('input_name', 'value'))
def update_graph(column_name):
    dff = top15[top15['name'] == column_name]
    fig = px.pie(dff, values='Count', names='Spouse Name', title= column_name + "'s Top Spouse Names")
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    return fig


@app.callback(
    Output('graphic', 'figure'),
    Input('input_name', 'value'))
def update_graph2(column_name):
    import plotly.graph_objects as go
    fig = go.Figure()
    dff = top15[top15['name'] == column_name]
    for nameb in dff["Spouse Name"].tolist():
        dff2 = df[(df["Spouse Name"] == nameb) & (df['name'] == column_name)]
        fig.add_trace(go.Scatter(x=dff2["Marriage Year"], y=dff2["Count"],
                        mode='lines',
                        name=nameb))
    fig.update_layout(title= column_name + "'s spouse name pattern over time")
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)



