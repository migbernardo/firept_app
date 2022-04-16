import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# store dir paths
data_dir = os.path.join(os.path.abspath(os.curdir), 'data')
assets_dir = os.path.join(os.path.abspath(os.curdir), 'assets')

# load data
df = pd.read_csv(os.path.join(data_dir, 'main_data.csv'), low_memory=False)
df.drop('Unnamed: 0', axis=1, inplace=True)
exp = pd.read_csv(os.path.join(data_dir, 'expenditure.csv'), low_memory=False)
regions = pd.read_excel(os.path.join(data_dir, 'regions.xlsx'))

# app
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([

        html.Div([
            html.H1('Fires in Portugal: Sparking Smart Insights')
        ], className='column', style={'width': '50%'}),

        html.Div([
            html.Img(src=app.get_asset_url('ims_logo.png'), style={'height': '60px', 'width': 'auto', 'float': 'right'})
        ], className='column', style={'width': '50%'})

    ], className='header', style={'width': '100%', 'display': 'flex'}),

    html.Div([

        html.P([

            'Environmental, human, and economic losses due to fires are an ever-present and increasing '
            'threat in Portugal. ’Megafires’ similar to the 2017 Pedrógão Grande fire have been identified '
            'by the EU Climate Action and Resource Efficiency Unit as a major concern, since they challenge '
            'the suppression capacities of many wildfire protection programs. The unit indicates that '
            'cultural perception and awareness of the risk of fires are critical to understanding and '
            'managing fires, and should be integrated into fire-related policies at local, national, '
            'and EU levels, empowered by local communities. This dashboard is presented to aid in the EU '
            'call to action, and to reinforce the exchange of information and collaboration in regards to '
            'fires within the Portuguese community.'

        ], className='intro_text', style={'margin': '1%'})

    ], className='intro_box', style={'padding': '0.1px'}),

    html.Br(),

    html.Div([

        html.Div([

            html.Div([

                html.Div([

                    html.Div([

                        html.P('1. Burnt area (hectares) by region', style={'font-weight': 'bold'}),

                        dcc.Graph(figure={}, id='barplot'),

                        html.Br(),

                        html.Div([

                            html.P('Regions that had the most burnt area on the selected year',
                                   style={'text-align': 'center'}),

                        ], className='plot_text_box', style={'padding': '10px'}),

                    ], className='plot_box', style={'padding': '10px'})

                ], className='column', style={'width': '49%', 'margin-right': '0.5%'}),

                html.Div([

                    html.Div([

                        html.P('2. Number of fires by location', style={'font-weight': 'bold'}),

                        dcc.Graph(figure={}, id='sun'),

                        html.Br(),

                        html.Div([

                            html.P('Number of fires of each location (region and county) on the selected year',
                                   style={'text-align': 'center'}),

                        ], className='plot_text_box', style={'padding': '10px'}),

                    ], className='plot_box', style={'padding': '10px'})

                ], className='column', style={'width': '49%', 'margin-left': '0.5%'}),

            ], className='inner_col_box', style={'width': '100%', 'display': 'flex'}),

            html.Br(),

            html.Div([

                html.P('Select a range of years:'),

                html.P('(Figures 4 and 5 are affected)', style={'font-size': '70%', 'position': 'top'}),

                dcc.RangeSlider(2001,
                                2018,
                                1,
                                value=[2010, 2018],
                                marks={i: {'label': '{}'.format(i), 'style': {'color': 'black'}}
                                       for i in range(2001, 2019)},
                                dots=True,
                                pushable=2,
                                id='range_slider'
                                )

            ], className='range_slider_box', style={'padding': '10px', 'width': '97.3%', 'margin-right': '0.1%'}),

            html.Br(),

            html.Div([

                html.Div([

                    html.Div([

                        html.P('4. Burnt area (hectares) by category', style={'font-weight': 'bold'}),

                        dcc.Graph(figure={}, id='sankey'),

                        html.Br(),

                        html.Div([

                            html.P('Total burnt area split by each category and subcategory on the selected range',
                                   style={'text-align': 'center'})

                        ], className='plot_text_box', style={'padding': '10px'})

                    ], className='plot_box', style={'padding': '10px'})

                ], className='column', style={'width': '49%', 'margin-right': '0.5%'}),

                html.Div([

                    html.Div([

                        html.P('5. Fire brigade expenditure over the years', style={'font-weight': 'bold'}),

                        dcc.Graph(figure={}, id='barplot2'),

                        html.Br(),

                        html.Div([

                            html.P('Evolution of total burnt area and fire brigade expenditure on the selected range',
                                   style={'text-align': 'center'}),

                        ], className='plot_text_box', style={'padding': '10px'})

                    ], className='plot_box', style={'padding': '10px'})

                ], className='column', style={'width': '49%', 'margin-left': '0.5%'}),

            ], className='inner_col_box', style={'width': '100%', 'display': 'flex'}),

        ], className='column', style={'width': '70%'}),

        html.Div([

            html.Div([

                html.P('Select a year:'),

                html.P('(Figures 1 to 3 are affected)', style={'font-size': '70%', 'position': 'top'}),

                dcc.Dropdown(
                    list(range(2001, 2019)),
                    value=2007,
                    clearable=False,
                    id='dropdown'
                )

            ], className='dropdown_box', style={'padding': '10px'}),

            html.Br(),

            html.Div([

                html.P('3. Log of burnt area by region', style={'font-weight': 'bold'}),

                dcc.Graph(figure={}, id='map', style={'height': '84vh'}),

                html.Br(),

                html.Div([

                    html.P('Geographic distribution of the burnt areas on the selected year',
                           style={'text-align': 'center'}),

                ], className='mapbox_text_box', style={'padding': '10px'})

            ], className='map_box', style={'padding': '10px'}),

            html.Br(),

            html.Div([

                html.P('Authors:', style={'font-weight': 'bold'}),

                html.P('Bruno Mendes (20210627), Lucas Neves (20211020),'),

                html.P('Marjorie Kinney (20210647), Miguel Bernardo (20210580)'),

                html.P('Sources:', style={'font-weight': 'bold'}),

                html.A(href='https://www.icnf.pt/', children=[html.P('Instituto da Conservação da Natureza e das '
                                                                     'Florestas (ICNF)')]),

                html.A(href='https://op.europa.eu/en/publication-detail/-/publication/0b74e77d-f389-11e8-9982'
                            '-01aa75ed71a1/language-en/format-PDF/source-91693190',
                       children=[html.P('Publication Office of the EU (POEU)')]),

                html.A(href='https://www.pordata.pt/en/Portugal/Fire+Brigade+expenditure-1132',
                       children=[html.P('Pordata')])

            ], className='authors_box', style={'padding': '10px'}),

        ], className='column', style={'width': '30%'}),

    ], className='inner_box', style={'width': '100%', 'display': 'flex'})

], className='main_box', style={'margin': '1%'})


