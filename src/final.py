#!/usr/bin/env python
# coding: utf-8

# In[124]:


import pandas as pd


# In[125]:


df = pd.read_csv("full_data.csv")
# In[126]:


df = df.drop(columns = 'Unnamed: 0')


# In[127]:


df.columns = ['name','Spouse Name', 'Marriage Year', 'Count']


# In[128]:


from jupyter_dash import JupyterDash


# In[129]:


import dash
from dash import dcc
from dash import html


# In[131]:


JupyterDash.infer_jupyter_proxy_config()


# In[132]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# In[133]:


from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# Create server variable with Flask server object for use with gunicorn
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


# In[136]:


app.run_server(debug=False)


# In[ ]:




