import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## overall2019
overall2019_df = pd.read_csv('./modificatedData/overall2019.csv', sep=',')
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
            input_value = int(input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m"))

            if input_value != 0 and input_value != index+2 and input_value != index+3: #when 0 abort all, i+2 select all, i+3 finish

                while input_value < 0 or input_value-1 > len(toFilter):
                    print(errorCodes("Entrada incorreta"))
                    input_value = int(input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m")) #request new input

                selection = toFilter[input_value-1] #the selecion is the input_value on index toFilter

                if selection not in theSelectedFilters: #if selection wasnt select after
                    theSelectedFilters.append(selection)
                else: #remove the term if was select after
                    theSelectedFilters.remove(selection)
                viewDataFrame(df[theSelectedFilters].drop_duplicates())

            elif input_value == index+2: #selected all filters
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
    for index, value in enumerate(toFilter):
        print(f"\33[1m{index+1} \033[0;0m{value}")
    input_value = int(input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m"))

    while input_value <1 and input_value > len(toFilter)-1:
        print(errorCodes("Entrada incorreta"))
        input_value = int(input(f"\33[0;0mEscolha um número para selecionar {messange}: \33[0;0m\n"))
    
    theSelectedFilters = toFilter[input_value-1]
       
    return theSelectedFilters #return de array with all selected filters

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

#axis categorical variable, axis Y numeric variable
def barChart(df, axisX, axisY):

    if 'data' in df.columns.to_list(): #if the dataframe has a column called 'data'
        df['data'] = pd.to_datetime(df['data'])
        
        df['day'] = df['date'].dt.to_period('D')
        df['month'] = df['date'].dt.to_period('M')
        df['year'] = df['date'].dt.to_period('Y')

    if 'Distrito' in df.columns.to_list() and 'Território Nacional' in df['Distrito'].to_list(): #if the dataFrame has a collumns called 'territoryFullName' and if this column has 'National Territory'
        df = df.drop(df[df['Distrito'] == 'Território Nacional'].index)

    print(f'AxisX {df[axisX]}\nAxisY {df[axisY]}')
    plt.figure(figsize=(10, 6))
    plt.bar(df[axisX], df[axisY])
    plt.title(f'Número de {axisY} por {axisX}')
    plt.xlabel(axisX)
    plt.ylabel(axisY)

    plt.xticks(rotation=70)  # Rotaciona os rótulos do eixo x para facilitar a leitura
    # Formatando a escala do eixo y para não usar notação científica
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(axis='y')  # Adiciona grades apenas no eixo y
    plt.tight_layout()  # Ajusta automaticamente os espaços para evitar sobreposição de elementos
    plt.show()

def barGraphic(df, columnX, axisX, axisY):

    if 'data' in df.columns.to_list(): #if the dataframe has a column called 'data'
        df['data'] = pd.to_datetime(df['data'])
        
        df['day'] = df['date'].dt.to_period('D')
        df['month'] = df['date'].dt.to_period('M')
        df['year'] = df['date'].dt.to_period('Y')

    toX = pd.DataFrame()
    for element in axisX:
        toX = pd.concat([toX, (df[df[columnX]==element])], axis=0)
    
    plt.figure(figsize=(10, 6))
    plt.bar(toX[columnX], toX[axisY])
    plt.title(f'Número de {axisY} por {columnX}')
    plt.xlabel(columnX)
    plt.ylabel(axisY)

    plt.xticks(rotation=70)  # Rotaciona os rótulos do eixo x para facilitar a leitura
    # Formatando a escala do eixo y para não usar notação científica
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(axis='y')  # Adiciona grades apenas no eixo y
    plt.tight_layout()  # Ajusta automaticamente os espaços para evitar sobreposição de elementos
    plt.show()


def votesParty2019(df): 
    parties = getUserFiltersLoop(result_parishes2019_df, result_parishes2019_df['Partido'].drop_duplicates(), 'os partidos') # list with selected parties
    print(f'\nAgora que já escolheu os partidos basta escolher a localidade que deseja visualizar\n')

    place = userFilter(['Freguesia', 'Concelho', 'Distrito', 'Região'], 'a localidade')
    locations = locationFilter(df, place) # list with selected localities

    print(f'\nQue dados deseja visualizar?\n')
    type_votes = userFilter(['Percentagem','Percentagem de Votos Válidos','Votos'], 'os dados de visualização')

    location_df = pd.DataFrame()
    for locality in locations:
        for party in parties:
            location_df = pd.concat([location_df, df[(df[place]==locality) & (df['Partido']==party)]], axis=0) #filtered dataFrame

    labels = []
    for party_acronym in parties:
        party_name = party_info_df.loc[party_info_df['Partido'] == party_acronym, 'Nome'].iloc[0]  #Find party name
        label = f'{party_acronym} - {party_name}'
        labels.append(label)

    if type_votes == 'Votos':    
        #groupby([columns name to group])[element to view].sum/mean()
        analisis_groupby = location_df.groupby([place, 'Partido'])[type_votes].sum().unstack()

        plt.figure(figsize=(10, 6))
        bar_width = 0.1
        position = bar_width/2

        for i, party in enumerate(parties):
            position_element = [x + i * bar_width - position for x in range(len(analisis_groupby.index))]
            plt.bar(position_element, analisis_groupby[party], width=bar_width, label=party)

        plt.xlabel(place)
        plt.ylabel(f'Número de {type_votes}')
        plt.title(f'{type_votes} por Partido em {place}')
        plt.xticks(range(len(analisis_groupby.index)), analisis_groupby.index, rotation=70)
        plt.legend(title='Legenda', labels=labels)
        plt.tight_layout()

        plt.show()
    
    else:
        #groupby([columns name to group])[element to view].sum/mean()
        analisis_groupby = location_df.groupby([place, 'Partido'])[type_votes].mean().unstack()

        plt.figure(figsize=(10, 6))
        bar_width = 0.1
        position = bar_width/2

        for i, party in enumerate(parties):
            position_element = [x + i * bar_width - position for x in range(len(analisis_groupby.index))]
            plt.bar(position_element, analisis_groupby[party], width=bar_width, label=party)

        plt.xlabel(place)
        plt.ylabel(f'Média da {type_votes}')
        plt.title(f'{type_votes} por Partido em {place}')
        plt.xticks(range(len(analisis_groupby.index)), analisis_groupby.index, rotation=70)

        plt.legend(title='Legenda', labels=[f'{party_acronym} - {party_name}' for party_acronym, party_name in zip(parties, party_info_df['Nome'])])
        plt.tight_layout()

        plt.show()

    return location_df

votesParty2019(result_parishes2019_df)

#barGraphic(result_parishes2019_df, 'Partido', ['PS', 'CH'], 'Votos')

#barChart(overall2019_df, axisX='Distrito', axisY='Votos Nulos')
#user_filters = getUserFiltersLoop(overall2019_df, overall2019_df.columns.tolist())