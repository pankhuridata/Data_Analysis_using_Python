#Author:Pankhuri

#import libraries
# Load necessary libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv('FloodArchive.csv')

# Convert the date columns to datetime format
df['Began'] = pd.to_datetime(df['Began'], format='%Y-%m-%d')
df['Ended'] = pd.to_datetime(df['Ended'], format='%Y-%m-%d')

# Create the Dash app
app = dash.Dash(__name__)
# dropdown menu to present the value of Dead
fig1 = px.scatter(df, x='long', y='lat', color='Country', hover_name='Country',
                  hover_data={'Dead': ':.0f'}, size='Dead')

dropdown1 = dcc.Dropdown(
    id='dead-dropdown',
    options=[{'label': i, 'value': i} for i in df['Country'].unique()],
    value='India'
)

layout1 = html.Div([
    html.H1('Number of Dead due to Floods'),
    html.Div([
        html.Div([
            dcc.Graph(id='dead-plot', figure=fig1)
        ], className='six columns'),

        html.Div([
            html.H3('Select a Country'),
            dropdown1
        ], className='six columns')
    ], className='row')
])

@app.callback(Output('dead-plot', 'figure'),
              Input('dead-dropdown', 'value'))
def update_figure1(selected_country):
    filtered_df = df[df['Country'] == selected_country]
    fig = px.scatter(filtered_df, x='long', y='lat', color='Country', hover_name='Country',
                     hover_data={'Dead': ':.0f'}, size='Dead')
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.layout = layout1
    app.run_server(debug=True)


fig2 = px.scatter(df, x='long', y='lat', color='Country', hover_name='Country',
                  hover_data={'Displaced': ':.0f'}, size='Displaced')

# slider bar to present the value of Displaced
slider1 = dcc.Slider(
    id='displaced-slider',
    min=df['Displaced'].min(),
    max=df['Displaced'].max(),
    step=1000,
    value=df['Displaced'].min(),
    marks={
        0: {'label': '0'},
        5000: {'label': '5000'},
        10000: {'label': '10000'},
        15000: {'label': '15000'},
        20000: {'label': '20000'},
        25000: {'label': '25000'},
        30000: {'label': '30000'},
    }
)

layout2 = html.Div([
    html.H1('Number of Displaced due to Floods'),
    html.Div([
        html.Div([
            dcc.Graph(id='displaced-plot', figure=fig2)
        ], className='six columns'),

        html.Div([
            html.H3('Select the Minimum Number of Displaced'),
            slider1
        ], className='six columns')
    ], className='row')
])

@app.callback(Output('displaced-plot', 'figure'),
              Input('displaced-slider', 'value'))
def update_figure2(selected_value):
    filtered_df = df[df['Displaced'] >= selected_value]
    fig = px.scatter(filtered_df, x='long', y='lat', color='Country', hover_name='Country',
                     hover_data={'Displaced': ':.0f'}, size='Displaced')
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.layout = layout2
    app.run_server(debug=True)

