#!/usr/local/bin python
#-*- coding: utf-8 -*-
import pathlib
import dash
import pandas as pd
import plotly
import pybso.charts as charts
import json
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import chart_studio.tools as tls
import chart_studio.plotly as py
import config

# chart studio credentials
tls.set_credentials_file(username='azurscd', api_key='K7ljyIXPB3XU6Lyk9QUp')

# config variables
port = config.PORT
host = config.HOST
url_subpath = config.URL_SUBPATH

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
    url_base_pathname=url_subpath
)
app.title = "Baromètre OA UCA"
server = app.server

# Load data

df_structures = pd.read_json(DATA_PATH.joinpath(
    "df_structures.json"), encoding="utf-8")
dict_structures = df_structures[df_structures.parent_id != 0][[
    "id", "affiliation-name"]].rename(columns={"id": "value", "affiliation-name": "label"}).to_dict('records')
dict_structures.insert(0, {'value': 0, 'label': 'UCA toutes structures'})
df_corpus = pd.read_csv(DATA_PATH.joinpath(
    "df_corpus.csv"), sep=',', encoding="utf-8")
df_doi_oa = pd.read_csv(DATA_PATH.joinpath(
    "df_doi_oa.csv"), sep=',', encoding="utf-8", dtype={"doi_prefix": str})

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
)

# Create app layout
app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url(
                                "logo_UCA_bibliotheque_ligne_couleurs.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Baromètre Open Access UCA",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Version minimale one page", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Documentation",
                                        id="learn-more-button"),
                            href="#",
                        ),
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Sélectionner une structure de recherche:",
                               className="control_label"),
                        dcc.Dropdown(
                            id="selected_structures",
                            options=dict_structures,
                            # for multiselect : value=[num["value"] for num in dict_structures],
                            value=0,
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    # widgets totaux
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("2016-2021"),
                                     html.P("Période analysée")],
                                    id="period",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="nb_publis_text"), html.P(
                                        "Nombre de publications")],
                                    id="nb_publis",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="nb_structures_text"), html.P(
                                        "Nombre de structures de recherche")],
                                    id="nb_structures",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="rate_open_text"),
                                     html.P("Taux d'ouverture")],
                                    id="rate_open",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        )
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="oa_rate_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="oa_rate_by_year_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
         html.Div(
            [
                 html.Div(
                    [ 
                    html.P("Choisir un nombre d'éditeurs à afficher :", className="control_label"), 
                    dcc.Slider(
                      id='nb_publishers',
                      min=5,
                      max=50,
                      step=5,
                      value=10,
                      className="dcc_control",
                      updatemode = "drag",
                      marks = {i: "{}".format(i) for i in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]},
                           ),                       
                        ],
                    className="pretty_container three columns",
                ),
                html.Div(
                    [dcc.Graph(id="rate_by_publisher_graph",style={"height": "600px"})],
                    className="pretty_container nine columns",
                )
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="by_status_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="by_type_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),

        html.Div(
            [
                html.Footer(
                    [
                        html.P(
                            [
                                "2022 - SCD Université Côte d'Azur. | Built with",
                                html.Img(
                                    src=app.get_asset_url('dash-logo.png'),
                                    height='43 px',
                                    width='auto')
                            ])
                    ]
                )
            ],
            id="footer",
            className="row flex-display",
            style={"margin-bottom": "25px"}
        )
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# Helper functions
def doi_synthetics_aff(ids):
    if ids == 0:
        data = df_doi_oa
    else:
        selected = ids
        # print(selected)
        # for multiselect : list_doc = df_corpus[df_corpus["aff_internal_id"].isin(selected)]["doi"].unique().tolist()
        list_doc = df_corpus[df_corpus["aff_internal_id"]
                             == selected]["doi"].unique().tolist()
        list_doc = list(map(str, list_doc))
        print(len(list_doc))
        data = df_doi_oa[df_doi_oa['doi'].isin(list_doc)]
    return data

# Text Callbacks


@app.callback(
    Output("nb_publis_text", "children"),
    [Input("selected_structures", "value")],
)
def update_nb_publis_text(selected_structures):
    dff = doi_synthetics_aff(selected_structures)
    return dff.shape[0]


@app.callback(
    Output("nb_structures_text", "children"),
    [Input("selected_structures", "value")],
)
def update_nb_structures_text(selected_structures):
    return len(dict_structures)


@app.callback(
    Output("rate_open_text", "children"),
    [Input("selected_structures", "value")],
)
def update_rate_open_text(selected_structures):
    dff = doi_synthetics_aff(selected_structures)
    rate = round(float(dff[dff["is_oa_normalized"] ==
                 "Accès ouvert"].shape[0] / dff.shape[0] * 100), 2)
    return '{} %'.format(rate)

# Charts callbacks


@app.callback(
    Output("rate_by_publisher_graph", "figure"),
    Output("oa_rate_graph", "figure"),
    Output("oa_rate_by_year_graph", "figure"),
    Output("by_status_graph", "figure"),
    Output("by_type_graph", "figure"),
    [
        Input("selected_structures", "value"),
		Input("nb_publishers", "value")
    ],
)
def generate_figure(selected_structures,nb_publishers):
    dff = doi_synthetics_aff(selected_structures)
    return charts.oa_rate_by_publisher(dataframe=dff, publisher_field="publisher_by_doiprefix", n=int(nb_publishers)), charts.oa_rate(dataframe=dff), charts.oa_rate_by_year(dataframe=dff), charts.oa_by_status(dataframe=dff), charts.oa_rate_by_type(dataframe=dff)


# Main
if __name__ == "__main__":
    app.run_server(port=port, host=host)
