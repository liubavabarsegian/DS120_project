#the index page is the file that work whenn user goes into your page, it is the landing page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Connect to main app.py file
from app import app #importing app object
from app import server

# Connect to your app pages
from apps import choose_cosmetics,cosmetics_suitability, Intro_page #add third page if there is

app.layout = html.Div([

    html.Img(#logo
        src=app.get_asset_url('logo.png'),
        style = {
            'margin-top':'30px',
            'margin-left':'25px',
        }
    ),
    dcc.Location(id='url', refresh=False), #allows the app to read  the url, given the path, by default the pathname is empty
    html.Div([#these are three menu options, that allow user to select the page of the app
        
        dcc.Link('Home Page', href='/apps/Intro_page', 
        style = {
            'margin-left':'50px', 
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px',
            
            'font-family':'cursive'
        }),
        dcc.Link('Choose your Cosmetics', href='/apps/choose_cosmetics',
        style = {
            'margin-left':'50px',
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px',
            'font-family':'cursive'
        }),
        dcc.Link('Cosmetics Suitability', href='/apps/cosmetics_suitability', 
        style = {
            'margin-left':'50px',
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px',
            'font-family':'cursive'
        }),
        
    ], className="row", 
    style = {
        'text-align':'center',
        'margin-top':'-70px',
        'margin-bottom':'25px'
        
    }),
    html.Div(id='page-content', children=[]),

],
 style = {
    'background':'landever',
    'marginBottom':'0px',
    'margin-bottom':'0px',
    'margin':'-10px',
    'background-color':'lavender',
    
 },
)



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/choose_cosmetics':
        return choose_cosmetics.layout
    if pathname == '/apps/cosmetics_suitability':
        return cosmetics_suitability.layout
    else:
        return Intro_page.layout        


if __name__ == '__main__':
    app.run_server(debug=False)