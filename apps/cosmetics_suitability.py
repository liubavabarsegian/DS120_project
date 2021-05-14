import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app
#import app


#app = dash.Dash(__name__, suppress_callback_exceptions=True,
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}]
                
#                 )
#server = app.server



#app.config['suppress_callback_exceptions']=True



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
            #'transform':'scale(1.5)'
                }
            ),
        html.H1('How does it work?', 
        style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
        }),
        html.H2('First, upload a photo accourding to the instructions below', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
        }), 
        html.H2('Second, our app converts the image to text', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
        }),
        html.H2('After it, little people inside the machine are rushing to find out whether the product is suitable for you:)', 
            style = {
            'margin-left':'25px',
            'margin-right':'25px',
            'color':'#1A3E5C', 
        }),
        html.H1('Here are some instructions of the photo uploading', 
            style={
                'text-align':'center',
                'color':'#1A3E5C', 
            }),
        html.Img(src='photos/image1.jpg',
                style={
                    'text-align':'center',
                    'height':'200px',
                    'width':'200px',
                    'display': 'inline-block',
                    'margin-left':'250px',
                    'margin-right':'50px',
                }
        ),
       html.Img(src='photos/image2.jpg',
                style={
                    'text-align':'center',
                    'height':'200px',
                    'width':'200px',
                    'display': 'inline-block',
                    'margin-left':'50px',
                    'margin-right':'50px',
                }

       ),
       html.Img(src='photos/image3.jpg',
                style={
                    'text-align':'center',
                    'height':'200px',
                    'width':'200px',
                    'display': 'inline-block',
                    'margin-left':'50px',
                    'margin-right':'50px',
                }

       ),
       html.Img(src='photos/image4.jpg',
                style={
                    'text-align':'center',
                    'height':'200px',
                    'width':'200px',
                    'display': 'inline-block',
                    'margin-left':'25px',
                    'margin-right':'25px',
                },

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
                #"background": "blue",
                #"background": "blue",
                'color':'#1A3E5C', 
                "filter": "progid:DXImageTransform.Microsoft.gradient(startColorstr='#46fcb1',endColorstr='#3ffb6e',GradientType=1)"
            },

            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
        html.H2("Please specify the skincare product you want\n", 
        style={
            'color':'#1A3E5C', 
            'margin':'15px',
            'margin-left':'25px',
            'margin-right':'25px',
            #'margin-left':'center'
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
            value='Moisturizer', #the default value set
            multi=True
        ),
    html.H2("Please specify your skin type\n", 
            style= {
                'color':'#1A3E5C',
                'margin':'15px',
                'margin-left':'25px',
                'margin-right':'25px',
            }),
    html.H2("Here is a picture that can help you determine the skin type. If anyway you cannot do it, please select 'Not sure' option\n", 
        style= {
                'color':'#1A3E5C', 
                'margin':'15px',
                'margin-left':'25px',
                'margin-right':'25px',
            }),
    html.Img(
        src='https://3.bp.blogspot.com/-efc9Jwzy_xg/WxW09_1PB3I/AAAAAAAAAWk/7QwYJ1T03CYVfLr2NHmACZ33dX3Uuqk1gCLcBGAs/s640/IMG_8215.JPG',
        style={
            #'padding':'50px',
            #'borderRadius':'10px',
            'border-style':'solid',
            'border-color':'#1A3E5C',
            'borderRadius':'50x',
            'text-align':'center',
            'display':'block',
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
                #'display':'inline-block',
                'margin-top':'25px',
                'margin-bottom':'25px',
                'borderRadius':'25px',
                'font-size':'20px'
            },
                value='Combination',
                multi=True
            ),
        html.H1('Thank you!', 
        style = {
            'margin-top':'100px',
            'margin-left':'25px',
            'margin-right':'25px',
        }),
        
],
style = {
        'backgroundColor':'lavender',
        'marginBottom':'0px',
        'margin-bottom':'0px',
        'background':'lavender',

        },
)


def parse_contents(contents, filename):
    return html.Div([
        html.H3(filename),
        print(contents),
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),


    ])




def save_file(contents):
    """Decode and store a file uploaded with Plotly Dash."""

    data = contents.encode("utf8").split(b";base64,")[1]
    with open('some_image.png', "wb") as fp:
        fp.write(base64.decodebytes(data))


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

        save_file(contents)
        



if __name__ == '__main__':
    app.run_server(debug=True)



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
