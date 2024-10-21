import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from itertools import *
from sklearn.linear_model import LinearRegression
from scipy import stats

from load_data import beer, dem, pop

############################### view 1 ##################################

# # # # # # # # # # # # # # # # fig_A # # # # # # # # # # # # # # # # # 

def fig_A_heatmap():
    return px.imshow(beer.sort_values(by=2017, ascending=False), color_continuous_scale="Spectral", text_auto=False).update_coloraxes(showscale=False).update_xaxes(scaleanchor="x", scaleratio=1).update_layout({
         "title": {"text": "BCPC", "x":0.73}})

 # # # # # # # # # # # # # # # # fig_A # # # # # # # # # # # # # # # # # 

def fig_B_bubblechart():
    x = beer[2017]
    y = dem[2017]
    z = pop[2017]

    colors = list(islice(cycle(iter(px.colors.diverging.Spectral)), len(beer)))
    
    return px.scatter(x=x, y=y, size=z, color=x, hover_name=x.index, color_continuous_scale="Spectral").update_traces({"marker": {"size": z*10,  "line": {"width": 1, "color":"black"}}}).update_layout({
        "title": "Beer Consumption Per Capita by Democratic Qualty and Population Size",
        "xaxis": {"title": "Beer Consumption Per Capita"},
        "yaxis": {"title": "Democratic Quality"},
        "coloraxis_colorbar": {"title": "Beer"},
        "coloraxis_showscale": False,
    })




############################### view 2 ##################################

 # # # # # # # # # # # # # # # # fig_C # # # # # # # # # # # # # # # # # 

def wrangle_year_difference(df, year1, year2):
    dem_dash = df.T.reset_index().rename(columns={"index": "Year"})
    mask_gt = ( dem_dash["Year"] >= year1 )
    mask_lt = ( dem_dash["Year"] <= year2)
    
    dem_dash = dem_dash[mask_gt & mask_lt].set_index("Year")
    dem_dash.loc[-1] = dem_dash.mean(axis=0)
    return pd.DataFrame(dem_dash.loc[-1])

from sklearn.linear_model import LinearRegression
from scipy import stats

def fig_C_scatter(df1, df2, year1, year2, size=None, conf=0.95, colors=px.colors.diverging.Temps, opacity=0.5, title=None):


    x = pd.Series(wrangle_year_difference(beer, year1, year2).values.flatten(), index=df1.index)
    y = pd.Series(wrangle_year_difference(dem, year1, year2).values.flatten(), index=df2.index)

    # x = df1[year]
    # y = df2[year]
    
    x_vals = x.interpolate()
    y_vals = y.interpolate()

        
    # sort x and y
    list_of_tuples = [(a,b) for a,b in zip(x_vals, y_vals)]
    list_of_sorted_tuples = sorted(list_of_tuples, key=lambda j: j[0])
    x_arr = np.asarray([a[0] for a in list_of_sorted_tuples])
    y_arr = np.asarray([b[1] for b in list_of_sorted_tuples])

    # linear regression model
    model = LinearRegression()
    model.fit(x_arr.reshape(-1, 1), y_arr)
    y_hat = model.predict(x_arr.reshape(-1, 1))

    # figures needed for inferential statistics
    n = x_arr.size
    m = len(x_arr.shape)
    dof = n - m
    t = stats.t.ppf(conf, dof)

    resid = y_arr - y_hat
    se = np.sqrt(np.sum(resid**2) / dof)

    ci = t * se * np.sqrt(1/n + (x_arr - np.mean(x_arr))**2 / np.sum((x_arr - np.mean(x_arr))**2))
    pi = t * se * np.sqrt(1 + 1/n + (x_arr - np.mean(x_arr))**2 / np.sum((x_arr - np.mean(x_arr))**2))

    pi2 = np.linspace(pi.min(), pi.max(), 100)
    x2 = np.linspace(x_arr.min(), x_arr.max(), 100)
    y_hat2 = np.linspace(y_hat.min(), y_hat.max(), 100)

    # scatterplot with ci // pi bands
    ff = go.Figure()

    ff.add_trace(
        go.Scatter(
            x=x_arr,
            y=y_hat+ci,
            mode="lines",
            line={"color": colors[2], "width": 0},
            name="upper ci band limit",
            showlegend=False
        )
    )

    ff.add_trace(
        go.Scatter(
            x=x_arr,
            y=y_hat-ci,
            mode="none",
            line={"color": colors[2], "width": 0},
            name=f"{round(conf * 100)}% Confidence Interval (mean)",
            fill="tonexty",
            fillcolor=colors[2]
        )
    )


    ff.add_trace(
        go.Scatter(
            x=x_arr,
            y=y_hat,
            mode="lines",
            line={"color": colors[1]},
            name="Linear model",
        )
    )
    
    
    ff.add_trace(
        go.Scatter(
            x=x_arr,
            y=y_arr,
            mode="markers",
            marker={"color": colors[0], "opacity": opacity, "size": size},
            name="Countries"
        )
    )

    ff.add_trace(
        go.Scatter(
            x=x2,
            y=y_hat2+pi2,
            mode="lines",
            line={"color": colors[3], "width": 1, "dash": "dash"},
            name=f"{round(conf*100)}% Prediction Interval (one datapoint)",
        )
    )

    ff.add_trace(
        go.Scatter(
            x=x2,
            y=y_hat2-pi2,
            mode="lines",
            line={"color": colors[3], "width": 1, "dash": "dash"},
            name="lower pi band limit",
            showlegend=False
        )
    )


    return ff.update_layout({"title": f"Beer Consumption and Democratic Quality, {year1} to {year2}",
                            "xaxis":{"title": "Beer Consumption Per Capita", "range": [0, 6]},
                            "yaxis": {"title": "Democratic Quality", "range": [-2.5, +2.5]},
                            "legend": {"visible": False}
                           })




