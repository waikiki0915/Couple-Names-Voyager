import pandas as pd
df = pd.read_csv("df.csv")
df = df.sort_values(by = ['name','Count_overall','Marriage Year'], ascending=[False, False, True])
top1pair_perYear = pd.read_csv("top1pair_perYear.csv")
top15 = pd.read_csv("top15.csv")
top15.columns = ['name','Spouse Name', 'Count']
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
server = app.server

markdown_text1 = '''
- We showcase a 163-year trend of marriage couple names in King County, providing a fun and informative way to explore historical naming trends for couples.
- With this tool, you can delve into the fascinating world of marriage names and discover how they've changed over time.
- To reveal the underlying name patterns and uncover people's (subconscious) name preferences.
- A deeper understanding of the cultural, historical, and social aspects that influence name choices in relationships.
- For comprehensive details and additional information about this project, we invite you to visit our [GitHub repository](https://github.com/cse512-23s/Couple-Names-Voyager/).
'''

markdown_text2 = '''
### Overall Trend 
- By showing the top 1 marriage couple name per year, you can witness their evolution across time. Additionally,
you can check [Baby Names Voyager](https://namerology.com/baby-name-grapher/) to see how those popular names become top marriage names 30 years later.
'''


markdown_text3 = '''
### Cultural and Historical Trend
- Now, let's delve into the rich tapestry of data encompassing 1.2 million marriage records, allowing us to explore the cultural, historical, and social factors that shape name choices within relationships.
- You can enter a Latin American/Asian/Arabic name and see their changes over time because of racial population makeup shift
- You can enter your own first name to embark on a personal exploration! 
'''

colors = {
    'background': '#F3F6FA',
    'text': '#333333',
    'accent': '#3366CC'
}


app.layout = html.Div(
    [  
    
    html.H1(children='Couple Names Voyager', style={
                'text-align': 'center',
                'margin-bottom': '20px',
                'color': colors['accent']
            }),
    html.Div([
    dcc.Markdown(children=markdown_text1,style={'margin-bottom': '30px'},)
]),
        html.Div([
    dcc.Markdown(children=markdown_text2,style={'margin-bottom': '30px'})
]),
    dcc.Graph(id='overall'),
    
    html.Div([
    dcc.Markdown(children=markdown_text3, style={'margin-bottom': '30px'})
]),

    html.H4(children='''
        Enter a first name, and discover the evolving pattern of their spouse's name over time! 
    ''',style={'margin-bottom': '10px', 'color': colors['accent']}),
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['name'].unique(),
                'John',
                id='input_name', 
                placeholder="Type/Choose a first name"
            ),
            dcc.Graph(id='pie')
    ]),
    html.H5(children='''
        Choose "count" or "percentage" to see the evolving pattern: 
    ''',style={ 'margin-top': '30px', 'color': colors['accent']}),
            dcc.RadioItems(
                ['Count', 'Percentage'],
                'Count',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '60%', 'display': 'inline-block'}),
    
    dcc.Graph(id='graphic')
], style={
        'font-family': 'Open Sans, sans-serif',
        'padding': '20px',
        'background-color': colors['background'],
        'color': colors['text']
    })



@app.callback(
    Output('overall', 'figure'),
    Input('input_name', 'value'))
def update_graph(column_name):
    fig = px.scatter(top1pair_perYear, x="Marriage Year", y="Count", hover_data=['Name Pair'],color="Person A name",
                  text = 'Name Pair')
    fig.update_layout(title='Unveiling the Reigning Duo: The Top Marriage Name Pair of Each Year',
                  xaxis_title="Marriage Year",
    yaxis_title="Count",
    legend_title="Popular Names", height=800,width=1200)
    fig.update_traces(textposition='top center',textfont_size=9)
    return fig

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



