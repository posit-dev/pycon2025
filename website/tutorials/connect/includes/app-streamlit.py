import streamlit as st
from palmerpenguins import load_penguins
from plotnine import aes, geom_histogram, ggplot, theme_minimal
import matplotlib.pyplot as plt

# Load the data
dat = load_penguins()
species = dat["species"].unique().tolist()

# Add radio button widget
selected_species = st.radio("Species", species, horizontal=True)

# Filter data based on selection
sel = dat[dat["species"] == selected_species]

# Create plot
plot = (
    ggplot(aes(x="bill_length_mm"))
    + geom_histogram(dat, fill="#C2C2C4", binwidth=1)
    + geom_histogram(sel, fill="#447099", binwidth=1)
    + theme_minimal()
)

# Display the plot
st.pyplot(ggplot.draw(plot))
