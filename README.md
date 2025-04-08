##  Como Usar

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

### 2. Instalar as Dependências

Crie um ambiente virtual e instale os pacotes necessários:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

(Adicione um `requirements.txt` com: `dash`, `sqlalchemy`, `pandas`, `plotly`, `numpy`.)

### 3. Criar as Tabelas no Banco de Dados

```bash
python init_db.py
```

### 4. Popular os Dados

O "analise_economica.zip" já tem populado as seguintes tabelas: `ativos`, `bovespa_data`, `indice_historico` e `indices`. Basta apenas descompactar.

### 5. Gerar Volatilidade Histórica

Para visualizar o gráfico de volatilidade, você precisa executar:

```bash
python volatilidade_data.py
```

Isso calculará a volatilidade histórica anualizada em janelas de 22 pregões e preencherá a tabela `volatilidade_historica`.

### 6. Rodar o Dashboard

```bash
python app_finance.py
```

Acesse o dashboard no navegador em: [http://127.0.0.1:8050](http://127.0.0.1:8050)

##  Funcionalidades do Dashboard

- Seletor de ativo e índice benchmark.
- Opções de período (YTD, 12M, 24M, customizado).
- Gráfico candlestick do ativo com benchmark ajustado.
- Gráfico de volatilidade histórica (após rodar `volatilidade_data.py`).


##  Observações

- A análise de volatilidade é baseada em janelas móveis de 22 pregões.
- O benchmark é ajustado proporcionalmente ao preço inicial do ativo selecionado.
- A aplicação pode ser facilmente estendida para novos indicadores.
