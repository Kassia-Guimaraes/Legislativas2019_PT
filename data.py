import pandas as pd

regioes = {
    'Aveiro': 'Norte',
    'Beja': 'Alentejo',
    'Braga': 'Norte',
    'Bragança': 'Norte',
    'Castelo Branco': 'Centro',
    'Coimbra': 'Centro',
    'Évora': 'Alentejo',
    'Faro': 'Algarve',
    'Guarda': 'Centro',
    'Leiria': 'Centro',
    'Lisboa': 'Lisboa',
    'Portalegre': 'Alentejo',
    'Porto': 'Norte',
    'Santarém': 'Centro',
    'Setúbal': 'Lisboa',
    'Viana do Castelo': 'Norte',
    'Vila Real': 'Norte',
    'Viseu': 'Centro',
    'Açores':'Açores',
    'Madeira':'Madeira',
    'Ilha Terceira':'Açores',
    'Ilha Graciosa': 'Açores'
}


### overall2019
overall2019_df = pd.read_csv('./oldDataSet/legislativas2019/overall_results.csv', sep=',')

overall2019_df = overall2019_df.fillna(int(0))
overall2019_df = overall2019_df.drop(overall2019_df.loc[overall2019_df['territoryName']=='Território Nacional'].index)
overall2019_df = overall2019_df.drop(['territoryFullName','pre.totalMandates', 'pre.availableMandates', 'pre.blankVotes', 'pre.blankVotesPercentage', 'pre.nullVotes', 'pre.nullVotesPercentage', 'pre.votersPercentage', 'pre.subscribedVoters', 'pre.totalVoters'], axis=1) #coluna territoryFullName = territoryName

overall2019_df = overall2019_df.rename(columns={'time':'Data', 'territoryName':'Distrito', 'territoryKey':'Código Territorial', 'totalMandates':'Total Mandatos', 'availableMandates':'Mandatos Disponíveis', 'numParishes':'Total Freguesias', 'numParishesApproved':'Freguesias Apuradas', 'blankVotes':'Votos Brancos', 'blankVotesPercentage':'Percentagem Votos Brancos', 'nullVotes':'Votos Nulos', 'nullVotesPercentage':'Percentagem Votos Nulos', 'votersPercentage':'Percentagem Votantes', 'subscribedVoters':'Votantes Inscritos', 'totalVoters':'Total de Votos'})

overall2019_df['Região'] = overall2019_df['Distrito'].map(regioes)

overall2019_df.to_csv('./modificatedData/overall2019.csv', index=False)



### parishes2019
parishes2019_df = pd.read_csv('./oldDataSet/legislativas2019/parishes.csv', sep=',')

parishes2019_df = parishes2019_df.fillna(int(0))
parishes2019_df = parishes2019_df.drop(parishes2019_df[['territoryFullName',"pre.totalMandates","pre.availableMandates","pre.blankVotes","pre.blankVotesPercentage","pre.nullVotes","pre.nullVotesPercentage","pre.votersPercentage","pre.subscribedVoters","pre.totalVoters"]], axis=1) #coluna territoryFullName = territoryName
parishes2019_df = parishes2019_df.drop(parishes2019_df[["numParishes", "numParishesApproved"]], axis=1)

parishes2019_df = parishes2019_df.rename(columns={'time':'Data', 'territoryName':'Freguesia', 'territoryKey':'Código Territorial', 'totalMandates':'Total Mandatos', 'availableMandates':'Mandatos Disponíveis', 'blankVotes':'Votos Brancos', 'blankVotesPercentage':'Percentagem Votos Brancos', 'nullVotes':'Votos Nulos', 'nullVotesPercentage':'Percentagem Votos Nulos', 'votersPercentage':'Percentagem Votantes', 'subscribedVoters':'Votantes Inscritos', 'totalVoters':'Total de Votos', 'Council':'Concelho', 'District':'Distrito'})

parishes2019_df['Região'] = parishes2019_df['Distrito'].map(regioes)

parishes2019_df.to_csv('./modificatedData/parishes2019.csv', index=False)



### result_parishes
result_parishes2019_df = pd.read_csv('./oldDataSet/legislativas2019/votes_parishes.csv', sep=',')

result_parishes2019_df = result_parishes2019_df.rename(columns={"Trade":'Freguesia',"Party":'Partido',"Percentage":'Percentagem',"validVotesPercentage":'Percentagem de Votos Válidos',"Votes":'Votos',"Council":'Concelho',"District":'Distrito'})

result_parishes2019_df['Região'] = result_parishes2019_df['Distrito'].map(regioes)

result_parishes2019_df.to_csv('./modificatedData/result_parishes2019.csv', index=False)



# parties

