import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
#from app import app
import app

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                
                )
server = app.server



app.config['suppress_callback_exceptions']=True


colors = {
    'background':'#111111',
    'text':'black'
}
app.layout = html.Div([
    html.H1(children = "Check whether the cosmetics suits you", 
    style = {
        'textAlign':'center',
        'colors': colors['text']
    }),

     dcc.Markdown(
         ```hello```
            id = 'python',
            style={
                'background-color':'blue'
            },),

        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '20%',
                'height': '40px',
                'lineHeight': '60p',
                'borderStyle': 'hidden',
                'borderRadius': '15px',
                'text-align': 'center',
                "boxShadow": "0px 15px 30px -10px grey",
                "margin-left": "auto",
                "margin-right": "auto",
                "transform": "scale(1.5)",

                "background": "c",
                #"background": "blue",
                #"background": "blue",
                'color':'darkslateblue',
                "background": "lightblue",
                "filter": "progid:DXImageTransform.Microsoft.gradient(startColorstr='#46fcb1',endColorstr='#3ffb6e',GradientType=1)"
            },

            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),


])


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
