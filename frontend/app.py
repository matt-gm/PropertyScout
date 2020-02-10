import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


la_data = pd.read_csv('LA_data.csv')
cd = la_data
selectable_cities = cd.city.unique()
selectable_neighborhoods = cd.neighborhood.unique()
selectable_streets = cd.street.unique()
cities = ["Los Angeles", "San Francisco", "New York City", "Denver",
          "Las Vegas", "Austin"]

app.layout = html.Div([
    html.H1("PropertyScout", style={"textAlign": "center"}),

    #html.Div({
    #    html.Label('Enter City'),
    #    dcc.Dropdown(
    #        id='major-city-dropdown',
    #        options=[{'label': i, 'value': i} for i in cities],
    #        value="Los Angeles"
    #    )
    #}),

    html.Div([
        html.Div([
            html.Label('Enter City Subdivison'),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_cities],
                value='Begin typing here...'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Enter Neighborhood'),
            dcc.Dropdown(
                id='neighborhood-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_neighborhoods],
                value='Begin typing here...'
            )],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div([
            html.Label('Enter Street'),
            dcc.Dropdown(
                id='street-dropdown',
                options=[{'label': i, 'value': i} for i in selectable_streets],
                value='Begin typing here...'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(
            id='assessor-values-over-time-series'
            #,hoverData={'points':}
        )]
    ),

    html.Div([
        dcc.Graph(
            id='assessor-values-by-type-bars'
            #,hoverData={'points':}
        )]
    )
])


def create_time_series(dff, title):
    return {
        'data': [dict(
            x=dff['year'].unique(),
            y=(dff['avg_land_value'] + dff['avg_improvement_value']),
            mode='lines+markers'
        )],
        'layout': {
            'height': 700,
            'margin': {'l': 40, 'b': 40, 'r': 20, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }]
        }
    }

@app.callback(
    Output('assessor-values-over-time-series', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('neighborhood-dropdown', 'value'),
     Input('street-dropdown', 'value')])
def update_scatter(city, neighborhood, street):
    selected_data = cd
    selected_data = selected_data.loc[str(selected_data['city']) == str(city)]
    selected_data = selected_data.loc[str(selected_data['neighborhood']) == str(neighborhood)]
    selected_data = selected_data.loc[str(selected_data['street']) == str(street)]


    print("selected_data shape is : " + str(selected_data.shape))

    weighted_mean = lambda x: np.average(x, weights=selected_data.loc[x.index, "count"])
    function_dict = {'count': np.sum,
                     'avg_land_value': weighted_mean,
                     'avg_improvement_value': weighted_mean}

    grouped = selected_data.groupby(
                    ["year"]).agg(function_dict).reset_index()
    print("grouped shape is : " + str(grouped.shape))
    print(list(grouped))

    return create_time_series(grouped, "Assessor Value over Time")

if __name__ == '__main__':
    app.run_server(debug=True)
