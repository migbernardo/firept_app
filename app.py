import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

data_dir = os.path.join(os.path.abspath(os.curdir), 'data')
assets_dir = os.path.join(os.path.abspath(os.curdir), 'assets')

df = pd.read_csv(os.path.join(data_dir, 'main_data.csv'), low_memory=False)
df.drop('Unnamed: 0', axis=1, inplace=True)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([html.H1('TITLE')], className='container_row'),

    html.Div([dcc.Slider(2001, 2018, 1, value=2001, marks=None,
                         tooltip={"placement": "bottom", "always_visible": True},
                         id='slider')], className='container_row'),

    html.Div([
        html.Div([

            html.Div([
                html.Center([
                    html.Div([dcc.Graph(figure={}, id='sun')], className='column', style={'width': '50%'}),
                    html.Div([dcc.Graph(figure={}, id='barplot')], className='column', style={'width': '50%'})
                ])
            ], className='row'),

            html.Div([html.H4('SOMETHING'),
                      dcc.RangeSlider(2001, 2018, 1, value=[2001, 2003], marks=None,
                                      tooltip={"placement": "bottom", "always_visible": True}, dots=True, pushable=2,
                                      id='range_slider')], className='row'),

            html.Div([
                html.Div([dcc.Graph(figure={}, id='sankey')], className='column', style={'width': '50%'}),
                html.Div([dcc.Graph(figure={}, id='barplot2')], className='column', style={'width': '50%'}),
            ], className='row'),

        ], className='column', style={'width': '75%'}),

        html.Div([dcc.Graph(figure={}, id='map')],
                 className='column', style={'width': '25%'}),
    ], className='container_row'),

    html.Div([html.H4('SOURCES/AUTHORS')], className='container_row'),

], className='container')


@app.callback(
    Output(component_id='barplot', component_property='figure'),
    Input(component_id='slider', component_property='value')
)
def bar_update(year):
    bardata = df[df['year'] == year].groupby('region').agg('sum')
    zone = []

    for i in bardata.index:
        if i == 'Aveiro':
            zone.append('North')
        elif i == 'Beja':
            zone.append('South')
        elif i == 'Braga':
            zone.append('North')
        elif i == 'Bragança':
            zone.append('North')
        elif i == 'Castelo Branco':
            zone.append('Center')
        elif i == 'Coimbra':
            zone.append('Center')
        elif i == 'Faro':
            zone.append('South')
        elif i == 'Guarda':
            zone.append('North')
        elif i == 'Leiria':
            zone.append('Center')
        elif i == 'Lisboa':
            zone.append('Center')
        elif i == 'Portalegre':
            zone.append('Center')
        elif i == 'Porto':
            zone.append('North')
        elif i == 'Santarém':
            zone.append('Center')
        elif i == 'Setúbal':
            zone.append('South')
        elif i == 'Viana do Castelo':
            zone.append('North')
        elif i == 'Vila Real':
            zone.append('North')
        elif i == 'Viseu':
            zone.append('North')
        elif i == 'Évora':
            zone.append('South')

    bardata['zone'] = zone

    fig = px.bar(bardata, x=bardata.index, y="total_ba", color='zone',
                 text_auto='.2s',
                 labels={"region": "Region", "total_ba": "Burnt Area", "zone": "Zone"},
                 color_discrete_map={"North": "seagreen", "South": "lightseagreen", "Center": "burlywood"})

    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
