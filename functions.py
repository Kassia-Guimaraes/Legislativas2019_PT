import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

overall2019_df = pd.read_csv('./modificatedData/overall2019.csv', sep=',')
overall2019_df['Data'] = pd.to_datetime(overall2019_df['Data'], format='%Y-%m-%d %H:%M:%S')

parliamentary_seats_df = pd.read_csv('./eleicoes-1975-2022/mandatos-por-partido-1975-2022.csv')
party_info_all = pd.read_csv('./modificatedData/parties_info_all.csv', sep=',')
result_parties_df = pd.read_csv('./modificatedData/result_parties.csv', sep=',')
parishes2019_df = pd.read_csv('./modificatedData/parishes2019.csv', sep=',')
result_parishes2019_df = pd.read_csv('./modificatedData/result_parishes2019.csv', sep=',')
party_info_df = pd.read_csv('./modificatedData/parties.csv', sep=',')


def errorCodes(typeError):
    return f"\33[91mWARNING: {typeError.title()}\33[0;0m\n"

def exitMessange(index_value,typeMessange):
    return f"\033[93m{index_value} {typeMessange}\033[0m\n"

def nextMessange(index_value, typeMessange):
    return f"\033[94m{index_value} {typeMessange}\033[0m\n"

def viewDataFrame(df):
    return print(f"{df.to_markdown(index=False)}\n")

def filtersMenu(toFilter, selectedFilters): #return index in filterMenu
    if selectedFilters == []:
        for index, value in enumerate(toFilter):
            print(f"\33[1m{index+1} \033[0;0m{value}")
        print(f"\33[1m{index+2}\033[0;0m selecionar todos\n{exitMessange(0, "sair")}")
    else:
        for index, value in enumerate(toFilter):
            print(f"\33[1m{index+1} \033[0;0m{value}")
        print(f"\33[1m{index+2}\033[0;0m selecionar todos\n{nextMessange(index+3, 'next')}{exitMessange(0, "sair")}")
    return index

#dataFrame, elements in dataFrame to filter, information messange
def getUserFiltersLoop(df, toFilter, messange): #return array with all filters to use
    theSelectedFilters = []
    while True:
        index = filtersMenu(toFilter, theSelectedFilters)
        try:
            print(f"\33[0;0mFiltros selecionados: {theSelectedFilters} \33[0;0m\nSe quiser alterar a seleção apenas selecionar novamente o item") #show what filters was select
            input_value = input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m")

            if int(input_value) != 0 and int(input_value) != index+2 and int(input_value) != index+3: #when 0 abort all, i+2 select all, i+3 finish

                while int(input_value) < 0 or int(input_value)-1 > len(toFilter):
                    print(errorCodes("Entrada incorreta"))
                    input_value = input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m") #request new input

                selection = toFilter[int(input_value)-1] #the selecion is the input_value on index toFilter

                if selection not in theSelectedFilters: #if selection wasnt select after
                    theSelectedFilters.append(selection)
                else: #remove the term if was select after
                    theSelectedFilters.remove(selection)
                viewDataFrame(df[theSelectedFilters].drop_duplicates())

            elif int(input_value) == index+2: #selected all filters
                while True:
                    allfilters_value = int(input(f"\nDeseja selecionar todos os filtros?\n\033[1m1 \033[0;0mSim\n\033[1m2 \033[0;0mNão\nSelecione uma opção: "))
                    match allfilters_value:
                        case 1: #confirm selection all terms
                            theSelectedFilters = toFilter
                            print(f"\033[0;0mFiltros selecionados: {theSelectedFilters} \033[0;0m\n")
                            break
                        case 2: #return to choice the filters
                            break  # Break out of the loop without changing theSelectedFilters
                        case _: #error code
                            print(errorCodes("Entrada incorreta"))

                if allfilters_value == 1: #before confirmation about selection all filters
                    break
                else: #new selection filters
                    print("\n")
                    continue
            
            else: # if choice 0, abort all
                return theSelectedFilters
            
        except: #errorCodes
            print('\n\n')
    return theSelectedFilters #return de array with all selected filters

