import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pandas as pd
import pathlib
from app import app


layout = html.Div([
    html.H1('Welcome to Snikdetectorisator!', 
        style = {
            'color':'#1A3E5C',
            'background-color':'#7F7DA9',
            'margin-top':'200px',
            'text-align':'center',
            'borderRadius':'50px',
            'height':'50px'
         }
         ),
    html.H2("This website will help you to choose the most suitable for you cosmetics product", 
    style = {
        'margin-left':'25px',
        'color':'#1A3E5C'
    }
    ),
    html.H2("If you want some products to be suggested, click on 'Choose your Cosmetics'. If you have the product and want to test its suitability, go to 'Cosmetics Suitability'.",
    style = {
        'margin-left':'25px',
        'color':'#1A3E5C'
    }),
    html.H4('created by: Aram Adamyan, Liuba Barsegian, Tamara Sedrakyan', 
    style = {
        'margin-top':'260px',
        'margin-left':'25px',
        'color':'#1A3E5C',
    }),
], 
style = {
    'backgroundColor':'lavender',
        'marginBottom':'0px',
        'margin-bottom':'0px',
    
}
)
