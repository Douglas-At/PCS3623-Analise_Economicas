import plotly.graph_objs as go

class PlotsHist:

    def candlestick(self,df, benchmark):
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
        if not benchmark.empty:
            #conferir o df
            benchmark['valor'] = benchmark['valor'].add(1).cumprod()*df["preco_ultimo_negocio"].iloc[0]
            fig.add_scatter(
                x=benchmark['data'],
                y=benchmark['valor'],
                mode='lines',
                name=benchmark.nome.unique()[0],
                line=dict(color='black')

            )

        fig.update_layout(
            title=f'Candlestick - {ativo_selecionado}',
            xaxis_title='Data',
            yaxis_title='Preço',
            xaxis_rangeslider_visible=False
        )
        return fig
    
    def linha_volatilidade(self, df):
        if df.empty:
            return go.Figure()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['data_fim'], y=df['volatilidade'],  # ou o nome da coluna certa
            mode='lines',
            name='Volatilidade'
        ))
        fig.update_layout(title="Volatilidade Histórica Anualizada", xaxis_title="Data", yaxis_title="Volatilidade")
        return fig

