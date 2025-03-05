from flet import *
import pytubefix as pt
import requests
import os
import moviepy as mp
import shutil
import subprocess
import time

modo=''
url=''
py_get_inf_mus_vid=['title','author','thumb_link','description','publish_date','views','resoluções do vídeo']
py_get_inf_playlist=['title','author','thumb_link','quantidade_videos','videos_playlist_urls']
res_qual=''
cont_select=0
tempo_select='00:00:00'

async def programa(janela: Page): 

#------------------------------------------------------------------------------------------
#Funções relacionadas a estrutura da janela do programa
    janela.window.width=500  #tamanho correto -> 500
    janela.window.height=380 #tamanho correto -> 380
    janela.window.resizable=False

    janela.theme = Theme(
        scrollbar_theme=ScrollbarTheme(
            thickness=0  
        )
    )

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas ao pytube

#-------------------------------------------
#Funções de obtenção de informações das urls informadas

    def py_get_inf_mus_vid_func(e): #Função responsável por obter as informações do vídeo
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

    def py_get_inf_playlist_func(e):
        pl=pt.Playlist(url)
        pl_title=pl.title
        pl_author=pl.owner
        pl_thumb_link=pl.thumbnail_url
        pl_quantidade_videos=pl.length
        videos_playlist_urls=pl.video_urls
        return [pl_title,pl_author,pl_thumb_link,pl_quantidade_videos,videos_playlist_urls]

    def py_get_inf_videos_playlist_func(urls):
        py_get_inf_videos_playlist=list()
        aux=list()
        for url_video_atual in urls:
            yt=pt.YouTube(url_video_atual)
            yt_atual_title=yt.title
            yt_atual_thumb_url=yt.thumbnail_url
            yt_atual_tempo_video=ajuste_tempo_video_func(yt.length)
            yt_atual_tempo_video_seg=yt.length
            aux=[yt_atual_title,yt_atual_thumb_url,yt_atual_tempo_video,yt_atual_tempo_video_seg]
            py_get_inf_videos_playlist.append(aux)
            aux=['']
        return py_get_inf_videos_playlist

    def res_qualidade_video_func(e): #Função que define se a resolução de 1080p está disponível no vídeo
        resolucoes=py_get_inf_mus_vid[6]
        if '1080p' in resolucoes:
            return '1080p'
        else:
            return '720p'

    def res_qualidade_playlist_func(e):
        list_videos=list()
        resolucoes=dict()
        for i in py_get_inf_playlist[4]:
            yt=pt.YouTube(i)
            stream=yt.streams.filter(adaptive=True,file_extension='mp4')
            for res in stream:
                if res.resolution:
                    resolucoes[f'{res.resolution}']=True
            list_videos.append(resolucoes.copy())
            resolucoes.clear()
        return list_videos

    def res_quali_get_playlist_func(lista_res_videos):
        res_1080p=True
        res_720p=True
        print(lista_res_videos)
        for i in lista_res_videos:
            if '1080p' not in i:
                res_1080p=False
                break
        if res_1080p==False:
            for i in lista_res_videos:
                if '720p' not in i:
                    res_720p=False
                    break
            if res_720p==False:
                return '480p'
            else:
                return '720p'
        else:
            return '1080p'
            

#-------------------------------------------

#-------------------------------------------
#Funções para o download de thumbs

    def baixar_thumb_func(e): #Função que cria, caso necessário, uma pasta definida como Thumb e salva a imagem do vídeo escolhido
        thumb_bin= requests.get(py_get_inf_mus_vid[2])
        if not os.path.exists(r'C:\Users\pedro\Desktop\Youtube Download\Thumb'):
            os.makedirs(r'C:\Users\pedro\Desktop\Youtube Download\Thumb')
            pass
        with open(fr'C:\Users\pedro\Desktop\Youtube Download\Thumb\{py_get_inf_mus_vid[1]}_TMB.png',"wb") as im:
            im.write(thumb_bin.content)
            pass
        pass

    def baixar_thumb_videos_playlist(e):
        pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Thumbs\{py_get_inf_playlist[0]}'
        req=e.control.data
        yt=pt.YouTube(py_get_inf_playlist[4][req])
        url_thumb=yt.thumbnail_url
        thumb_bin= requests.get(url_thumb)
        if not os.path.exists(pasta_principal):
            os.makedirs(pasta_principal)
            pass
        with open(os.path.join(pasta_principal,fr'{yt.video_id}.png'),"wb") as im:
            im.write(thumb_bin.content)
            pass
        pass

    def baixar_thumb_todos_videos_playlist(e):
        for i in range(0,len(py_get_inf_playlist[4])):
            pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Thumbs\{py_get_inf_playlist[0]}'
            yt=pt.YouTube(py_get_inf_playlist[4][i])
            url_thumb=yt.thumbnail_url
            thumb_bin= requests.get(url_thumb)
            if not os.path.exists(pasta_principal):
                os.makedirs(pasta_principal)
                pass
            with open(os.path.join(pasta_principal,fr'{yt.video_id}.png'),"wb") as im:
                im.write(thumb_bin.content)
                pass
            pass
