import requests as rq
import json
import flet as ft
from time import sleep

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLACK
    link_do_cloud = 'https://painel-animes-default-rtdb.firebaseio.com/lista/.json'
    r = rq.get(link_do_cloud)

    # ................ ESSA E A PAGINA DO ANIME ESCOLHIDO ........................
    def mostrar_informacoes(anime_nome):
        global linha_
        r_ = rq.get(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{anime_nome}/.json')
        
        #pega a imagen e o nome no banco de dados
        img = f"{r_.json()['img']}"
        nome = f"{r_.json()['nome']}"
        
        #pega o episodio e a tempodara no banco de dados
        e = f"{r_.json()['e']}"
        t = f"{r_.json()['t']}"
        
        # cria a img da pagina do anime escolhido
        img_criar = ft.Container(
            content=ft.Image(
                src=f"{img}",
                width=200,
                height=300,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(10),
            )
        )
        
        #adiciona o nome a temporada e o ep do anime escolhido
        texto_temporada_ = ft.Text(f'Temporada: {t}', size=20, color=ft.colors.PINK)
        texto_ep_ = ft.Text(f'EP: {e}', size=20, color=ft.colors.PINK)

        texto_nome = ft.Row([ft.Text(f'{nome}', size=20, weight='bold', color=ft.colors.WHITE,)], wrap=True, alignment='center', width=400)
        texto_temporada = ft.Row([texto_temporada_],alignment='center')
        texto_ep = ft.Row([texto_ep_],alignment='center')
        
        
        #adiciona os elementos anteriormente criados a uma coluna e depois a uma linha
        texto_info = ft.Column([texto_nome, texto_temporada, texto_ep])
        linha_ = ft.Row([img_criar], alignment='center')

        coluna_ = ft.Column([linha_, texto_info])

        # configuraçoes do btn voltar
        def config_voltar(e):
            page.remove(conteiner_)
            conteiner_.controls.clear()
            page.add(btn_add_anime)
            page.add(conteiner_anime)
            page.add(busca)
            page.update()

        #btn deletar
        btn_deletar = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color='#4B0082',
            icon_size=40,
            tooltip='Deletar',
            on_click=lambda e: page.open(dlg_modal_)
        )    

        #opçoes sim ou nao do alerta a ser escolhido ao aprtar o btn_deletar
        def op_sim(e):
            url_deletar = f'https://painel-animes-default-rtdb.firebaseio.com/lista/{anime_nome}/.json'
            rq.delete(url_deletar)
            #depois de deletar volta para a pagina de escolha dos animes
            page.remove(conteiner_)
            #conteiner_.controls.clear()
            #page.add(btn_add_anime)
            #page.add(conteiner_anime)
            #page.add(busca)
            #page.update()
            #feixa o alerta
            #conteiner_anime.clean()
            dlg_modal_.open = False
            dlg_modal_.update()
            #conteiner_.update()
            sleep(1)
            inicio()

            

        def op_nao(e):
            dlg_modal_.open = False
            dlg_modal_.update()
            conteiner_.update()

        # alerta para confirmar que realmente quer apagar usando o btn_deletar
        dlg_modal_ = ft.AlertDialog(
            modal=True,
            title=ft.Text("Por favor, confirme"),
            content=ft.Text("Você realmente deseja excluir todos esses arquivos?"),
            actions=[
                ft.TextButton("Sim", on_click=op_sim),
                ft.TextButton("Nao", on_click=op_nao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            #on_dismiss=lambda e: page.add(
            #    ft.Text("Modal dialog dismissed"),
            #),
        )
            

        # btn voltar
        btn_voltar = ft.IconButton(
            icon=ft.icons.BACKSPACE,
            icon_color='#4B0082',
            icon_size=40,
            tooltip='Voltar',
            on_click=config_voltar,
        )
        
        #adiciona os elementos btn_deletar btn_voltar e linha_ ao conteiner_ que tanbem pode ser chamado de pagina do anime escolhido
        linha_btns = ft.Row([btn_voltar, btn_deletar], alignment='center')
        
        conteiner_.controls.append(linha_btns)
        conteiner_.controls.append(coluna_)
        
        #ativado ao mudar a temporada na pagina do anime escolhido
        def mudar_temporada(e):
            if caixa_temporada.value.isnumeric():
                dados = {'t': f'{caixa_temporada.value}'}
                requisicao = rq.patch(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{anime_nome}/.json', data=json.dumps(dados))
                texto_temporada_.value = f'Temporada: {caixa_temporada.value}'
                caixa_temporada.value = ''
                page.update()
            else:
                caixa_temporada.value = ''
                page.update()
        
        #ativado ao mudar o ep na pagina do anime escolhido       
        def mudar_ep(e):
            if caixa_ep.value.isnumeric():
                dados = {'e': f'{caixa_ep.value}'}
                requisicao = rq.patch(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{anime_nome}/.json', data=json.dumps(dados))
                texto_ep_.value = f'EP: {caixa_ep.value}'
                caixa_ep.value = ''
                page.update()
            else:
                caixa_ep.value = ''
                page.update()
        
        #cria um input na pagina do anime escolhido para fazer a mudanssa deles
        
        caixa_temporada = ft.TextField(label='Mudar Temporada',label_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE) , bgcolor='#4B0082',color=ft.colors.WHITE , on_submit=mudar_temporada)
        caixa_ep = ft.TextField(label='Mudar ep',label_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE) , bgcolor='#4B0082',color=ft.colors.WHITE, on_submit=mudar_ep)

        #adiciona os inputes anteriormente criados a pagina do anime escolhido
        conteiner_.controls.append(caixa_temporada)
        conteiner_.controls.append(caixa_ep)
        
        #ao escolher um dos animes remove a pagina de escolha e a opsao de busca e adiciona a pagina esolhida em ceguida
        page.remove(conteiner_anime)
        page.remove(btn_add_anime)
        page.remove(busca)
        page.add(conteiner_)
        page.update()

    # ................ ESSA E A PAGINA DE ESCOLHA DE ANIMES ..........................
    def inicio():
        link_do_cloud_ = 'https://painel-animes-default-rtdb.firebaseio.com/lista/.json'
        r___ = rq.get(link_do_cloud_)

        global btn_add_anime
        global conteiner_anime
        global conteiner_
        global busca
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        #cria a pagina de escolha de animes e tanbem cria a pagina do anime escolhido
        conteiner_anime = ft.Column(expand=1, spacing=10, scroll=ft.ScrollMode.AUTO, width=1000, controls=[]) 
        conteiner_ = ft.Column(expand=1, spacing=10, scroll=ft.ScrollMode.AUTO, width=1000, controls=[])
        
        #cria uma lista lista_dos_animes e um dicionario animes_data
        lista_dos_animes = []
        animes_data = {}

        #pega todos os animes no banco de dados
        for x in r___.json():
            r_ = rq.get(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{x}/.json')

            #pega a imagen e o nome dos animes no banco de dados
            img = f"{r_.json()['img']}"
            nome = f"{r_.json()['nome']}"
            
            #adiciona o nome dos animes a lista_dos_animes
            lista_dos_animes.append(nome)
            
            #pega o episodio e a tempodara no banco de dados
            e = f"{r_.json()['e']}"
            t = f"{r_.json()['t']}"
            
            #adiciona algun elementos ao dicionario animes_data
            animes_data[nome.lower()] = {
                'img': img,
                'nome': nome,
                'e': e,
                't': t
            }
            
            #cria a imagen da pagina de escolha dos animes
            img_criar = ft.Container(
                content=ft.Image(
                    src=f"{img}",
                    width=250,
                    height=300,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                ),
                alignment=ft.MainAxisAlignment,
                on_click=lambda e, nome=nome: mostrar_informacoes(nome)
            )
            
            #adiciona o nome a temporada e o ep na pagina da escolha dos animes
            texto_nome = ft.Text(f'{nome}', size=25, color=ft.colors.WHITE)
            texto_temporada = ft.Text(f'Temporada: {t}', color=ft.colors.WHITE)
            texto_ep = ft.Text(f'EP: {e}', color=ft.colors.WHITE)
            
            #adiciona os elementos anteriormente criados a uma coluna e depois a uma linha
            texto_info = ft.Column([texto_nome, texto_temporada, texto_ep])
            linha_ = ft.Column([img_criar, texto_info], width=1000)
            page.update()
        
        #crai a funcao de busca dos animes
        def buscar_anime(e):
            termo_busca = busca.value.lower()
            conteiner_anime.controls.clear()
            
            for nome, dados in animes_data.items():
                if termo_busca in nome:
                    img_criar = ft.Container(
                        content=ft.Row([ft.Image(
                            src=f"{dados['img']}",
                            width=200,
                            height=250,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(10),
                        )], alignment='center'),
                        on_click=lambda e, nome=dados['nome']: mostrar_informacoes(nome)
                    )
                    
                    #adiciona o nome a temporada e o ep na pagina da escolha dos animes usando a opsao de busca
                    texto_nome = ft.Row([ft.Text(f'{dados["nome"]}', size=25, color=ft.colors.RED)],wrap=True, alignment='center', width=400)
                    #texto_temporada = ft.Text(f'Temporada: {dados["t"]}')
                    #texto_ep = ft.Text(f'EP: {dados["e"]}')
                    
                    #adiciona os elementos anteriormente criados a uma coluna e depois a uma linha usando a opsao de busca
                    texto_info = ft.Column([texto_nome])
                    linha_ = ft.Column([img_criar, texto_info], width=1000)
                    conteiner_anime.controls.append(linha_)
            
            page.update()
        
        #cria o input de busca na pagina de escolha dos animes
        busca = ft.TextField(label='Busque o anime desejado',label_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE), bgcolor='#4B0082', on_change=buscar_anime)
        
        #cria o btn de add anime
        #global dlg_modal
        campo_1_nome = ft.TextField(label="Nome", label_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE))
        campo_2_img = ft.TextField(label="Img", label_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE))
        
        
        #configura o que acontece ao apertar o btn_add_anime
        texto_de_add_bem_sucedido = ft.Text("Adicionado com sucesso")
        def config_btn_add_anime(e):
            dlg_modal = ft.AlertDialog(
                bgcolor='#4B0082',
                modal=True,
                #title=ft.Text("Por favor confirme", color=ft.colors.RED),
                content=ft.Column([campo_1_nome, campo_2_img]),
                actions=[
                    ft.Row([ft.ElevatedButton("Confirmar", color=ft.colors.BLACK, on_click=lambda e: pegar_valores(page, campo_1_nome, campo_2_img))],alignment='center')
                ],
                actions_alignment=ft.MainAxisAlignment.START,

                #on_dismiss=lambda e: page.add(
                #    texto_de_add_bem_sucedido,
                #),
            )
            campo_1_nome.value = ''
            campo_2_img.value = ''
            campo_1_nome.text_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE)
            campo_2_img.text_style=ft.TextStyle(size=17, weight='bold', italic=False, color=ft.colors.WHITE)

            page.overlay.append(dlg_modal)
            #page.dialog = dlg_modal 
            dlg_modal.open = True
            page.update()
            
            def pegar_valores(page, campo_1_nome, campo_2_img):
                campo_1_nome_valor = campo_1_nome.value
                campo_2_img_valor = campo_2_img.value
                if campo_1_nome_valor == '' or campo_2_img_valor == '':
                    dlg_modal.open = False
                    dlg_modal.update()
                    conteiner_anime.update()
                else:
                    
                    
                    data = {campo_1_nome_valor: {'e': '0', 'img': campo_2_img_valor, 'nome': campo_1_nome_valor, 't': '0'}}
                    rq.patch('https://painel-animes-default-rtdb.firebaseio.com/lista/.json', data=json.dumps(data))
                    
                    #print opcional ......
                    #print(f"Valor do Campo 1: {campo_1_nome_valor}") 
                    #print(f"Valor do Campo 2: {campo_2_img_valor}")
                    #............ 
                    dlg_modal.open = False
                    dlg_modal.disabled
                    dlg_modal.update()
                    conteiner_anime.update()
                    atualizar_apos_add_anime(e, campo_1_nome_valor, campo_2_img_valor)

        #configurasoes do btn_add_anime 
        btn_add_anime = ft.IconButton(
            icon=ft.icons.ADD_LINK,
            icon_color='#4B0082',
            icon_size=40,
            tooltip='Voltar',
            on_click=config_btn_add_anime

        )
        
        def atualizar_apos_add_anime(e, campo_1_nome_valor, campo_2_img_valor):
            #cria a imagen da pagina de escolha dos animes
            img_criar = ft.Container(
                content=ft.Row([ft.Image(
                    src=f"{campo_2_img_valor}",
                    width=200,
                    height=300,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                )], alignment='center'),
                on_click=lambda e, nome=campo_1_nome_valor: mostrar_informacoes(nome)
            )
            
            #adiciona o nome a temporada e o ep na pagina da escolha dos animes usando a opsao de busca
            texto_nome = ft.Row([ft.Text(f'{campo_1_nome_valor}', size=25, color=ft.colors.RED)],wrap=True, alignment='center', width=400)
            #texto_temporada = ft.Text(f'Temporada: {dados["t"]}')
            #texto_ep = ft.Text(f'EP: {dados["e"]}')
                    
            #adiciona os elementos anteriormente criados a uma coluna e depois a uma linha usando a opsao de busca
            texto_info = ft.Column([texto_nome])
            linha_ = ft.Column([img_criar, texto_info], width=1000)
            conteiner_anime.controls.append(linha_)
            page.update()
        
        #adiciona a pagina de escolha de animes e a opsao de busca
        page.add(btn_add_anime)
        page.add(conteiner_anime)
        page.add(busca)
        buscar_anime(None)

        #page.update()
    # inicia o funçao do app
    inicio()
ft.app(target=main)
