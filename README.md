# you-tube-datamining-v1.3
You Tube Data Harvesting using Key based Google API service. 
# This project is created to harvest data from the you tube using its API in Python.
I will explain one by one how this project is designed
#app.py    
This file is created to keep the DB related connection details( fill with your db connection URL, User name and password.)
#config.py 
This file holds the api_key (you have to create your api key in google develope console and update it here)
#YTB_app.py 
This file is to invoke the streamlit dash board api (gui). once above steps are completed then you can proceed with this.  i beleive you already installed mongoDB and mysql in you machine.
#YOUTUBE+STREAMLIT_app.py 
This will invoke the stream lit GUI for our project. this project created for harvesting you tube channel data by providing the channel id in the stream lit app , we can provide multiple channel at a time to harvest the details.
once the data is harvested of the particular channel, it will move the data to mongo db (harvested data will be in semi-structured dict format), you can use the side bar to upload the nosql data from mongo data to the SQL 
Once dadta is uploaded you can see the uploaded and already uploaded channel name / channel details in the sidebad.
if you tried to harvest the existing data in db of a channel, it will ask you to deleted the existing data and then harvest again.
you will prompt for drop button once you searched for the channel id and its already existing.
you can also see the raw data that has been harvested using view raw data from the side bar.
#ytb_data_collection.py 
This file bill be invoked when you hit the havest button from the streamlit gui.
This file has multiple gui call using the YouTube Data API v3 service.  Build api service (build(api_service_name, api_version, developerKey=api_key))
Then we call channel, video, playlist, comment api to collect the below data.
        Channel api call - channel_id', 'channel_name', 'channel_type', 'channel_views', 'channel_description', 'channel_status'
        playlist api call - 'playlist_name', 'playlist_id'
        Video api call - 'video_name', 'video_id', 'playlist_id', 'video_description', 'published_date', 'view_count', 'like_count', 'dislike_count',                              'favorite_count', 'comment_count', 'duration', 'thumbnail', 'caption_status' (note : there are few datas were restricted for the                           api call so those will be added as NAN )
        comment api call - 'comment_id', 'comment_text', 'comment_author', 'comment_published_date'
 #ytb_mng_to_mysql.py
 This will convert the dictionary format data to the structured format and move the data to the SQL server .

