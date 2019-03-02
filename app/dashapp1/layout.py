import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Helpers: they build selectors in dropdown menus & axis labels in the layout.
month_conv = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
    10: 'October', 11: 'November', 12: 'December'}
int_from_month = {v: k for k, v in month_conv.items()}

def month_generator(dataset):
    months_list = []
    for i in dataset['Year'].unique():
        for j in dataset[dataset['Year'] == i]['Month'].unique():
            months_list.append(month_conv[j] + " " + str(i))
    return months_list

# Main function: creates the layout for the Dash app.
def create_layout(dataset):

    month_select = month_generator(dataset)
    spaces_list = ['Space1', 'Space2', 'Space3', 'Space4', 'Space5', 'Space6', 'Space7',
            'Space8', 'Space9', 'Space10', 'Space11', 'Space12']

    layout = html.Div([
        html.Div([html.H2(children = 'Building X Occupancy Data', style={
                'textAlign': 'center'})]),
        html.Div([
            html.Div([
                html.Div([html.H3('Total weekday hourly average', style={
                        'textAlign': 'center'})]),
                dcc.Dropdown(id='weekday-total',
                            options=[{'label': l, 'value': l} for l in month_select],
                            value=month_select[-1],
                            multi=True),
                dcc.Graph(id='graph1', animate=True)
            ], className="six columns"),

            html.Div([
                html.Div([html.H3('Total weekend hourly average', style={
                        'textAlign': 'center'})]),
                dcc.Dropdown(id='weekend-total',
                            options=[{'label': l, 'value': l} for l in month_select],
                            value=month_select[-1],
                            multi=True),
                dcc.Graph(id='graph2', animate=True)
            ], className="six columns")
        ], className="row"),


        html.Div([
            html.Div([
                html.Div([html.H3('Space-specific weekday hourly average', style={
                        'textAlign': 'center'})]),
                dcc.Dropdown(id='weekday-by-space-month',
                            options=[{'label': l, 'value': l} for l in month_select],
                            value=month_select[-1],
                            multi=False),
                dcc.Dropdown(id='weekday-by-space',
                            options=[{'label': l, 'value': l} for l in spaces_list],
                            value=spaces_list,
                            multi=True),
                dcc.Graph(id='graph3', animate=True)
            ], className="six columns"),

            html.Div([
                html.Div([html.H3('Space-specific weekend hourly average', style={
                        'textAlign': 'center'})]),
                dcc.Dropdown(id='weekend-by-space-month',
                            options=[{'label': l, 'value': l} for l in month_select],
                            value=month_select[-1],
                            multi=False),
                dcc.Dropdown(id='weekend-by-space',
                            options=[{'label': l, 'value': l} for l in spaces_list],
                            value=spaces_list,
                            multi=True),
                dcc.Graph(id='graph4', animate=True)
            ], className="six columns")
        ], className="row")
    ])

    return layout
