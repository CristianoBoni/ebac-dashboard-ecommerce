from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

DATA = Path(__file__).resolve().parent / 'ecommerce_estatistica.csv'
df = pd.read_csv(DATA)
app = Dash(__name__)
server = app.server
GENRES = sorted(df['Gênero'].dropna().unique())
app.layout = html.Div([
    html.H1('Produtos de e-commerce'),
    html.P('Preços, avaliações e descontos da amostra fornecida pela EBAC.'),
    html.Label('Gênero do produto'),
    dcc.Dropdown(id='genero', options=[{'label':'Todos','value':'Todos'}]+[{'label':g,'value':g} for g in GENRES], value='Todos', clearable=False),
    html.P(id='resumo'),
    html.Div([dcc.Graph(id=f'g{i}') for i in range(7)], style={'display':'grid','gridTemplateColumns':'repeat(auto-fit,minmax(420px,1fr))','gap':'12px'}),
    html.P('Cada registro representa um produto. Quantidades vendidas são faixas anunciadas; esta base não mede faturamento realizado. Correlação não demonstra causalidade.')
], style={'maxWidth':'1300px','margin':'auto','padding':'24px','fontFamily':'Arial, sans-serif','color':'#152238','background':'#f5f7fa'})

def figures(d):
    hist=px.histogram(d,x='Preço',nbins=25,title='Distribuição de preços',labels={'Preço':'Preço (R$)'})
    hist.update_yaxes(title='Quantidade de produtos')
    scatter=px.scatter(d,x='Preço',y='Nota',title='Preço e nota dos produtos',labels={'Preço':'Preço (R$)','Nota':'Nota média'})
    cols=['Preço','Nota','N_Avaliações','Desconto']
    heat=px.imshow(d[cols].corr(),zmin=-1,zmax=1,color_continuous_scale='RdBu_r',text_auto='.2f',title='Correlação entre indicadores')
    counts=d['Marca'].fillna('Não informado').value_counts().head(10).rename_axis('Marca').reset_index(name='Produtos')
    bar=px.bar(counts,x='Produtos',y='Marca',orientation='h',title='Marcas com mais produtos')
    genres=d['Gênero'].fillna('Não informado').value_counts().rename_axis('Gênero').reset_index(name='Produtos')
    pie=px.pie(genres,names='Gênero',values='Produtos',title='Composição por gênero')
    values=d['Desconto'].dropna().to_numpy()
    density=go.Figure()
    if len(values)>1 and np.std(values)>0:
        grid=np.linspace(values.min(),values.max(),150)
        density.add_trace(go.Scatter(x=grid,y=gaussian_kde(values)(grid),fill='tozeroy',name='Densidade'))
    else: density.add_annotation(text='A amostra filtrada não tem variação suficiente',showarrow=False)
    density.update_layout(title='Densidade dos descontos',xaxis_title='Desconto (%)',yaxis_title='Densidade estimada')
    regression=px.scatter(d,x='Desconto',y='Preço',title='Associação entre desconto e preço',labels={'Desconto':'Desconto (%)','Preço':'Preço (R$)'})
    xy=d[['Desconto','Preço']].dropna()
    if len(xy)>1 and xy['Desconto'].nunique()>1:
        slope,intercept=np.polyfit(xy['Desconto'],xy['Preço'],1)
        line=np.array([xy['Desconto'].min(),xy['Desconto'].max()])
        regression.add_trace(go.Scatter(x=line,y=intercept+slope*line,mode='lines',name='Regressão linear'))
    for f in [hist,scatter,heat,bar,pie,density,regression]:f.update_layout(template='plotly_white',margin={'l':45,'r':20,'t':65,'b':50},font_family='Arial')
    return [hist,scatter,heat,bar,pie,density,regression]

@app.callback([Output('resumo','children')]+[Output(f'g{i}','figure') for i in range(7)],Input('genero','value'))
def update(genero):
    d=df if genero=='Todos' else df[df['Gênero']==genero]
    resumo=f"{len(d)} produtos | Preço mediano R$ {d['Preço'].median():.2f} | Nota média {d['Nota'].mean():.2f}"
    return [resumo]+figures(d)

if __name__=='__main__': app.run(host='127.0.0.1',port=8050,debug=False)
