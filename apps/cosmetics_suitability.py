#!pip install pytesseract
# !pip install opencv-python
# !pip install pillow
# !pip install textdistance
# !pip install dash
# !pip install base64
# !pip install nltk
# !pip install pathlib
# !pip install dash_table
import os
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from app import app
import dash_table
import textdistance as td
import pathlib
# import app
import base64
import regex
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords_ = stopwords.words('english')
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
from PIL import ImageEnhance
from PIL import Image, ImageFilter
from PIL import ImageOps
import numpy as np
import pandas as pd
import os
import datetime
import re
import string

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
currpath = os.getcwd()

# get relative data folder, we are doiing this, as the datasets are in the datasets folder, not the current directory
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("Sephora_cosmetics_df.csv"))

app.config['suppress_callback_exceptions']=True

layout = html.Div(
    [
        html.H1(children = "Check whether the cosmetics suits you", 
        style={
            'vertical-align':'buttom',
            'textAlign':'center',
            'color':'#1A3E5C', 
            'background-color':'#7F7DA9',
            
            'height':'70px',
            'text-align':'50PX',
            'borderRadius':'25px',
            "boxShadow": "0px 15px 30px -10px grey",
            'font-family':'Segoe Print'
                }
            ),
        html.H1('How does it work?', 
        style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
            'font-family':'cursive'
        }),
        html.H2('First, you upload a photo according to the instructions below. Please, make sure that the the photo is not blurry, and the text is readable. Also, do not forget to crop the photo so only ingredients are visible.', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
            'font-family':'cursive'
        }), 
        html.H2('Second, our app converts the image to text', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
            'font-family':'cursive'
        }),
        html.H2('After it, little people inside the machine are rushing to find out whether the product is suitable for you:)', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
            'font-family':'cursive'
        }),
        html.H1('Here are some instructions of the photo uploading', 
            style={
                'text-align':'center',
                'color':'#1A3E5C', 
                'font-family':'cursive'
            }),
        html.Div([
        html.Img(src=app.get_asset_url('image1.jpg'),
                style={
                    'text-align':'center',
                    'height':'200px',
                    #'width':'200px',
                    'display': 'inline-block',
                    'margin-right':'3%',
                    'margin-left':'3%'
                    
                }
        ),
       html.Img(src=app.get_asset_url('image2.jpg'),
                style={
                    'text-align':'center',
                    'height':'200px',
                    'display': 'inline-block',
                    'margin-left':'3%' ,
                    'margin-right':'3%',                 
                }

       ),
       html.Img(src=app.get_asset_url('image3.jpg'),
                style={
                    'text-align':'center',
                    'height':'200px',
                    #'width':'200px',
                    'display': 'inline-block',
                    'margin-right':'3%',
                    'margin-left':'3%',
                }

       ),
       html.Img(src=app.get_asset_url('image4.jpg'),
                style={
                    'text-align':'center',
                    'height':'200px',
                    #'width':'200px',
                    'display': 'inline-block',
                    'margin-left':'3%'
                },

       ),
        ],style = {
            'text-align':'center',
        }
        ),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files', 
                )
            ],
            style = {
                    'fontSize':'23px',
                    'verical-align':'center',
                    'margin':'2px',
                    'margin-top':'5px',
                    'font-family':'Segoe Print'
                }
            ),
            style={
                'width': '20%',
                'height': '40px',
                'lineHeight': '80p',
                'borderStyle': 'hidden',
                'borderRadius': '15px',
                'text-align': 'center',
                
                "boxShadow": "0px 15px 30px -10px grey",
                "margin-left": "auto",
                "margin-right": "auto",
                "transform": "scale(1.5)",
                'margin-top':'50px',
                'margin-bottom':'50px',


                "background": "#7F7DA9",
                'color':'#1A3E5C', 
                "filter": "progid:DXImageTransform.Microsoft.gradient(startColorstr='#46fcb1',endColorstr='#3ffb6e',GradientType=1)",
                'font-family':'Segoe Print',
                'width':'400px',
            },

            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload',
                 style={
                     'text-align': 'center',
                 }),
        html.H5(id='output-ingredients_str'),
        html.H2("Please specify the skincare product you want\n",
                 style={
            'color':'#1A3E5C', 
            'margin':'25px',
            'margin-left':'25px',
            'margin-right':'25px',
            'font-family':'cursive'
        }),
        dcc.Dropdown(  # dropdown for product type
            id='product_dd',
            options=[
                {'label': 'Moisturizer', 'value': 'Moisturizer'},
                {'label': 'Cleanser', 'value': 'Cleanser'},
                {'label': 'Treatment', 'value': 'Treatment'},
                {'label': 'Eye cream', 'value': 'Eye cream'},
                {'label': 'Sun protect', 'value': 'Sun protect'},
                {'label': 'Face Mask', 'value': 'Face Mask'},
                {'label': 'Not sure', 'value': 'Not sure'}
            ],
            style = {
                'color':'#1A3E5C', 
                'background-color':'#A5AFDC', 
                #'display':'inline-block',
                'margin-top':'25px',
                'margin-bottom':'25px',
                'borderRadius':'25px',
                'font-size':'20px'
            },
            # value='Moisturizer', #the default value set
            multi=True
        ),
        html.H2("Please specify your skin type\n", 
            style= {
                'color':'#1A3E5C',
                'margin':'15px',
                'margin-left':'25px',
                'margin-right':'25px',
                'font-family':'cursive'
            }),
    html.H2("Here is a picture that can help you determine the skin type. If anyway you cannot do it, please select 'Not sure' option\n", 
        style= {
                'color':'#1A3E5C', 
                'margin':'15px',
                'margin-left':'25px',
                'margin-right':'25px',
                'font-family':'cursive'
            }),
    html.Div([
    html.Img(
        src=app.get_asset_url('skintypes.jpg'),
        style={
            'border-style':'solid',
            'border-color':'navy',
            'borderRadius':'50x',
            'display':'block',
                                    
        }),
    ],
    style = {
        #'text-align':'center',
        'margin-left':'20%',
        'margin-right':'20%'
    }),
        dcc.Dropdown( #dropdown for skin type
                id = 'skintype_dd',
                options=[
                    {'label': 'Oily', 'value': 'Oily'},
                    {'label': 'Dry', 'value': 'Dry'},
                    {'label': 'Combination', 'value': 'Combination'},
                    {'label': 'Sensitive', 'value': 'Sensitive'},
                    {'label' : 'Normal', 'value' : 'Normal'},
                    {'label': 'Not sure', 'value' : 'Not sure'}
                ],
                style = {
                'color':'#1A3E5C', 
                'background-color':'#A5AFDC', 
                'margin-top':'25px',
                'margin-bottom':'25px',
                'borderRadius':'25px',
                'font-size':'20px'
            },
                #value='Combination',
                multi=True
            ),

        html.H2(
            id = 'text1',
            style={
                        'color': 'navy',
                        'margin': '20px',
                    }),

        dash_table.DataTable(
            id='df_output',

            style_header={
                'border': '1px solid indigo',
                'fontWeight': 'bold'},
            style_cell={
                'backgroundColor': '#98B2C8',
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'navy',

                'border': '1px solid indigo',
                'textAlign': 'left',

            },
        ),

        html.H1('Thank you!',
                style={
                    'margin-top': '100px',
                    'margin-left': '25px',
                    'margin-right': '25px',
                }),

    ],
    style={
        style = {
        'backgroundColor':'lavender',
        'marginBottom':'0px',
        'margin-bottom':'0px',
        'background':'lavender',
        'margin-left':'10%',
        'margin-right':'10%',
        },


    },
)


