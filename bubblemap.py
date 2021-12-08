import plotly.express as px
import pandas as pd

state_df = pd.read_csv('MapData2.csv', encoding='latin-1')

# fig = px.choropleth(state_df,  # Input Pandas DataFrame
#                     locations="state",  # DataFrame column with locations
#                     color="Value",  # DataFrame column with color values
#                     hover_name="state", # DataFrame column hover info
#                     locationmode = 'USA-states') # Set to plot as US States


fig = px.scatter_geo(state_df,  # Input Pandas DataFrame
                    locations="city",  # DataFrame column with locations
                    # color="Value",  # DataFrame column with color values
                    hover_name="state", # DataFrame column hover info
                    size='value',
                    locationmode = 'USA-states',) # Set to plot as US States


fig.update_layout(
    title_text = 'State Rankings', # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
)
fig.show()
