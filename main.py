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
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #fim das configuracoes adicionais .............................

    #lista animes ......................................
    img = ft.Image(
        src=f"https://th.bing.com/th?id=OIP.hikJA5g24vjrPsmbiq_M-QHaMF&w=195&h=319&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=ft.border_radius.all(50),
    )
    lista_animes = ft.Row(controls=[])
    lista_animes.controls.append(ft.Container(content=ft.Column(controls=[img, ft.Text(value='ola')], horizontal_alignment='center')))
    lista_animes.controls.append(ft.Container(content=ft.Column(controls=[img, ft.Text(value='ola')], horizontal_alignment='center')))
    

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