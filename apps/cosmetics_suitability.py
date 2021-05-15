#!pip install pytesseract
#!pip install opencv-python
#!pip install pillow
import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app
#import app
import base64
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
path = os.getcwd()
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
        html.H2('First, you upload a photo accourding to the instructions below. Please, make sure that the the photo is not blurry, and the text is readable. Also, do not forget to crop the photo so only ingredients are visible.', 
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
        style = {
            'text-align':'center',
        }),
        html.H5(id = 'output-ingredients_ls'),
        html.H2("Please specify the skincare product you want\n", 
        style={
            'color':'#1A3E5C', 
            'margin':'25px',
            'margin-left':'25px',
            'margin-right':'25px',
            'font-family':'cursive'
        }),
    dcc.Dropdown( #dropdown for product type
            id = 'product_dd',
            options=[
                {'label': 'Moisturizer', 'value': 'Moisturizer'},
                {'label': 'Cleanser', 'value': 'Cleanser'},
                {'label': 'Treatment', 'value': 'Treatment'},
                {'label': 'Eye cream', 'value': 'Eye cream'},
                {'label': 'Sun protect', 'value': 'Sun protect'},
                {'label': 'Face Mask', 'value': 'Face Mask'},
                {'label': 'Not sure', 'value' : 'Not sure'}
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
            #value='Moisturizer', #the default value set
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
                    {'label' : 'Normal', 'value' : 'Noraml'},
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
            
        html.H1('Thank you for using our app!', 
        style = {
            'margin-top':'250px',
            'margin-left':'25px',
            'margin-right':'25px',
            'font-family':'cursive'
        }),
        html.Img(
        src=app.get_asset_url('doggy.jpg'),
        style = {
            'margin-left':'25px',
            'height':'300px',
            'color':'#1A3E5C', 
        }
    )
        
],
style = {
        'backgroundColor':'lavender',
        'marginBottom':'0px',
        'margin-bottom':'0px',
        'background':'lavender',
        'margin-left':'10%',
        'margin-right':'10%',
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

#defining OCR function
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
    return t[13:]


@app.callback(Output('output-ingredients_ls', 'children'),
              Input('upload-image', 'contents'))
def ocr_output(contents):  # function for ocr output
    if contents is not None:
        save_file(contents)     #saves the imported image in the apps directory, whenever an image has been uploaded
        filename = path + "/some_image.png"
        ingredients_ls = ocr(filename)  # reads the text from the image
        print(ingredients_ls)
        return ingredients_ls


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(contents, names): #function for showing the uploaded picture
    if contents is not None:
         return parse_contents(contents, names)
        






#
# #another page, that upload a picture and shows for which skin type the cosmetics is suitable
# import dash_core_components as dcc
# import dash_html_components as html
#
# layout = html.Div([
#     html.H1("Check whether the cosmetics suits you"),
#     #the upload button
#     html.Div([
#         dcc.Upload(
#             id='upload-image',
#             children=html.Div(
#                 ['Upload picture'],
#                 style={
#                     "margin-left": "auto",
#                     "margin-right": "auto",
#                     'text-align': 'center',
#                     'display': 'inline-block'
#                 }
#             ),
#             style={
#                 'width': '20%',
#                 'height': '40px',
#                 'lineHeight': '60p',
#                 'borderStyle': 'hidden',
#                 'borderRadius': '15px',
#                 'text-align': 'center',
#                 "boxShadow": "0px 15px 30px -10px grey",
#                 "margin-left": "auto",
#                 "margin-right": "auto",
#                 "transform": "scale(1.5)",
#
#                 "background": "c",
#                 "background": "-moz-radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
#                 "background": "-webkit-radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
#                 "background": "radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
#                 "filter": "progid:DXImageTransform.Microsoft.gradient(startColorstr='#46fcb1',endColorstr='#3ffb6e',GradientType=1)"
#             },
#             multiple=False
#         )
#     ])
#
# ])
#
