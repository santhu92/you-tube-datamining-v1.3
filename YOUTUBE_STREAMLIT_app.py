import pandas as pd
import streamlit as st
import subprocess
import sys
import os
from app import engine
cwd = os.getcwd()


st.title("Youtube Data Scrapping")

st.write("Please enter Channel Id with comma seperated")
ytb_channel_id = st.text_input("channel_ids")
j = []
try:
    extxhnl = pd.read_sql_query("SELECT * from channel_id_info;", con=engine)
    j = [i for i in extxhnl['channel_id'] if i in ytb_channel_id]
except BaseException as e:
    pass

if len(j)>0:
    k=str(j[0:])
    k=k.replace("[","")
    k=k.replace("]","")
    st.write(k.replace("[",""))
    st.write("data already exist for channels if you want to harvest again drop existing data using options in sidebar and harvest")
else:
    button = st.button("Click to start harvesting", key="button2")
    if button:
        f = open("temp.txt", "w")
        st.write(ytb_channel_id)
        f.write(ytb_channel_id)
        f.close()
        subprocess.run([f"{sys.executable}", cwd + "\\ytb_data_collection.py"])
st.sidebar.title("you tube data insights ")
button1 = st.sidebar.button("Upload to MYSQL DB", key="button3")
if button1:
    subprocess.run([f"{sys.executable}", cwd + "\\ytb_mng_to_mysql.py"])


Selected_channel_id = ytb_channel_id.split(",")
raw_data_option = st.sidebar.selectbox('select the harvested channel, in which you want to see raw data', (Selected_channel_id))
button2 = st.sidebar.button("display raw data", key="button4")
if button2:
    cwd = os.getcwd()
    pathfile = cwd + "\\" + raw_data_option.strip()
    st.write('You selected:', raw_data_option + ".json")
    file = open(fr"{pathfile}.json", "r")
    data = file.read()
    st.write(data)

try:

    More_comments = pd.read_sql_query("Select * from more_comments;", con=engine)

    Channel_that_published_video_in_year2022s = pd.read_sql_query(
        "SELECT * from channel_that_published_video_in_year2022;", con=engine)

    most_liked_videos = pd.read_sql_query("SELECT * from most_liked_videos;", con=engine)

    channel = pd.read_sql_query("SELECT channel_views, channel_name from channel;", con=engine)

    videos_basic_info = pd.read_sql_query("SELECT * from videos_Basic_info;", con=engine)

    Least_Watched_videos = pd.read_sql_query("SELECT * from least_Watched_videos;", con=engine)

    Top_videos = pd.read_sql_query("SELECT * from top_videos;", con=engine)

    video_comment_count = pd.read_sql_query("SELECT comment_count, video_name from video;", con=engine)

    channel_id_info = pd.read_sql_query("SELECT * from channel_id_info;", con=engine)
    
    Average_videos_duration_of_Each_channel = pd.read_sql_query("SELECT * from Average_videos_duration_of_Each_channel;", con=engine)
    
except BaseException as e:
    pass


option = st.sidebar.selectbox('Search By', (
    'More_comments', 'Channel_that_published_video_in_year2022s', 'most_liked_videos',
    'channel', 'videos_basic_info', 'Least_Watched_videos', 'Top_videos',
    'video_comment_count','Average_videos_duration_of_Each_channel'))
button4 = st.sidebar.button("Click to proceed", key="button5")
if button4:
    if option == 'More_comments':
        st.write(More_comments)
    elif option == 'Channel_that_published_video_in_year2022s':
        st.write(Channel_that_published_video_in_year2022s)
    elif option == 'most_liked_videos':
        st.write(most_liked_videos)
    elif option == 'channel':
        st.write(channel)
    elif option == 'videos_basic_info':
        st.write(videos_basic_info)
    elif option == 'videos_basic_info':
        st.write(videos_basic_info)
    elif option == 'Least_Watched_videos':
        st.write(Least_Watched_videos)
    elif option == 'Top_videos':
        st.write(Top_videos)
    elif option == 'video_comment_count':
        st.write(video_comment_count)
    elif option == 'Average_videos_duration_of_Each_channel':
        st.write(Average_videos_duration_of_Each_channel)
try:
    drop_data_list = k.split(",")
    drop_data = st.sidebar.selectbox('select the channel to drop, (drop_data_list))

    drop_button = st.sidebar.button("drop button")
    if drop_button:
        engine.execute("SET FOREIGN_KEY_CHECKS=0;")
        engine.execute("DELETE FROM comment WHERE video_id IN (SELECT video_id FROM video, playlist WHERE video.playlist_id = playlist.playlist_id AND playlist.channel_id = " + drop_data + ");")
        engine.execute("DELETE FROM video WHERE playlist_id IN (SELECT playlist_id FROM playlist WHERE channel_id = " + drop_data + ");")
        engine.execute("DELETE FROM channel WHERE channel_id = "+ drop_data +";")
        engine.execute("DELETE FROM playlist WHERE channel_id = "+ drop_data +";")
        engine.execute("SET FOREIGN_KEY_CHECKS=1;")
        cwd = os.getcwd()
        pathfile = cwd + "\\" + drop_data.replace("'","")
        filename = f"{pathfile}.json"
        os.remove(filename)
except BaseException as e:
    pass
st.sidebar.text("channels and their total video count exist in Data base")
try:
    st.sidebar.write(channel_id_info)
except BaseException as e:
    pass
