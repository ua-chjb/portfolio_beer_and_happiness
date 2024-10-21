import dash_bootstrap_components as dbc
from load_data import beer, dem, pop

Card_top_left = html.Div([
    # heatmap
])

Card_top_right = html.Div([
    # CI scatter, with slider
])


Card_below = html.Dvi([
    # boxplots
])





lyt = dbc.Container([
    above_fold,
    below_fold
])