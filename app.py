import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

data_dir = os.path.join(os.path.abspath(os.curdir), 'data')
assets_dir = os.path.join(os.path.abspath(os.curdir), 'assets')

df = pd.read_csv(os.path.join(data_dir, 'main_data.csv'), low_memory=False)
df.drop('Unnamed: 0', axis=1, inplace=True)
exp = pd.read_csv(os.path.join(data_dir, 'expenditure.csv'), low_memory=False)
regions = pd.read_excel(os.path.join(data_dir, 'regions.xlsx'))

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([html.H1('Fires in Portugal: An In-Depth Look')], className='title'),

    html.Div([html.H6('Environmental, human, and economic losses due to fires are an ever-present and increasing '
                      'threat in Portugal. ’Megafires’ similar to the 2017 Pedrógão Grande fire have been identified '
                      'by the EU Climate Action and Resource Efficiency Unit as a major concern, since they challenge '
                      'the suppression capacities of many wildfire protection programs. The unit indicates that '
                      'cultural perception and awareness of the risk of fires are critical to understanding and '
                      'managing fires, and should be integrated into fire-related policies at local, national, '
                      'and EU levels, empowered by local communities. This dashboard is presented to aid in the EU '
                      'call to action, and to reinforce the exchange of information and collaboration in regards to '
                      'fires within the Portuguese community.')]),

    html.Div([dcc.Slider(2001, 2018, 1, value=2001, marks={i: '{}'.format(i) for i in range(2001, 2019)},
                         tooltip={"placement": "bottom", "always_visible": True},
                         included=False,
                         id='slider', className='slider')], className='slider_box'),

    html.Div([

        html.Div([

            html.Div([
                html.H6('Title')
            ], className='text_box'),

            html.Div([

                html.Div([dcc.Graph(figure={}, id='barplot')], className='inner_column',
                         style={'width': '49%', 'margin': '0.5%'}),
                html.Div([dcc.Graph(figure={}, id='sun')], className='inner_column',
                         style={'width': '49%', 'margin': '0.5%'})
            ], className='graph_box'),

            html.Div([
                html.H4('TITLE'),
                dcc.RangeSlider(2001, 2018, 1, value=[2001, 2003],
                                marks={i: '{}'.format(i) for i in range(2001, 2019)},
                                tooltip={"placement": "bottom", "always_visible": True}, dots=True, pushable=2,
                                id='range_slider')
            ], className='range_slider_box'),

            html.Div([
                html.H6('Title')
            ], className='text_box'),

            html.Div([
                html.Div([dcc.Graph(figure={}, id='sankey')], className='inner_column',
                         style={'width': '49%', 'margin': '0.5%'}),
                html.Div([dcc.Graph(figure={}, id='barplot2')], className='inner_column',
                         style={'width': '49%', 'margin': '0.5%'})
            ], className='graph_box'),
        ], className='column', style={'width': '69%', 'margin': '0.5%'}),

        html.Div([
            html.Div([dcc.Graph(figure={}, id='map', style={'height': '100vh'})], className='map')
        ], className='column', style={'width': '29%', 'margin': '0.5%'})

    ], className='inner_box'),

    html.Div([html.H6('Title')], className='authors_box')

], className='box')


@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='slider', component_property='value')
)
def map_update(year):
    map_df = df[df['year'] == year].groupby('region').agg('sum')
    mapdata = map_df.merge(regions, left_on=map_df.index, right_on='region').set_index('region')

    fig = px.density_mapbox(mapdata, lat='lat', lon='lon', z=np.log(mapdata['total_ba']), radius=60,
                            center=dict(lat=39.557191, lon=-7.8536599), zoom=6,
                            opacity=1,
                            color_continuous_scale='solar_r',
                            mapbox_style="stamen-terrain")

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


