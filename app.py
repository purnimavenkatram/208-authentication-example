import dash
import dash_auth
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Mickey': 'Mouse', 'Donald': 'Duck' , 'Daisy':'Duck'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='auth example'
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=2.5, step=0.1,
        marks={0: '0', 2.5: '2.5'},
        value=[0.5, 2]
    ),

    html.Div(id='graph-title'),
    dcc.Graph(id='graph'),
    html.A('Code on Github', href='https://github.com/purnimavenkatram/208-authentication-example'),
    html.Br(),
    html.A("Data Source", href='https://dash.plotly.com/authentication'),
], className='container')

@app.callback(
    Output('graph-title', 'children'),
    Output('graph', 'figure'),
    Input('range-slider', 'value'),
    )
def update_graph(slider_range):
    df = px.data.iris() # replace with your own data source
    low, high = slider_range
    mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(
        df[mask], x="sepal_width", y="sepal_length", 
        color="species", size='petal_length', 
        hover_data=['petal_width'])
    graph_title='Graph of filtered petal width of {}'.format(str(slider_range))
    return graph_title, fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
