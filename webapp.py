import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go

import pandas as pd


dset = pd.read_csv('test2.csv')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)


month_conv = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
            10: 'October', 11: 'November', 12: 'December'}
int_from_month = {v: k for k, v in month_conv.items()}

month_select = []
for i in dset['Year'].unique():
    for j in dset[dset['Year'] == i]['Month'].unique():
        month_select.append(month_conv[j] + " " + str(i))

spaces_list = ['Space1', 'Space2', 'Space3', 'Space4', 'Space5', 'Space6', 'Space7',
                'Space8', 'Space9', 'Space10', 'Space11', 'Space12']

def upd_X_values(weekday):
    if weekday == True:
        return sorted(dset['W-Day Time'].unique())[:-1]
    elif weekday == False:
        return sorted(dset['W-End Time'].unique())[:-1]

def upd_Y_values(weekday, year, month, X_values):
    times = 'W-Day Time' if weekday==True else 'W-End Time'
    y, m = year, month
    return list(dset[(dset[times] == i) & (dset['Year'] == y) & (dset['Month'] == m)]['Total_perc'].mean() for i in X_values)

def upd_Y_values_spc(weekday, year, month, X_values, space):
    times = 'W-Day Time' if weekday==True else 'W-End Time'
    y, m = year, month
    return list(dset[(dset[times] == i) & (dset['Year'] == y) & (dset['Month'] == m)][space+'_perc'].mean() for i in X_values)

app.layout = html.Div([
    html.Div([html.H2(children = 'Building X Occupancy Study Data', style={
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

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='weekday-total', component_property='value')]
    )
def update_value(periods):
    if type(periods) == str:
        periods = [periods]

    selectors = []
    for p in periods:
        month, year = p.split()
        month = int_from_month[month]
        year = int(year)
        selectors.append((year, month))

    data = []
    X_val = upd_X_values(True)
    for (y, m) in selectors:
        Y_val = upd_Y_values(True, y, m, X_val)

        temp = plotly.graph_objs.Scatter(
            x= X_val,
            y= Y_val,
            name = month_conv[m] + " " + str(y),
            mode='lines+markers'
        )
        data.append(temp)

    labels = ['10am', '12pm', '2pm', '4pm', '6pm', '7pm', '8pm', '9pm', '10pm']
    tickvals = upd_X_values(True)
    return {'data': data,
            'layout': go.Layout(title='Average hourly weekday occupancy of the building',
                    xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                    yaxis=dict(title='Occupancy (%)',range=[0,100]),)}

@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input(component_id='weekend-total', component_property='value')]
    )
def update_value(periods):
    if type(periods) == str:
        periods = [periods]

    selectors = []
    for p in periods:
        month, year = p.split()
        month = int_from_month[month]
        year = int(year)
        selectors.append((year, month))

    data = []
    X_val = upd_X_values(False)
    for (y, m) in selectors:
        Y_val = upd_Y_values(False, y, m, X_val)

        temp = plotly.graph_objs.Scatter(
            x= X_val,
            y= Y_val,
            name = month_conv[m] + " " + str(y),
            mode='lines+markers'
        )
        data.append(temp)


    labels = ['11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm']
    tickvals = upd_X_values(False)
    return {'data': data,
            'layout': go.Layout(title='Average hourly weekend occupancy of the building',
                    xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                    yaxis=dict(title='Occupancy (%)',range=[0,100]),)}

@app.callback(
    Output(component_id='graph3', component_property='figure'),
    [Input(component_id='weekday-by-space-month', component_property='value'),
    Input(component_id='weekday-by-space', component_property='value')
    ])
def update_value(periods, spc_selected):
    month, year = periods.split()
    m = int_from_month[month]
    y = int(year)

    if type(spc_selected) == str:
        spc_selected = [spc_selected]

    data = []
    X_val = upd_X_values(True)
    for s in spc_selected:
        Y_val = upd_Y_values_spc(True, y, m, X_val, s)

        temp = plotly.graph_objs.Scatter(
            x= X_val,
            y= Y_val,
            name = s,
            mode='lines+markers'
        )
        data.append(temp)

    labels = ['10am', '12pm', '2pm', '4pm', '6pm', '7pm', '8pm', '9pm', '10pm']
    tickvals = upd_X_values(True)
    return {'data': data,
            'layout': go.Layout(title='Average hourly weekday occupancy for each space within the building',
                    xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                    yaxis=dict(title='Occupancy (%)',range=[0,100]),)}

@app.callback(
    Output(component_id='graph4', component_property='figure'),
    [Input(component_id='weekend-by-space-month', component_property='value'),
    Input(component_id='weekend-by-space', component_property='value')
    ])
def update_value(periods, spc_selected):
    month, year = periods.split()
    m = int_from_month[month]
    y = int(year)

    if type(spc_selected) == str:
        spc_selected = [spc_selected]

    data = []
    X_val = upd_X_values(False)
    for s in spc_selected:
        Y_val = upd_Y_values_spc(False, y, m, X_val, s)

        temp = plotly.graph_objs.Scatter(
            x= X_val,
            y= Y_val,
            name = s,
            mode='lines+markers'
        )
        data.append(temp)

    labels = ['11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm']
    tickvals = upd_X_values(False)
    return {'data': data,
            'layout': go.Layout(title='Average hourly weekend occupancy for each space within the building',
                    xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                    yaxis=dict(title='Occupancy (%)',range=[0,100]),)}


if __name__ == '__main__':
    app.run_server(debug = True)