# fig_C_scatter(beer, dem, year1, year2, size=None, conf=0.95, colors=px.colors.sequential.Oryel[::-1])

 # # # # # # # # # # # # # # # # fig_D # # # # # # # # # # # # # # # # # 
def fig_D_top_line_dem(df, country, year1, year2):

    dem_dash = dem.T.reset_index().rename(columns={"index": "Year"})
    
    mask_gt = ( dem_dash["Year"] >= year1 )
    mask_lt = ( dem_dash["Year"] <= year2)
    df = dem_dash[[country, "Year"]][mask_gt & mask_lt]
    return px.line(df, x="Year", y=country, markers=True).update_traces(line_color=px.colors.diverging.Spectral[1]).update_layout({
        "title": "Democratic Quality"
    })




def fig_E_top_line_beer(df, country, year1, year2):

    beer_dash = beer.T.reset_index().rename(columns={"index": "Year"})

    mask_gt = ( beer_dash["Year"] >= year1 )
    mask_lt = ( beer_dash["Year"] <= year2)
    df = beer_dash[[country, "Year"]][mask_gt & mask_lt]
    return px.line(df, x="Year", y=country, markers=True).update_traces(line_color=px.colors.diverging.Spectral[2]).update_layout({
        "title": "Beer Consumption Per Capita"
    })


 # # # # # # # # # # # # # # # # fig_E # # # # # # # # # # # # # # # # # 




############################### view 3 ##################################

 # # # # # # # # # # # # # # # # fig_F # # # # # # # # # # # # # # # # # 

def IQR(series):
    x = series
    mask = ((x >= x.quantile(0.25) - 1.5*(x.quantile(0.75)-x.quantile(0.25))) & (x <= x.quantile(0.75) + 1.5*(x.quantile(0.75)-x.quantile(0.25))))
    return mask


def fig_F_popbar():

    pop_dash = pop.T.reset_index().rename(columns={"index": "Year"})
    mask = ( pop_dash["Year"]==2017 )
    pop_dash = pop_dash[mask].drop(["Year"], axis=1).T.rename(columns={9:"pop"}).sort_values(by=["pop"], ascending=False)    

    mask = IQR(pop_dash["pop"])

    return go.Figure(go.Bar(y=pop_dash[mask]["pop"], x=pop_dash[mask].index, marker={"color": pop_dash[mask]["pop"], "colorscale": "Spectral"})).update_layout({
        "title": "Population by Country, outliers [China and India] removed",
        "xaxis": {"title": "Country"},
        "yaxis": {"title": "Population"},
    })



paper_bgcolor="white"
plot_bgcolor="white"
font_color="black"
legend_color="white"

def layout_func(fig):
    
    fig.update_layout(
        dict(
            paper_bgcolor=paper_bgcolor,
            plot_bgcolor=plot_bgcolor,
            font={"color": font_color},
            clickmode="select",
            legend={"bgcolor":legend_color,
                    "font": {"color":font_color},
                    "title":{"font":{"color":font_color}},
                    },
            # title=dict(
                # font={"size": 28.5, "color": font_color},
                # ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
            )
        )
    )

    return fig.update_layout({
        "xaxis": {"mirror": False, "showline": True, "linecolor": "lightgrey", "linewidth": 2},
        "yaxis": {"mirror": False, "showline": True, "linecolor": "lightgrey", "linewidth": 2},

    })