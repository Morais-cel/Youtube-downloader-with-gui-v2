from flet import *
import pytubefix as pt
import requests
import os
import moviepy as mp
import shutil
import subprocess

modo=''
url=''
py_get_inf=['title','author','thumb_link','description','publish_date','views','resoluções do vídeo']
res_qual=''

def res_qualidade_video_func(e): #Função que define se a resolução de 1080p está disponível no vídeo
        resolucoes=py_get_inf[6]
        if '1080p' in resolucoes:
            return '1080p'
        else:
            return '720p'


def baixar_thumb_func(e): #Função que cria, caso necessário, uma pasta definida como Thumb e salva a imagem do vídeo escolhido
    thumb_bin= requests.get(py_get_inf[2])
    if not os.path.exists(r'C:\Users\pedro\Desktop\Youtube Download\Thumb'):
        os.makedirs(r'C:\Users\pedro\Desktop\Youtube Download\Thumb')
        pass
    with open(fr'C:\Users\pedro\Desktop\Youtube Download\Thumb\{py_get_inf[1]}_TMB.png',"wb") as im:
        im.write(thumb_bin.content)
        pass
    pass

def ajustes_data_lanc_func(e): #Função que define a formatação correta da data de publicação do vídeo
    data_ajustada=dict()
    meses=('jan.','fev.','mar.','abr.','mai.','jun.','jul.','ago.','set.','out.','nov.','dez.')
    data=str(py_get_inf[4]).split()
    data.pop()
    data=data[0].split('-')
    data_ajustada['dia']=int(data[2])
    data_ajustada['mes']=meses[int(data[1])-1]
    data_ajustada['ano']=int(data[0])
    return data_ajustada

def musica_download_m4a(e): #Função que baixa somente o aúdio do vídeo selecionado, fomato -> M4A
    yt=pt.YouTube(url)
    pasta_principal=r'C:\Users\pedro\Desktop\Youtube Download\Música\M4A' #Local onde o arquivo o arquivo princiap será salvo
    audio=yt.streams.filter(only_audio=True).first()
    if not os.path.exists(pasta_principal): #Criação de pasta MP4 caso não exista
        os.makedirs(pasta_principal)
        pass
    audio.download(output_path=pasta_principal) #Download música 
    pass

def musica_download_mp3(e): #Função que baixa somente o aúdio do vídeo selecionado, fomato -> MP3
    yt=pt.YouTube(url)
    pasta_principal=r'C:\Users\pedro\Desktop\Youtube Download\Música\MP3' #Local onde o arquvio mp3 será salvo
    pasta_auxiliar=r'C:\Users\pedro\Desktop\Youtube Download\Música\MP4_AUX' #Pasta m4a criada para auxiliar durante a conversão das músicas
    audio=yt.streams.filter(file_extension='mp4').first()
    if not os.path.exists(pasta_auxiliar): #Criação de pasta MP4_AUX caso não exista
        os.makedirs(pasta_auxiliar)
        pass
    if not os.path.exists(pasta_principal): #Criação de pasta MP3 caso não exista
        os.makedirs(pasta_principal)
        pass
    audio.download(output_path=pasta_auxiliar) #Download música 
    for na1,na2, arquivos in os.walk(pasta_auxiliar): #Mapeamento da pasta MP4_AUX
        for video in arquivos: #Análise dos arquivos existentes na pasta MP4_AUX
            print(arquivos)
            conversao=mp.VideoFileClip(os.path.join(pasta_auxiliar,video))
            nome=str(video).replace('mp4','mp3')
            conversao.audio.write_audiofile(os.path.join(pasta_principal,nome))
            conversao.close()
    shutil.rmtree(pasta_auxiliar) #Excluir pasta temporária MP4_AUX
    pass

def video_download_fast(e): #Função que baixa o vídeo escolhido resolução 360p
    yt=pt.YouTube(url)
    pasta_principal=r'C:\Users\pedro\Desktop\Youtube Download\Video\Download rápido (360p)' #Local onde o arquivo o arquivo princiap será salvo
    video=yt.streams.filter(res='360p',file_extension='mp4').first() #Definir como será o formato do vídeo
    if not os.path.exists(pasta_principal): #Criar diretório Download rápido (360p) caso ele não exista
        os.makedirs(pasta_principal)
        pass
    video.download(output_path=pasta_principal) #Download vídeo
    pass

