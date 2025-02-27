import pytubefix as pt
import moviepy as mp
yt=pt.YouTube('https://www.youtube.com/watch?v=N6j5UK-BCqM&t=3254s')

video_clip=mp.VideoFileClip(r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade (1080p)\Video\JENNIE & Dominic Fike - Love Hangover (Official Video).mp4')
audio_clip=mp.AudioFileClip(r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade (1080p)\Audio\JENNIE & Dominic Fike - Love Hangover (Official Video).mp3')
video_clip.audio=audio_clip
video_clip.write_videofile(r'C:\Users\pedro\Desktop\Youtube Download\Download qualidade (1080p)\Teste.mp4',fps=30,codec='libx264',audio_codec='aac')
