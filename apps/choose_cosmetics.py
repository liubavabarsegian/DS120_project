#one of the pages of the app, where the person chooses its skintype and the product is recommended

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_table


# get relative data folder, we are doiing this, as the datasets are in the datasets folder, not the current directory
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Sephora_cosmetics_df.csv"))
app.config['suppress_callback_exceptions']=True

layout = html.Div([
    html.H1("Choose cosmetics"),
    html.Div([
        html.P('We will help you to choose the best fitting skincare product.\n')
        #html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ]),
    html.H4("Please specify the skincare product you want\n"),
    dcc.Dropdown( #dropdown for product type
            id = 'product_dd',
            options=[       #{'value': x, 'label': x} for x in labels],
                {'label': 'Moisturizer', 'value': 'Moisturizer'},
                {'label': 'Cleanser', 'value': 'Cleanser'},
                {'label': 'Treatment', 'value': 'Treatment'},
                {'label': 'Eye cream', 'value': 'Eye cream'},
                {'label': 'Sun protect', 'value': 'Sun protect'},
                {'label': 'Face Mask', 'value': 'Face Mask'},
                {'label': 'Not sure', 'value': 'Not sure'}
            ],
            multi=True,
            value=['Moisturizer','Cleanser']  #the default value set

    ),
    html.H4("Please specify your skin type\n"),
    dcc.Dropdown( #dropdown for skin type
                id = 'skintype_dd',
                options=[
                    {'label': 'Oily', 'value': 'Oily'},
                    {'label': 'Dry', 'value': 'Dry'},
                    {'label': 'Combination', 'value': 'Combination'},
                    {'label': 'Sensitive', 'value': 'Sensitive'},
                    {'label': 'Not sure', 'value': 'Not sure'}
                ],
                multi=True,
                value=['Combination','Sensitive']

    ),
    #html.Div(id='my_output')

    html.Div([
        dash_table.DataTable(
        id='my_output',
        # columns=[],#[{"name": i, "id": i} for i in []],
        # data = {}
        )
    ])
])


@app.callback(
    [Output(component_id='my_output', component_property="data"),
     Output(component_id='my_output', component_property="columns")],
    [Input(component_id='product_dd', component_property='value'),
    Input(component_id ='skintype_dd', component_property='value')]
)
def cosmetics(label, skintype):
    if label is None and skintype is None:
        raise PreventUpdate
    if ('Not sure' not in skintype) and ('Not sure' in label):
        df_full = df[df.Rank >=4.5]
        skintypes_test = {}
        for i in df_full.index:
            skins = []
            the_best_one_test = df_full[df_full.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins
        matched=[]
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if set(skintype).issubset(set(v)):
                matched.append(i)
        final = df_full.loc[matched]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Label', inplace=True)
        final = final[['Label','Brand', 'Name', 'Price', 'Rank']]
        final.reset_index(inplace = True, drop=True)
        return final.to_dict('records'), [{"name": i, "id": i} for i in final.columns]

    elif ('Not sure' in skintype) and ('Not sure' not in label):
        df_label = df[df.Label.apply(lambda x: x in label)]
        df_label = df_label[df_label.Rank >=4.5]
        skintypes_test = {}
        for i in df_label.index:
            skins = []
            the_best_one_test = df_label[df_label.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins
        more_skins = []
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if len(v) == 5:
                more_skins.append(i)
        if len(more_skins)==0:
            for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
                if len(v) == len(max(skintypes_test.values())):
                    more_skins.append(i)


        final = df_label.loc[more_skins]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Brand', inplace=True)
        final = final[['Brand', 'Name', 'Price', 'Oily', 'Combination', 'Dry', 'Sensitive', 'Normal']]
        final.reset_index(inplace = True, drop=True)
        # final = final.style.set_properties(**{'background-color': 'thistle',
        #                               'color': 'navy',
        #                               'border-color': 'purple4'})
        return final.to_dict('records'), [{"name": i, "id": i} for i in final.columns]

    elif ('Not sure' not in skintype) and ('Note sure' not in label):
        df_label = df[df.Label.apply(lambda x: x in label)]
        df_label = df_label[df_label.Rank >=4.5]
        skintypes_test = {}
        for i in df_label.index:
            skins = []
            the_best_one_test = df_label[df_label.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins

        matched=[]
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if set(skintype).issubset(v):
                matched.append(i)
        final = df_label.loc[matched]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Brand', inplace=True)
        final = final[['Brand', 'Name', 'Price']]
        final.reset_index(inplace = True, drop=True)
        return(final.to_dict('records'), [{"name": i, "id": i} for i in final.columns])

    elif ('Not sure' in label) and ('Not sure' in skintype):
        df_full = df[df.Rank >=4.5]
        skintypes_test = {}
        for i in df_full.index:
            skins = []
            the_best_one_test = df_full[df_full.index == i]
            if the_best_one_test.Combination[i] == 1:
                skins.append('Combination')
            if the_best_one_test.Dry[i] == 1:
                skins.append('Dry')
            if the_best_one_test.Normal[i] == 1:
                skins.append('Normal')
            if the_best_one_test.Oily[i] == 1:
                skins.append('Oily')
            if the_best_one_test.Sensitive[i] ==1:
                skins.append('Sensitive')
            skintypes_test[i] = skins
        more_skins = []
        for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
            if len(v) == 5:
                more_skins.append(i)
        if len(more_skins)==0:
            for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
                if len(v) == len(max(skintypes_test.values())):
                    more_skins.append(i)
        final = df_full.loc[more_skins]
        final.drop_duplicates(inplace = True)
        final.sort_values('Rank', ascending=False, inplace=True)
        final.drop_duplicates('Label', inplace=True)
        final = final[['Label','Brand', 'Name', 'Price', 'Rank','Oily', 'Combination', 'Dry', 'Sensitive', 'Normal']]
        final.reset_index(inplace = True, drop=True)
        return(final.to_dict('records'), [{"name": i, "id": i} for i in final.columns])