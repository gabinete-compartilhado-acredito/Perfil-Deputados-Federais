import streamlit as st 
import plotly.graph_objects as go 
import json 
from glob import glob
import pandas as pd
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from string import punctuation
import matplotlib.pyplot as pl
import GetOldTweets3 as got
from datetime import datetime, timedelta





# Como utilizar CSS no streamlit (duas opções):
#st.write("<style> body {background-color: powderblue;} h1 {color: red;} p {color: blue;} </style>", unsafe_allow_html=True) 
#st.write('<link rel="stylesheet" href="http://www.fma.if.usp.br/~hsxavier/test_style.css">', unsafe_allow_html=True)

imagem = '<img id="icone" src="https://www.movimentoacredito.org/wp-content/uploads/2018/08/acredito_fundobranco.png" style="float:middle" width=73%>'
st.write( imagem, unsafe_allow_html=True)

# Título do site
st.markdown(" # Perfil dos Deputados Federais")

# Abrindo o arquivo json

def openfile():
	diretorio = sorted(glob('perfil_deputados*.json'))
	arquivo = diretorio[-1]	

	with open(arquivo, 'r', encoding='utf8') as f:
		dados = json.load(f)

	# Alterando valores de None para 0
	colunas = ['alinhamento_rigoni', 'alinhamento_tabata', 'alinhamento_gov', 'alinhamento_partido']
	for i in range(len(dados)):
		for coluna in colunas:
			if dados[i][coluna] == None:
				dados[i][coluna] = 0 
	return dados


#chamada a função para obter os dados
dados = openfile()


####################### SELEÇÃO DE PARTIDO ###############################
partidos = []
for i in range(len(dados)):
	if dados[i]['sigla_partido'] not in partidos:
		partidos.append(dados[i]['sigla_partido'])
partidos.sort()

partidos_ = ['TODOS']
partidos_.extend(partidos)
partido = st.selectbox('Selecione o partido:', partidos_)

#################### SELEÇÃO DE UF ############################################

### Seleção por UF
estados = []

if partido == 'TODOS':
	for i in range(len(dados)):
		if dados[i]['uf'] not in estados:
			estados.append(dados[i]['uf'])
else:
	for i in range(len(dados)):
		if dados[i]['sigla_partido'] == partido:
			if dados[i]['uf'] not in estados:
				estados.append(dados[i]['uf'])
	
estados.sort()	# Ordenando a lista de estados 
uf = ['TODOS']	# Adicionando a opçao todos ás opções
uf.extend(estados) 	# unindo a lista de estados a opção TODOS

#Selectbox de UF
estado = st.selectbox('Selecione o estado: ', uf)

###################### SELEÇÃO DE DEPUTADO ##################################

# Criando lista com deputados após seleção de partido e estado
candidatos = []

# Condições para filtrar deputados baseado em partido e estado
if partido == 'TODOS' and estado == 'TODOS' :
	for i in range(len(dados)):
		candidatos.append(dados[i]['ultimoStatus_nome'])


elif partido == 'TODOS' and estado !=  'TODOS':
	for i in range(len(dados)):
		if dados[i]['uf'] == estado:
			candidatos.append(dados[i]['ultimoStatus_nome'])
	

elif partido !=  'TODOS' and estado == 'TODOS':
	for i in range(len(dados)):
		if dados[i]['sigla_partido'] == partido:
			candidatos.append(dados[i]['ultimoStatus_nome'])
	
else:
	for i in range(len(dados)):
		if dados[i]['sigla_partido'] == partido and  dados[i]['uf'] == estado:
			candidatos.append(dados[i]['ultimoStatus_nome'])
	
candidatos.sort()


# Selectbox para Parlamentar
deputado = st.selectbox('Selecione o parlamentar:', candidatos)


# capturando o index do deputado selecionado
dept = 0
for i in range(len(dados)):
	if dados[i]['ultimoStatus_nome'] == deputado:
		dept = i



################################# TABELA COM FOTO DO PARLAMENTAR ###################################### 

# Concatenando o link + id do parlamentar
src = "https://www.camara.leg.br/internet/deputado/bandep/" + dados[dept]["id_deputado"] +".jpg"
img_src = '<img src=' + src + '>' 