def parse_contents(contents, filename):
    """Parses the uploaded image on dash"""
    return html.Div([
        html.H3(filename),
        print(contents),
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
    ])


def save_file(contents):
    """Decode and store a file uploaded with Plotly Dash."""
    data = contents[0].encode("utf8").split(b";base64,")[1]
    with open('some_image.png', "wb") as fp:
        fp.write(base64.decodebytes(data))


# defining OCR function
def ocr(pic):
    # Read image
    im = Image.open(pic)
    # make black
    bw = im.convert('L')

    enh = ImageEnhance.Contrast(bw).enhance(2.8)

    # enh = ImageOps.invert(enh)

    ##display image
    # enh.show()

    # #saves the image in the current directory
    # enh.save("black.jpg")
    a = pytesseract.image_to_string(enh, lang='eng')
    n = re.findall("\w+", a)
    t = ", ".join(n)
    t = t[13:]
    t = ''.join([word for word in t if word not in string.punctuation])
    t = ' '.join([word for word in t.split() if word not in stopwords_])
    return t




@app.callback(Output('output-ingredients_str', 'children'),
              Input('upload-image', 'contents'))
def ocr_output(contents):  # function for ocr output
    if contents is not None:
        save_file(contents)  # saves the imported image in the apps directory, whenever an image has been uploaded
        filename = currpath + "/some_image.png"
        ingredients_str = ocr(filename)  # reads the text from the image
        return ingredients_str


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(contents, names):  # function for showing the uploaded picture
    if contents is not None:
        return parse_contents(contents, names)


