import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

# Charger les données depuis Excel
stock_df = pd.read_excel('data.xlsx', sheet_name='Stock')
ventes_df = pd.read_excel('data.xlsx', sheet_name='Ventes')

app = dash.Dash(__name__)

app.layout = html.Div([
    # Titre et filtres
    html.Div([
        html.H1("Dashboard de Gestion de Stock", style={'flex': '90%'}),
        html.Div([
            dcc.RadioItems(
                id='filtre-temps',
                options=[
                    {'label': 'Jour', 'value': 'J'},
                    {'label': 'Mois', 'value': 'M'},
                    {'label': 'Année', 'value': 'A'}
                ],
                value='J',
                inline=True,
                style={'margin': 'auto'}
            )
        ], style={'flex': '10%'})
    ], style={'display': 'flex', 'margin-bottom': '20px'}),
    
    # Statistiques principales
    html.Div([
        html.Div([
            html.H3("Stock Total"),
            html.P(id='total-stock')
        ], className='stats-box'),
        
        html.Div([
            html.H3("Ventes Total"),
            html.P(id='total-ventes')
        ], className='stats-box'),
        
        html.Div([
            html.H3("Produits en Rupture"),
            html.P(id='rupture-stock')
        ], className='stats-box')
    ], className='row'),
    
    # Graphiques
    html.Div([
        html.Div([
            dcc.Graph(id='stock-produits'),
            dcc.Graph(id='ventes-categories')
        ], className='six columns'),
        
        html.Div([
            dcc.Graph(id='ventes-produits'),
            dcc.Graph(id='stock-categories')
        ], className='six columns')
    ], className='row'),
    
    # Tableaux
    html.Div([
        html.Div([
            html.H4("Dernières Ventes"),
            html.Table(id='dernieres-ventes')
        ], className='six columns'),
        
        html.Div([
            html.H4("Meilleures Ventes"),
            html.Table(id='meilleures-ventes')
        ], className='six columns')
    ], className='row')
])

@app.callback(
    [Output('total-stock', 'children'),
     Output('total-ventes', 'children'),
     Output('rupture-stock', 'children'),
     Output('stock-produits', 'figure'),
     Output('stock-categories', 'figure'),
     Output('ventes-produits', 'figure'),
     Output('ventes-categories', 'figure'),
     Output('dernieres-ventes', 'children'),
     Output('meilleures-ventes', 'children')],
    [Input('filtre-temps', 'value')]
)
def update_dashboard(filtre):
    # Filtrer les données selon la période sélectionnée
    today = datetime.today()
    
    if filtre == 'J':
        date_filter = today.strftime('%Y-%m-%d')
    elif filtre == 'M':
        date_filter = today.strftime('%Y-%m')
    else:
        date_filter = today.strftime('%Y')
    
    filtered_ventes = ventes_df[ventes_df['Date'].astype(str).str.contains(date_filter)]
    
    # Calcul des statistiques
    total_stock = stock_df['Quantité'].sum()
    total_ventes = filtered_ventes['Quantité'].sum()
    rupture_stock = len(stock_df[stock_df['Quantité'] == 0])
    
    # Graphiques Stock
    fig_stock_produits = px.bar(stock_df, x='Produit', y='Quantité', title='Stock par Produit')
    fig_stock_categories = px.pie(stock_df, names='Catégorie', values='Quantité', title='Stock par Catégorie')
    
    # Graphiques Ventes
    ventes_par_produit = filtered_ventes.groupby('Produit')['Quantité'].sum().reset_index()
    ventes_par_categorie = filtered_ventes.groupby('Catégorie')['Quantité'].sum().reset_index()
    
    fig_ventes_produits = px.bar(ventes_par_produit, x='Produit', y='Quantité', title='Ventes par Produit')
    fig_ventes_categories = px.pie(ventes_par_categorie, names='Catégorie', values='Quantité', title='Ventes par Catégorie')
    
    # Tables
    dernieres_ventes = filtered_ventes.sort_values('Date', ascending=False).head(10)
    meilleures_ventes = filtered_ventes.groupby('Produit')['Quantité'].sum().nlargest(10).reset_index()
    
    def generate_table(df):
        return html.Table([
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(len(df))
            ])
        ])
    
    return (
        total_stock,
        total_ventes,
        rupture_stock,
        fig_stock_produits,
        fig_stock_categories,
        fig_ventes_produits,
        fig_ventes_categories,
        generate_table(dernieres_ventes),
        generate_table(meilleures_ventes)
    )

if __name__ == '__main__':
    app.run_server(debug=True)