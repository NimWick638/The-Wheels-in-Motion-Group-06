import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load data
df = pd.read_csv('Cleaned_PassengerVehicle_Stats2.csv')

# Group data for specific visualizations
wheelchair_grouped_data = df.groupby(['Vehicle Type', 'Wheelchair Accessible']).size().reset_index(name='wheelchair_count')
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

# Wheelchair Accessibility Chart
wheelchair_bar_fig = px.bar(
    wheelchair_grouped_data,
    x='Vehicle Type',
    y='wheelchair_count',
    color='Wheelchair Accessible',
    title='Vehicle type counts with wheelchair accessibility',
    labels={'Vehicle Type':'Vehicle Type', 'wheelchair_count': 'Number of vehicles'},
    barmode='stack',
    width=700,
    height=600
)

wheelchair_bar_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  
    plot_bgcolor="rgba(0,0,0,0)",  
    title_font=dict(size=20, color="black"),  
    font=dict(color="black"), 
    yaxis=dict(
        dtick=500,
        showgrid=True,               
        gridcolor='rgba(169, 169, 169, 0.3)' 
    ),
    xaxis=dict(
        showgrid=False,               
        gridcolor='rgba(169, 169, 169, 0.3)'
    ),
    title={
        'text': 'Wheelchair Accessibility of vehicles',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.95,
        'yanchor':'top',
        'font': {
            'size': 24,
            'family':"Arial, sans-serif",
            'color': "black"
        }
    }
)

# Initializing Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={
       'display': 'flex',
       'flexDirection': 'column',
       'gap': '15px'
    },
    children=[
        html.H1(
            "Wheel in the Motion",
            style={
                'textAlign': 'center',
                'fontSize': '70px',
                'color': '#7e79f8',
                'fontFamily': 'Arial, sans-serif',
                'fontWeight': 'bold',
                'marginTop': '20px',
                'marginBottom': '10px'
            }
        ),
        html.H2(
            "Public Passenger Vehicle Statistical Analysis in Illinois state",
            style={
                'textAlign': 'center',
                'fontSize': '40px',
                'color': '#363b4e',
                'fontFamily': 'Arial, sans-serif',
                'fontWeight': 'bold',
                'marginTop': '5px',
                'marginBottom': '30px'
            }
        ),
         html.Div(
            dcc.Graph(id='wheelchair-accessibility-bar-chart',figure=wheelchair_bar_fig))
])

if __name__ == '__main__':
    app.run_server(debug=True)