@app.callback(
    [Output(component_id='df_output', component_property="data"),
    Output(component_id='df_output', component_property="columns"),
    Output(component_id='text1', component_property="children")],
    [Input(component_id='output-ingredients_str', component_property='children'),
    Input(component_id='product_dd', component_property='value'),
    Input(component_id ='skintype_dd', component_property='value')]
)



def cosmetics_with_ingredients(ingredients, label, skintype):
    if ingredients is None or label is None or skintype is None:
        raise PreventUpdate

    elif ('Not sure' in label) and ('Not sure' in skintype):
        df_high_rank = df[df.Rank >= 4]
        df_high_rank.reset_index(drop=True, inplace=True)
        matches = []
        indexes = []
        for i in df_high_rank.Ingredients:
            matches.append(td.sorensen.normalized_similarity(ingredients, i))
        for i, value in enumerate(matches):
            if value == max(matches):
                indexes.append(i)

        if max(matches) * 100 >= 60:
            skintypes_test = {}
            for i in indexes:
                skins = []
                the_best_one_test = df_high_rank[df_high_rank.index == i]
                if the_best_one_test.Combination[i] == 1:
                    skins.append('Combination')
                if the_best_one_test.Dry[i] == 1:
                    skins.append('Dry')
                if the_best_one_test.Normal[i] == 1:
                    skins.append('Normal')
                if the_best_one_test.Oily[i] == 1:
                    skins.append('Oily')
                if the_best_one_test.Sensitive[i] == 1:
                    skins.append('Sensitive')
                skintypes_test[i] = skins

            more_skins = []
            for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
                if len(v) >= 4:
                    more_skins.append(i)

            final = df_high_rank.iloc[more_skins]
            final = final[final.columns[~(final.columns == 'Ingredients')]]
            final.reset_index(drop=True, inplace=True)
            final.sort_values('Rank', ascending=False, inplace=True)
            final = final.iloc[:,1:]
            output_text = ("With the given ingredients, we found the following products. This table should help you decide whether you can use the cosmetics or not.")
            return final.to_dict('records'), [{"name": i, "id": i} for i in final.columns], output_text
        else:
            output_text= 'Sorry, we are not familiar with such a combination of cosmetics.'
            return {}, [], output_text


