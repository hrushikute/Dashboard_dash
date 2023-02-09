import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
import dash
from dash.dependencies import Output, Input

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

data = airline_data.sample(n=700, random_state=42)
fig = px.pie(data,values='Flights',names='DistanceGroup',title='Distance Group Proportion by Flight')

# Create an app
app = dash.Dash(__name__)

# Create a layout
app.layout=html.Div(
    children=[
                html.H1("Airline On-time Performance Dashboard",
                    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),
                html.P('Proportion of distance group (250 mile distance interval group) by flights.',
                        style={'textAlign':'center', 'color': '#F57241'}),
                html.Div(dcc.Graph(figure=fig)),

                html.Div(["Input : ", dcc.Input(id='input-yr',value='2010',type='number',style={'height': '50-px','fornt-size':40}),
                ],style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40},),
                html.Div(["State Abbreviation", dcc.Input(id='input-ab',value='AL',type='text',style={'height': '50-px','fornt-size':40}),
                ],style={'textAlign': 'center', 'color': '#503D36', 'font-size':40},),
                html.Br(),
                html.Div(dcc.Graph(id='bar-plot')),


            ])
# Create a call back for input year.
@app.callback(Output(component_id='bar-plot',component_property='figure'),
              [Input(component_id='input-yr',component_property='value'),
              Input(component_id='input-ab',component_property='value')],
              )
def get_graph(entered_year,entered_state):
    df = airline_data[(airline_data['Year'] == int(entered_year)) &(airline_data['OriginState'] == entered_state)]
    g1 = df.groupby(['Reporting_Airline'])['Flights'].sum().nlargest(10).reset_index()
    fig_1 = px.bar(g1,x='Reporting_Airline',y='Flights', title=f'Top 10 Airline carrier for year: {entered_year} in terms of number of flights')
    fig_1.update_layout()
    return fig_1
# Run the application
if __name__ == '__main__':
    app.run_server(port=8002, host='127.0.0.1',debug=True)