def userFilter(toFilter, messange):
    theSelectedFilters = []
    while True:
        try:
            for index, value in enumerate(toFilter):
                print(f"\33[1m{index+1} \033[0;0m{value}")
            input_value = input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m")

            while int(input_value) <1 and int(input_value) > len(toFilter)-1:
                print(errorCodes("Entrada incorreta"))
                input_value = int(input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m\n"))
            theSelectedFilters = toFilter[int(input_value)-1]

            return theSelectedFilters #return de array with all selected filters
        except:
            print(errorCodes('Entrada inválida'))

def locationFilter(df, locationChoice):

    if locationChoice == 'Freguesia':
        parishes_choices = []
        while True:
            try:
                print(f'\nEscolha o \033[95mDistrito\033[0;0m que pertence a freguesia\n')
                district = userFilter(df['Distrito'].drop_duplicates().to_list(), 'a freguisia no distrito')

                print(f'\n\nEscolha o \033[95mConcelho\033[0;0m que pertence a freguesia\n')
                council = userFilter(df[(df['Distrito']==district)]['Concelho'].drop_duplicates().to_list(), 'a freguesia no concelho')

                print(f'\n\nAgora só escolher as \033[95mFreguesias\033[0;0m\n')
                location = df[(df['Distrito']==district) & (df['Concelho']==council)]
                parishes = getUserFiltersLoop(location, location['Freguesia'].drop_duplicates().to_list(), 'a freguesia')

                for element in parishes:
                    parishes_choices.append(element)
                parishes_choices = list(set(parishes_choices))
                
                other_parishes = int(input(f'\nFreguesias selecionadas {parishes_choices}\n\nDeseja selecionar mais alguma freguesia?\n1 Sim\n2 Não\nSelecione um número: '))
                while other_parishes != 1 and other_parishes!=2:
                    print(errorCodes('Entrada Invalida'))
                    
                    other_parishes = int(input(f'\n\nDeseja selecionar mais alguma freguesia?\n1 Sim\n2 Não\nSelecione um número: '))
                
                if other_parishes == 2:
                    return parishes_choices                
            
            except:
                print(errorCodes('Entrada Incorreta'))

    elif locationChoice == 'Concelho':
        council_choices = []
        while True:

            try:
                print(f'\nEscolha o \033[95mDistrito\033[0;0m que pertence o concelho\n')
                district = userFilter(df['Distrito'].drop_duplicates().to_list(), 'a freguisia no distrito')

                print(f'\n\nAgora só escolher os \033[95mConcelhos\033[0;0m\n')
                location = df[(df['Distrito']==district)]
                council = getUserFiltersLoop(location, location['Concelho'].drop_duplicates().to_list(), 'o concelho')

                for element in council:
                    council_choices.append(element)
                council_choices = list(set(parishes_choices))
                
                other_council = int(input(f'Freguesias selecionadas {council_choices}\nDeseja selecionar mais alguma freguesia?\n1 Sim\n2 Não\nSelecione um número: '))
                while other_council != 1 and other_council !=2:
                    print(errorCodes('Entrada Invalida'))
                    
                    other_parishes = int(input(f'Freguesias selecionadas {council_choices}\nDeseja selecionar mais alguma freguesia?\n1 Sim\n2 Não\nSelecione um número: '))
                
                if other_council == 2:
                    return council_choices                
            
            except:
                print(errorCodes('Entrada Incorreta'))

    elif locationChoice == 'Distrito':
        print(f'\nEscolha os \033[95mDistrito\033[0;0m\n')
        district_choices = getUserFiltersLoop(df, df['Distrito'].drop_duplicates().to_list(), 'o distrito')
                
        return district_choices                

    else:
        print(f'\nEscolha as \033[95mRegiões\033[0;0m\n')
        region_choices = getUserFiltersLoop(df, df['Região'].drop_duplicates().to_list(), 'a região')
        return region_choices

def choosingHour():
    while True: #choosing hour
        hours = input('\nQual intervalo de \033[95mhorários\033[0;0m deseja visualizar?\nA apuração dos votos é entre 20:10 do dia 06 de junho até 00:35 do dia 07 de junho\nPara escolher digite o horário formato 20:10-21:30: ')
        hours = hours.split('-')

        while len(hours)!=2:

            print(errorCodes('hora inválida'))
            hours = input('\nQue \033[95mhorários\033[0;0m deseja visualizar?\nA apuração dos votos vai desde 20:10 até 00:35 do dia 07/06\nPara escolher digite o horário formato 20:10-21:30: ')
            hours = hours.split('-')

        initial_hour = hours[0].split(':')
        final_hour = hours[1].split(':')

        while (len(initial_hour) !=2 or len(initial_hour[0])!=2 or len(initial_hour[0])!=2 or 
            len(final_hour)!=2 or len(final_hour[0])!=2 or len(final_hour[1])!=2 or
            (int(initial_hour[0])<20 and int(initial_hour[0])!=0) or
            (int(initial_hour[0])>23) or (int(initial_hour[1])>59) or (int(final_hour[1])>59) or
            (int(initial_hour[0])==20 and int(initial_hour[1])<10) or
            (int(final_hour[0])<int(initial_hour[0]) and int(final_hour[0])!=0) or
            (int(final_hour[0])==int(initial_hour[0]) and int(final_hour[1])<int(initial_hour[1])) or
            (int(final_hour[0])>23)): #verification time

            print(errorCodes('hora inválida'))
            hours = input('\nQue \033[95mhorários\033[0;0m deseja visualizar?\nA apuração dos votos vai desde 20:10 até 00:35 do dia 07/06\nPara escolher digite o horário formato 20:10-21:30: ')
            hours = hours.split('-')
            
            initial_hour = hours[0].split(':')
            final_hour = hours[1].split(':')
        
        return initial_hour, final_hour

def votesParty2019(df): 
    parties = getUserFiltersLoop(df, df['Partido'].drop_duplicates(), 'os partidos') # list with selected parties
    print(f'\nAgora que já escolheu os partidos basta escolher a localidade que deseja visualizar\n')

    place = userFilter(['Freguesia', 'Concelho', 'Distrito', 'Região'], 'a localidade')
    locations = locationFilter(df, place) # list with selected localities

    print(f'\nQue \033[95mdados\033[0;0m deseja visualizar?\n')
    type_votes = userFilter(['Percentagem de Votos Válidos','Votos'], 'os dados de visualização')

    location_df = pd.DataFrame()
    for locality in locations:
        for party in parties:
            location_df = pd.concat([location_df, df[(df[place]==locality) & (df['Partido']==party)]], axis=0) #filtered dataFrame

    labels = []
    for party_acronym in parties: #creating legend with parties name
        party_name = party_info_df.loc[party_info_df['Partido'] == party_acronym, 'Nome'].iloc[0]  #Find party name
        label = f'{party_acronym} - {party_name}'
        labels.append(label)

    if type_votes == 'Votos':    
        #groupby([columns name to group])[element to view].sum/mean()
        analisis_groupby = location_df.groupby([place, 'Partido'])[type_votes].sum().unstack()

        plt.figure(figsize=(10, 6))
        bar_width = 0.1
        position = bar_width/2

        for i, party in enumerate(parties): #bar plot
            position_element = [x + i * bar_width - position for x in range(len(analisis_groupby.index))]
            party_color = party_info_df[party_info_df['Partido']==party]['Cor'].iloc[0] #add color by party
            
            plt.bar(position_element, analisis_groupby[party], width=bar_width, label=party, color=party_color)

            for x, y in zip(position_element, analisis_groupby[party]):
                plt.text(x, y, f'{y:.1f}', ha='center', va='bottom', rotation=80, fontsize=8, color='black')

        plt.xlabel(place)
        plt.ylabel(f'Número de {type_votes}')
        plt.title(f'{type_votes} por Partido em {place}')
        plt.xticks(range(len(analisis_groupby.index)), analisis_groupby.index, rotation=70)
        plt.legend(title='Legenda', labels=labels)
        plt.tight_layout()

        plt.show()
    
    else: #if percentage
        #groupby([columns name to group])[element to view].sum/mean()
        analisis_groupby = location_df.groupby([place, 'Partido'])[type_votes].mean().unstack()

        plt.figure(figsize=(10, 6))
        bar_width = 0.1
        position = bar_width/2

        for i, party in enumerate(parties): #bar plot
            position_element = [x + i * bar_width - position for x in range(len(analisis_groupby.index))]
            party_color = party_info_df[party_info_df['Partido']==party]['Cor'].iloc[0] #add color by party    

            plt.bar(position_element, analisis_groupby[party], width=bar_width, label=party, color=party_color)

            for x, y in zip(position_element, analisis_groupby[party]):
                plt.text(x, y, f'{y:.1f}', ha='center', va='bottom', rotation=80, fontsize=8, color='black')
                
        plt.xlabel(place)
        plt.ylabel(f'Média da {type_votes}')
        plt.title(f'{type_votes} por Partido em {place}')
        plt.xticks(range(len(analisis_groupby.index)), analisis_groupby.index, rotation=70)

        plt.legend(title='Legenda', labels=labels)
        plt.tight_layout()

        plt.show()

    return location_df

def geographicVotes(df):
    place = userFilter(['Freguesia', 'Concelho', 'Distrito', 'Região'], 'a localidade')
    locations = locationFilter(df, place) # list with selected locality

    print(f'\nQue \033[95mdados\033[0;0m deseja visualizar?\n')
    type_votes = userFilter(['Votos Brancos','Percentagem Votos Brancos','Votos Nulos','Percentagem Votos Nulos','Percentagem Votantes','Votantes Inscritos','Total de Votos'], 'os dados de visualização')

    df_filtered = pd.DataFrame()
    for locality in locations: 
        df_filtered = pd.concat([df_filtered, df[(df[place]==locality)]])


    if place == 'Freguesia':

        plt.figure(figsize=(10, 6))
        bar_chart = plt.bar(df_filtered[place], df_filtered[type_votes], width=0.1)

        for bar in bar_chart: #add number of votes on bars
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, '{:,.0f}'.format(height),
                        ha='center', va='bottom', fontsize=10, color='black')

        plt.xlabel(place)
        plt.ylabel(f'Número de {type_votes}')
        plt.title(f'{type_votes} por {place}')
        plt.xticks(rotation=70)
        plt.legend()
        plt.tight_layout()

        plt.show()

        return df_filtered


    else: #if not parishe
        grouping_votes = pd.DataFrame(columns=[place, type_votes])
        grouping_votes = grouping_votes.dropna()
        if 'Percentagem' not in type_votes: #if votes sum all votes in locality
            
            for locality in locations:

                sum_votes = df_filtered[df_filtered[place]==locality][type_votes].sum()
                new_row = pd.DataFrame({place:[locality], type_votes:[sum_votes]})
                if not grouping_votes.empty:
                    grouping_votes = pd.concat([grouping_votes.dropna(), new_row], ignore_index=True) 
                else:
                    grouping_votes = new_row.copy()
            
            print('\nComo deseja \033[95mvisualizar os votos\033[0;0m?\n')
            format_votes = userFilter(['De todos os habitantes','A cada 10 habitantes', 'A cada 100 habitantes', 'A cada mil habitantes'], 'a visualização dos votos por habitante')

            if format_votes=='A cada 10 habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/10
            elif format_votes=='A cada 100 habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/100
            elif format_votes=='A cada mil habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/1000

            plt.figure(figsize=(10, 6))
            bar_chart = plt.bar(grouping_votes[place].dropna(), grouping_votes[type_votes], width=0.1)

            for bar in bar_chart:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, '{:,.0f}'.format(height),
                         ha='center', va='bottom', fontsize=10, color='black')

            plt.xlabel(place)
            plt.ylabel(f'Número de {type_votes} ')
            plt.title(f'{type_votes} por {place} {format_votes.lower()}')
            plt.xticks(rotation=50)
            plt.legend()
            plt.tight_layout()

            plt.show()
        
        else: #if percentage

            for locality in locations:

                sum_votes = df_filtered[df_filtered[place]==locality][type_votes].mean()
                new_row = pd.DataFrame({place:[locality], type_votes:[sum_votes]})
                if not grouping_votes.empty:
                    grouping_votes = pd.concat([grouping_votes.dropna(), new_row], ignore_index=True) 
                else:
                    grouping_votes = new_row.copy() 

            plt.figure(figsize=(10, 6))
            bar_chart = plt.bar(grouping_votes[place], grouping_votes[type_votes], width=0.1)

            for bar in bar_chart:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, '{:,.2f}'.format(height),
                         ha='center', va='bottom', fontsize=10, color='black')

            plt.xlabel(place)
            plt.ylabel(f'Média de {type_votes} ')
            plt.title(f'{type_votes} por {place}')
            plt.xticks(rotation=50)
            plt.legend()
            plt.tight_layout()

            plt.show()

