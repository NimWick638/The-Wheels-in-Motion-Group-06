import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from geopy.geocoders import Nominatim

# Load data
df = pd.read_csv('Cleaned_PassengerVehicle_Stats2.csv')

# Group data for specific visualizations
wheelchair_grouped_data = df.groupby(['Vehicle Type', 'Wheelchair Accessible']).size().reset_index(name='wheelchair_count')
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

# Geocode function
geolocator = Nominatim(user_agent="vehicle_dashboard")
def geocode_zip(zip_code):
    try:
        location = geolocator.geocode({"postalcode": str(int(zip_code)), "country": "United States"})
        if location:
            return location.latitude, location.longitude
    except:
        return None, None

# Prepare ZIP code distribution data
zip_code_distribution = df['ZIP Code'].value_counts().reset_index()
zip_code_distribution.columns = ['ZIP Code', 'Count']
zip_code_distribution[['Latitude', 'Longitude']] = zip_code_distribution['ZIP Code'].apply(
    lambda z: pd.Series(geocode_zip(z))
)

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
    title_font=dict(size=20, color="white"),  
    font=dict(color="white"), 
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
            'color': "white"
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
            "The Wheels in Motion",
            style={
                'textAlign': 'center',
                'fontSize': '70px',
                'color': '#7e79f8',
                'fontFamily': 'Arial, sans-serif',
                'fontWeight': 'bold',
                'marginTop': 'auto',
                'marginBottom': '5px'
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
        dcc.Dropdown(
        id='vehicle-type-dropdown',
        options=[{'label': vtype, 'value': vtype} for vtype in df['Vehicle Type'].unique()],
        placeholder="Select a Vehicle Type",
        clearable=True,
        className='custom-dropdown',
        style={
                'width': '50%',
                'margin': '10px auto',
                'padding': '10px',
                'borderRadius': '5px',
                'border': '1px solid #ccc',
                'textAlign':'center',
                'fontSize':'20px',
                'background': 'rgba(255, 255, 255, 0.1)',
                'backdropFilter': 'blur(10px)',
                'color': 'white',
                'fontFamily': 'Courier New, monospace',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'position':'relative'
            }
        ),

        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'center',
                'gap': '15px'
            },
            children=[
                html.Div(dcc.Graph(id='bar-chart', className='glass-container')),
                html.Div(dcc.Graph(id='pie-chart', className='glass-container'))
            ]
        ),

        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'center',
                'gap': '15px'
            },
            children=[
               html.Div(dcc.Graph(id='map-chart', className='glass-container')),
               html.Div(dcc.Graph(id='hist-chart', className='glass-container'))
            ]
            ),
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'center',
                'gap': '15px'
            },
            children=[
                html.Div(dcc.Graph(id='wheelchair-accessibility-bar-chart',figure=wheelchair_bar_fig, className='glass-container'))
            ]
        )
],
className='body app-content background-container verticle-container'
)

# Callbacks for updating graphs
@app.callback(
   [ Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('hist-chart', 'figure'),
   ],
    [Input('vehicle-type-dropdown', 'value')]
)

def update_charts(vehicle_type):
    # Filter data based on dropdown selection
    filtered_df = df[df['Vehicle Type'] == vehicle_type] if vehicle_type else df
    filtered_zip = zip_code_distribution[zip_code_distribution['ZIP Code'].isin(filtered_df['ZIP Code'].unique())]

    # Bar Chart
    status_counts_filtered = filtered_df['Status'].value_counts().reset_index()
    status_counts_filtered.columns = ['Status', 'Count']

    bar_fig = px.bar(
    status_counts_filtered,
    x='Status', y='Count',
    title='Vehicle type counts by license status',
    width=700, height=600
     )

    bar_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  
    plot_bgcolor="rgba(0,0,0,0)",  
    title_font=dict(size=20, color="white"),  
    font=dict(color="white"), 
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
        'text': 'Vehicle type counts by license status',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.95,
        'yanchor':'top',
        'font': {
            'size': 24,
            'family':"Arial, sans-serif",
            'color': "white"
        }
    }
   )
    # Pie Chart
    pie_fig = px.pie(
        filtered_df, names="Vehicle Fuel Source",
        title="Fuel Source Distribution",
        width=700, height=600
    )

    pie_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  
    title_font=dict(size=20, color="white"),  
    font=dict(color="white"), 
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
        'text': 'Fuel Source Distribution',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.95,
        'yanchor':'top',
        'font': {
            'size': 24,
            'family':"Arial, sans-serif",
            'color': "white"
        }
    }
    )

    # Map Chart
    map_fig = px.scatter_mapbox(
        filtered_zip,
        lat='Latitude', lon='Longitude', size='Count', color='Count',
        hover_name='ZIP Code', mapbox_style='open-street-map',
        title='Vehicle Distribution by ZIP Code',
        width=700, height=600
    )

    map_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  
    plot_bgcolor="rgba(0,0,0,0)", 
    title_font=dict(size=20, color="black"),  
    font=dict(color="black"), 

    title={
        'text': 'Vehicle Distribution accross State',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.95,
        'yanchor':'top',
        'font': {
            'size': 24,
            'family':"Arial, sans-serif",
            'color': "white"
        }
    }
   ) 

    # Histogram
    hist_fig = px.histogram(
        filtered_df, x='Vehicle Model Year',
        title='Vehicle Count by Model Year',
        width=700, height=600
    )

    hist_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  
    plot_bgcolor="rgba(0,0,0,0)",  
    title_font=dict(size=20, color="white"),  
    font=dict(color="white"), 
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
        'text': 'Vehicle Makes Over the Years',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.95,
        'yanchor':'top',
        'font': {
            'size': 24,
            'family':"Arial, sans-serif",
            'color': "white"
        }
    }
    )
    return bar_fig, pie_fig, map_fig, hist_fig


if __name__ == '__main__':
    app.run_server(debug=True)