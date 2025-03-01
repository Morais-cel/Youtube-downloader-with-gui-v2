import pytubefix as pt

pl=pt.YouTube('https://www.youtube.com/watch?v=VNkrMLnk_Co')

s=pl.length

m=s//60
s=s%60
h=m//60
m=m%60
print(h,m,s)