def votesPerHour(df):

    initial_hour, final_hour = choosingHour()

    df = df[((df['Data'].dt.hour>=int(initial_hour[0])) & (df['Data'].dt.minute>=int(initial_hour[1]))) &
            ((df['Data'].dt.hour<=int(final_hour[0])) & (df['Data'].dt.minute<=int(final_hour[1])))]
    
    print(f'\nQue \033[95mlocalidade\033[0;0m deseja visualizar?\n')
    place = userFilter(['Distrito', 'Região'], 'a localidade que deseja ver a apuração')
    locations = locationFilter(df, place)

    print(f'\nQue \033[95mdados\033[0;0m deseja visualizar?\n')
    type_votes = userFilter(['Freguesias Apuradas','Votos Brancos','Percentagem Votos Brancos','Votos Nulos','Percentagem Votos Nulos','Percentagem Votantes','Total de Votos'], 'os dados de visualização')

    location_df = pd.DataFrame()
    for locality in locations: 
        location_df = pd.concat([location_df, df[(df[place]==locality)]], ignore_index=True)

    location_df[['Data','Hora']] = location_df['Data'].astype(str).str.split(' ').to_list()

    grouping_votes = pd.DataFrame(columns=[place, type_votes])
    if 'Percentagem' not in type_votes and 'Votos' not in type_votes: #if votes sum all votes in locality
        
        analisis_groupby = location_df.groupby(['Hora', place])[type_votes].sum().unstack()

        plt.figure(figsize=(10, 6))

        for zone in locations:
            plt.plot(analisis_groupby.index, analisis_groupby[zone], marker='o',label=zone)

        plt.xlabel('Hora')
        plt.ylabel(f'Número de {type_votes}')
        plt.title(f'Apuração {type_votes} por Hora em {place}')
        plt.xticks(rotation=70)
        plt.legend()
        plt.tight_layout()

        plt.show()

        #okok


    elif 'Votos' in type_votes:
            
            print('\nComo deseja \033[95mvisualizar os votos\033[0;0m?\n')
            format_votes = userFilter(['De todos os habitantes','A cada 10 habitantes', 'A cada 100 habitantes', 'A cada mil habitantes'], 'a visualização dos votos por habitante')

            if format_votes=='A cada 10 habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/10
            elif format_votes=='A cada 100 habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/100
            elif format_votes=='A cada mil habitantes':
                grouping_votes[type_votes] = grouping_votes[type_votes]/1000
            
            plt.figure(figsize=(10, 6))

            analisis_groupby = location_df.groupby(['Hora', place])[type_votes].sum().unstack()

            for zone in locations:
                plt.plot(analisis_groupby.index, analisis_groupby[zone], marker='o',label=zone)

            plt.xlabel('Hora')
            plt.ylabel(f'Número de {type_votes} {format_votes.lower}')
            plt.title(f'Apuração {type_votes} por Hora em {place}')
            plt.xticks(rotation=70)
            plt.legend()
            plt.tight_layout()

            plt.show()


    else: #if percentage and not votes

        plt.figure(figsize=(10, 6))

        analisis_groupby = location_df.groupby(['Hora', place])[type_votes].mean().unstack()

        for zone in locations:
            plt.plot(analisis_groupby.index, analisis_groupby[zone], marker='o',label=zone)

        plt.xlabel('Hora')
        plt.ylabel(f'Média de {type_votes}')
        plt.title(f'Apuração {type_votes} por Hora em {place}')
        plt.xticks(rotation=70)
        plt.legend()
        plt.tight_layout()

        plt.show()

