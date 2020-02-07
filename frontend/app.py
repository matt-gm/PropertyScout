import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import s3_file_manager

app = dash.Dash(__name__)
app.title = 'PropertyScout'

# la_data =
# sf_data =
# nyc_data =
# denver_data =
# austin_data =
# lv_data =

app.layout = html.Div([
    html.H1(
        html.Div('PropertyScout', className='nine columns')
    ),
    html.Div(
        [
            dt.Data
        ]
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
