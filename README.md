# Produtos de e-commerce

Aplicação Dash com os sete gráficos do módulo 22 e filtro por gênero. Inclui histograma, dispersão, mapa de correlações, barras, pizza, densidade e regressão linear.

## Executar

Com Python 3.11 ou superior, instale `pip install -r requirements.txt` e execute `python app.py`. Abra http://127.0.0.1:8050. Para hospedagem compatível com WSGI, use `gunicorn app:server`.

## Dados e interpretação

Fonte: material de apoio do módulo 22 da EBAC, `ecommerce_estatistica.csv`. Cada registro descreve um produto. As faixas de quantidade vendida não são tratadas como volume exato. As regressões representam associações exploratórias. O painel não calcula faturamento realizado.