def video_download_quality(e):
    video_local=r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade\Video' #Local onde o vídeo sem audio será salvo
    audio_local=r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade\Audio' #Local onde o audio do vídeo será salvo
    pasta_principal=r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade'
    yt=pt.YouTube(url)
    video=yt.streams.filter(file_extension='mp4',res=f'{res_qual}').first()
    audio=yt.streams.filter(file_extension='mp4').first()
    if not os.path.exists(video_local): #Criar pasta do local do vídeo(sem audio), caso não exista
        os.makedirs(video_local)
    if not os.path.exists(audio_local): #Criar pasta do local do audio do vídeo, caso não exista
        os.makedirs(audio_local)
    video.download(output_path=video_local)
    audio.download(output_path=audio_local)
    for i1, i2, arquivos in os.walk(audio_local):
            for arq_atual in arquivos:
                video_path=os.path.join(audio_local,arq_atual)
                audio_path=os.path.join(audio_local,str(arq_atual).replace('mp4','mp3')) 
                convert_mp4_mp3(video_path,audio_path)
    video_arquivo=os.path.join(video_local,f'{yt.title}.mp4')
    audio_arquivo=os.path.join(audio_local,f'{yt.title}.mp3')
    output_arquivo=os.path.join(pasta_principal,f'{yt.title}.mp4')
    video_maker_func(video_arquivo,audio_arquivo,output_arquivo)
    shutil.rmtree(video_local)
    shutil.rmtree(audio_local)

def convert_mp4_mp3(video_path,audio_path):
    clip=mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    os.remove(video_path)

def video_maker_func(video_local,audio_local,output_local):
    command=[
        'ffmpeg',
        '-i', video_local,
        '-i', audio_local,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_local
    ]
    subprocess.run(command)