#-------------------------------------------

#-------------------------------------------
#Funções de alteração de formatação de data e tempo

    def ajustes_data_lanc_func(e): #Função que define a formatação correta da data de publicação do vídeo
        data_ajustada=dict()
        meses=('jan.','fev.','mar.','abr.','mai.','jun.','jul.','ago.','set.','out.','nov.','dez.')
        data=str(py_get_inf_mus_vid[4]).split()
        data.pop()
        data=data[0].split('-')
        data_ajustada['dia']=int(data[2])
        data_ajustada['mes']=meses[int(data[1])-1]
        data_ajustada['ano']=int(data[0])
        return data_ajustada

    def ajuste_tempo_video_func(tamanho_s):
        min=tamanho_s//60
        seg=tamanho_s%60
        hora=min//60
        min=min%60
        return f'{hora:02d}:{min:02d}:{seg:02d}'

#-------------------------------------------

#-------------------------------------------
#Funções de download de músicas e vídeos únicos

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

#-------------------------------------------

#-------------------------------------------
#Funções relacionadas a conversão de arquivos

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

#-------------------------------------------

#-------------------------------------------
#Funções de download de playlist

    def itens_selecionados_playlist_func(e):
        itens_selecionados=list()
        op_selec=e.control.data
        aux=0
        for i in itens_playlist_estrut.content.controls:
            if i.content.controls[0].value==True:
                itens_selecionados.append(py_get_inf_playlist[4][aux])
            aux+=1
        match op_selec:
            case 'MP3':
                music_playlist_download_mp3(itens_selecionados)
                pass
            case 'M4A':
                music_playlist_download_m4a(itens_selecionados)
            case 'RAPIDO':
                video_playlist_download_fast(itens_selecionados)
                pass
            case 'QUALIDADE':
                video_playlist_download_quality(itens_selecionados)
                pass
        pass

    def music_playlist_download_m4a(urls):
        pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\M4A\{py_get_inf_playlist[0]}' #Local onde o arquivo o arquivo princiap será salvo
        for i in urls:
            yt=pt.YouTube(i)
            audio=yt.streams.filter(only_audio=True).first()
            if not os.path.exists(pasta_principal): #Criação de pasta MP4 caso não exista
                os.makedirs(pasta_principal)
                pass
            audio.download(output_path=pasta_principal,filename=f'{yt.video_id}.m4a') #Download música 

    def music_playlist_download_mp3(urls):
        pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\MP3\{py_get_inf_playlist[0]}' #Local onde o arquvio mp3 será salvo
        pasta_auxiliar=r'C:\Users\pedro\Desktop\Youtube Download\Playlist\MP4_AUX' #Pasta m4a criada para auxiliar durante a conversão das músicas
        for i in urls:
            yt=pt.YouTube(i)
            audio=yt.streams.filter(file_extension='mp4').first()
            if not os.path.exists(pasta_auxiliar): #Criação de pasta MP4_AUX caso não exista
                os.makedirs(pasta_auxiliar)
                pass
            if not os.path.exists(pasta_principal): #Criação de pasta MP3 caso não exista
                os.makedirs(pasta_principal)
                pass
            audio.download(output_path=pasta_auxiliar,filename=f'{yt.video_id}.mp4') #Download música 
        for na1,na2, arquivos in os.walk(pasta_auxiliar): #Mapeamento da pasta MP4_AUX
            for video in arquivos: #Análise dos arquivos existentes na pasta MP4_AUX
                conversao=mp.VideoFileClip(os.path.join(pasta_auxiliar,video))
                nome=str(video).replace('mp4','mp3')
                conversao.audio.write_audiofile(os.path.join(pasta_principal,nome))
                conversao.close()
        shutil.rmtree(pasta_auxiliar) #Excluir pasta temporária MP4_AUX

    def video_playlist_download_fast(urls):
        pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Download rápido\{py_get_inf_playlist[0]}' #Local onde o arquivo o arquivo princiap será salvo
        for i in urls:
            yt=pt.YouTube(i)
            video=yt.streams.filter(res='360p',file_extension='mp4').first() #Definir como será o formato do vídeo
            if not os.path.exists(pasta_principal): #Criar diretório Download rápido (360p) caso ele não exista
                os.makedirs(pasta_principal)
                pass
            video.download(output_path=pasta_principal,filename=f'{yt.video_id}.mp4') #Download vídeo

    def video_playlist_download_quality(urls):
        video_local=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Download qualidade\{py_get_inf_playlist[0]}\Video' #Local onde o vídeo sem audio será salvo
        audio_local=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Download qualidade\{py_get_inf_playlist[0]}\Audio' #Local onde o audio do vídeo será salvo
        pasta_principal=fr'C:\Users\pedro\Desktop\Youtube Download\Playlist\Download qualidade\{py_get_inf_playlist[0]}'
        for i in urls:
            yt=pt.YouTube(i)
            video=yt.streams.filter(file_extension='mp4',res=f'{res_qual}').first()
            audio=yt.streams.filter(file_extension='mp4').first()
            if not os.path.exists(video_local): #Criar pasta do local do vídeo(sem audio), caso não exista
                os.makedirs(video_local)
            if not os.path.exists(audio_local): #Criar pasta do local do audio do vídeo, caso não exista
                os.makedirs(audio_local)
            video.download(output_path=video_local,filename=f'{yt.video_id}.mp4')
            audio.download(output_path=audio_local,filename=f'{yt.video_id}.mp4')
            for i1, i2, arquivos in os.walk(audio_local):
                    for arq_atual in arquivos:
                        video_path=os.path.join(audio_local,arq_atual)
                        audio_path=os.path.join(audio_local,str(arq_atual).replace('mp4','mp3')) 
                        convert_mp4_mp3(video_path,audio_path)
            video_arquivo=os.path.join(video_local,f'{yt.video_id}.mp4')
            audio_arquivo=os.path.join(audio_local,f'{yt.video_id}.mp3')
            output_arquivo=os.path.join(pasta_principal,fr'{yt.video_id}.mp4')
            video_maker_func(video_arquivo,audio_arquivo,output_arquivo)
            shutil.rmtree(video_local)
            shutil.rmtree(audio_local)
        pass

