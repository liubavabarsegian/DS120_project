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

    
    dcc.Location(id='url', refresh=False), #allows the app to read  the url, given the path, by default the pathname is empty
    html.Div([
        dcc.Link('Home Page', href='/apps/Intro_page', 
        style = {
            'margin-left':'50px', 
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px',
            #'text-align':'center',
        }),
        dcc.Link('Choose your Cosmetics', href='/apps/choose_cosmetics',
        style = {
            'margin-left':'50px',
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px'
        }),
        dcc.Link('Cosmetics Suitability', href='/apps/cosmetics_suitability', 
        style = {
            'margin-left':'30px',
            'background-color':'lavender',
            'borderRadius':'25px',
            'font-size':'30px'
        }),
        
    ], className="row"),
    html.Div(id='page-content', children=[]),

],
 style = {
    'background':'landever',
    'marginBottom':'0px',
    'margin-bottom':'0px',
    'margin':'-10px',
    'background-color':'lavender',
    #'text-align':'center'
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