async def programa(janela: Page): 

    janela.window.width=500  #tamanho correto -> 500
    janela.window.height=380 #tamanho correto -> 380
    janela.window.resizable=False

    #-------------------------------------------------------------------------
    #Funções relacionadas ao pytube

    def pytube_inf(e): #Função responsável por obter as informações do vídeo
        resoluções=dict()
        yt=pt.YouTube(url)
        stream=yt.streams.filter(adaptive=True,file_extension='mp4')
        pt_title=yt.title
        pt_author=yt.author
        pt_thumb_link=yt.thumbnail_url
        pt_description=yt.description
        pt_publish_date=yt.publish_date
        pt_views=yt.views
        for res in stream:
            if res.resolution:
                resoluções[f'{res.resolution}']=True
            
        return [pt_title,pt_author,pt_thumb_link,pt_description,pt_publish_date,pt_views,resoluções]

    #-------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 1
    def esc_colum_dowl_func_page3(e): #Função que define a coluna que será colocada no quadro a depender da escolha na página 1
        global modo
        if modo=='MUSICA':
            return botoes_download_musica
        else:
            return botoes_download_video

    def link_func(e): #Função responsável por atribuir o modo para a variável global modo
        global modo
        modo=e.control.data
        pass

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 2

    def bot_url_func(e): #Função responsável por realizar o processo de bloquear o funcionamento dos botões presentes na página 1 (página inicial)
        page2.controls[0].offset=transform.Offset(0,0)
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=True
        janela.update()    
        pass

    def config_urlpg_func(e): #Função que configura o funcionamento do botão de chamada da página 2
        link_func(e)
        bot_url_func(e)
        pass

    def prosseguir_func(e): #Função responsável por abrir a página 3 (página de informações da URL)
        voltar_func(e) #Redefine o estado das páginas 1 e 2 para o inicial, evitando problemas futuros
        global modo
        global url
        global py_get_inf
        global res_qual
        url=link.controls[0].value
        py_get_inf=pytube_inf(e) #Processo para se obter as informações do vídeo presente na URL informada
        res_qual=res_qualidade_video_func(e)
        thumbnail.controls[0].src=py_get_inf[2] #Atualização da imagem da thumbnail
        botoes_download_video.controls[1].content.value=f'Qualidade ({res_qual})'
        link.controls[0].value='' #Resetando o valor do textfield do link para evitar futuros problemas
        if modo=='MUSICA' or modo=='VIDEO':
            janela.window.width=800
            janela.window.height=270
            janela.clean()
            janela.update()
            janela.add(page3)
        else:
            janela.window.width=450
            janela.window.height=500
            janela.window.resizable=False
            janela.clean()
            #page4
        pass

    def url_value_func(e): #Função que trava o botão prosseguir na página dois quando o textfield estiver vazio
        if link.controls[0].value=='':
            link.controls[1].controls[1].disabled=True
            janela.update()
        else:
            link.controls[1].controls[1].disabled=False
            janela.update()

    def voltar_func(e): #Função responsável por realizar o processo de fechar a segunda página (página da URL) e liberar o funcionamento dos botões presentes na página 1 (página inicial)
        page2.controls[0].offset=transform.Offset(0,1)
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=False
        janela.update()     

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 3

    def autor_display_hover(e): #Função que define o processo de hover para o container com informações do autor do vídeo
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=417
            e.control.content=Text(
                                value=(py_get_inf[1]),
                                color=colors.BLACK,
                                size=17,
                                max_lines=1,
                                weight=FontWeight.BOLD,
                            )
            e.control.alignment=alignment.center_left
        else: #Mouse FORA do container
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

    def download_hover_func(e): #Função responsável pelo funcionamento pela barra de download na página 3
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=130
            e.control.border_radius=border_radius.all(5)
            e.control.content=Column(
                                    alignment=MainAxisAlignment.START,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Container( #Header
                                            width=120,
                                            height=40,
                                            content=Text(
                                                        value='DOWNLOAD',
                                                        color=colors.BLACK,
                                                        weight=FontWeight.BOLD,
                                                        size=15),
                                            bgcolor=colors.RED_900,
                                            border_radius=border_radius.all(5),
                                            padding=5,
                                            alignment=alignment.center
                                        ),
                                        Icon( #Icone indicador
                                            name=Icons.ARROW_DOWNWARD_ROUNDED,
                                            color=colors.BLACK
                                        ),
                                        esc_colum_dowl_func_page3(e) #Função irá definir quais funções serão chamados para a coluna a depender de qual opção de download foi escolhida na página 1
                                ])
        else: #Mouse FORA do container
            e.control.width=10
            e.control.border_radius=border_radius.all(3)
            e.control.content=Text('')
            pass
        janela.update()
        pass

    def inf_display_hover(e):
        data=dict()
        data=ajustes_data_lanc_func(e) #Chama o dicionário que informa a data de publicação do vídeo
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=457
            e.control.height=205
            e.control.content=Column( #Desenvolvimento de coluna para disposição de informações 
                                    spacing=6,
                                    controls=[
                                            Row( #Row que irá conter informações de visuações e de data de publicação
                                                controls=[
                                                        Container( #Bg da Row
                                                            width=446,
                                                            height=30,
                                                            content=Row( #Row para introduzir os valores
                                                                        spacing=3,
                                                                        controls=[
                                                                                Container( #Container que contém o valor das visualizações do vídeo
                                                                                    content=Row(
                                                                                                alignment=MainAxisAlignment.START,
                                                                                                spacing=-6,
                                                                                                controls=[
                                                                                                        Container(
                                                                                                                content=Row( #Row preparada para futora legenda
                                                                                                                            vertical_alignment=CrossAxisAlignment.END,
                                                                                                                            alignment=MainAxisAlignment.START,
                                                                                                                            spacing=-2,
                                                                                                                            controls=[
                                                                                                                                    
                                                                                                                            ]
                                                                                                                        ),
                                                                                                        ),
                                                                                                        Text( #Valor de visualizações do vídeo
                                                                                                            value=f' {py_get_inf[5]:,} visualizações |'.replace(',','.'),
                                                                                                            color=colors.BLACK,
                                                                                                            size=15,
                                                                                                            weight=FontWeight.BOLD,
                                                                                                        )
                                                                                            ])
                                                                                ),
                                                                                Container( #Container que contém o valor da data de publicação do vídeo
                                                                                    content=Row(
                                                                                                alignment=MainAxisAlignment.START,
                                                                                                spacing=-3,
                                                                                                controls=[
                                                                                                        Container(
                                                                                                                content=Row( #Row preparada para futora legenda
                                                                                                                            vertical_alignment=CrossAxisAlignment.END,
                                                                                                                            alignment=MainAxisAlignment.START,
                                                                                                                            spacing=-1,
                                                                                                                            controls=[
                                                                                                                                    
                                                                                                                            ]
                                                                                                                        )
                                                                                                        ),
                                                                                                        Text( #Data de publicação do vídeo
                                                                                                            value=f'{data['dia']} de {data['mes']} de {data['ano']}',
                                                                                                            color=colors.BLACK,
                                                                                                            size=15,
                                                                                                            weight=FontWeight.BOLD,
                                                                                                        )
                                                                                                ]
                                                                                            )
                                                                                    )
                                                                        ]),
                                                            bgcolor=colors.WHITE30,
                                                            border_radius=border_radius.all(5),
                                                            padding=5
                                                        )
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                        Container(
                                                                width=446,
                                                                height=158,
                                                                content=Text(
                                                                            value=py_get_inf[3],
                                                                            color=colors.BLACK,
                                                                            weight=FontWeight.BOLD,
                                                                            size=11
                                                                        ),
                                                                bgcolor=colors.WHITE30,
                                                                border_radius=border_radius.all(5),
                                                                padding=5
                                                        )
                                                ]
                                            )
                                    ]
                            )
            thumbnail.width=260
        else: #Mouse FORA do container
            e.control.width=230
            e.control.height=50
            e.control.content=Row(
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
                            ])
            thumbnail.width=300
            pass
        janela.update()
        pass

    def titulo_display_hover(e): #Função que define o processo de hover para o container com informações do título do vídeo
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=417
            e.control.content=Text(
                                value=(py_get_inf[0]),
                                color=colors.BLACK,
                                size=17,
                                max_lines=1,
                                weight=FontWeight.BOLD,
                            )
            e.control.alignment=alignment.center_left
        else: #Mouse FORA do container
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

    def thumb_display_func(e): #Função que possibilita o efeito de surgimento do container presente por cima da imagem definida como THUMBNAIL
        if e.data=='true': #Mouse EM CIMA do container
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
        else: #Mouse FORA do container
            e.control.bgcolor=colors.WHITE10
            e.control.content=Text('')
        e.control.update()

    def voltar_page3_func(e): #Função responsável por retornar ao estado de página 2 
        janela.window.width=500
        janela.window.height=380
        voltar_hover_func(e)
        url_value_func(e)
        bot_url_func(e)
        janela.clean()
        janela.add(bg)
        janela.update()
        pass

    def voltar_hover_func(e): #Função que define o processo de hover para o container resposável por realizar a ação de voltar 
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=50
            e.control.border_radius=border_radius.all(5)
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
            e.control.on_click=voltar_page3_func
        else: #Mouse FORA do container
            e.control.width=10
            thumbnail.width=300
            e.control.border_radius=border_radius.all(3)
            e.control.content=Text('')
        janela.update()
        pass

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 4

    def thumb_page4_display_func(e): #Função que possibilita o efeito de surgimento do container presente por cima da imagem definida como THUMBNAIL_page4
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
                                            size=12,
                                            overflow=TextOverflow.FADE,
                                            text_align=TextAlign.CENTER
                                        ),
                                        Icon(
                                            name=Icons.FILE_DOWNLOAD_ROUNDED,
                                            size=20,
                                            color=colors.BLACK
                                        )
                        ])
        else: #Mouse FORA do container
            e.control.bgcolor=colors.WHITE10
            e.control.content=Text('')
        e.control.update()

    def titulo_page_4_hover(e):
        if e.data=='true':
            e.control.width=259
            e.control.content=Text(
                                value=(py_get_inf[0]),
                                color=colors.BLACK,
                                size=12,
                                max_lines=1,
                                weight=FontWeight.BOLD,
                                overflow=TextOverflow.ELLIPSIS
                            )
            e.control.alignment=alignment.center_left
        else:
            e.control.width=70
            e.control.content=Row(alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Titulo'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=12,
                                    
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=12,
                                )
                        ])
        janela.update()
        pass

    def autor_page_4_hover(e):
        if e.data=='true':
            e.control.width=259
            e.control.content=Text(
                                value=(py_get_inf[1]),
                                color=colors.BLACK,
                                size=12,
                                max_lines=1,
                                weight=FontWeight.BOLD,
                                overflow=TextOverflow.ELLIPSIS
                            )
            e.control.alignment=alignment.center_left
        else:
            e.control.width=70
            e.control.content=Row(alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Text(
                                    value=('Autor'),
                                    color=colors.BLACK,
                                    weight=FontWeight.BOLD,
                                    size=12,
                                    
                                ),
                                Icon(
                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                    color=colors.BLACK,
                                    size=12,
                                )
                        ])
        janela.update()
        pass


