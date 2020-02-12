import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from jitcache import Cache

cache = Cache()
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Global Vaiables to control what data is stored
LA_DATA = pd.read_parquet('LA_2006_2019.parquet')
cd = LA_DATA
selectable_cities = cd.city.unique()
selectable_neighborhoods = cd.neighborhood.unique()
selectable_streets = cd.street.unique()
selectable_use = cd.use.unique()
cities = ["Los Angeles", "San Francisco", "New York City", "Denver",
          "Las Vegas", "Austin"]

# Main App
app.layout = html.Div([
    html.H1("PropertyScout", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label('Enter City Subdivison'),
            dcc.Dropdown(
                id='city-dropdown',
                multi=True,
                options=[{'label': i, 'value': i} for i in selectable_cities],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Label('Enter Neighborhood'),
            dcc.Dropdown(
                id='neighborhood-dropdown',
                multi=True,
                options=[{'label': i, 'value': i} for i in selectable_neighborhoods],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Label('Enter Street'),
            dcc.Dropdown(
                id='street-dropdown',
                multi=True,
                options=[{'label': i, 'value': i} for i in selectable_streets],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='assessor-values-over-time-series')]
        , style={'width': '90%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Property Use'),
            dcc.Checklist(
                id='uses-checkbox',
                options=[{'label': i, 'value': i} for i in selectable_use],
                value=selectable_use)]
        , style={'width': '9%', 'display': 'inline-block',
                 'top': '0%', 'position': 'absolute'})
        ], style={'position': 'relative'}
    ),

    html.Div(
        dcc.RangeSlider(
            id='filter-year-slider',
            min=cd['year'].min(),
            max=cd['year'].max(),
            value=[cd['year'].min(), cd['year'].max()],
            marks={str(year): str(year) for year in cd['year'].unique()},
            step=None),
        style={'padding': '0px 20px 20px 20px', 'width': '85%'}
    ),

    html.Div([
        dcc.Graph(id='assessor-count-by-type-pie')]
    ),

    html.Div([
        dcc.Graph(id='assessor-improvment-value-by-type')]
            ),

    html.H4("Developed by Matthew Maatubang", style={"textAlign": "center"})
])


def create_time_series(dff, title):
    return {
        'data': [dict(
            x=dff['year'].unique(),
            y=(dff['avg_land_value'] + dff['avg_improvement_value']),
            mode='lines+markers',
            name='Average Total Value'
        ), dict(
            x=dff['year'].unique(),
            y=(dff['avg_land_value']),
            mode='lines+markers',
            name='Average Land Value'
        ), dict(
            x=dff['year'].unique(),
            y=(dff['avg_improvement_value']),
            mode='lines+markers',
            name='Average Improvement Value'
        )],
        'layout': {
            'height': 700,
            'margin': {'l': 60, 'b': 40, 'r': 20, 't': 40},
            'bgcolor': 'rgba(237, 237, 237, 0.5)',
            'xaxis': {
                'title': "Years"
            },
            'yaxis': {
                'title': "Assessed Value in USD",
                'tickprefix':"$"
            },
            'annotations': [{
                'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'text': title
            }],
            'legend': {
                'x': 0,
                'y': 1
            }
        }
    }


def create_pie_chart(dff, title):
    return {
        'data': [dict(
            type="pie",
            values=dff['count'],
            labels=dff['use']
        )],
        'layout': {
            'height': 700,
            'margin': {'l': 60, 'b': 40, 'r': 20, 't': 100},
            'annotations': [{
                'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'center',
                'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }]
        }
    }


def create_bar_chart(dff, title):
    return {
        'data': [dict(
            type="bar",
            y=dff['avg_improvement_value'],
            x=dff['use']
        )],
        'layout': {
            'height': 700,
            'margin': {'l': 60, 'b': 40, 'r': 20, 't': 100},
            'xaxis': {
                'title': "Use Type"
            },
            'yaxis': {
                'title': "Average Improvement Value in USD",
                'tickprefix':"$"
            },
            'annotations': [{
                'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'center',
                'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }]
        }
    }


@app.callback(
    [Output('assessor-values-over-time-series', 'figure'),
     Output('assessor-count-by-type-pie', 'figure'),
     Output('assessor-improvment-value-by-type', 'figure')],
    [Input('city-dropdown', 'value'),
     Input('neighborhood-dropdown', 'value'),
     Input('street-dropdown', 'value'),
     Input('filter-year-slider', 'value'),
     Input('uses-checkbox', 'value')])
@cache.memoize
def update_chart(city, neighborhood, street, years, uses):
    selected_data = cd.loc[(cd['year'] >= min(years)) &
                           (cd['year'] <= max(years))]
    selected_data = selected_data.loc[selected_data['use'].isin(uses)]

    title_str = "LA County Assessor Value"
    chart_str = "Property Use Percentage in LA County"
    bar_str = "Average Improvement Value in LA County"
    if city:
        if not isinstance(city, list):
            city = list(city)
        selected_data = selected_data.loc[selected_data['city'].isin(city)]
        city_name = ','.join(city)
        title_str = city_name + " Assessor Value"
        chart_str = city_name + " Property Use Percentage"
        bar_str = city_name + " Average Improvement Value"
    if neighborhood:
        if not isinstance(neighborhood, list):
            neighborhood = list(neighborhood)
        selected_data = selected_data.loc[
                        selected_data['neighborhood'].isin(neighborhood)]
        neighborhood_name = ','.join([str(i) for i in neighborhood])
        title_str += " in " + neighborhood_name
        chart_str += " in " + neighborhood_name
        bar_str += " in " + neighborhood_name
    if street:
        if not isinstance(street, list):
            street = list(street)
        selected_data = selected_data.loc[selected_data['street'].isin(street)]
        street_name = ','.join(street)
        title_str += " on " + street_name
        chart_str += " on " + street_name
        bar_str += " on " + street_name
    if selected_data.empty:
        title_str = "Selection does not exist."
        chart_str = "Selection does not exist."
        bar_str = "Selection does not exist."
        pass

    weighted_mean = lambda x: np.average(x, weights=selected_data.loc[x.index,
                                                                      "count"])
    function_dict = {'count': np.sum,
                     'avg_land_value': weighted_mean,
                     'avg_improvement_value': weighted_mean}

    year_group = selected_data.groupby(
        ["year"]).agg(function_dict).reset_index()
    use_group = selected_data.groupby(
        ["year", "use"]).agg(function_dict).reset_index()

    latest_year = use_group["year"].max()
    use_group = use_group.loc[use_group['year'] == latest_year]

    chart_str += " in Year " + str(latest_year)
    bar_str += " in Year " + str(latest_year)

    return (create_time_series(year_group, title_str),
            create_pie_chart(use_group, chart_str),
            create_bar_chart(use_group, bar_str))



if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80)
