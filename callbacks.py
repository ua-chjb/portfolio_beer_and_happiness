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
        



# def callbacks_baby(app):
#     @app.callback(
#         Output(component_id="beerstore", component_property="data", allow_duplicate=True),
#         [Input(component_id="aragorn", component_property="value"), 
#         Input(component_id="kingofmen", component_property="value")],
#         prevent_initial_call=True,
#     )
#     def buy_sword(years, country):
#         mask = ( beer["Country"]==country )
#         beer = beer[mask]

#         year1 = years[0]
#         year2 = years[1]

#         return wrangle_year_difference(beer).to_json()

#     @app.callback(
#             Output(component_id="demstore", component_property="data", allow_duplicate=True),
#             [Input(component_id="aragorn", component_property="value"),
#             Input(component_id="kingofmen", component_property="value")],
#             prevent_initial_call=True
#     )
#     def buy_shield(years, country):
#         mask = ( dem["Country"]==country )
#         dem = dem[mask]
        
#         year1 = years[0]
#         year2 = years[1]

#         return wrangle_year_difference(dem, year1, year2).to_json()


#     @app.callback(
#         [Output(component_id="bbdgraph", component_property="figure"),
#         Output(component_id="demgraph", component_property="figure"),
#         Output(component_id="beergraph", component_property="figure")],
#         [
#             Input(component_id="beerstore", component_property="data"),
#             Input(component_id="demstore", component_property="data"),
#         ],
#     )
#     def destroy_orcs(data1, data2):
#         return fig_C_scatter(beer, dem, year1, year2), fig_D_top_line_beer(beer, "Average", year1, year2), fig_E_top_line_beer(dem, "Average", year1, year2)


# def callbacks_baby(app):
#     @app.callback(
#         Output(component_id="left_lg_dd", component_property="options"),
#         Input(component_id="left_ct_dd", component_property="value"),
#     )
#     def left_dropdown_country_to_league(country_value):
#         mask_country = ( home["country_name"]==country_value )
#         home1 = home[mask_country].copy()
#         return [j for j in home1["league_name"].unique()]
