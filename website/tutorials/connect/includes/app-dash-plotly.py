import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from palmerpenguins import load_penguins

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the data
dat = load_penguins()
species = dat["species"].unique().tolist()

# Define the layout
app.layout = html.Div([
    html.H1("Palmer Penguins Bill Length"),

    # Radio buttons for species selection
    html.Div([
        html.Label("Species:"),
        dcc.RadioItems(
            id='species-radio',
            options=[{'label': s, 'value': s} for s in species],
            value=species[0],
            inline=True
        )
    ]),

    # Graph container
    dcc.Graph(id='histogram-plot')
])

# Callback to update the plot based on species selection
@app.callback(
    Output('histogram-plot', 'figure'),
    Input('species-radio', 'value')
)
def update_plot(selected_species):
    # Create two histogram traces
    # 1. All penguins (light gray)
    all_penguins = go.Histogram(
        x=dat["bill_length_mm"].dropna(),
        xbins=dict(size=1),
        marker_color='#C2C2C4',
        name='All Penguins'
    )

    # 2. Selected species (blue)
    sel = dat[dat["species"] == selected_species]
    selected_penguins = go.Histogram(
        x=sel["bill_length_mm"].dropna(),
        xbins=dict(size=1),
        marker_color='#447099',
        name=f'{selected_species}'
    )

    # Create the figure
    fig = go.Figure(data=[all_penguins, selected_penguins])

    # Update layout
    fig.update_layout(
        title=f'Bill Length Distribution',
        xaxis_title='Bill Length (mm)',
        yaxis_title='Count',
        barmode='overlay',
        template='plotly_white',
        showlegend=False
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run()
