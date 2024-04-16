import pandas as pd
from functions import *

welcome = '''

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    Bem-vindo ao Programa de \033[1;96mAnálise das Eleições Legislativas de Potrugal\033[0;0m    ║
║                                                                              ║
║    Este programa permite que você \033[4mcrie seus próprios gráficos\033[0m                ║
║    para analisar os resultados das eleições legislativas de Portugal         ║
║                                                                              ║
║    Você pode visualizar diferentes métricas, como o número de assentos       ║
║    ocupados por partido, o número de votos por partido e muito mais.         ║
║                                                                              ║
║    Vamos começar!                                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

'''

main_menu = '''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
                        \033[1;96mAnálise das Eleições\033[0;0m
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

\033[92m M E N U  P R I N C I P A L\033[0;0m
================================================================================
\033[1m┇ 1️⃣ \033[0;0m Apuração dos votos                                                         ┇
\033[1m┇ 2️⃣ \033[0;0m Distribuição geográfica dos votos                                          ┇
\033[1m┇ 3️⃣ \033[0;0m Resultados por partido                                                     ┇
\033[1m┇ 4️⃣ \033[0;0m Assentos ocupados por partidos desde 1975                                  ┇
\033[1m┇ 5️⃣ \033[0;0m Votos por partidos desde 1975                                              ┇
\033[1m┇ 0️⃣ \033[0;93m sair da Análise das Eleições\033[0;0m                                               ┇
================================================================================
Por favor selecione a opção pelo número >>>  '''

good_bye = '''

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   Agradecemos por utilizar a \033[1;96mAnálise das Eleições Legislativas de Potrugal\033[0;0m   ║
║                                                                              ║
║   Esperamos que tenha gostado de fazer sua própria análise das eleições      ║
║                                                                              ║
║   Até uma próxima vez!                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

'''

print(welcome)
while True:
    selected_function = input(main_menu)
    match(selected_function):
        case('1'):
            print(f'\nAqui você pode fazer a análise com base nos horários da apuração dos votos na eleição legislativa de 2019')
            votesPerHour(overall2019_df)
        case('2'):
            print('\nAqui é possível fazer uma verificação dos votos, percentagem de votos por freguesias, concelhos, distritos e regiões na eleição de 2019\n')
            geographicVotes(parishes2019_df)
        case('3'):
            print('\nEsta funcionalidade permite fazer a visualização de votos por partido político')
            votesParty2019(result_parishes2019_df)
        case('4'):
            print('\nNesta funcionalidade você pode ver os assentos ocupados pelos partidos políticos desde 1975 até 2022')
            parliamentarySeats(parliamentary_seats_df)
        case('5'):
            print('\nAqui você poderá consultar o número de votos recebido por cada partido desde 1975 até 2011')
            votesPartyAll(result_parties_df)
        case('0'):
            print(good_bye)
            break
        case(_):
            print(errorCodes('entrada inválida'))