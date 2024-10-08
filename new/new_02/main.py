import flet as ft
import requests as rq
from time import sleep
import json


def main(page: ft.Page):
    #configuracos adicionais .....................................
    global user
    global senha
    global btn
    global a
    global lista_animes
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #fim das configuracoes adicionais .............................

    #lista animes ......................................
    lista__ = rq.get(r'https://painel-animes-default-rtdb.firebaseio.com/lista/.json')
    rr = json.loads(lista__.text)
    #tela do flet onde  fica a lista_animes ...................
    lista_animes = ft.Row(width=1100, wrap=True)

    
    #fim da tela .............................

    contagem = (0)

    lista_01 = ft.Row(controls=[],on_scroll=True)
    lista_02 = ft.Row(controls=[],on_scroll=True)
    lista_03 = ft.Row(controls=[],on_scroll=True)
    lista_04 = ft.Row(controls=[],on_scroll=True)
    lista_05 = ()
    lista_06 = ()
    lista_07 = ()
    lista_08 = ()
    lista_09 = ()

    co = 'n'*10
    #co.append('n'*10)
    lista_=[]
    nn = 0
    for item in co:
        nn = nn + 1
        lista_.append(item+str(nn))

    for i in range(50):
        for item in lista_:
            globals()[f'item_{i}'] = item = ft.Row(controls=[],on_scroll=True)

    for item in rr:
        contagem = contagem + 1
        anime_img_=rq.get(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{item}/img/.json')
        anime_nome_=rq.get(f'https://painel-animes-default-rtdb.firebaseio.com/lista/{item}/nome/.json')
        
        #remocao do "" nas strings ........
        remover = '"'

        for i in remover:
            anime_img = anime_img_.text.replace(i, '')
            anime_nome = anime_nome_.text.replace(i, '')
        #fim da remocao ........................
        
        #imagem puxada do firebase ........
        img = ft.Image(
            src=f"{anime_img}",
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(5),
        )
        #fim img ..........................

        #add conteudo a tela ..................
        if contagem < 10:
            lista_animes.controls.append(ft.Container(content=ft.Column(controls=[img, ft.Text(value=f'{anime_nome}')], horizontal_alignment='center')))
        elif contagem > 6:
            pass
        
        # .....................................


    
    
    #lista_animes.controls.append(ft.Container(content=ft.Column(controls=[img, ft.Text(value='ola')], horizontal_alignment='center')))
    #lista_animes.controls.append(ft.Container(content=ft.Column(controls=[img, ft.Text(value='ola')], horizontal_alignment='center')))
    

    #animes ..........................

    def config_animes(e):
        animes.visible=False
        page.add(ft.Row([texto_animes], alignment='center'))
        page.update()

    anime_01 = ft.Image(
        src=f"https://th.bing.com/th/id/OIG2.v47jSGBUIqfHrYqT10H9?w=1024&h=1024&rs=1&pid=ImgDetMain",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
        semantics_label='Animes',
        tooltip='Animes',
        border_radius=ft.border_radius.all(10),
        
    )

    texto_animes = ft.Text(value='Animes')
    animes = ft.Column(controls=[ft.Container(on_click=config_animes, content=ft.Column(controls=[anime_01, texto_animes],horizontal_alignment='center'))])
    # fim configuracoes animes ...........................

    #verificacao de usuarios ao apertar o btn .................
    def check_usuario(e):
        lista_usuario={'willy': '030999', 'luana': '12345'} # usuarios cadastrados
        if user.value in lista_usuario:
            if senha.value == lista_usuario[user.value]:
                #user.visible=False
                #senha.visible=False
                #btn.visible=False
                usuario.visible=False
                #animes.visible=True
                page.add(animes)
                page.update()
            else:
                pass
    #fim da verificacao de usuarios ............................

    #painel usuario ................................
    user = ft.TextField(hint_text='Usuario', on_submit=check_usuario)
    senha = ft.TextField(hint_text='Senha' ,password=True, on_submit=check_usuario)
    btn = ft.ElevatedButton(text='logim', on_click=check_usuario)
    usuario = ft.Column(controls=[
        user,
        senha,
        btn
    ])
    # fim do painel usuario .........................
    #animes.visible=False
    page.add(ft.Row([lista_animes], alignment='center'))





ft.app(main, view=ft.AppView.WEB_BROWSER)