def parliamentarySeats(df):
    print('Escolha os anos para visualização:')
    years = getUserFiltersLoop(df, df['Anos'].unique().tolist(), 'os anos')

    print('\nEscolha os partidos que deseja ver:')
    parties = getUserFiltersLoop(df, df.columns[2:].tolist(), 'os partidos')

    # DataFrame filter years
    df_filtered = df[df['Anos'].isin(years)]
    df_filtered = df_filtered[['Anos'] + parties]  # select parties

    plt.figure(figsize=(10, 6))

    labels = []
    for party in parties:
        party_color = party_info_df[party_info_df['Partido']==party]['Cor'].iloc[0] #add color by party

        party_name = party_info_df.loc[party_info_df['Partido'] == party, 'Nome'].iloc[0]  #Find party name
        label = f'{party} - {party_name}'
        labels.append(label)

        plt.plot(df_filtered['Anos'], df_filtered[party], marker='o', label=party, color=party_color)

    plt.xlabel('Anos')
    plt.ylabel(f'Número de assentos conquistados')
    plt.title(f'Apuração assentos conquistados por por partido pelo ano')
    plt.xticks(rotation=70)
    plt.legend(title='Legenda', labels=labels)
    plt.tight_layout()

    plt.show()

def votesPartyAll(df):

    print('Escolha os anos para visualização:')
    years = getUserFiltersLoop(df, df['Ano'].unique().tolist(), 'os anos')

    print('\nEscolha os partidos que deseja ver:')
    parties = getUserFiltersLoop(df, df['Partido'].drop_duplicates().tolist(), 'os partidos')

    plt.figure(figsize=(10, 6))

    for party in parties:
        df_party = df[(df['Partido'] == party) & (df['Ano'].isin(years))]
        analisis_groupby = df_party.groupby('Ano')['Total Votos'].sum()

        plt.plot(analisis_groupby.index, analisis_groupby.values, marker='o', label=party)

    plt.xlabel('Anos')
    plt.ylabel('Votos Totais')
    plt.title('Total de Votos por Ano e Partido')
    plt.xticks(rotation=70)
    plt.legend(title='Partido')
    plt.tight_layout()

    plt.ticklabel_format(axis='y', style='plain')

    plt.tight_layout()
    plt.show()

    
    print('\nPara entender um pouco mais sobre os partidos aqui está uma breve descrição sobre eles.\n')
    for party_acronym in parties: #creating legend with parties name
        party_name = party_info_all.loc[party_info_all['Partido'] == party_acronym, 'Nome'].iloc[0]  #Find party name
        party_description = party_info_all.loc[party_info_all['Partido'] == party_acronym, 'Descrição'].iloc[0]  #Find party description
        label = f'{party_acronym} - \033[95m{party_name}\033[0;0m: {party_description}'
        print(f'\n{label}')