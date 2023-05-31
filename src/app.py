import pandas as pd
df = pd.read_csv("df.csv")
top1pair_perYear = pd.read_csv("top1pair_perYear.csv")
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server = app.server
markdown_text1 = '''
- We showcase a 163-year trend of marriage couple names in King County, providing a fun and informative way to explore historical naming trends for couples.
- With this tool, you can delve into the fascinating world of marriage names and discover how they've changed over time.
- To reveal the underlying name patterns and uncover people's (subconscious) name preferences.
- A deeper understanding of the cultural, historical, and social aspects that influence name choices in relationships.
'''

markdown_text2 = '''
### Overall Trend 
- By showing the top 1 marriage couple name per year, you can discover how they've changed over time. Additionally,
you can check [Baby Names Voyager](https://namerology.com/baby-name-grapher/) to see how those popular names become top marriage names 30 years later.
'''


markdown_text3 = '''
### Cultural and Historical Trend
- Now let's play around the data (1.2 million marriage records) and see the cultural, historical, and social aspects that influence name choices in relationships.
- You can enter a Latin American/Asian/Arabic name and see their changes over time because of racial population makeup shift
- You can enter your own first name to see if it make sense to you! 
'''


app.layout = html.Div([
   
    html.H1(children='Couple Names Voyager'),
    html.Div([
    dcc.Markdown(children=markdown_text1)
]),
        html.Div([
    dcc.Markdown(children=markdown_text2)
]),
    dcc.Graph(id='overall'),
    
    html.Div([
    dcc.Markdown(children=markdown_text3)
]),

    html.Div(children='''
        Enter a first name, and discover the evolving pattern of their spouse's name over time! 
    '''),
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['name'].unique(),
                'John',
                id='input_name', 
                placeholder="Type/Choose a first name"
            ),
            dcc.RadioItems(
                ['Count', 'Percentage'],
                'Count',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='graphic')
])


@app.callback(
    Output('overall', 'figure'),
    Input('input_name', 'value'))
def update_graph(column_name):
    fig = px.scatter(top1pair_perYear, x="Marriage Year", y="Count", hover_data=['Name Pair'],color="Person A name",
                  text = 'Name Pair')
    fig.update_layout(title='Top 1 marriage name pair per year',
                  xaxis_title="Marriage Year",
    yaxis_title="Count",
    legend_title="Popular Names", height=800,width=1000)
    fig.update_traces(textposition='top center',textfont_size=9)
    return fig


@app.callback(
    Output('graphic', 'figure'),
    Input('input_name', 'value'),
Input('crossfilter-yaxis-type', 'value'))
def update_graph2(column_name, yaxis):
    dff = df[df['name'] == column_name]
    fig = px.line(dff, x="Marriage Year", y= yaxis, color="Spouse Name")
    fig.update_layout(title= column_name + "'s spouse name pattern over time")
    if yaxis == 'Percentage':
         fig.layout.yaxis.tickformat = ',.1%'
    fig.update_yaxes(title=yaxis)
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)



