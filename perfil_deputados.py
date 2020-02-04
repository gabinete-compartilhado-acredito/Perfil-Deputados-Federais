import streamlit as st 
import plotly.graph_objects as go 
import json
import numpy as np 
from glob import glob


st.markdown("hello world!!!")


imagem = '<img id="icone" src="https://www.movimentoacredito.org/wp-content/uploads/2018/08/acredito_fundobranco.png" style="float:middle" width=73%>'
st.write( imagem, unsafe_allow_html=True)


# Título do site
st.markdown(" # Perfil dos Deputados Federais")

# Abrindo o arquivo json
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


####################### Caixa de seleção por partido ###############################
partidos = []
for i in range(len(dados)):
    if dados[i]['sigla_partido'] not in partidos:
        partidos.append(dados[i]['sigla_partido'])
partidos.sort()

partidos_ = ['TODOS']
partidos_.extend(partidos)
partido = st.selectbox('Escolha o partido', partidos_)

#################### Seleção por UF ############################################

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
estado = st.selectbox('Selecione o Estado: ', uf)

###################### Seleção por Deputados ##################################

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
deputado = st.selectbox('Selecione o Parlamentar', candidatos)


# capturando o index do deputado selecionado
dept = 0
for i in range(len(dados)):
    if dados[i]['ultimoStatus_nome'] == deputado:
        dept = i



#################################Criando Tabela com foto do parlamentar###################################### 

# Concatenando o link + id do parlamentar
src = "https://www.camara.leg.br/internet/deputado/bandep/" + dados[dept]["id_deputado"] +".jpg"
img_src = '<img src=' + src + '>' 

# Selecionando as bancadas que o deputado faz parte
bancadas = ' - '

if len(dados[dept]['array_bancadas']) > 0:
	bancadas = ', '.join(dados[dept]['array_bancadas'])

#Criando tabela com foto e informações do parlamentar
tabela_foto = """<table frame='void' rules='cols' width=%(largura)s>

<tr>
    <td><img src="%(foto)s" height=200px></td>
    <td> 
        <table  frame='void' rules='cols' width=%(largura2)s height=%(altura)s> 
            <tr>
                <td><b> Nome: </b>%(deputado)s</td>                
            </tr>
            <tr>
                <td><b> Partido </b>%(partido)s  </td>
            </tr>
            <tr>
                <td><b> UF: </b>%(estado)s</td>
            </tr>
            <tr>
            	<td><b> Bancadas: </b>%(bancadas)s</td>
            </tr>
        </table>
    </td>
	
</tr>


</table>""" %{'foto':src, 'largura':'60%', 'largura2':'250px', 'altura':'100%', 'deputado':dados[dept]['ultimoStatus_nome'],
 'partido':dados[dept]['sigla_partido'], 'estado':dados[dept]['uf'],'largura3':'280px', 'bancadas': bancadas}

st.write( tabela_foto , unsafe_allow_html=True)



################################# Criando tabela Liderança ######################################################
st.write("    ")
cargo_lider=[]
sigla_bloco = []

for lideranca in dados[dept]['liderancas']:
    cargo_lider.append(lideranca['cargo'])
    sigla_bloco.append(lideranca['sigla_bloco'])    


texto1 = ''
if len(cargo_lider) == 0:
	texto1 = "<tr><td> - </td><td> - </td></tr>"	
else:	
	for i in range(len(cargo_lider)):
		texto1 = "<tr><td>"+ cargo_lider[i]+"</td><td>"+ sigla_bloco[i]+ "</td></tr>"

tabela2 = """<table frame='void' rules='cols'>
			<tr>
			    <th>Cargo</th>
			    <th>Sigla do Bloco</th>
			    %(texto1)s				
			</tr> 
		</table>""" %{'texto1': texto1}
	


################################# Criando tabela Orgãos######################################################3333
entidade=[]
cargo = []


for orgao in dados[dept]['orgaos']:
    entidade.append(orgao['sigla_orgao'])
    cargo.append(orgao['titulo'])
    

texto = ''
if len(entidade) > 0:
	for i in range(len(entidade)):
		texto = texto + "<tr><td>"+ entidade[i]+"</td><td>"+ cargo[i]+ "</td></tr>"
else:
	texto = "<tr><td> - </td><td> - </td></tr>"


tabela_orgao = """<table frame='void' rules='cols'>
					<tr>
					<th>Órgão</th>
					<th>Cargo</th>
					</tr>
					%(texto)s
				</table>""" %{'texto': texto}

st.write(tabela_orgao, unsafe_allow_html=True)

st.write("  ")

st.write( tabela2, unsafe_allow_html=True)

################################### Criando o dashboard de Alinhamento ##############################################
st.write('            ')
st.markdown('## Alinhamentos')


################################# RIGONI ###########################################################
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

fig1.update_layout(
	autosize=True,
	height=200,
	width=475,
	margin=go.layout.Margin(
		l=80,
		r=200,
		b=5,
		t=90,
		))

st.plotly_chart(fig1)

######################################### Tabata ####################################################
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
fig2.update_layout(
	autosize=True,
	height=200,
	width=475,
	margin=go.layout.Margin(
		l=80,
		r=200,
		b=5,
		t=90,
		))

st.plotly_chart(fig2)

######################################## Governo ####################################################
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
fig3.update_layout(
	autosize=True,
	height=200,
	width=475,
	margin=go.layout.Margin(
		l=80,
		r=200,
		b=5,
		t=90,
		))

st.plotly_chart(fig3)

######################################## Partido ######################################################
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
fig4.update_layout(
	autosize=True,
	height=200,
	width=475,
	margin=go.layout.Margin(
		l=80,
		r=200,
		b=5,
		t=90,
		))

st.plotly_chart(fig4)


############################### Gráfico de Interesses #######################################
labels = []
values = []
for j in range(5):	# 5 primeiros interesses
	labels.append(dados[dept]['interesse'][j]['tema'])
	values.append(round(float(dados[dept]['interesse'][j]['frequencia'])* 100,2))

# Revertendo a ordem das listas
labels = labels[::-1]
values = values[::-1] 


fig = go.Figure(go.Bar(
            x= values,
            y= labels,
            orientation='h',
            marker_color='MediumSeaGreen',            
            hoverinfo= "none",            
            ))

def annotations(fig, labels, values, j):

    fig.add_annotation(
        go.layout.Annotation(
            x = values[4] / 2,
            text= labels[j], 
            y = j ,
            align='center',    
            font=dict(       
            family="arial",   
            size=20,          
            color="black"),
            ))

# Chamando a função para definir atributos do gráfico
for j in range(5):
    annotations(fig, labels, values, j)



fig.update_annotations(dict(
            xref="x",
            yref="y",
            showarrow=False,
            ax=0,
            ay=0,
            
        ))


fig.update_layout(title_text= 'PRINCIPAIS INTERESSES',
                  yaxis={ 'showticklabels':False, 'showgrid': False },
                  xaxis={'showgrid': False, 'showticklabels':True, 'tick0':0, 'dtick':3 },
                  paper_bgcolor= 'rgba(0,0,0,0)',
                  plot_bgcolor= 'rgba(0,0,0,0)',
                  
                  autosize=True,
                  margin=go.layout.Margin(
			        l=0,
			        r=300,
			        b=100,
			        t=100,
			        pad=4
			    	)
                  )
        
st.plotly_chart(fig)


