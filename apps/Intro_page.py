import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pandas as pd
import pathlib
from app import app


layout = html.Div([#this is the first page that the user sees when opens the app
    
    html.H1('Welcome to Skindetectorisator!', 
        style = {
            'color':'#1A3E5C',
            'background-color':'#7F7DA9',
            'margin-top':'150px',
            'text-align':'center',
            'borderRadius':'50px',
            
            'font-family':'Segoe Print'
         }
         ),
    html.H2("Hi! This website is created for helping you to choose the most suitable for you cosmetics product or to check whether it is suitable for your skin type.", 
    style = {
        'margin-left':'25px',
        'color':'#1A3E5C', 
        'font-family':'cursive',
    }
    ),
    html.H2("If you want some products to be suggested, click on 'Choose your Cosmetics'. If you have the product and want to test its suitability, go to 'Cosmetics Suitability'. For coming back and trying to remember the name of our app, click on 'Home Page'.",
    style = {
        'margin-left':'25px',
        'color':'#1A3E5C',
        'font-family':'cursive',
    }),
    html.H4('created by: Aram Adamyan, Liuba Barsegian, Tamara Sedrakyan', 
    style = {
        'margin-top':'180px',
        'margin-left':'25px',
        'color':'#1A3E5C',
        'margin-bottom':'0px',
        'font-family':'cursive',
    }),
], 
style = {
    'backgroundColor':'lavender',
        'marginBottom':'0px',
        'margin-bottom':'0px',
        'margin-left':'10%',
        'margin-right':'10%',
    
}
)
