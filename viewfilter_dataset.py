import pandas as pd

legistalitvas_1975_2011 = pd.read_csv('./Dataset/complementares/resultados-legislativas-1975-2011.csv', sep=',')

type_ARI = legistalitvas_1975_2011[legistalitvas_1975_2011['tipo']=='ARI'] #as eleições ARI só aconteceram em 1979
type_AR = legistalitvas_1975_2011[legistalitvas_1975_2011['tipo']=='AR']



########
overall_results_df = pd.read_csv('./Dataset/legislativas2019/overall_results.csv', sep=',')

totalmandetes = overall_results_df[['time','territoryName', "totalMandates"]]

mandetes_perzone = totalmandetes[totalmandetes['territoryName']=='Porto']

zones = overall_results_df[
    (overall_results_df['territoryName']!='Território Nacional') &
    (overall_results_df['territoryName']!='Açores') &
    (overall_results_df['territoryName']!='Madeira')
    ]

totalzones = zones['territoryName'].drop_duplicates().tolist()



#########
votes_2019_df = pd.read_csv('./Dataset/legislativas2019/votes.csv', sep=',')

'''
while True:
    partido = input('Nome do partido: ')
    vote_national = votes_2019_df[
        (votes_2019_df['District']=='Braga') &
        (votes_2019_df['Party']==partido)
        ]

    print(f'\n{vote_national[['time', 'Party','Votes']].to_markdown(index=False)}\n\n')
'''
data_pervotes = votes_2019_df['time'].drop_duplicates().tolist()
#print(f'TODAS AS DATAS: {data_pervotes}')


'''
total_votes_global = []
for data in data_pervotes:
    counter_votes = votes_2019_df[(votes_2019_df['District']=='Território Nacional') &
                                  (votes_2019_df['time']==data)]
    
    total_votes = counter_votes['Votes']
    print(f'TOTAL VOTOS: \n{total_votes}')
    total_votes_global.append(sum(total_votes.drop_duplicates().tolist()))
    #print(f'TOTAL VOTES; DATA {data}:\n {sum(total_votes.tolist())}\n\n')

total = list(set(total_votes_global))
print(f'TOTAL DE VOTAÇÕES SEM REPETIÇÃO EM TERRITÓRIO NACIONAL: \n {total}\n')
print('SOMA TOTAL DE VOTOS',sum(total))
'''


''' 
vote_national = votes_2019_df[
        (votes_2019_df['District']!='Território Nacional') &
        (votes_2019_df['time']=='2019-10-06 18:56:26') &
        (votes_2019_df['Party']=='PS')
        ]

total_national_votes = vote_national['Votes'].tolist()

print(sum(total_national_votes))
'''

'''
total_territory = votes_2019_df[
    votes_2019_df['District']=='Território Nacional'
]

total_votes_territory = total_territory['Votes'].drop_duplicates().tolist()

print(sum(total_votes_territory))
'''


####
votes_parishes_df = pd.read_csv('./Dataset/legislativas2019/votes_parishes.csv', sep=',')

'''
while True:

    district = input('Nome do distrito: ')
    perdistrict = votes_parishes_df[
        votes_parishes_df['District']==district]
    
    #print(f'VOTOS DE ACORDO COM OS DISTRITOS: \n{perdistrict[['Trade', 'Votes']]}')

    total_votesdistrict = perdistrict['Votes'].tolist()
    print(f'TOTAL DE VOTOS NO DISTRITO DE {district}: {sum(total_votesdistrict)}\n\n')
'''


####
parishes_df = pd.read_csv('./Dataset/legislativas2019/parishes.csv', sep=',')

#district = input('Nome do distrito: ')
perdistrict = parishes_df[
    (parishes_df['District']=='Braga')]

print('TODOS OS VOTANTES EM BRAGA:\n',perdistrict[['totalVoters', 'Council', 'District']])
print('\nSOMA DE TODOS OS VOTANTES EM BRAGA: ',perdistrict['totalVoters'].sum())