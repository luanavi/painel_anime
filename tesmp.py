lista_animes = ft.ListView()
    img = ft.Image(
        src=f"https://th.bing.com/th?id=OIP.hikJA5g24vjrPsmbiq_M-QHaMF&w=195&h=319&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    i = ft.Container(content=ft.Row(controls=[img, ft.ElevatedButton(text='usuario02')]))
    #lista_animes.controls.append(i)