#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Itens presentes na página 1

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

    i1=Row( #Linha baixar vídeo (pág 1)
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
                                on_click=config_urlpg_func,
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

    i2=Row( #Linha baixar música (pág 1)
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
                                on_click=config_urlpg_func,
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

    i3=Row( #Linha baixar playlist (pág 1)
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
                                on_click=config_urlpg_func,
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

    itens=Column( #Alinhas linhas (pág 1)
                controls=[
                i1,
                i2,
                i3
    ])

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

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Itens presentes na página 2

    link=Column( #Layout de tela de onde será inserido o URL (pág 2)
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

    bg_link=Container( #bg link layout (pág 2)
                    width=janela.window.width,
                    height=janela.window.height,
                    content=Stack([
                                    link
                                ]),
                    bgcolor=colors.WHITE38,
                    border_radius=border_radius.all(5),
                    padding=5
    )

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
                        animate_offset=Animation(400, AnimationCurve.EASE_IN_OUT_SINE)
                    )
                ]
            )

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Itens presentes na página 3

    botoes_download_musica=Column( #Coluna botões de opções de download de música
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                        ElevatedButton( #Botão baixar música MP3
                                                        width=120,
                                                        height=50,
                                                        content=Text(
                                                                    value='Clássico (MP3)',
                                                                    color=colors.BLACK
                                                                ),
                                                        bgcolor=colors.WHITE30,
                                                        style=ButtonStyle(
                                                                        shape=RoundedRectangleBorder(radius=5),
                                                                        side=(
                                                                            BorderSide(1,colors.BLACK)
                                                                            )
                                                                    ),
                                                        on_click=musica_download_mp3
                                        ),
                                        ElevatedButton( #Botão baixar música M4A
                                                        width=120,
                                                        height=50,
                                                        content=Text(
                                                                    value='Universal (M4A)',
                                                                    color=colors.BLACK,
                                                                    size=13),
                                                                    bgcolor=colors.WHITE30,
                                                                    style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(radius=5),
                                                                                    side=(
                                                                                        BorderSide(1,colors.BLACK)
                                                                                        )
                                                                                ),
                                                        on_click=musica_download_m4a
                                        ),
                                ]
    )

    botoes_download_video=Column( #Coluna botões de opções de download de música
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                    ElevatedButton( #Botão baixar vídeo opção rápida
                                    width=120,
                                    height=50,
                                    content=Text(
                                                value='Rápido (360p)',
                                                color=colors.BLACK
                                            ),
                                    bgcolor=colors.WHITE30,
                                    style=ButtonStyle(
                                                    shape=RoundedRectangleBorder(radius=5),
                                                    side=(
                                                        BorderSide(1,colors.BLACK)
                                                        )
                                                ),
                                    on_click=video_download_fast
                    ),
                    ElevatedButton( #Botão baixar vídeo opcão qualidade
                                    width=120,
                                    height=50,
                                    content=Text(
                                                value=f'Qualidade ()',
                                                color=colors.BLACK,
                                                size=11),
                                                bgcolor=colors.WHITE30,
                                                style=ButtonStyle(
                                                                shape=RoundedRectangleBorder(radius=5),
                                                                side=(
                                                                    BorderSide(1,colors.BLACK)
                                                                    )
                                                            ),
                                    on_click=video_download_quality
                    ),
                                    
    ])

    Download= Container( #Container Download (pág 3)
                        width=10,
                        height=270,
                        content=Text(''),
                        bgcolor=colors.WHITE30,
                        ink=False,
                        border_radius=border_radius.all(3),
                        border=border.all(1,colors.BLACK),
                        padding=5,
                        on_hover=download_hover_func,
                        animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE),
    )

    inf_i1=Container( #Container que contêm a chamada para o título do vídeo selecionado (pág 3)
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

    inf_i2=Container( #Container que contêm a chamada para o autor do vídeo selecionado (pág 3)
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

    inf_i3=Container( #Container que contêm a chamada para as informações sobre o vídeo selecionado (pág 3)
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
                    animate_size=animation.Animation(600,AnimationCurve.EASE_OUT_SINE)
    )

    inf_video=Column( #Organização das informações em formato de coluna (pág 3)
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    controls=[
                    inf_i3,
                    inf_i1,
                    inf_i2
            ])

    thumbnail=Stack( #Região de amostragem da thumb do vídeo desejado (pág 3)
                    controls=[
                            Image(
                                src=py_get_inf[2],
                                width=300,
                                height=270,
                                fit=ImageFit.FILL,
                                border_radius=border_radius.all(5),
                                animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE),
                        ),
                            Container(
                                    width=300,
                                    height=270, 
                                    bgcolor=colors.WHITE10,
                                    alignment=alignment.center,
                                    border_radius=border_radius.all(5),
                                    ink=False,
                                    on_hover=thumb_display_func,
                                    on_click=baixar_thumb_func,
                                    animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE),
                        ),
        ])

    voltar=Container( #Container voltar (pág 3)
                    width=10,
                    height=270,
                    content=Text(''),
                    bgcolor=colors.WHITE30,
                    ink=False,
                    border_radius=border_radius.all(3),
                    border=border.all(1,colors.BLACK),
                    padding=5,
                    on_hover=voltar_hover_func,
                    animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE),
    )

    page3=Container( #Página final das opções de vídeo e música
                    height=215,
                    width=800,
                    content=Row(
                                alignment=MainAxisAlignment.START,
                                controls=[
                                        Row( #Thumb do vídeo e botão de voltar para a página de URL (página 2)
                                            spacing=3,
                                            controls=[
                                                    voltar,
                                                    thumbnail,
                                        ]),    
                                        Row( #Linhas de informação do vídeo e botão de prosseguir com download
                                            width=430,
                                            spacing=3,
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                    inf_video,
                                                    Download,
                                        ])
                                        
                        ]),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    padding=5,
    )

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Itens presentes na página 4

    thumbnail_page4=Stack(
                        controls=[
                                Image(
                                    width=130,
                                    height=130,
                                    src='https://media.tenor.com/_zWYqfZdneIAAAAM/shocked-face-shocked-meme.gif',  #py_get_inf[2]
                                    border_radius=border_radius.all(5),
                                    fit=ImageFit.FILL,
                                ),
                                Container(
                                    width=130,
                                    height=130,
                                    bgcolor=colors.WHITE10,
                                    alignment=alignment.center,
                                    border_radius=border_radius.all(5),
                                    ink=False,
                                    on_hover=thumb_page4_display_func,
                                    on_click=baixar_thumb_func
                                )
                        ]
    )

    inf_playlist=Column(
                        controls=[
                                Container(
                                        height=35,
                                        width=70,
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                    Text(
                                                        value=('Titulo'),
                                                        color=colors.BLACK,
                                                        weight=FontWeight.BOLD,
                                                        size=12,
                                                    ),
                                                    Icon(
                                                        name=Icons.ARROW_FORWARD_ROUNDED,
                                                        color=colors.BLACK,
                                                        size=12,
                                                    )
                                            ]
                                        ),
                                        bgcolor=colors.WHITE12,
                                        border_radius=border_radius.all(5),
                                        padding=5,
                                        on_hover=titulo_page_4_hover,
                                        animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
                                ),
                                Container(
                                        height=35,
                                        width=70,
                                        content=Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                    Text(
                                                        value=('Autor'),
                                                        color=colors.BLACK,
                                                        weight=FontWeight.BOLD,
                                                        size=12,
                                                    ),
                                                    Icon(
                                                        name=Icons.ARROW_FORWARD_ROUNDED,
                                                        color=colors.BLACK,
                                                        size=12,
                                                    )
                                            ]
                                        ),
                                        bgcolor=colors.WHITE12,
                                        border_radius=border_radius.all(5),
                                        padding=5,
                                        on_hover=autor_page_4_hover,
                                        animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
                                ),
                        ]
    )

    header_page4=Container(
                        height=130,
                        width=450,
                        content=(
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    spacing=5,
                                    controls=[
                                            thumbnail_page4,
                                            inf_playlist
                                    ]
                                )
                        ),
                        bgcolor=colors.WHITE12,
                        border_radius=border_radius.all(5),
                        padding=5
    )

    page4=Container(
                        height=442,
                        width=450,
                        content=(
                                Column(
                                    alignment=MainAxisAlignment.START,
                                    controls=[
                                            header_page4,
                                            #itens_playlist,
                                            #botoes_playlist
                                    ]
                                )
                        ),
                        bgcolor=colors.WHITE24,
                        border_radius=border_radius.all(5),
                        padding=5
        )

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Input inicial de página  

    bg=Container( #bg inicial do aplicativo (pág 1)
                height=janela.window.height-55,
                width=janela.window.width,
                content=Stack([
                    page1,
                    page2
                ]), 
                bgcolor=colors.WHITE24,
                border_radius=border_radius.all(5),
    )

#------------------------------------------------------------------------------------------

    janela.add(bg)

app(programa) 
