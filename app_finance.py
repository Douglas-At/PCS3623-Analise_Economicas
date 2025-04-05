import pandas as pd
from dash import Dash, dcc, html, Input, Output
from datetime import datetime, timedelta
from database import engine
from utils import PlotsHist

ph = PlotsHist()
app = Dash(__name__)

# Lista de ativos
lista_ticker = pd.read_sql("SELECT ticker FROM ativos a", engine).ticker.to_list()

lista_benchmark = pd.read_sql("SELECT nome FROM indices i", engine).nome.to_list()


app.layout = html.Div([
    html.H2("Gráfico Histórico"),
    
    html.Div([
        dcc.Dropdown(
            id='dropdown-ativo',
            options=[{'label': ativo, 'value': ativo} for ativo in lista_ticker],
            value="PETR4",
            style={'width': '200px'}
        ),

        dcc.Dropdown(
            id='dropdown-benchmark',
            options=[{'label': nome, 'value': nome} for nome in lista_benchmark],
            placeholder="ibov",
            style={'width': '220px'}
        ),
        dcc.RadioItems(
            id='periodo-opcao',
            options=[
                {'label': 'YTD', 'value': 'YTD'},
                {'label': '12 meses', 'value': '12M'},
                {'label': '24 meses', 'value': '24M'},
                {'label': 'Custom', 'value': 'CUSTOM'}
            ],
            value='YTD',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
            style={'margin-left': '30px'}
        ),

        html.Div([
            dcc.DatePickerSingle(
                id='data-inicial',
                placeholder='Data Inicial',
                style={'margin-right': '10px'}
            ),
            dcc.DatePickerSingle(
                id='data-final',
                placeholder='Data Final'
            ),
        ], id='date-picker-container', style={'display': 'none', 'margin-top': '10px'})
    ], style={'display': 'flex', 'align-items': 'center', 'gap': '30px'}),

    dcc.Graph(id='grafico-candlestick')
])

@app.callback(
    Output('date-picker-container', 'style'),
    Input('periodo-opcao', 'value')
)
def mostrar_ocultar_datepicker(periodo_opcao):
    if periodo_opcao == 'CUSTOM':
        return {'display': 'flex', 'margin-top': '10px', 'gap': '10px'}
    return {'display': 'none'}

@app.callback(
    Output('grafico-candlestick', 'figure'),
    Input('dropdown-ativo', 'value'),
    Input('dropdown-benchmark', 'value'), 
    Input('periodo-opcao', 'value'),
    Input('data-inicial', 'date'),
    Input('data-final', 'date')
)
def atualizar_grafico(ativo_selecionado, benchmark, periodo_opcao, data_inicial, data_final):
    hoje = datetime.today().date()
    
    if periodo_opcao == 'YTD':
        data_ini = datetime(hoje.year, 1, 1).date()
        data_fim = hoje
    elif periodo_opcao == '12M':
        data_ini = hoje - timedelta(days=365)
        data_fim = hoje
    elif periodo_opcao == '24M':
        data_ini = hoje - timedelta(days=730)
        data_fim = hoje
    elif periodo_opcao == 'CUSTOM':
        if not data_inicial or not data_final:
            return ph.candlestick(pd.DataFrame())
        data_ini = pd.to_datetime(data_inicial).date()
        data_fim = pd.to_datetime(data_final).date()

    query = f"""
        SELECT 
            bd.data_pregao AS date_aux, a.ticker AS cod_negociacao, 
            bd.preco_abertura, bd.preco_maximo, bd.preco_minimo, 
            bd.preco_medio, bd.preco_ultimo_negocio 
        FROM bovespa_data bd
        JOIN ativos a ON a.id = bd.ativo_id 
        WHERE a.ticker = '{ativo_selecionado}'
        AND bd.data_pregao BETWEEN '{data_ini}' AND '{data_fim}'
        ORDER BY bd.data_pregao ASC
    """
    df_ativo = pd.read_sql(query, engine)

    df_benchmark = pd.DataFrame()
    if benchmark:
        data_fim = df_ativo["date_aux"].iloc[-1]
        query = f"""
            SELECT ih.data, ih.valor, i.nome
            FROM indice_historico ih
            JOIN indices i ON i.id = ih.indice_id
            WHERE i.nome = '{benchmark}'
            AND ih.data BETWEEN '{data_ini}' AND '{data_fim}'
            ORDER BY ih.data ASC
        """
        df_benchmark = pd.read_sql(query, engine)
    
    
    fig = ph.candlestick(df_ativo, benchmark=df_benchmark)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