# Selecionando as bancadas que o deputado faz parte
bancadas = ' - '

if len(dados[dept]['array_bancadas']) > 0:
	bancadas = ', '.join(dados[dept]['array_bancadas'])

#Criando tabela com foto e informações do parlamentar
tabela_foto = """<table frame='void'>

<tr>
	<td><img src="%(foto)s" height=150px></td>
	<td> 
		<table frame='void'> 
			<tr>
				<td><b>%(deputado)s</b></td>                
			</tr>
			<tr>
				<td>%(partido)s-%(estado)s </td>
			</tr>
			<tr>
				<td><b> Bancadas: </b>%(bancadas)s</td>
			</tr>
		</table>
	</td>
	
</tr>

</table>
""" %{'foto':src, 'deputado':dados[dept]['ultimoStatus_nome'],
	  'partido':dados[dept]['sigla_partido'], 'estado':dados[dept]['uf'], 'bancadas': bancadas}

st.write(tabela_foto, unsafe_allow_html=True)



################################# DADOS LIDERANÇA ######################################################
cargo_lider=[]
sigla_bloco = []

for lideranca in dados[dept]['liderancas']:
	cargo_lider.append(lideranca['cargo'])
	sigla_bloco.append(lideranca['sigla_bloco'])    	

################################# DADOS DE ÓRGÃOS ######################################################
entidade=[]
cargo = []

for orgao in dados[dept]['orgaos']:
	entidade.append(orgao['sigla_orgao'])
	cargo.append(orgao['titulo'])

#################################### DADOS DE COMISSOES ##############################################
comissoes = []
titulo = []
for comissao in dados[dept]['comissoes']:
	comissoes.append(comissao['sigla_orgao'])
	titulo.append(comissao['titulo'])

###################### TABELA DE PRESIDENCIA DE COMISSOES E LIDERANÇAS#######################



st.markdown('### Lideranças')
if len(cargo_lider) == 0:
	st.write('Nenhuma liderança.')
else:
	df = pd.DataFrame({'Bloco': sigla_bloco, 'Cargo': cargo_lider}, index=range(1, len(cargo_lider) + 1))
	st.table(df)

st.markdown('### Cargos de direção')
if len(cargo) == 0:
	st.write('Nenhum cargo diretor em comissões.')
else:
	df = pd.DataFrame({'Comissão': entidade, 'Cargo': cargo}, index=range(1, len(cargo) + 1))
	st.table(df)

st.markdown('### Participação em Comissões')
if len(comissoes) == 0:
	st.write("Nenhuma Comissão")
else:
	df = pd.DataFrame({'Comissão':comissoes, 'Título': titulo}, index=range(1, len(comissoes) + 1))
	st.table(df)



################################### DASHBOARD DE ALINHAMENTOS ##############################################
st.write('            ')
st.markdown('### Alinhamentos')


                     ################ ALINH. COM RIGONI ##############
fig1 = go.Figure()

fig1.add_trace(go.Indicator(
	mode = "gauge+number",
	number ={'suffix':'%'},
	value = float(dados[dept]['alinhamento_rigoni']) * 100 ,
	title = {'text': "Rigoni", 'font': {'size': 18}},
	gauge = {
		'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black", 'nticks':6},
		'bar': {'color': "royalblue"},
		'bgcolor': "white",
		'borderwidth': 2,
		'bordercolor': "lightgrey",
		'steps': [
			{'range': [0, 100], 'color': 'lightgrey'}
		]}))

#fig1.update_layout(
#	autosize=False)
#	height=200,
#	width=475,
#	margin=go.layout.Margin(
#		l=80,
#		r=200,
#		b=5,
#		t=90,
#		))

st.plotly_chart(fig1)

			     
			     ############## ALINH. COM TABATA ###########

fig2 = go.Figure()
fig2.add_trace(go.Indicator(
	mode = "gauge+number",
	number ={'suffix':'%'},
	value = float(dados[dept]['alinhamento_tabata']) * 100 ,
	title = {'text': "Tabata", 'font': {'size': 18}},
	gauge = {
		'axis': {'range': [None, 100],'tickwidth': 1, 'tickcolor': "black", 'nticks':6},
		'bar': {'color': "royalblue"},
		'bgcolor': "white",
		'borderwidth': 2,
		'bordercolor': "lightgrey",
		'steps': [
			{'range': [0, 100], 'color': 'lightgrey'}
		]}))

