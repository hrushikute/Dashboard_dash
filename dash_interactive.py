import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
# Get the data of airlines
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)
app.layout=html.Div(
    children=[
        html.H1("Airline Performance Dashboard",style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),
        html.Div(["Input : ", dcc.Input(id='input-yr',value=2011,type='number',style={'textAlign': 'left', 'height':'50px',
                                                                                      'color': '#503D36', 'font-size': 35})],
                 style={'font-size': 50}),
        html.Br(),
        html.Div(dcc.Graph(id='line-chart')),


    ]
)

@app.callback(Output(component_id='line-chart', component_property='figure'),
              Input(component_id='input-yr', component_property='value'))
def get_chart(input_year):
    data=airline_data[airline_data['Year']==int(input_year)]
    df=data.groupby(['Month'])['ArrDelay'].mean().reset_index()
    fig = px.line(df,x='Month',y='ArrDelay',title='Avg Airline Delay vs Month')
    fig.update_layout()
    return fig

if __name__=='__main__':
    # app.run_server(port=8002,host='127.0.0.1',debug=True)
    app.run_server(port=8002, host='127.0.0.1', debug=True)

