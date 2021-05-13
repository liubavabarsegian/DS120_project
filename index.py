#the index page is the file that work whenn user goes into your page, it is the landing page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Connect to main app.py file
from app import app #importing app object
from app import server

# Connect to your app pages
from apps import choose_cosmetics,cosmetics_suitability #add third page if there is

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), #allows the app to read  the url, given the path, by default the pathname is empty
    html.Div([
        dcc.Link('Choose your Cosmetics|', href='/apps/choose_cosmetics'),
        dcc.Link('Cosmetics Suitability', href='/apps/cosmetics_suitability'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/choose_cosmetics':
        return choose_cosmetics.layout
    if pathname == '/apps/cosmetics_suitability':
        return cosmetics_suitability.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)