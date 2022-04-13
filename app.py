import dash
from dash import dcc, html

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


if __name__ == '__main__':
    app.run_server(debug=True)
