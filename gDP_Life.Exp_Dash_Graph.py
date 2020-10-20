# -*- coding: utf-8 -*-
"""
Dash Graph, 
With callbacks
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('gapminderDataFiveYear.csv')



#Create the application
app = dash.Dash()

year_options = []
'''
We are creating a tuple where the year value is a integer, allowing us to use it as an input
and we all have a unique numeric value for each, 
creating year options for the dropdown component
'''
for year in df['year'].unique():
    year_options.append({'label':str(year), 
                         'value':year})


app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id = 'year-picker',
                 options = year_options, 
                 value = df['year'].min()) #Options for the user to play aroudn with
                                         # user will import it we will use list comprehensions for this
    ])


'''
Now let's create an update figure function 

'''

@app.callback(Output('graph','figure'), 
              [Input('year-picker','value')])
def update_figuer(selected_year):
    '''
    based off the selected year we have as out input, 
    we will filter the data
    '''
    filtered_df = df[df['year']==selected_year]
    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent']==continent_name]
        traces.append(go.Scatter(
            x = df_by_continent['gdpPercap'], 
            y = df_by_continent['lifeExp'], 
            mode = 'markers',
            opacity = .7,
            name= continent_name))
    
    return {'data': traces,
            'layout':go.Layout(title = 'My Plot',
                               xaxis = {'title':'GDP Per Cap', 
                                        'type':'log'}, 
                               yaxis = {'title':' Life Expect.'})} 

if __name__ == '__main__':
    app.run_server()
