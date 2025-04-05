import plotly.graph_objs as go

class PlotsHist:

    def candlestick(self,df):
        ativo_selecionado = df.cod_negociacao.unique()[0]
        fig = go.Figure(data=[
            go.Candlestick(
                x=df['date_aux'],
                open=df['preco_abertura'],
                high=df['preco_maximo'],
                low=df['preco_minimo'],
                close=df['preco_ultimo_negocio'],
                name=ativo_selecionado
            )
        ])

        fig.update_layout(
            title=f'Candlestick - {ativo_selecionado}',
            xaxis_title='Data',
            yaxis_title='Preço',
            xaxis_rangeslider_visible=False
        )
        return fig