st.plotly_chart(fig2)

             ################### ALINH. COM GOVERNO ############

fig3 = go.Figure()
fig3.add_trace(go.Indicator(
	mode = "gauge+number",
	number ={'suffix':'%'},
	value = float(dados[dept]['alinhamento_gov']) * 100 ,
	title = {'text': "Governo", 'font': {'size': 18}},
	gauge = {
		'axis': {'range': [None, 100],'tickwidth': 1, 'tickcolor': "black", 'nticks':6},
		'bar': {'color': "royalblue"},
		'bgcolor': "white",
		'borderwidth': 2,
		'bordercolor': "lightgrey",
		'steps': [
			{'range': [0, 100], 'color': 'lightgrey'}
		]}))

st.plotly_chart(fig3)

 	          
 	          ################## ALINH. COM  PARTIDO ##############

fig4 = go.Figure()
fig4.add_trace(go.Indicator(
	mode = "gauge+number",
	number ={'suffix':'%'},
	value = float(dados[dept]['alinhamento_partido']) * 100 ,
	title = {'text': "Partido", 'font': {'size': 18}},
	gauge = {
		'axis': {'range': [None, 100],'tickwidth': 1, 'tickcolor': "black", 'nticks':6},
		'bar': {'color': "royalblue"},
		'bgcolor': "white",
		'borderwidth': 2,
		'bordercolor': "lightgrey",
		'steps': [
			{'range': [0, 100], 'color': 'lightgrey'}
		]}))

st.plotly_chart(fig4)


############################### GRÁFICO DE INTERESSES #######################################
labels = []
values = []

for j in range(5):	# 5 primeiros interesses
	labels.append(dados[dept]['interesse'][j]['tema'])
	values.append(round(float(dados[dept]['interesse'][j]['frequencia'])* 100,2))

# Revertendo a ordem das listas
labels = labels[::-1]
values = values[::-1] 


###### Plot de interesses #########

st.markdown('### Interesses')

def annotations(ax, labels, values):
	for label, value in zip(labels, values):
		ax.text(values[-1] / 2, label, label, 
				fontsize=font_size, horizontalalignment='center', verticalalignment='center')

font_size=16
fig = pl.figure()
ax  = fig.add_subplot(1,1,1)

ax.barh(labels, values, color='MediumSeaGreen')
annotations(ax, labels, values)

ax.tick_params(labelsize=font_size, labelleft=False, left=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
pl.xlabel('%', fontsize=font_size)

st.pyplot(fig)


################################### NUVEM DE PALAVRAS  ###########################################################

st.markdown('### Nuvem de Palavras (Twitter)')

def scrap(usuario):      
       
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(usuario).setSince('2019-02-01')
    
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    # Creating list of chosen tweet data
    user_tweets = [{'date': tweet.formatted_date, 'username': tweet.username, 'text': tweet.text} for tweet in tweets]
    
    return user_tweets



# Buscando o perfil do twitter dos deputados
perfil_twitter = pd.read_excel('deputados_redes_sociais.xlsx')

perfil_twitter = perfil_twitter.set_index('Deputado')



if deputado.lower() not in perfil_twitter.index :
	st.warning("Perfil do Twitter não encontrado")

else:

	twitter = perfil_twitter.loc[deputado.lower()].perfil[1:]
	
	df = scrap(twitter)
	
	if len(df) < 1:
		st.error("Não foi possível recuperar dados do twitter do parlamentar")

	else:
			
		#criando uma lista com todas as palavras dos ultimos 200 twites
		big_string = ''
		for i in range(1,len(df)):    
			big_string = big_string + df[i]['text']

		
		#Definindo stopwords
		stopwords = stopwords.words('portuguese') + list(punctuation)
		stopwords.extend(['https', 'http', 'sobre', 'vamos', 'co', 'rt', 'todos', 'todo', 'rs', 'vc', 'ser','pra', 'tudo', 'vai', 'vcs'])


		# Criando WordCloud
		wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(big_string)
		pl.figure(figsize=(20,12))
		pl.imshow(wordcloud, interpolation='bilinear')
		pl.axis('off')
		st.pyplot(pl.show())

