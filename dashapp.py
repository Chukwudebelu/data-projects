from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL # Clientsidefunction
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import os
import sqlite3

# Create the app
request_path_prefix=None
workspace_user = os.getenv('JUPYTERHUB_USER') # Get DS4A workspace user name

if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = Dash(__name__, requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.FLATLY],
          meta_tags=[{'name':'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

# Load the GeoJSON files for each location
with open('map_atl.geojson') as geo:
    geojson = json.loads(geo.read())
    
# Get the data
# df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_atlanta_06_10_2022__18_57_36.csv')
# df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_austin_06_10_2022__18_52_39.csv')
# df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_baltimore_06_23_2022__21_52_58.csv')
# df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_miami_06_10_2022__19_21_10.csv')
# df = pd.read_csv('zillow_crawled_data/raw_housing_data_new_york_06_10_2022__18_41_58.csv')
# df = pd.read_csv('zillow_crawled_data/raw_housing_data_philadelphia_06_23_2022__21_18_46.csv')
# df = pd.read_csv('zillow_crawled_data/raw_housing_data_richmond_06_23_2022__21_50_06.csv')
# df = pd.read_csv('zillow_crawled_data/raw_housing_data_phoenix_06_23_2022__21_28_04.csv')
# df = pd.read_csv('zillow_crawled_data/raw_housing_data_seattle_06_10_2022__19_53_51.csv')
# df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_houston_06_23_2022__21_17_10.csv')

# Clean the scraped data
def clean_data(df):
    '''# Drop row of records with NaN values in any column'''
    # Iterate through the rows
    for i in list(df.index):
        if df.loc[i,:].isnull().values.any(): # if any row is 'NaN'
            df.drop(i, axis=0, inplace=True) # remove row
            
    '''Drop "-" values in the # of bedroom column'''
    for j in list(df.index):
        for k in ['beds']:
            if df.loc[j,k] == '-':
                df.drop(j, axis=0, inplace=True)
    
    '''Drop "-" values in the # of bathroom column'''
    for l in list(df.index):
        for m in ['baths']:
            if df.loc[l,m] == '-':
                df.drop(l, axis=0, inplace=True)
                
    '''Drop "--" values in the square footage column'''
    for n in list(df.index):
        for p in ['area_sq_ft']:
            if df.loc[n,p] == '--':
                df.drop(n, axis=0, inplace=True)
    
    # Convert the Zip codes, number of beds & baths and square footage to integers
    df[['zip_code','beds','baths']] = df[['zip_code','beds','baths']].astype('int')
    
    # Remove the $ values and ','
    df['price']=df['price'].str.replace(',','').str.strip('$').astype('int')
    
    # Remove ',' from square footage column
    df['area_sq_ft']=df['area_sq_ft'].str.replace(',','').astype('int')
    
    # Reset the index of the new dataframe
    df = df.reset_index()
    del df['index']
    
    return df

global city_dict

# Dictionary of U.S. cities and 3-letter abbreviation
city_dict = {'Atlanta, GA': 'ATL', 'Birmingham': 'AL', 'Austin, TX': 'ATX', 'Boston': 'MA', 'Baltimore': 'MD',
           'Charlotte': 'NC', 'Chicago': 'IL', 'Houston': 'TX', 'Las Vegas': 'NV', 'Los Angeles': 'CA', 
           'Miami': 'FL', 'Nashville': 'TN', 'New York': 'NY', 'Oklahoma City': 'OK', 'Philadelphia': 'PA',
           'Portland': 'OR', 'Phoenix': 'AZ', 'Richmond': 'VA', 'Seattle': 'WA', 'Washington': 'DC'
          }
global city_list
city_list = { 'Atlanta, GA': 'ATL', 'Austin, TX': 'ATX'}

# Call the function to clean rows with missing values
# df_clean = clean_data(df_city)

# Get the number of listings
# num_listings = df_clean.shape[0]

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiY2NhbnVtYmEiLCJhIjoiY2w0dDhjdjR6MDI1YzNrbTlhNXFoc3hwbiJ9.hz073LZBQMGS4RJy36GjbQ'

#-----------------------------------------------------------------------------------------------------------------------------------------
# city = df_clean['city'][0]
# state = df_clean['state'][0]

fig = px.scatter_mapbox(#df_clean,
                        
#                      lat=-37, 
#                      lon=94, 
#                      hover_name='address_street',
#                      hover_data=['city','state','zip_code'],
#                      color='price',
#                      size='area_sq_ft',
#                      size_max=12,
#                     location="usa",
                     zoom=3,
                     width=800,
                     height=600,
#                      color_continuous_scale='Plasma',
                     opacity=0.9)

fig.update_layout(title='House listings in <b>' + city + ', ' + state + '</b>',
                  title_x=0.5,
                  mapbox_style='open-street-map',
                  autosize=True,
                  mapbox=dict(accesstoken=mapbox_access_token))
fig.show()

# # Get the bathrooms count and strore as a list
# num_baths = [str(i) for i in list(df_clean['baths'].unique())]
# num_baths.sort(reverse=False)

# # Convert the baths column to string to display discretely in graph
# df_clean['baths'] = df_clean['baths'].astype('str')

# fig2=px.scatter(df_clean,
#                x='area_sq_ft', 
#                y='price', 
#                color='baths',
#                size='beds',
#                size_max=20,
#                log_y=True,
#                color_discrete_sequence=px.colors.qualitative.G10,
#                category_orders={"baths": num_baths})
# fig2.update_layout(title='Plot of <b>Home value ($)</b> vs <b>Square footage</b>',
#                    title_x = 0.5, # center the title
#                     legend=dict(
#                     yanchor="top",
#                     y=1,
#                     xanchor="left",
#                     x=1))
# fig2.show()

# Create a layout
app.layout = html.Div([
    html.Div([
        # Display title & logo
        html.P([
            html.H2('Zillow+', 
                    style={'textAlign': 'center', 'color': 'blue', 'backgroundColor': '#F8F9F9'}
                   ), # html.H2
#             html.Img(src="https://workspace.ds4a.com/user/chisom213@gmail.com/view/DE%201.0%20Team%205%20data/vox.png", height=10, id='logo')
        ])
    ]), # html.Div1

    html.Div([
        # Display map
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(fig, id='map-plot')
                ]) # html.Div
            ], width=7), # col

            dbc.Col([
                html.Div([
                    dbc.Card([
                        dbc.CardHeader("No. of listings"),
                        dbc.CardBody([
                            html.H5(id="listings-number",
                                    className="card-title", style={'textAlign': 'center', 'color': 'blue'},
                                   ) # html.H6
                        ], id='num-listings')
                    ], outline=True, color="dark"
                    ) # card
                ], id="value-1", className="mini_container_1", style={'textAlign': 'center'}
                ), # html.Div
                html.Div([
                    dcc.Dropdown(options=['Austin, TX', 'Atlanta, GA'],
                                 value='ATX',
                                 placeholder="Select a city",
                                 searchable=True,
                                 clearable=True,
                                 id='dropdown-menu'
                            ), # dropdown
                    html.Div(id='dropdown-container')
                ], id = 'dropdown-div')
            ], width=2) # col
        ]), # row

        #Display the dropdown menu