#### This part of code is not working as expected #####

    # elif 'Not sure' not in label and 'Not sure' in skintype:
    #     df_label = df.loc[df.Label.apply(lambda x: x in label)]
    #     matches = []
    #     indexes = []
    #     for i in df_label.Ingredients:
    #         matches.append(td.sorensen.normalized_similarity(ingredients, i))
    #     for i, value in enumerate(matches):
    #         if value == np.max(matches):
    #             indexes.append(i)
    #
    #     if max(matches) * 100 >= 60:
    #         skintypes_test = {}
    #         for i in indexes:
    #             skins = []
    #             the_best_one_test = df_label[df_label.index == i]
    #             if the_best_one_test.Combination[i] == 1:
    #                 skins.append('Combination')
    #             if the_best_one_test.Dry[i] == 1:
    #                 skins.append('Dry')
    #             if the_best_one_test.Normal[i] == 1:
    #                 skins.append('Normal')
    #             if the_best_one_test.Oily[i] == 1:
    #                 skins.append('Oily')
    #             if the_best_one_test.Sensitive[i] == 1:
    #                 skins.append('Sensitive')
    #             skintypes_test[i] = skins
    #
    #         more_skins = []
    #         for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
    #             if len(v) == len(max(skintypes_test.values())):
    #                 more_skins.append(i)
    #
    #         final = df_label.iloc[more_skins]
    #         the_best_cosmetics = final[final.Rank == final.Rank.max()]
    #
    #         final_skins = []
    #         for i in range(len(final)):
    #             df_ = final.iloc[i]
    #             if df_.Combination == 1:
    #                 final_skins.append('Combination')
    #             if df_.Dry == 1:
    #                 final_skins.append('Dry')
    #             if df_.Normal == 1:
    #                 final_skins.append('Normal')
    #             if df_.Oily == 1:
    #                 final_skins.append('Oily')
    #             if df_.Sensitive == 1:
    #                 final_skins.append('Sensitive')
    #
    #         final_skins = list(set(final_skins))
    #         final_skins = ', '.join([i for i in final_skins])
    #         output_text = 'The given cosmetics matches with the following skin types: ' + str(final_skins)
    #         return {}, [], output_text
    #
    #     else:
    #         output_text = 'Sorry, we are not familiar with such a combination of cosmetics.'
    #         return {}, [], output_text

    # elif ('Not sure' not in label) and ('Not sure' not in skintype):
    #     df_label = df[df.Label.apply(lambda x: x in label)]
    #     matches = []
    #     indexes = []
    #     for i in df_label.Ingredients:
    #         matches.append(td.sorensen.normalized_similarity(ingredients, i))
    #     for i, value in enumerate(matches):
    #         if value == np.max(matches):
    #             indexes.append(i)
    #
    #     if max(matches) * 100 >= 60:
    #         skintypes_test = {}
    #         for i in indexes:
    #             skins = []
    #             the_best_one_test = df_label[df_label.index == i]
    #             if the_best_one_test.Combination[i] == 1:
    #                 skins.append('Combination')
    #             if the_best_one_test.Dry[i] == 1:
    #                 skins.append('Dry')
    #             if the_best_one_test.Normal[i] == 1:
    #                 skins.append('Normal')
    #             if the_best_one_test.Oily[i] == 1:
    #                 skins.append('Oily')
    #             if the_best_one_test.Sensitive[i] == 1:
    #                 skins.append('Sensitive')
    #             skintypes_test[i] = skins
    #
    #         matched = []
    #         for i, v in zip(skintypes_test.keys(), skintypes_test.values()):
    #             if set(skintype).issubset(set(skintypes_test.values())):
    #                 matched.append(i)
    #
    #             if len(matches) != 0:
    #                 output_text = 'This cosmetics fits your skin type with ' + str(int(max(matches) * 100)) + '%'
    #                 return {}, [], [output_text]
    #             else:
    #                 output_text = 'This cosmetics does not match your skin type, please use our first page to get a recommendation from us'
    #                 return {}, [], [output_text]
    #     else:
    #         output_text = 'Sorry, we are not familiar with such a combination of cosmetics.'
    #         return {}, [], [output_text]

    elif ('Not sure' in label) and ('Not sure' not in skintype):
        matches = []
        for i in df.Ingredients:
            matches.append(td.sorensen.normalized_similarity(ingredients, i))
        for i, value in enumerate(matches):
            if value == np.max(matches):
                max_index = i

        if max(matches) * 100 >= 60:
            the_best_cosmetics = df[df.index == max_index]
            skintypes = []
            if the_best_cosmetics.Combination[max_index] == 1:
                skintypes.append('Combination')
            if the_best_cosmetics.Dry[max_index] == 1:
                skintypes.append('Dry')
            if the_best_cosmetics.Normal[max_index] == 1:
                skintypes.append('Normal')
            if the_best_cosmetics.Oily[max_index] == 1:
                skintypes.append('Oily')
            if the_best_cosmetics.Sensitive[max_index] == 1:
                skintypes.append('Sensitive')

            if set(skintype).issubset(set(skintypes)):
                output_text = 'These ingredients are okay for your skin type! You can use the cosmetics with the given ingredients. The cosmetics matches with your skin with approximately '+ str(int(max(matches) * 100)) + '%'
                return {}, [], output_text
        else:
            output_text = 'Sorry, we are not familiar with such a combination of cosmetics.'
            return {}, [], output_text