@app.callback(
    Output(component_id='sun', component_property='figure'),
    Input(component_id='slider', component_property='value')
)
def sun_update(year):
    sundata = df[(df['year'] == year)]
    sundata = sundata[sundata['total_ba'] > 100]
    zona = []
    for i in list(sundata['region'].values):
        if i == 'Aveiro':
            zona.append('North')
        elif i == 'Beja':
            zona.append('South')
        elif i == 'Braga':
            zona.append('North')
        elif i == 'Bragança':
            zona.append('North')
        elif i == 'Castelo Branco':
            zona.append('Center')
        elif i == 'Coimbra':
            zona.append('Center')
        elif i == 'Faro':
            zona.append('South')
        elif i == 'Guarda':
            zona.append('North')
        elif i == 'Leiria':
            zona.append('Center')
        elif i == 'Lisboa':
            zona.append('Center')
        elif i == 'Portalegre':
            zona.append('Center')
        elif i == 'Porto':
            zona.append('North')
        elif i == 'Santarém':
            zona.append('Center')
        elif i == 'Setúbal':
            zona.append('South')
        elif i == 'Viana do Castelo':
            zona.append('North')
        elif i == 'Vila Real':
            zona.append('North')
        elif i == 'Viseu':
            zona.append('North')
        elif i == 'Évora':
            zona.append('South')

    sundata['zona'] = zona
    sundata = sundata.sort_values(by=['zona'])

    fig = px.sunburst(sundata, path=['region', 'county'], values='total_ba', color='zona',
                      labels={"region": "Portuguese Districts", "total_ba": "Burnt Area", "zona": "Zone"},
                      color_discrete_map={"North": "seagreen", "South": "lightseagreen", "Center": "burlywood"})

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


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


@app.callback(
    Output(component_id='sankey', component_property='figure'),
    Input(component_id='range_slider', component_property='value')
)
def sankey_update(years):
    sankeydata = df[(df['year'] >= years[0]) & (df['year'] <= years[1])].groupby(['main_cat', 'category']).agg(
        'sum')
    sankeydata.reset_index(inplace=True)
    pivot = sankeydata.pivot(index='main_cat', columns='category', values='total_ba')
    pivot = pivot.fillna(0)

    label = list(pivot.index) + list(pivot.columns)

    source = []
    for i in pivot.index:
        for j in range(len(pivot.columns)):
            source.append(list(pivot.index).index(i))

    target = []
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            shift = len(list(pivot.index))
            target.append(j + shift)

    value = []
    for i in range(len(pivot.index)):
        value.append(list(pivot.iloc[i, :].values))

    value = [item for sublist in value for item in sublist]

    colors_all = ["firebrick", "red", "orange", "darksalmon", "orangered", "tomato", "rosybrown", "goldenrod",
                  "darkred", "lightsalmon", "moccasin", "sienna", "orange", "maroon"]
    link_colors = [colors_all[i] for i in target]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
            color=colors_all
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colors
        ))])

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


@app.callback(
    Output(component_id='barplot2', component_property='figure'),
    Input(component_id='range_slider', component_property='value')
)
def bar2_update(years):
    bar2 = exp[(exp['year'] >= years[0]) & (exp['year'] <= years[1])]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=bar2['year'],
            y=bar2['total_ba'],
            fill='tozeroy',
            line_color='orange',
            name='Burnt Area (Hectare)'
        )
    )

    fig.add_trace(
        go.Bar(
            x=bar2['year'],
            y=bar2['expenditure'],
            name='Fire Brigade Expenditure (EUR)'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=bar2['year'],
            y=bar2['ratio'],
            marker_color='black',
            name='Expenditure per Burnt Area',
        ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Years")
    fig.update_yaxes(title_text="EUR / Hectare", secondary_y=False)
    fig.update_yaxes(title_text="Expenditure per Burnt Area", secondary_y=True)

    fig.update_layout(
        legend={'yanchor': 'top', 'y': 1.4, 'xanchor': 'left', 'x': 0.01},
        paper_bgcolor=None,
        plot_bgcolor=None,
        hovermode='x unified'
    )
    fig.update_xaxes(nticks=len(range(years[0], years[1] + 2)))
    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