# #         dbc.Row([
#             html.Div([
#                 dcc.Dropdown(options=['Austin, TX', 'Atlanta, GA'],
#                              value='ATX',
#                              placeholder="Select a city",
#                              searchable=True,
#                              id='dropdown-menu'
#                             ), # dropdown
#                 html.Div(id='dropdown-container')
#             ], id='dropdown-div'
#             ) # html.Div
#         ]), # row
#         ], width=2) # col
#             ]) # row
    ]), # html.Div2

    html.Div([
        # Display scatter plot
#             dbc.Row([
#                 dbc.Col([
                html.Div([
                    dcc.Graph(id='scat-plot')
                ]) # html.Div
#                 ]) # col
#             ]) # row
    ]) # html.Div3

]) # html.Div
#-------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('dropdown-container', 'children'),
    Input('dropdown-menu', 'value')
)
def update_value(value):
#     city_list = ['Austin, TX', 'Atlanta, GA']
#     nonlocal city_list
    city_list = { 'Atlanta, GA': 'ATL', 'Austin, TX': 'ATX'}
    
    if value in city_list:
        return f'You selected {city_list[value]}'
     
@app.callback(
    Output('map-plot', 'figure'),
    Output('scat-plot', 'figure'),
    Output('listings-number', 'children'),
    Input('dropdown-menu', 'value')
)
def update_plots(value):
    if value == city_list[value]:
        df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_austin_06_10_2022__18_52_39.csv')
    elif value == city_list[value]:
        df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_atlanta_06_10_2022__18_57_36.csv')
    else:
        df_city = pd.read_csv('zillow_crawled_data/raw_housing_data_atlanta_06_10_2022__18_57_36.csv')
        
    df_clean = clean_data(df_city)
    
    # Get the number of listings
    num_listings = df_clean.shape[0]
    
    city = df_clean['city'][0]
    state = df_clean['state'][0]

    fig=px.scatter_mapbox(df_clean,
                         lat='latitude', 
                         lon='longitude', 
                         hover_name='address_street',
                         hover_data=['city','state','zip_code'],
                         color='price',
                         size='area_sq_ft',
                         size_max=12,
                         zoom=10,
                         width=800,
                         height=600,
                         color_continuous_scale='Plasma',
                         opacity=0.9,
                         labels=dict(area_sq_ft='<i>Area (ft<sup>2</sup>)</i>', latitude='<i>Latitude (&deg;)</i>',
                                     longitude='<i>Longitude (&deg;)</i>', city='<i>City</i>', state='<i>State</i>',
                                     price='<i>Price ($)</i>', zip_code='<i>ZIP Code</i>'))

    fig.update_layout(title='House listings in <b>' + city + ', ' + state + '</b>',
                      title_x=0.5,
                      mapbox_style='open-street-map',
                      autosize=True,
                      mapbox=dict(accesstoken=mapbox_access_token))
    
    # Get the bathrooms count and strore as a list
    num_baths = [str(i) for i in list(df_clean['baths'].unique())]
    num_baths.sort(reverse=False)

    # Convert the baths column to string to display discretely in graph
    df_clean['baths'] = df_clean['baths'].astype('str')

    fig2=px.scatter(df_clean,
                   x='area_sq_ft', 
                   y='price', 
                   color='baths',
                   size='beds',
                   size_max=20,
                   log_y=True,
                   color_discrete_sequence=px.colors.qualitative.G10,
                   category_orders={"baths": num_baths},
                   labels=dict(area_sq_ft='Total Area (ft<sup>2</sup>)', price='Price (USD)', 
                               baths='Bathrooms', beds='Bedrooms'))

    fig2.update_layout(title='Bubble Chart of <b>Property value</b> vs <b>Square footage</b>',
                       title_x = 0.5, # center the title
                       legend=dict(yanchor="top", y=1, xanchor="left", x=1))
    return fig, fig2, num_listings
    
#-------------------------------------------------------------------------------------------------------------------------------------------

# Initiate the server where the app will run
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)