#-------------------------------------------

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 1

    def global_modo_def_func(e): #Função responsável por atribuir o valor da variável global modo
        global modo
        modo=e.control.data
        pass

    def page1_config_caller_page2_func(e): #Função que configura o funcionamento dos botões de chamada da página 2
        global_modo_def_func(e)
        page2_animation_surge_func(e)
        page2_buttons_page1_lock_func(e)
        pass

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 2

    def page2_buttons_page1_lock_func(e): #Função que trava os botões presentes na pagina 1
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=True
        janela.update()   

    def page2_buttons_page1_unlock_func(e): #Função que destrava os botões presentes na pagina 1
        for i in itens.controls:
            i.controls[0].content.controls[1].disabled=False
        janela.update()   

    def page2_button_prosseguir_lock_unlock_func(e): #Função que trava o botão prosseguir na página 2 quando o textfield estiver vazio
        if link.controls[0].value=='':
            link.controls[1].controls[1].disabled=True
            janela.update()
        else:
            link.controls[1].controls[1].disabled=False
            janela.update()

    def page2_button_voltar_config_func(e): #Função responsável por realizar o processo de fechar a página 2 
        page2_buttons_page1_unlock_func(e)
        page2_animation_unsurge_func(e)

    def page2_button_prosseguir_config_func(e): #Função responsável por abrir a página 3 ou página 4
        if modo=='MUSICA' or modo=='VIDEO':
            pytube_music_video_func(e)
            janela.window.width=800
            janela.window.height=270
            janela.clean()
            janela.update()
            janela.add(page3)
        else:
            pytube_playlist_func(e)
            janela.window.width=450
            janela.window.height=500
            janela.clean()
            janela.update()
            janela.add(Stack_4e5)
        pass

    def pytube_music_video_func(e): #Função que adquire as informações do vídeo selecionado para as opções de "VIDEO" e "MUSICA"
    #--------------------------------------------
    #Definindo variáveis globais
        global url
        global py_get_inf_mus_vid
        global res_qual

    #--------------------------------------------

        url=link.controls[0].value
        py_get_inf_mus_vid=py_get_inf_mus_vid_func(e) #Processo para se obter as informações do vídeo presente na URL informada
        res_qual=res_qualidade_video_func(e) #Processo de adquirir a maior qualidade presente no vídeo (1080p ou 720p)
        thumbnail.controls[0].src=py_get_inf_mus_vid[2] #Atualização da imagem da thumbnail
        botoes_download_video.controls[1].content.value=f'Qualidade ({res_qual})' #Retorna o texto para o container coluna download na página 3
        link.controls[0].value='' #Resetando o valor do textfield do link para evitar futuros problemas

    def pytube_playlist_func(e): #Função que adquire as informações do vídeo selecionado para a opção de "PLAYLIST"
    #--------------------------------------------------------------------
    #Definindo as variáveis globais trabalhadas

        global py_get_inf_playlist
        global url
        global tempo_select
        global tempo_playlist
        global res_qual
    #--------------------------------------------------------------------

        url=link.controls[0].value
        py_get_inf_playlist=py_get_inf_playlist_func(e) #Processo para se obter as informações da playlist presente na URL informada
        py_get_inf_videos_playlist=py_get_inf_videos_playlist_func(py_get_inf_playlist[4]) #Cria uma lista contendo [título do vídeo,URL thumb,tempo de vídeo]
        tempo_playlist=page4_total_time(py_get_inf_videos_playlist)
        inf_playlist.controls[2].content.controls[2].content.value=f'{tempo_select}/{tempo_playlist}'
        thumbnail_playlist_page4.controls[0].src=py_get_inf_playlist[2] #Atualização da imagem da thumbnail presente na página 4
        inf_playlist.controls[2].content.controls[0].content.value=f'{cont_select:02d}/{py_get_inf_playlist[3]:02d}' #Endereça a quantidade de vídeo ao container destinado
        link.controls[0].value='' #Resetando o valor do textfield do link para evitar futuros problemas
        page4_video_playlist_func(py_get_inf_videos_playlist)
        res_qual=res_quali_get_playlist_func(res_qualidade_playlist_func(e))
        page5_column_video.controls[2].controls[1].content=Text(
                                                                value=f'Qualidade ({res_qual})',
                                                                color=colors.BLACK,
                                                                size=13
                                                            )
        print(res_qual)
        pass

    def page2_animation_surge_func(e): #Função que realiza o processo da animação de surgimento da página 2
        page2.controls[0].offset=transform.Offset(0,0)
        janela.update()  

    def page2_animation_unsurge_func(e): #Função que realiza o processo da animação de desaparecimento da página 2
        page2.controls[0].offset=transform.Offset(0,1)
        janela.update()  

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 3

    def page3_author_hover_func(e): #Função que realiza o processo de hover do container que contem as informações do autor do vídeo
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=417
            e.control.content=Text(
                                value=(py_get_inf_mus_vid[1]),
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

    def page3_download_hover_func(e): #Função responsável pelo funcionamento pela barra de download na página 3
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
                                        page3_column_choice_mode_func(e) #Função irá definir quais funções serão chamados para a coluna a depender de qual opção de download foi escolhida na página 1
                                ])
        else: #Mouse FORA do container
            e.control.width=10
            e.control.border_radius=border_radius.all(3)
            e.control.content=Text('')
            pass
        janela.update()
        pass

    def page3_inf_hover_func(e): #Função que realiza o processo de hover do container que contem as informações do vídeo
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
                                                                                                            value=f' {py_get_inf_mus_vid[5]:,} visualizações |'.replace(',','.'),
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
                                                                            value=py_get_inf_mus_vid[3],
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

    def page3_title_hover_func(e): #Função que define o processo de hover para o container com informações do título do vídeo
        if e.data=='true': #Mouse EM CIMA do container
            e.control.width=417
            e.control.content=Text(
                                value=(py_get_inf_mus_vid[0]),
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

    def page3_thumb_hover_func(e): #Função que possibilita o efeito de surgimento do container presente por cima da imagem definida como THUMBNAIL
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

    def page3_container_voltar_press_config_func(e): #Função que configura o funcionamento do 'botão' voltar na página 3
        janela.window.width=500
        janela.window.height=380
        page3_container_voltar_hover_func(e) #Retorna o container com a função voltar para o estado inicial
        page2_button_prosseguir_lock_unlock_func(e) #Bloqueia novamente o botão prosseguir na página 2
        janela.clean()
        janela.add(Stack_1e2)
        janela.update()
        pass

    def page3_container_voltar_hover_func(e): #Função que define o processo de hover para o container resposável por realizar a ação de voltar 
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
            e.control.on_click=page3_container_voltar_press_config_func
        else: #Mouse FORA do container
            e.control.width=10
            thumbnail.width=300
            e.control.border_radius=border_radius.all(3)
            e.control.content=Text('')
        janela.update()
        pass

    def page3_column_choice_mode_func(e): #Função que define a coluna que será colocada no quadro a depender da escolha na página 1
        global modo
        if modo=='MUSICA':
            return botoes_download_musica
        else:
            return botoes_download_video

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 4

    def page4_thumb_hover_fu(e): #Função que possibilita o efeito de surgimento do container presente por cima da imagem definida como THUMBNAIL_page4
        if e.data=='true':
            e.control.bgcolor=colors.WHITE38
            e.control.content=Column(
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            value=('Clique para baixar todas as imagens.'),
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

    def page4_thumb_videos_hover_fu(e): 
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

    def page4_title_hover_func(e):
        if e.data=='true':
            e.control.width=259
            e.control.content=Text(
                                value=(py_get_inf_playlist[0]),
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

    def page4_author_hover_func(e):
        if e.data=='true':
            e.control.width=259
            e.control.content=Text(
                                value=(py_get_inf_playlist[1]),
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

    def page4_video_playlist_func(videos_inf):
        videos=[]
        aux=0
        for video_atual in videos_inf:
            videos.append(
                        Container(
                            width=450,
                            height=100,
                            content=Row(
                                    spacing=5,
                                    controls=[
                                            Checkbox(
                                                    check_color=colors.BLACK,
                                                    active_color=colors.RED_900,
                                                    hover_color=colors.WHITE10,
                                                    splash_radius=0,
                                                    shape=RoundedRectangleBorder(radius=4),
                                                    on_change=pag4_checkbox_func
                                            ),
                                            Stack(
                                                controls=[
                                                        Image(
                                                            width=130,
                                                            src=fr'{video_atual[1]}', 
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
                                                            data=aux,
                                                            on_hover=page4_thumb_videos_hover_fu,
                                                            on_click=baixar_thumb_videos_playlist
                                                        )
                                                ]
                                            ),
                                            Column(
                                                alignment=MainAxisAlignment.END,
                                                spacing=16,
                                                controls=[
                                                        Container(
                                                            width=213,
                                                            height=50,
                                                            content=Text(
                                                                        value=f'{video_atual[0]}',
                                                                        color=colors.BLACK,
                                                                        size=12,
                                                                        weight=FontWeight.BOLD,
                                                                        max_lines=2,
                                                                        overflow=TextOverflow.ELLIPSIS
                                                                    ),
                                                            bgcolor=colors.RED_900,
                                                            border_radius=border_radius.all(5),
                                                            padding=5
                                                        ),
                                                        Row(
                                                            spacing=104,
                                                            width=212,
                                                            alignment=MainAxisAlignment.END,
                                                            controls=[
                                                                    Container(
                                                                            width=80,
                                                                            height=25,
                                                                            content=Text(
                                                                                        value=f'{video_atual[2]}',
                                                                                        color=colors.BLACK,
                                                                                        size=13,
                                                                                        weight=FontWeight.BOLD,
                                                                                    ),
                                                                            bgcolor=colors.RED_900,
                                                                            border_radius=border_radius.all(5),
                                                                            padding=5,
                                                                            alignment=alignment.top_center
                                                                    ),
                                                                    Container(
                                                                            width=30,
                                                                            height=25,
                                                                            content=Text(
                                                                                        value=f'{(len(videos)+1):02d}',
                                                                                        color=colors.BLACK,
                                                                                        weight=FontWeight.BOLD
                                                                                        ),
                                                                            bgcolor=colors.RED_900,
                                                                            border_radius=border_radius.all(5),
                                                                            padding=2,
                                                                            alignment=alignment.top_center
                                                                    )
                                                            ]
                                                        )
                                                ]
                                            ),
                                    ]
                            ),
                            bgcolor=colors.WHITE10,
                            border_radius=border_radius.all(5),
                            padding=5
                        )
            )
            aux+=1
        itens_playlist_estrut.content.controls=videos

    def page4_total_time(inf_videos):
        tempos=[]
        for videos in inf_videos:
            tempos.append(videos[3])
            pass
        tempo_total_playlist=ajuste_tempo_video_func(sum(tempos))
        return tempo_total_playlist

    def pag4_checkbox_func(e):
        global cont_select
        if e.control.value==True:
            cont_select+=1
        else:
            cont_select-=1
        page4_tempo_cont_func(e)

    def page4_tempo_cont_func(e):
    #--------------------------------------------------------------------
    #Definindo as variáveis globais trabalhadas

        global tempo_select
        tempo_video=['00:00:00']
    #--------------------------------------------------------------------

        page4_switch_off_func(e)
        page4_switch_on_func(e)
        inf_playlist.controls[2].content.controls[0].content.value=f'{cont_select:02d}/{py_get_inf_playlist[3]:02d}'
        for i in itens_playlist_estrut.content.controls:
            if i.content.controls[0].value==True:
                tempo_video.append(i.content.controls[2].controls[1].controls[0].content.value)
        page4_atualizar_cont_func(tempo_video)
        inf_playlist.controls[2].content.controls[2].content.value=f'{tempo_select}/{tempo_playlist}'
        inf_playlist.update()

    def page4_atualizar_cont_func(tempo_video):
    #--------------------------------------------------------------------
    #Definindo as variáveis globais trabalhadas

        global tempo_select
        tempo_select='00:00:00'
        s_video=0
    #--------------------------------------------------------------------
        tempo_global=tempo_select.split(':')

        #------------------------------------------
        #Transformar tempo_list em segundos
        for item_video in tempo_video:
            tempo_list=item_video.split(':')
            s_video=s_video+(int(tempo_list[0])*3600)
            s_video=s_video+(int(tempo_list[1])*60)
            s_video=s_video+int(tempo_list[2])
        #------------------------------------------

        #------------------------------------------
        #Transformar tempo_list em segundos
        s_select=int(tempo_global[0])*3600
        s_select=s_select+(int(tempo_global[1])*60)
        s_select=s_select+int(tempo_global[2])
        #------------------------------------------

        #------------------------------------------
        #Somar valores e retornar já formatado
        s_select=s_select+s_video
        tempo_select=ajuste_tempo_video_func(s_select)
        #------------------------------------------

    def page4_switch_hover_func(e):
        if e.data=='true':
            e.control.width=55
            e.control.border_radius=border_radius.all(5)
            e.control.content=page4_switch
        else:
            e.control.width=5
            e.control.border_radius=border_radius.all(3)
            e.control.content=Text('') 
        janela.update()
        pass

    def page4_switch_change_func(e):
    #--------------------------------------------------------------------
    #Definindo as variáveis globais trabalhadas

        global cont_select
        cont_select=0

    #--------------------------------------------------------------------
        if page4_switch.controls[1].value==True:
            for i in itens_playlist_estrut.content.controls:
                i.content.controls[0].value=True
                cont_select+=1
        else:
            for i in itens_playlist_estrut.content.controls:
                i.content.controls[0].value=False
        page4_tempo_cont_func(e)
        janela.update()
        pass

    def page4_switch_off_func(e):
        for i in itens_playlist_estrut.content.controls:
            if i.content.controls[0].value==False:
                page4_switch.controls[1].value=False
        pass

    def page4_switch_on_func(e):
        aux=True
        for i in itens_playlist_estrut.content.controls:
            if i.content.controls[0].value==False:
                aux=False
                break
        if aux==True:
            page4_switch.controls[1].value=True

    def page4_button_voltar_config_func(e):
    #--------------------------------------------------------------------
    #Definindo as variáveis globais trabalhadas

        global cont_select
        cont_select=0

    #--------------------------------------------------------------------
        janela.window.width=500
        janela.window.height=380
        page2_button_prosseguir_lock_unlock_func(e) #Bloqueia novamente o botão prosseguir na página 2

        janela.clean()
        janela.add(Stack_1e2)
        janela.update()
        pass

    def page4_button_prosseguir_config_func(e):
        page5_animation_surge_function(e)
        pass

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Funções relacionadas a página 4

    def page5_animation_surge_function(e):
        page5.offset=transform.Offset(0,0)
        janela.update()

    def page5_voltar_page4_func(e):
        page5.offset=transform.Offset(0,1)
        janela.update()

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
                                on_click=page1_config_caller_page2_func,
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
                                on_click=page1_config_caller_page2_func,
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
                                on_click=page1_config_caller_page2_func,
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
                        on_change=page2_button_prosseguir_lock_unlock_func,
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
                            on_click=page2_button_voltar_config_func,
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
                                on_click=page2_button_prosseguir_config_func,
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
                        on_hover=page3_download_hover_func,
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
                    on_hover=page3_title_hover_func,
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
                    on_hover=page3_author_hover_func,
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
                    on_hover=page3_inf_hover_func,
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
                                src=py_get_inf_mus_vid[2],
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
                                    on_hover=page3_thumb_hover_func,
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
                    on_hover=page3_container_voltar_hover_func,
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

    thumbnail_playlist_page4=Stack(
                        controls=[
                                Image(
                                    width=130,
                                    height=130,
                                    src='https://media.tenor.com/_zWYqfZdneIAAAAM/shocked-face-shocked-meme.gif',  #py_get_inf_mus_vid[2]
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
                                    on_hover=page4_thumb_hover_fu,
                                    on_click=baixar_thumb_todos_videos_playlist
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
                                        on_hover=page4_title_hover_func,
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
                                        on_hover=page4_author_hover_func,
                                        animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
                                ),
                                Container(
                                        height=30,
                                        width=199,
                                        content=Row(
                                                    spacing=4,
                                                    controls=[
                                                            Container(
                                                                    width=50,
                                                                    content=Text(
                                                                                value=f'XX/XX',
                                                                                color=colors.BLACK,
                                                                                weight=FontWeight.BOLD,
                                                                                size=12,),
                                                                    bgcolor=colors.RED_900,
                                                                    border_radius=border_radius.all(5),
                                                                    padding=4
                                                            ),
                                                            Icon(
                                                                name=Icons.ARROW_FORWARD_ROUNDED,
                                                                color=colors.BLACK,
                                                                size=14
                                                            ),
                                                            Container(
                                                                    width=120,
                                                                    content=Text(
                                                                                value=f'00:00:00/00:00:00',
                                                                                color=colors.BLACK,
                                                                                weight=FontWeight.BOLD,
                                                                                size=12,
                                                                                text_align=TextAlign.CENTER),
                                                                    bgcolor=colors.RED_900,
                                                                    border_radius=border_radius.all(5),
                                                                    padding=4
                                                            )
                                                ]
                                        ),
                                        bgcolor=colors.WHITE10,
                                        border_radius=border_radius.all(5),
                                        padding=3
                                )
                        ]
    )

    page4_switch=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                                Container(
                                        width=40,
                                        height=20,
                                        content=Text(
                                                    value='All',
                                                    color=colors.BLACK,
                                                    size=14,
                                                    weight=FontWeight.BOLD,
                                                    text_align=TextAlign.CENTER
                                                )
                                ),
                                Switch(
                                    width=50,
                                    height=30,
                                    active_color=colors.RED_900,
                                    track_outline_color=colors.BLACK,
                                    track_color=colors.BLACK38,
                                    thumb_icon=ControlState.HOVERED,
                                    hover_color=ControlState.DISABLED,
                                    on_change=page4_switch_change_func
                                )
                        ]
    ) 

    page4_switch_container=Container(
                        width=5,
                        height=60,
                        content=Text(''),
                        bgcolor=colors.WHITE10,
                        border_radius=border_radius.all(3),
                        on_hover=page4_switch_hover_func,
                        animate_size=animation.Animation(400,AnimationCurve.EASE_OUT_SINE)
    )

    header_page4=Container(
                        height=130,
                        width=450,
                        content=(
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    spacing=5,
                                    controls=[
                                            thumbnail_playlist_page4,
                                            Row(
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                spacing=2,
                                                width=260,
                                                controls=[
                                                        inf_playlist,
                                                        Column(
                                                            controls=[
                                                                    page4_switch_container
                                                            ]
                                                        )
                                                        
                                                ]
                                            )
                                    ]
                                )
                        ),
                        bgcolor=colors.WHITE12,
                        border_radius=border_radius.all(5),
                        padding=5
    )

    itens_playlist_estrut=Container(
                                    width=450,
                                    height=258,
                                    content=Column(
                                                    scroll='hidden',
                                                    controls=[
                                                            Container(
                                                                content=Text('')
                                                            )
                                                    ],
                                    ),
                                    bgcolor=colors.WHITE10,
                                    border_radius=border_radius.all(5),
                                    padding=5,
    )

    botoes_playlist=Row(
                        width=442,
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                                ElevatedButton(
                                            text='VOLTAR',
                                            color=colors.BLACK,
                                            icon=Icons.ARROW_BACK_ROUNDED,
                                            icon_color=colors.BLACK,
                                            style=ButtonStyle(
                                                            shape=RoundedRectangleBorder(radius=10),
                                                            bgcolor=colors.RED_900,
                                            ),
                                            on_click=page4_button_voltar_config_func
                                ),
                                ElevatedButton(
                                            content=Row(
                                                        controls=[
                                                                Text(
                                                                    value='PROSSEGUIR',
                                                                    color=colors.BLACK
                                                                ),
                                                                Icon(
                                                                    name=Icons.ARROW_FORWARD_ROUNDED,
                                                                    color=colors.BLACK
                                                                )
                                                        ]
                                            ),
                                            style=ButtonStyle(
                                                            shape=RoundedRectangleBorder(radius=10),
                                                            bgcolor=colors.RED_900,
                                            ),
                                            on_click=page4_button_prosseguir_config_func
                                )
                        ]
    )

    page4=Container(
                    height=442,
                    width=450,
                    content=(
                            Column(
                                alignment=MainAxisAlignment.START,
                                spacing=6,
                                controls=[
                                        header_page4,
                                        itens_playlist_estrut,
                                        botoes_playlist
                                ]
                            )
                    ),
                    bgcolor=colors.WHITE24,
                    border_radius=border_radius.all(5),
                    padding=5
    )

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#Itens presentes na página 5

    page5_column_music=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                    Container(
                                        height=70,
                                        width=170,
                                        content=Text(
                                                    value='Opções somente som',
                                                    color=colors.BLACK,
                                                    size=16,
                                                    weight=FontWeight.BOLD,
                                                    text_align=TextAlign.CENTER
                                                ),
                                        bgcolor=colors.RED_900,
                                        alignment=alignment.center,
                                        border_radius=border_radius.all(5),
                                        padding=5
                                    ),
                                    Icon(
                                        name=Icons.ARROW_DOWNWARD_ROUNDED,
                                        color=colors.RED_900,
                                        size=28
                                    ),
                                    Column(
                                        controls=[
                                                ElevatedButton( #Botão baixar música MP3
                                                                width=170,
                                                                height=70,
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
                                                                on_click=itens_selecionados_playlist_func,
                                                                data='MP3'
                                                ),
                                                ElevatedButton( #Botão baixar música M4A
                                                        width=170,
                                                        height=70,
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
                                                        on_click=itens_selecionados_playlist_func,
                                                        data='M4A'
                                        ),
                                        ]
                                    )
                            ]
    )

    page5_column_video=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                    Container(
                                        height=70,
                                        width=170,
                                        content=Text(
                                                    value='Opções somente vídeo',
                                                    color=colors.BLACK,
                                                    size=16,
                                                    weight=FontWeight.BOLD,
                                                    text_align=TextAlign.CENTER
                                                ),
                                        bgcolor=colors.RED_900,
                                        alignment=alignment.center,
                                        border_radius=border_radius.all(5),
                                        padding=5
                                    ),
                                    Icon(
                                        name=Icons.ARROW_DOWNWARD_ROUNDED,
                                        color=colors.RED_900,
                                        size=28
                                    ),
                                    Column(
                                        controls=[
                                                ElevatedButton( #Botão baixar vídeo 360p
                                                                width=170,
                                                                height=70,
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
                                                                on_click=itens_selecionados_playlist_func,
                                                                data='RAPIDO'
                                                ),
                                                ElevatedButton( #Botão baixar vídeo qualidade
                                                        width=170,
                                                        height=70,
                                                        content=Text(value='Qualidade ()',
                                                                    color=colors.BLACK,
                                                                    size=13
                                                                    ),
                                                        bgcolor=colors.WHITE30,
                                                        style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(radius=5),
                                                                                    side=(
                                                                                        BorderSide(1,colors.BLACK)
                                                                                        )
                                                                                ),
                                                        on_click=itens_selecionados_playlist_func,
                                                        data='QUALIDADE'
                                        ),
                                        ]
                                    )
                            ]
    )

    page5=Column(
                width=450,
                height=450,
                spacing=-2,
                offset=(0,1),
                animate_offset=Animation(400, AnimationCurve.EASE_IN_OUT_SINE),
                alignment=MainAxisAlignment.END,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                        Container(
                            width=450,
                            height=150,
                            content=Text(''),
                            opacity=0,
                            on_click=page5_voltar_page4_func
                        ),
                        Container(
                                width=420,
                                height=300,
                                content=Container(
                                                width=380,
                                                height=260,
                                                content=Row(
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                    page5_column_music,
                                                                    page5_column_video
                                                            ]
                                                        ),
                                                bgcolor=colors.WHITE30,
                                                padding=5,
                                                border_radius=border_radius.all(5)
                                ),
                                bgcolor=colors.GREY_900,
                                border_radius=border_radius.only(5,5),
                                padding=5,
                        )
                ]
    )
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#Stack de páginas

    Stack_1e2=Container( #bg inicial do aplicativo (pág 1)
                height=janela.window.height-55,
                width=janela.window.width,
                content=Stack([
                    page1,
                    page2
                ]), 
                bgcolor=colors.WHITE24,
                border_radius=border_radius.all(5),
    )

    Stack_4e5=Container(
                    content=Stack(
                                controls=[
                                        page4,
                                        page5
                                ]
                    ),
    )
#------------------------------------------------------------------------------------------

    janela.add(Stack_1e2)

app(programa) 
