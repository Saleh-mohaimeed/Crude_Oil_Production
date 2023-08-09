import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import Extract_Data

# Get data from Extract_Data module
data = Extract_Data.get_data()

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Title
    html.H1('Production of Crude Oil in Thousand Barrels per day',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Table displaying the data
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in data.columns],
        data=data.to_dict('records'),
        page_action='none',
        fixed_rows={'headers': True},
        style_table={'height': '300px', 'width': '95%', 'overflowY': 'auto', 'align': 'center'},
        style_cell={'textAlign': 'left'},
        style_data={'border': '1px solid black'},
        style_header={'border': '1px solid black', 'background': 'rgb(191, 191, 191)'}
    ),

    html.Br(),

    # DropDown to select the year for the pie chart
    dcc.Dropdown(
        id='pie-chart-years-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': '2022', 'value': 2022},
            {'label': '2023', 'value': 2023},
        ],
        value='All',
        placeholder="Select a Production Year",
        searchable=False
    ),

    # Add the pie chart
    html.Div(dcc.Graph(id='production-pie-chart')),
    html.Br(),

    # Dropdown for the bar chart
    dcc.Dropdown(
        id='production-by-year-month-dropdown',
        options=[
            {'label': 'Years', 'value': 'Years'},
            {'label': 'Months', 'value': 'Months'},
            {'label': 'Years-Months', 'value': 'Years-Months'},
        ],
        value='Years',
        placeholder="Select an Aggregation Type",
        searchable=False
    ),
    html.Div(dcc.Graph(id='production-by-year-month-bar-chart')),
    html.Br(),
])


# Define app callback for the pie chart
@app.callback(
    Output(component_id='production-pie-chart', component_property='figure'),
    Input(component_id='pie-chart-years-dropdown', component_property='value')
)
def get_pie_chart(entered_year):
    if entered_year == 'All':
        # Calculate sum of production values by country for all years
        sum_data = data.groupby(by="Country", as_index=False)["Value"].sum()
        fig = px.pie(sum_data[sum_data["Value"] > 0], values='Value', names="Country", title='Production By Country in All Years')
    else:
        # Calculate sum of production values by country for the selected year
        sum_data = data[data["Year"] == entered_year].groupby(by="Country", as_index=False).sum()
        fig = px.pie(sum_data[sum_data["Value"] > 0], values='Value', names="Country", title=f'Production By Country in {entered_year}')
    return fig


# Define app callback for the bar chart
@app.callback(
    Output(component_id='production-by-year-month-bar-chart', component_property='figure'),
    Input(component_id='production-by-year-month-dropdown', component_property='value')
)
def get_bar_chart(aggregation):
    if aggregation == 'Years':
        # Calculate sum of production values by year
        sum_data = data.groupby(by="Year", as_index=False).sum()
        fig = px.bar(sum_data, x='Year', y="Value", title='Production By Years')
    elif aggregation == "Months":
        # Calculate sum of production values by month
        sum_data = data.groupby(by="Month", as_index=False).sum()
        fig = px.bar(sum_data, x='Month', y="Value", title='Production By Months')
    elif aggregation == "Years-Months":
        # Calculate sum of production values by year and month
        sum_data = data.groupby(by=["Year", "Month"], as_index=False).sum()
        sum_data["Year-Month"] = sum_data["Year"].astype('string') + '-' + sum_data["Month"]
        fig = px.bar(sum_data, x='Year-Month', y="Value", title='Production By Years-Months')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
