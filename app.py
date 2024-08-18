import datetime
import yfinance as yf
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Initializes the Dash app
app = Dash(__name__)
app.title = "Stock Visualization"

# Defines the layout of the app
app.layout = html.Div(children=[
    html.H1("Stock Visualization Dashboard"),
    html.H4("Please enter the stock ticker symbol"),
    dcc.Input(id='input', value='BLK', type='text'),
    dcc.Graph(id='output-graph')
])

# Defines the callback function to update the graph
@app.callback(
    Output(component_id='output-graph', component_property='figure'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()

    try:
        # Uses yfinance to fetch stock data
        df = yf.download(input_data, start=start, end=end)

        # Prints the first few rows of the DataFrame
        print(df.head())

        # Checks if the DataFrame is empty
        if df.empty:
            return {
                'data': [],
                'layout': {'title': f"No data found for {input_data}"}
            }

        # Creates a line graph
        figure = {
            'data': [{'x': df.index, 'y': df['Close'], 'type': 'line', 'name': input_data}],
            'layout': {'title': input_data}
        }

        return figure

    except Exception as e:
        # Prints the exception to the console for debugging
        print(f"Error: {e}")
        return {
            'data': [],
            'layout': {'title': f"Error retrieving data for {input_data}"}
        }

# Runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
