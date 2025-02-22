from flet import *
import os
import requests
from pytubefix import YouTube


modo='MUSICA'
url_glb='https://youtu.be/L8OesNa-pkA?si=sp6eN2gNl9Na998Q'
thmb_glb='default'
autor_glb='default'
titulo_glb='default'
dur_glb_m='default'

def gui(janela: Page): 
    janela.window.width=500  #tamanho correto -> 500
    janela.window.height=380 #tamanho correto -> 380
    janela.window.resizable=False

    def url_value_func(e):
        if link.controls[0].value=='':
            link.controls[1].controls[1].disabled=True
            janela.update()
        else:
            link.controls[1].controls[1].disabled=False
            janela.update()

    def inicial_func(e):
        janela.window.width=500
        janela.window.height=380
        voltar_hover_func(e)
        janela.clean()
        janela.add(bg)
        janela.update()
        pass

    def voltar_hover_func(e):
        if e.data=='true':
            e.control.width=50
            e.control.content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                        Text(
                                            value='Voltar',
                                            color=colors.BLACK,
                                            size=12,
                                            weight=FontWeight.BOLD
                                        ),
                                        Icon(
                                            name=Icons.ARROW_BACK_ROUNDED,
                                            color=colors.BLACK,
                                            size=22
                                        )
                            ])
            thumbnail.width=260
            e.control.on_click=inicial_func
        else:
            e.control.width=10
            thumbnail.width=300
            e.control.content=Text('')
        janela.update()
        pass

    def titulo_display_hover(e):
        if e.data=='true':
            e.control.width=420
            e.control.content=Text(
                                value=('Titulo do Youtube gerado'),
                                color=colors.BLACK,
                                size=17,
                            )
            e.control.alignment=alignment.center_left
        else:
            e.control.width=130
            e.control.content=Row(alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Titulo'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=19,
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=22,
                                )
                        ])
        janela.update()
        pass

    def autor_display_hover(e):
        if e.data=='true':
            e.control.width=420
            e.control.content=Text(
                                value=('Autor do Youtube gerado'),
                                color=colors.BLACK,
                                size=17,
                            )
            e.control.alignment=alignment.center_left
        else:
            e.control.width=100
            e.control.content=Row(alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Autor'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=19,
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=22,
                                )
                        ])
        janela.update()
        pass

    def inf_display_hover(e):
        pass

    def baixar_thumb_func(e):
        pass

    def thumb_display_func(e):
        if e.data=='true':
            e.control.bgcolor=colors.WHITE38
            e.control.content=Column(
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            value=('Clique para baixar a imagem.'),
                                            color=colors.BLACK,
                                            weight=FontWeight.BOLD,
                                            size=20,
                                        ),
                                        Icon(
                                            name=Icons.FILE_DOWNLOAD_ROUNDED,
                                            size=27,
                                            color=colors.BLACK
                                        )
                        ])
        else:
            e.control.bgcolor=colors.WHITE10
            e.control.content=Text('')
        e.control.update()

    def prosseguir_func(e):
        global modo
        voltar_func(e)
        link.controls[0].value=''
        if modo=='MUSICA' or modo=='VIDEO':
            janela.window.width=800
            janela.window.height=270
            janela.clean()
            janela.update()
            janela.add(page3)
            janela.update
        else:
            janela.window.width=800
            janela.window.height=330
            janela.window.resizable=False
            janela.clean()
            #page4
        pass

    def voltar_func(e):
        page2.controls[0].offset=transform.Offset(0,1)
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=False
        janela.update()     

    def link_func(e):
        global modo
        modo=e.control.data
        page2.controls[0].offset=transform.Offset(0,0)
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=True
        janela.update()       

    header=Container( #Título do aplicativo
                    height=80,
                    width=450,
                    content=Text(
                                value='YOUTUBE VIDEO DOWNLOAD',
                                color=colors.BLACK,
                                size=30
                            ),
                    bgcolor=colors.RED_900,
                    border_radius=border_radius.all(5),
                    padding=5,
                    alignment=alignment.center
    )

    inf_i1=Container(
                    height=50,
                    width=130,
                    content=Row(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Titulo'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=19,
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=22,
                                )
                        ]),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    alignment=alignment.center,
                    on_hover=titulo_display_hover,
                    padding=5,
                    animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
    )

    inf_i2=Container(
                    height=50,
                    width=100,
                    content=Row(alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Autor'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=19,
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=20,
                                )
                        ]),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    alignment=alignment.center_left,
                    on_hover=autor_display_hover,
                    padding=5,
                    animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
    )

    inf_i3=Container(
                    height=50,
                    width=230,
                    content=Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Text(
                                        value=('Informações do vídeo'),
                                        color=colors.BLACK,
                                        weight=FontWeight.BOLD,
                                        size=16,
                                    ),
                                    Icon(
                                        name=Icons.ARROW_FORWARD_ROUNDED,
                                        color=colors.BLACK,
                                        size=20,
                                    )
                        ]),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    alignment=alignment.center_left,
                    on_hover=inf_display_hover,
                    padding=5,
                    animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
    )

    inf_video=Column(
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    controls=[
                    inf_i3,
                    inf_i1,
                    inf_i2
            ])

    voltar=Container(
        width=10,
        height=270,
        content=Text(''),
        bgcolor=colors.WHITE30,
        ink=False,
        border_radius=border_radius.all(5),
        border=border.all(1,colors.BLACK),
        padding=5,
        on_hover=voltar_hover_func,
        animate_size=animation.Animation(600,AnimationCurve.EASE_OUT_SINE),
    )

    thumbnail=Stack(
                    controls=[
                            Image(
                                src=r'https://media.tenor.com/_zWYqfZdneIAAAAM/shocked-face-shocked-meme.gif',
                                width=300,
                                height=270,
                                fit=ImageFit.FILL,
                                border_radius=border_radius.all(5),
                                animate_size=animation.Animation(600,AnimationCurve.EASE_OUT_SINE),
                        ),
                            Container(
                                    width=300,
                                    height=270, 
                                    bgcolor=colors.WHITE10,
                                    alignment=alignment.center,
                                    ink=False,
                                    on_hover=thumb_display_func,
                                    on_click=baixar_thumb_func,
                                    animate_size=animation.Animation(600,AnimationCurve.EASE_OUT_SINE),
                        ),
        ])

    i1=Row( #Linha baixar vídeo
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(
                height=60,
                width=420,
                content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        spacing=65,
                        controls=[
                            Text(
                                value='1 -> BAIXAR VÍDEOS NO YOUTUBE.',
                                size=16,
                                color=colors.BLACK,
                            ),
                            IconButton(
                                icon=Icons.ARROW_FORWARD_ROUNDED,
                                icon_color=colors.BLACK,
                                icon_size=20,
                                on_click=link_func,
                                data='VIDEO',
                                disabled=False,
                            )  
                        ]),
                bgcolor=colors.WHITE54,
                border_radius=border_radius.all(5),
                padding=5,
                alignment=alignment.center,
            ),
    ])

    i2=Row( #Linha baixar música 
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(
                height=60,
                width=420,
                content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        spacing=62,
                        controls=[
                            Text(
                                value='2 -> BAIXAR MÚSICA NO YOUTUBE.',
                                size=16,
                                color=colors.BLACK,
                            ),
                            IconButton(
                                icon=Icons.ARROW_FORWARD_ROUNDED,
                                icon_color=colors.BLACK,
                                on_click=link_func,
                                data='MUSICA',
                                icon_size=20
                            )
                    ]),
            bgcolor=colors.WHITE54,
            border_radius=border_radius.all(5),
            padding=5,
            alignment=alignment.center
        ),
    ])

    i3=Row( #Linha baixar playlist 
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Container(
                height=60,
                width=420,
                content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        spacing=55,
                        controls=[
                            Text(
                                value='3 -> BAIXAR PLAYLIST NO YOUTUBE.',
                                size=16,
                                color=colors.BLACK,
                            ),
                            IconButton(
                                icon=Icons.ARROW_FORWARD_ROUNDED,
                                icon_color=colors.BLACK,
                                on_click=link_func,
                                data='PLAYLIST',
                                icon_size=20
                            )
                    ]),
            bgcolor=colors.WHITE54,
            border_radius=border_radius.all(5),
            padding=5,
            alignment=alignment.center
        ),
    ])

    itens=Column( #Alinhas linhas
                controls=[
                i1,
                i2,
                i3
    ])

    link=Column( #Layout de tela de onde será inserido o URL
                alignment=MainAxisAlignment.END,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        label='URL',
                        hint_text='https://www.youtube.com/',
                        hint_style=TextStyle(
                            color=colors.BLACK26,
                            
                        ),
                        color=colors.BLACK,
                        border_radius=10,
                        border_color=colors.BLACK54,
                        content_padding=padding.all(5),
                        filled=True,
                        fill_color=colors.WHITE24,
                        focused_border_color=colors.BLACK54,
                        focused_border_width=1,
                        label_style=TextStyle(
                            color=colors.RED_900
                        ),
                        on_change=url_value_func,
                    ),
                    Row(alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                        ElevatedButton(
                            text='VOLTAR',
                            icon=Icons.ARROW_BACK_ROUNDED,
                            icon_color=colors.BLACK,
                            style=ButtonStyle(
                                icon_size=20,
                                shape=RoundedRectangleBorder(radius=10),
                                bgcolor=colors.RED_900,
                                color=colors.BLACK
                            ),
                            on_click=voltar_func,
                        ),
                        ElevatedButton(
                            content=Row(
                                    controls=[
                                        Text(
                                            value='PROSSEGUIR',
                                            size=14,
                                            color=colors.BLACK),
                                        Icon(Icons.ARROW_FORWARD_ROUNDED,
                                            color=colors.BLACK,
                                            size=20)
                                ]),
                                style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=10),
                                        bgcolor=colors.RED_900,
                                    ),
                                on_click=prosseguir_func,
                                disabled=True
                        ),
                    ])

    ])

    bg_link=Container( #bg link layout
                    width=janela.window.width,
                    height=janela.window.height,
                    content=Stack([
                                    link
                                ]),
                    bgcolor=colors.WHITE38,
                    border_radius=border_radius.all(5),
                    padding=5
    )

    page1=Column( #Página inicial
                height=900,
                width=janela.window.width,
                spacing=10,
                alignment=MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    header,
                    itens
            ])

    page2=Column( #Página de URL
                height=janela.window.height,
                width=janela.window.width,
                alignment=MainAxisAlignment.END,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        offset=transform.Offset(0,1),
                        width=janela.window.width,
                        height=120,
                        content=Stack([
                                bg_link
                            ]),
                        bgcolor=colors.GREY_900,
                        border_radius=border_radius.all(5),
                        padding=5,
                        animate_offset=Animation(500, AnimationCurve.EASE_IN_OUT_SINE)
                    )
                ]
            )

    page3=Container(
                    height=270-55,
                    width=800,
                    content=Row(
                                alignment=MainAxisAlignment.START,
                                controls=[
                                        Row(
                                            spacing=3,
                                            controls=[
                                                    voltar,
                                                    thumbnail,
                                        ]),    
                                        inf_video
                        ]),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    padding=5,
    )

    bg=Container( #bg inicial do aplicativo
                height=janela.window.height-55,
                width=janela.window.width,
                content=Stack([
                    page1,
                    page2
                ]), 
                bgcolor=colors.WHITE24,
                border_radius=border_radius.all(5),
    )

    janela.add(bg)
app(gui) 