parties = {'Partido': ['ADN','ASDI','B.E.','CDS-PP','CH','IL','L','MDP/CDE','PAN','PCP','PEV','PCP-PEV','PCP/PEV','PPD/PSD','PPM','PRD','PS','PSN','UDP','UEDS','A', 'R.I.R.','NC','PNR','PURP','PCTP/MRPP','PDR','MPT','JPP','MAS']}

parties_df = pd.DataFrame(parties)

partido_nome = {
    'ADN': 'Alternativa Democrática Nacional',
    'ASDI' : 'Ação Social Democrata Independente',
    'B.E.': 'Bloco de Esquerda',
    'CDS-PP': 'Centro Democrático Social - Partido Popular',
    'CH': 'Chega',
    'IL': 'Iniciativa Liberal',
    'L':'Livre',
    'MDP/CDE' : 'Movimento Democrático Português / Comissão Democrática Eleitoral',
    'PAN': 'Pessoas, Animais Natureza',
    'PCP': 'Partido Comunista Português',
    'PEV':'Partido Ecologista Os Verde',
    'PCP-PEV': 'CDU - Coligação Democrática Unitária',
    'PCP/PEV':'CDU - Coligação Democrática Unitária',
    'PPD/PSD': 'Partido Popular Democrático / Partido Social Democrático',
    'PPM':'Partido Popular Monárquico',
    'PRD':'Partido Renovação Democrática',
    'PS': 'Partido Socialista',
    'PSN':'Partido da Solidariedade Nacional',
    'UDP': 'União Democrática Popular',
    'UEDS' :'União da Esqueda para a Democracia Socialista',
    'A' : 'Aliança',
    'R.I.R.' : 'Reagir Incluir Reciclar',
    'NC': 'Nós, Cidadãos!',
    'PNR': 'Partido Nacional Renovador',
    'PURP': 'Partido Unido dos Reformados e Pensionistas',
    'PCTP/MRPP':'Partido Comunista dos Trabalhadores Portugueses / Movimento Reorganizativo do Partido do Proletariado',
    'PDR' : 'Partido Democrático Republicano',
    'MPT': 'Movimento Partido da Terra',
    'JPP' : 'Juntos pelo Povo',
    'MAS':'Movimento Alternativa Socialista'
}
partido_cor ={
    'ADN': '#204E84', #azul
    'ASDI' : '#2B2B2B', #preto/cinza
    'B.E.': '#CC1615', #vermelho
    'CDS-PP': '#127094', #azul claro
    'CH': '#1F2052', #roxo
    'IL': '#00AEEF', #azul claro
    'L': '#840D11', #vermelho
    'MDP/CDE': '#C10000', #vermelho
    'PAN': '#3D9177', #azul/verde
    'PCP': '#B20000', #vermelho
    'PEV': '#FDDA0B', #amarelo
    'PCP-PEV':'#4F4F4F', #cinza
    'PCP/PEV' : '#4F4F4F', #cinza
    'PPD/PSD': '#FF6500', #laranja
    'PPM': '#2A5392', #azul
    'PRD':'#216B31', #verde
    'PS': '#E21F26', #vermelho
    'PSN':'#2AAAF5', #azul
    'UDP': '#FF0000', #vermelho
    'UEDS':'#F40000', #vermelho
    'A' : '#0030A1', #azul escuro
    'R.I.R.' : '#02959F', #azul /verde
    'NC': '#E5A845', #amarelo queimado
    'PNR' : '#182D81', #azul escuro
    'PURP' : '#008836', #verde
    'PCTP/MRPP': '#E00C03', #vermelho
    'PDR': '#204E84', #azul
    'MPT': '#154026', #verde escuro
    'JPP' : '#00AB84', #verde/azul
    'MAS': '#D50000' #vermelho
}

parties_df['Nome'] = parties_df['Partido'].map(partido_nome)
parties_df['Cor'] = parties_df['Partido'].map(partido_cor)

parties_df.to_csv('./modificatedData/parties.csv', index=False)




# votes_party_75-11
votes_party_all = pd.read_csv('./oldDataSet/complementares/resultados-legislativas-1975-2011.csv', sep=',')

votes_party_all['data'] = pd.to_datetime(votes_party_all['data'])

votes_party_all['Ano'] = votes_party_all['data'].dt.year

votes_party_all = votes_party_all.rename(columns={'codigo':'Código', 'nome':'Distrito','tipo':'Tipo','data':'Data','partido':'Partido','num_votos':'Total Votos','perc_votos':'Percentual Votos','mandatos':'Mandatos'})

votes_party_all.to_csv('./modificatedData/result_parties.csv', index=False)



# parties_info_all 
parties_info_all = pd.read_csv('./eleicoes-1975-2022/parties_info_all.csv', sep=',')

parties_info_all = parties_info_all[['Partido', 'Nome', 'Descrição']]

parties_info_all.to_csv('./modificatedData/parties_info_all.csv', index=False)