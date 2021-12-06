import PySimpleGUI as sg
import pandas as pd

from Modules import Product, Refeicao, metabolismo_basal, CalculateCal

database_df = pd.read_csv('ProductsDataBase.csv')
database_df = database_df.drop_duplicates(subset=['Name'])
database_df = database_df.iloc[:, 1:4]
refeicao = Refeicao()
roman = 'Times New Roman'
sg.theme('GreenMono')
part1 = True
infos = [[sg.Text('Olá!', font=(roman, 15))],
         [sg.Text('Entre suas informaçoes para prosseguir', font=(roman, 15))],
         [sg.Text('Nome:'), sg.InputText(key='Nome'), sg.Text('Sexo:'),
          sg.Radio('Homem', group_id='Sexo', key='Homem', enable_events=True,
                   default=False,
                   disabled=False),
          sg.Radio('Mulher', group_id='Sexo', key='Mulher', enable_events=True,
                   default=False,
                   disabled=False)],
         [sg.Text('Peso:'), sg.InputText(key='Peso'), sg.Text(
             'Altura:'), sg.InputText(key='Altura')],
         [sg.Text('Idade '), sg.InputText(key='Idade')],
         [sg.Button('Entrar', key='__JOIN__'), sg.Button('Cancelar')]]
window = sg.Window('Perfil', infos, grab_anywhere=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        exit()
    elif event == '__JOIN__':
        lista_valores_1 = {'Peso': float(str(values['Peso']).replace('kg', '')),
                           'Altura': float(str(values['Altura']).replace('m', '')),
                           'Idade': float(values['Idade']),
                           'Genero': 'Homem' if values['Homem'] else 'Mulher'}
        values['Peso'] = str(values['Peso']).replace('kg', '')
        values['Altura'] = str(values['Altura']).replace('m', '')
        metal = metabolismo_basal(float(values['Peso']), float(values['Altura']), float(values['Idade']), 'm',
                                  'Homem' if values['Homem'] else 'Mulher')
        window.close()
        break


def find_content(kword: str, data=database_df) -> dict:
    list_results, list_visualize = [], []
    for key in data['Name']:
        if kword.lower() in key.lower():
            list_results.append(f'|{len(list_results) + 1} | {key}')
            list_visualize.append(key)
    return {'Visualize': list_results, 'Results': list_visualize}


pesquisar_alimento = [[sg.Text('Inserir alimentos de sua dieta', font=(roman, 15))],
                      [sg.InputText('Nome do Alimento'), sg.Button(
                          'Pesquisar', key='__SEARCH__')],
                      [sg.Button('Cancelar')]]
window = sg.Window('Alimentos', pesquisar_alimento, grab_anywhere=True)
resultado_alimentos = [sg.Text()]
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':  # if user closes window or clicks cancel
        exit()
    if event == '__SEARCH__':
        print(values[0])
        search_results = find_content(values[0])['Visualize']
        search_brutal = find_content(values[0])['Results']
        resultado_alimentos = [[sg.Text(f'Resultados da pesquisa sobre {values[0]}')],
                               [sg.Text('Coloque o numero que corresponda o seu alimento'), sg.InputText(
                                   '1')],
                               [sg.Listbox(search_results, size=(50, 3))],
                               [sg.Button('Próximo', key='Proximo'), sg.Button('Cancelar')]]
        window.close()
        break
window = sg.Window('Escolha', resultado_alimentos, grab_anywhere=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':  # if user closes window or clicks cancel
        part1 = False
        window.close()
        break

    elif event == 'Proximo':
        resultado = database_df[database_df['Name']
                                == search_brutal[int(values[0]) - 1]]
        resultado = resultado.to_dict('r')
        calories = resultado[0]['Calories']
        type_ = resultado[0]['Type']
        name = resultado[0]['Name']
        p1 = Product(calories=float(calories), name=name, tipo=type_)
        escolha_produto = [[sg.Text(p1.name, font=(roman, 15))],
                           [sg.Text('Calorias:'), sg.Text(p1.cal_up, key='__CAL__'),
                            sg.InputText('1', key='__QUAN__'), sg.Button(
                               'Recarregar', key='Refresh'),
                            sg.Text(f'Divididas por: {p1.tipo}')],
                           [sg.Button('Adicionar'), sg.Button('Cancelar')]]
        window.close()
        break
if part1:
    window = sg.Window('Produto', escolha_produto, grab_anywhere=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':  # if user closes window or clicks cancel
            window.close()
            break
        elif event == 'Refresh':
            p1.assign(float(values['__QUAN__']))
            window.Element('__CAL__').update(p1.cal_up)
        elif event == 'Adicionar':
            p1.assign(float(values['__QUAN__']))
            refeicao.insert(p1)
            window.close()
            break
menu_produtos = [[sg.Text('Seus alimentos', font=('', 15)), sg.Text('Calorias total: '),
                  sg.Text(refeicao.total_calories(), key='__CALTOTAL__')],
                 [sg.Listbox(str(refeicao).split(' $! '), size=(70, 15), background_color='lightgray',
                             key='__LISTA__'),
                  sg.Button('Remover alimento', key='__RM__', size=(6, 2)), sg.InputText('', size=(10, 2))],
                 [sg.Button('Pesquisar alimento', key='__ADD__'),
                  sg.InputText('Alimento',
                               key='__SEARCH__', size=(30, 2)),
                  sg.Button('Ir Produto', key='__GO__'), sg.InputText('1', key='__NUMPRODUTO__', size=(4, 2))],
                 [sg.Listbox(['Precione pesquisar alimento'],
                             size=(80, 2), key="__PROCS__")],
                 [sg.Text(f'Selecione um Alimento', key='__NOMP1__'),
                  sg.InputText('0', key='__NOMIN__', size=(4, 2)),
                  sg.Button('Recarregar', key='__FRESH__'), sg.Button('Adicionar produto', key='__ADDP1__')],
                 [sg.Button('Cancelar'), sg.Button('Próximo', key='__NEXT__')]]
window = sg.Window('Lista Produtos', menu_produtos, grab_anywhere=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        exit()
    if event == '__RM__':
        refeicao.remove(int(values[0]) - 1)
        window.Element('__LISTA__').update(str(refeicao).split(' $! '))
        window.Element('__CALTOTAL__').update(refeicao.total_calories())
    if event == '__ADD__':
        search_results = find_content(values['__SEARCH__'])['Visualize']
        search_brutal = find_content(values['__SEARCH__'])['Results']
        window.Element('__PROCS__').update(search_results)
    if event == '__GO__':
        resultado = database_df[database_df['Name'] ==
                                search_brutal[int(values['__NUMPRODUTO__']) - 1]]
        resultado = resultado.to_dict('r')
        calories = resultado[0]['Calories']
        type_ = resultado[0]['Type']
        name = resultado[0]['Name']
        p1 = Product(calories=float(calories), name=name, tipo=type_)
        window.Element('__NOMP1__').update(
            f'{p1.name} - {p1.cal_up} Calorias - Dividida por: {p1.tipo}')
        window.Element('__NOMIN__').update('1')
    if event == '__FRESH__':
        p1.assign(float(values['__NOMIN__']))
        window.Element('__NOMP1__').update(
            f'{p1.name} - {p1.cal_up} Calorias - Dividida por: {p1.tipo}')
    if event == '__ADDP1__':
        p1.assign(float(values['__NOMIN__']))
        refeicao.insert(p1)
        window.Element('__LISTA__').update(str(refeicao).split(' $! '))
        window.Element('__CALTOTAL__').update(refeicao.total_calories())
    if event == '__NEXT__':
        #         lista_valores_1 = {'Peso' : float(str(values['Peso']).replace('kg', '')),
        #                            'Altura' : float(str(values['Altura']).replace('m', '')),
        #                            'Idade' : float(values['Idade']),
        #                            'Genero' : 'Homem' if values['Homem'] else 'Mulher'}
        diario = CalculateCal.day(peso=lista_valores_1['Peso'], metabolismobasal=metal,
                                  calorias_diarias=refeicao.total_calories())
        #     def monthly(peso, calorias_diario, altura, idade, tipo_altura, genero, vezes:int):
        print(diario)
        print(CalculateCal.monthly(lista_valores_1['Peso'], refeicao.total_calories(), lista_valores_1['Altura'],
                                   lista_valores_1['Idade'], 'm', lista_valores_1['Genero'], 30))
        print(lista_valores_1, refeicao.total_calories())


        def facilacesso(dias):
            mensal = CalculateCal.monthly(lista_valores_1['Peso'], refeicao.total_calories(),
                                          lista_valores_1['Altura'],
                                          lista_valores_1['Idade'], 'm', lista_valores_1['Genero'], dias)
            return round(mensal, 2)


        lista_resultados = [
            [sg.Text('Uma análise de seu peso se voce seguir a dieta (sem fazer exercicios fisicos)',
                     font=('', 13))],
            [sg.Text(
                f'O seu peso atualmente é de: {lista_valores_1["Peso"]}kg')],
            [sg.Text(f'Seu metabolismo basal é de: {round(metal, 2)} calorias diarias')],
            [sg.Text(f'Seu peso em um dia de dieta: {facilacesso(1)}kg')],
            [sg.Text(f'Seu peso em uma semana de dieta: {facilacesso(7)}kg')],
            [sg.Text(f'Seu peso em 1 mes de dieta: {facilacesso(30)}kg')],
            [sg.Text(f'Seu peso em 1 ano de dieta: {facilacesso(360)}kg')],
            [sg.InputText('Coloque uma data customizada em dias aqui', key='_CUSTOM_'),
             sg.Button('OK', key='_GO_'), sg.Text('', key='_TEXT_')],
            [sg.Button('Cancelar')]]

        window.close()
        break

window = sg.Window('Resultados', lista_resultados, grab_anywhere=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':  # if user closes window or clicks cancel
        exit()
    if event == '_GO_':
        window.Element('_TEXT_').update(
            f'Seu peso {values["_CUSTOM_"]} dias de dieta: {facilacesso(int(values["_CUSTOM_"]))}kg')
