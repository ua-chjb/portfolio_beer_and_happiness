from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from load_data import beer
from charts import fig_A_heatmap, fig_B_bubblechart, fig_F_popbar, layout_func

# # # # # # # # # # # # # # # # # # # # # # # # #

Card_title = dbc.Card(
    dbc.CardBody([
        html.H1("What role does beer play in freedom?", className="title")
    ], className="knucklepuck")
)

Card_top_left = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure=fig_A_heatmap(), className="innerchart")
    ], className="knucklepuck"), className="lbabyflex"
)

Card_top_right = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure=layout_func(fig_B_bubblechart()), className="innerchart")
    ], className="knucklepuck"), className="rbabyflex"
)
# # # # # # # # # # # # # # # # # # # # # # # # #
Card_2fold_left = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure={}, id="bbdgraph", className="midfoldney")
    ], className="knucklepuck midfoldney")
)
    # statistical chart

Card_2fold_right_top = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure={}, id="demgraph", className="openmidone")
    ], className="knucklepuck openmidone")
)
    # beer consumption

Card_2fold_right_middle = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure={}, id="beergraph", className="openmidtwo")
    ], className="knucklepuck openmidtwo")
)
    # democratic quality

Card_2fold_right_bottom = dbc.Card(
    dbc.CardBody([
        dcc.RangeSlider(
            min=2008, max=2018, step=1, 
            marks={
                2008: "2008",
                2009: "2009",
                2010: "2010",
                2011: "2011",
                2012: "2012",
                2013: "2013",
                2014: "2014",
                2015: "2015",
                2016: "2016",
                2017: "2017",
                2018: "2018"
            },
            value=[2008, 2018],
            id="aragorn",
            className="openmidthree"
        ),
    ], className="knucklepuck openmidthree")
)
     # slider

# # # # # # # # # # # # # # # # # # # # # # # # #
Card_3fold = dbc.Card(
    dbc.CardBody([
        dcc.Graph(figure=layout_func(fig_F_popbar()))
    ], className="knucklepuck"), className="downbelow"
)
 #####################################################################################

fold1 = html.Div([
    Card_title,
    html.Div([
        Card_top_left,
        Card_top_right
    ],  className="flexdaddy")
])

fold2 = html.Div([
    html.Div([
        Card_2fold_left
    ], className="left"),
    html.Div([
        Card_2fold_right_top,
        Card_2fold_right_middle,
        Card_2fold_right_bottom,
    ], className="right midflex")
], className="fold2flex")

fold3 = html.Div([
    Card_3fold
], className="belowbelow")

 #####################################################################################


beerstore = html.Div([
    dcc.Store(id="beerstore", data={}, storage_type="memory"),
])

demstore = html.Div([
    dcc.Store(id="demstore", data={}, storage_type="memory"),
])

popstore = html.Div([
    dcc.Store(id="popstore", data={}, storage_type="memory"),
])


lyt = html.Div([
    fold1,
    fold2,
    fold3,
    beerstore,
    demstore,
    popstore
], className="goldenale")