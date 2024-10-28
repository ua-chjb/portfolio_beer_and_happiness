from dash import Input, Output, State, exceptions
from load_data import beer, dem, pop
from charts import fig_C_scatter, fig_D_top_line_dem, fig_E_top_line_beer, layout_func

def callbacks_baby(app):
    @app.callback(
        [Output(component_id="bbdgraph", component_property="figure"),
        Output(component_id="demgraph", component_property="figure"),
        Output(component_id="beergraph", component_property="figure")],
        Input(component_id="aragorn", component_property="value")
    )
    def aragorn_returns(years):
        year1 = years[0]
        year2 = years[1]
        return layout_func(fig_C_scatter(beer, dem, year1, year2)), layout_func(fig_D_top_line_dem(dem, "Average", year1, year2)), layout_func(fig_E_top_line_beer(beer, "Average", year1, year2))