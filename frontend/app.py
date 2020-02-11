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
                options=[{'label': i, 'value': i} for i in selectable_cities],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Label('Enter Neighborhood'),
            dcc.Dropdown(
                id='neighborhood-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_neighborhoods],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Label('Enter Street'),
            dcc.Dropdown(
                id='street-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_streets],
                value=None)],
            style={'width': '33%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='assessor-values-over-time-series')]
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
            'xaxis': {
                'title': "Years"
            },
            'yaxis': {
                'title': "Assessed Value in USD"
            },
            'annotations': [{
                'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left',
                'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }]
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
                'title': "Average Improvement Value in USD"
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
     Input('street-dropdown', 'value')])
@cache.memoize
def update_chart(city, neighborhood, street):
    selected_data = cd
    title_str = "LA County Assessor Value"
    chart_str = "Property Use Percentage in LA County"
    bar_str = "Average Improvement Value in LA County"
    if isSelected(city):
        selected_data = selected_data.loc[selected_data['city'] == city]
        title_str = city + " Assessor Value"
        chart_str = city + " Property Use Percentage"
        bar_str = city + " Average Improvement Value"
    if isSelected(neighborhood):
        selected_data = selected_data.loc[selected_data['neighborhood'] == neighborhood]
        title_str += " in " + str(neighborhood)
        chart_str += " in " + str(neighborhood)
        bar_str += " in " + str(neighborhood)
    if isSelected(street):
        selected_data = selected_data.loc[selected_data['street'] == street]
        title_str += " on " + street
        chart_str += " on " + street
        bar_str += " on " + street
    if selected_data.empty:
        title_str = "No matching data."
        chart_str = "No matching data."
        bar_str = "No matching data."
        pass

    weighted_mean = lambda x: np.average(x, weights=selected_data.loc[x.index, "count"])
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

def isSelected(in_val):
    return not isinstance(in_val, list) and (in_val is not None)


if __name__ == '__main__':
    app.run_server(debug=True)
