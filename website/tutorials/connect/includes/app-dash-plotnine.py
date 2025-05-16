from palmerpenguins import load_penguins
# Set matplotlib backend to non-GUI 'Agg' before importing plotnine
# Matplotlib is trying to create GUI elements outside the main thread, which is not allowed on macOS.
# common issue when using plotting libraries that rely on Matplotlib in threaded web applications
import matplotlib
matplotlib.use('Agg')
from plotnine import aes, geom_histogram, ggplot, theme_minimal
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from io import BytesIO
import base64

# Load the data
dat = load_penguins()
species = dat["species"].unique().tolist()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Palmer Penguins"),

    # Radio buttons for species selection
    html.Div([
        html.Label("Species"),
        dcc.RadioItems(
            id="species",
            options=[{"label": s, "value": s} for s in species],
            value=species[0],  # Default to first species
            inline=True
        )
    ]),

    # Image component to display the plotnine plot
    html.Img(id='plot-image')
])

# Define callback to update the plot based on species selection
@app.callback(
    Output('plot-image', 'src'),
    Input('species', 'value')
)
def update_plot(selected_species):
    # Filter data for selected species
    sel = dat[dat["species"] == selected_species]

    # Create the plotnine plot
    plot = (
        ggplot(aes(x="bill_length_mm"))
        + geom_histogram(dat, fill="#C2C2C4", binwidth=1)
        + geom_histogram(sel, fill="#447099", binwidth=1)
        + theme_minimal()
    )

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plot.save(img_buffer, format="png", dpi=100, width=8, height=6, units="in")
    img_buffer.seek(0)

    # Convert to base64 for displaying in the Dash app
    img_str = base64.b64encode(img_buffer.read()).decode()

    return f'data:image/png;base64,{img_str}'

# Run the app
if __name__ == '__main__':
    app.run()
