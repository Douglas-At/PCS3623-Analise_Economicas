from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Ativo(Base):
    __tablename__ = 'ativos'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    ibovespa = Column(Boolean, default=False)  
    historico = relationship("BovespaData", back_populates="ativo")  

class BovespaData(Base):
    __tablename__ = 'bovespa_data'

    id = Column(Integer, primary_key=True, autoincrement=True)  

    tipo_registro = Column(Integer)
    data_pregao = Column(DateTime)
    cod_bdi = Column(Float)
    ativo_id = Column(Integer, ForeignKey('ativos.id'))
    tipo_mercado = Column(Integer)
    nome_empresa = Column(String)
    especificacao_papel = Column(String)
    prazo_dias_merc_termo = Column(Float)
    moeda_referencia = Column(String)
    preco_abertura = Column(Float)
    preco_maximo = Column(Float)
    preco_minimo = Column(Float)
    preco_medio = Column(Float)
    preco_ultimo_negocio = Column(Float)
    preco_melhor_oferta_compra = Column(Float)
    preco_melhor_oferta_venda = Column(Float)
    numero_negocios = Column(Float)
    quantidade_papeis_negociados = Column(Float)
    volume_total_negociado = Column(Float)
    preco_exercicio = Column(Float)
    indicador_correcao_precos = Column(Float)
    data_vencimento = Column(Float)
    fator_cotacao = Column(Float)
    preco_exercicio_pontos = Column(Float)
    codigo_isin = Column(String)
    num_distribuicao_papel = Column(Float)
    
    ativo = relationship("Ativo", back_populates="historico")

class Indice(Base):
    __tablename__ = 'indices'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)  
    historico = relationship("IndiceHistorico", back_populates="indice")


class IndiceHistorico(Base):
    __tablename__ = 'indice_historico'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    valor = Column(Float, nullable=False)

    indice_id = Column(Integer, ForeignKey('indices.id'), nullable=False)
    indice = relationship("Indice", back_populates="historico")