# map callback
@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def map_update(year):
    map_df = df[df['year'] == year].groupby('region').agg('sum')
    mapdata = map_df.merge(regions, left_on=map_df.index, right_on='region').set_index('region')

    fig = px.density_mapbox(mapdata,
                            lat='lat',
                            lon='lon',
                            z=np.round(np.log(mapdata['total_ba']), decimals=2),
                            radius=60,
                            labels={'z': ''},
                            hover_data={'region': mapdata.index,
                                        'burnt area': np.round(mapdata['total_ba'], decimals=2)},
                            center=dict(lat=39.557191, lon=-7.8536599), zoom=5.5,
                            opacity=1,
                            color_continuous_scale='solar_r',
                            mapbox_style="stamen-terrain"
                            )

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


# sunburst callback
@app.callback(
    Output(component_id='sun', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def sun_update(year):
    sundata = df[(df['year'] == year)]
    sundata = sundata.groupby(['region', 'county'])['code'].count().to_frame().reset_index()
    sundata["lower"] = sundata.groupby(['region'])['code'].transform(lambda x: x.quantile(0.1))
    sundata = sundata[sundata.code > sundata.lower]
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

    fig = px.sunburst(sundata,
                      path=['region', 'county'],
                      values='code',
                      color='zona',
                      labels={"region": "Portuguese Districts", "code": "# Fires", "zona": "Zone"},
                      color_discrete_map={"North": "seagreen", "South": "lightseagreen", "Center": "burlywood"})

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


# barplot callback
@app.callback(
    Output(component_id='barplot', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
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

    fig = px.bar(bardata,
                 x=bardata.index,
                 y="total_ba",
                 color='zone',
                 text_auto='.2s',
                 labels={"region": "Region", "total_ba": "Burnt Area", "zone": "Zone"},
                 color_discrete_map={"North": "seagreen", "South": "lightseagreen", "Center": "burlywood"})

    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


# sankey callback
@app.callback(
    Output(component_id='sankey', component_property='figure'),
    Input(component_id='range_slider', component_property='value')
)
def sankey_update(years):
    sankeydata = df[(df['year'] >= years[0]) & (df['year'] <= years[1])].groupby(['main_cat', 'category']).agg('sum')
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

    fig = go.Figure(data=[go.Sankey(node=dict(pad=15,
                                              thickness=20,
                                              line=dict(color="black", width=0.5),
                                              label=label,
                                              color=colors_all
                                              ),

                                    link=dict(source=source,
                                              target=target,
                                              value=value,
                                              color=link_colors
                                              )
                                    )
                          ]
                    )

    fig.update_layout(go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    return fig


# subplot callback
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
    fig.update_yaxes(title_text="EUR or Hectare", secondary_y=False)
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
