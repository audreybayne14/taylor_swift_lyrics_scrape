#!/usr/bin/env python
# coding: utf-8

# In[1]:


# install and import necessary packages

get_ipython().system('pip install lyricsgenius')

from bs4 import BeautifulSoup
import re
import requests
from pathlib import Path

# set up client access token

client_access_token = "INSERT YOUR CLIENT ACCESS TOKEN HERE"

import lyricsgenius
LyricsGenius = lyricsgenius.Genius(client_access_token)


# In[2]:


# create a function to clean up songs

def clean_up(song_title):

    if "Ft" in song_title:
        before_ft_pattern = re.compile(".*(?=\(Ft)")
        song_title_before_ft = before_ft_pattern.search(song_title).group(0)
        clean_song_title = song_title_before_ft.strip()
        clean_song_title = clean_song_title.replace("/", "-")
    
    else:
        song_title_no_lyrics = song_title.replace("Lyrics", "")
        clean_song_title = song_title_no_lyrics.strip()
        clean_song_title = clean_song_title.replace("/", "-")
    
    return clean_song_title


# In[3]:


# create a second function to scrape song titles for album

def get_all_songs_from_album(artist, album_name):
    
    artist = artist.replace(" ", "-")
    album_name = album_name.replace(" ", "-")
    
    response = requests.get(f"https://genius.com/albums/{artist}/{album_name}")
    html_string = response.text
    document = BeautifulSoup(html_string, "html.parser")
    song_title_tags = document.find_all("h3", attrs={"class": "chart_row-content-title"})
    song_titles = [song_title.text for song_title in song_title_tags]
    
    clean_songs = []
    for song_title in song_titles:
        clean_song = clean_up(song_title)
        clean_songs.append(clean_song)
        
    return clean_songs


# In[15]:


# create a third function to download lyrics for all songs on album

def download_album_lyrics(artist, album_name): 
    
    # set up client access token
    LyricsGenius = lyricsgenius.Genius(client_access_token)
    LyricsGenius.remove_section_headers = True
    
    # get all songs from album
    clean_songs = get_all_songs_from_album(artist, album_name)
    
    for song in clean_songs:
        
        # search for each song in lyricsgenius
        song_object = LyricsGenius.search_song(song, artist)
        
        # if song is not empty...
        if song_object != None:
            
            # clean song file names
            artist_title = artist.replace(" ", "-")
            album_title = album_name.replace(" ", "-")
            song_title = song.replace("/", "-")
            song_title = song.replace(" ", "-")
            song_title = song.replace("?", "-")
            
            # establish filename structure that lists artist, album title, and then song title
            custom_filename=f"{artist_title}_{album_title}/{song_title}"
            
            # create a directory
            Path(f"{artist_title}_{album_title}").mkdir(parents=True, exist_ok=True)
            
            #Save the lyrics for the song as a text file
            song_object.save_lyrics(filename=custom_filename, extension='txt', sanitize=False)
        
        # if the song does not contain lyrics...
        else:
            print('No lyrics')


# In[5]:


# now we call the function for each album!
    # note: i am only including the original versions of her ten studio albums
    # another note: i ran each album separately as it kept timing out
    # final note: python did not like the fact that i was using parenthesis for (taylor's version) in the code, so i had to use the stolen versions of some of them
        #rip atwtmvftvtv


# In[6]:


# download album lyrics for debut

download_album_lyrics("Taylor Swift", "Taylor Swift")


# In[7]:


# download album lyrics for fearless

download_album_lyrics("Taylor Swift", "Fearless")


# In[8]:


# download album lyrics for sn

download_album_lyrics("Taylor Swift", "Speak Now")


# In[9]:


# download album lyrics for red

download_album_lyrics("Taylor Swift", "Red")


# In[11]:


# download album lyrics for 1989

download_album_lyrics("Taylor Swift", "1989")


# In[16]:


# download album lyrics for rep

download_album_lyrics("Taylor Swift", "reputation")

# if you notice, rep included the prologues and poems, so i will go into my directory and delete those later to exclude from any analysis i do!


# In[13]:


# download album lyrics for lover <3

download_album_lyrics("Taylor Swift", "Lover")


# In[14]:


# download album lyrics for folklore

download_album_lyrics("Taylor Swift", "folklore")


# In[17]:


# download album lyrics for evermore (my personal favorite!)

download_album_lyrics("Taylor Swift", "evermore")


# In[ ]:


# each album will create a separate folder in your directory
# each folder will contain .txt files for every song on the album
# if you have any questions about this process, how to duplicate it, etc., feel free to ask! however...
# i've seen several users on kapple and github do similar projects, so it may be faster to search for those!

