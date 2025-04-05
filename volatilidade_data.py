
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
from models import Base, Ativo, BovespaData,VolatilidadeHistorica 


from database import engine
Session = sessionmaker(bind=engine)
session = Session()


# Loop por ativos
ativos = session.query(Ativo).all()
for ativo in ativos:
    historico = (
        session.query(BovespaData)
        .filter_by(ativo_id=ativo.id)
        .filter(BovespaData.preco_ultimo_negocio != None)
        .order_by(BovespaData.data_pregao)
        .all()
    )

    if len(historico) < 22:
        continue

    df = pd.DataFrame([
        {
            'data': h.data_pregao,
            'preco': h.preco_ultimo_negocio
        }
        for h in historico if h.preco_ultimo_negocio and h.preco_ultimo_negocio > 0
    ])

    if df.empty or len(df) < 22:
        continue

    df = df.sort_values("data").reset_index(drop=True)
    df['retorno_pct'] = df['preco'].pct_change()

    for i in range(len(df) - 22):
        # 22 APROX 1 mes 
        janela = df.iloc[i:i+22].dropna(subset=["retorno_pct"])
        if len(janela) >= 10:
            volatilidade_pct = janela['retorno_pct'].std() * np.sqrt(252)
            #analizar a volatilidade 
            data_inicio = janela['data'].iloc[0]
            data_fim = janela['data'].iloc[-1]

            registro = VolatilidadeHistorica(
                ativo_id=ativo.id,
                data_inicio=data_inicio,
                data_fim=data_fim,
                volatilidade=volatilidade_pct
            )
            session.add(registro)

session.commit()
print("Volatilidade histórica registrada com base em janelas de 22 pregões.")