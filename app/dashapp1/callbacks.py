from dash.dependencies import Input
from dash.dependencies import Output
import plotly
import plotly.graph_objs as go
import pandas as pd

# HELPER FUNCTIONS: they select subsets of data
month_conv = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
    10: 'October', 11: 'November', 12: 'December'}
int_from_month = {v: k for k, v in month_conv.items()}

def upd_X_values(dset, weekday):
    if weekday == True:
        return sorted(dset['W-Day Time'].unique())[:-1]
    elif weekday == False:
        return sorted(dset['W-End Time'].unique())[:-1]

def upd_Y_values(dset, weekday, y, m, X_values):
    times = 'W-Day Time' if weekday==True else 'W-End Time'
    return list(dset[(dset[times] == i) & (dset['Year'] == y) & (dset['Month'] == m)]['Total_perc'].mean() for i in X_values)

def upd_Y_values_spc(dset, weekday, y, m, X_values, space):
    times = 'W-Day Time' if weekday==True else 'W-End Time'
    return list(dset[(dset[times] == i) & (dset['Year'] == y) & (dset['Month'] == m)][space+'_perc'].mean() for i in X_values)


# CALLBACKS

def register_callbacks1(dashapp, dataset):
    @dashapp.callback(
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
        X_val = upd_X_values(dataset, True)
        for (y, m) in selectors:
            Y_val = upd_Y_values(dataset, True, y, m, X_val)

            temp = plotly.graph_objs.Scatter(
                x= X_val,
                y= Y_val,
                name = month_conv[m] + " " + str(y),
                mode='lines+markers'
            )
            data.append(temp)

        labels = ['10am', '12pm', '2pm', '4pm', '6pm', '7pm', '8pm', '9pm', '10pm']
        tickvals = X_val
        return {'data': data,
                'layout': go.Layout(title='Average hourly weekday occupancy of the building',
                        xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                        yaxis=dict(title='Occupancy (%)',range=[0,100]),)}


def register_callbacks2(dashapp, dataset):
    @dashapp.callback(
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
        X_val = upd_X_values(dataset,False)
        for (y, m) in selectors:
            Y_val = upd_Y_values(dataset, False, y, m, X_val)

            temp = plotly.graph_objs.Scatter(
                x= X_val,
                y= Y_val,
                name = month_conv[m] + " " + str(y),
                mode='lines+markers'
            )
            data.append(temp)


        labels = ['11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm']
        tickvals = X_val
        return {'data': data,
                'layout': go.Layout(title='Average hourly weekend occupancy of the building',
                        xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                        yaxis=dict(title='Occupancy (%)',range=[0,100]),)}


def register_callbacks3(dashapp, dataset):
    @dashapp.callback(
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
        X_val = upd_X_values(dataset, True)
        for s in spc_selected:
            Y_val = upd_Y_values_spc(dataset, True, y, m, X_val, s)

            temp = plotly.graph_objs.Scatter(
                x= X_val,
                y= Y_val,
                name = s,
                mode='lines+markers'
            )
            data.append(temp)

        labels = ['10am', '12pm', '2pm', '4pm', '6pm', '7pm', '8pm', '9pm', '10pm']
        tickvals = X_val
        return {'data': data,
                'layout': go.Layout(title='Average hourly weekday occupancy for each space within the building',
                        xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                        yaxis=dict(title='Occupancy (%)',range=[0,100]),)}


def register_callbacks4(dashapp, dataset):
    @dashapp.callback(
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
        X_val = upd_X_values(dataset, False)
        for s in spc_selected:
            Y_val = upd_Y_values_spc(dataset, False, y, m, X_val, s)

            temp = plotly.graph_objs.Scatter(
                x= X_val,
                y= Y_val,
                name = s,
                mode='lines+markers'
            )
            data.append(temp)

        labels = ['11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm']
        tickvals = X_val
        return {'data': data,
                'layout': go.Layout(title='Average hourly weekend occupancy for each space within the building',
                        xaxis=go.layout.XAxis(title='Time (in Hours)', ticktext=labels, tickvals=tickvals),
                        yaxis=dict(title='Occupancy (%)',range=[0,100]),)}
