import os
import json
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from datetime import datetime
from config import api_key1
# Set up the YouTube Data API v3 service
api_service_name = "youtube"
api_version = "v3"
api_key = api_key1
# Replace with your API key
youtube = build(api_service_name, api_version, developerKey=api_key)


def get_playlists(channel_id):
    """
    Retrieves all playlists for a given channel ID.
    """
    try:
        response = youtube.playlists().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=100
        ).execute()
        return response.get("items", [])
    except googleapiclient.errors.HttpError as e:
        print("An error occurred:", e)


def get_videos(playlist_id, page_token=None):
    """
    Retrieves all videos within a given playlist.
    """
    try:
        response = youtube.playlistItems().list(
            part="id,snippet",
            playlistId=playlist_id,
            maxResults=100
        ).execute()
        return response.get("items", []), response.get("nextPageToken")
    except googleapiclient.errors.HttpError as e:
        print("An error occurred:", e)


def get_comments(video_id):
    """
    Retrieves all comments for a given video.
    """
    try:
        response = youtube.commentThreads().list(
            part="id,snippet",
            videoId=video_id,
            maxResults=100
        ).execute()
        return response.get("items", [])
    except googleapiclient.errors.HttpError as e:
        print("An error occurred:", e)

with open('temp.txt', 'r') as file:
    CHIDLIST1 = file.read()
    CHIDLIST = CHIDLIST1.split(",")
os.remove("temp.txt")
for i in CHIDLIST:
    channel_id = i.replace(" ", "")
    print("channel_id:",channel_id)
    # Create a dictionary to store the harvested data
    channel_data = {}
    # Get channel information
    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()
    channel = channel_response["items"][0]
    # Get all playlists for the specified channel
    playlists = get_playlists(channel_id)
    #print("play list:", playlists)
    # Iterate through each playlist
    for playlist in playlists:
        playlist_id = playlist["id"]
        playlist_title = playlist["snippet"]["title"]
        channel_data = {
            "Channel_Name": {
                "Channel_Name": channel["snippet"]["title"],
                "Channel_Id": channel_id,
                "Subscription_Count": int(channel["statistics"]["subscriberCount"]),
                "Channel_Views": int(channel["statistics"]["viewCount"]),
                "Channel_Description": channel["snippet"]["description"],
                "Playlist_Id": playlist_id,
                "playlist_Title": playlist_title
            }
        }
        # Get all videos within the playlist
        # videos = get_videos(playlist_id)
        videos = []
        next_page_token = None
        print("play list Id :", playlist_id)
        while True:
            page_videos, next_page_token = get_videos(playlist_id, page_token=next_page_token)
            videos.extend(page_videos)
            if next_page_token is None:
                break
        # Iterate through each video
        vid = 0
        for video in videos:
            video_id = video["snippet"]["resourceId"]["videoId"]
            # Get video information
            video_response = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            ).execute()
            video_items = video_response.get("items", [])
            #print("video_response:", video_response)
            if not video_items:
                continue  # Skip this video if no information is returned
            video_info = video_items[0]
            Video_Info = 'Video_Id' + str(vid)
            # Store video data
            video_plus = video_info['snippet']['publishedAt']
            video_plus = str(datetime.strptime(video_plus, "%Y-%m-%dT%H:%M:%SZ"))
            # video_plus = datetime.fromisoformat(video_plus)  ###getting error like "TypeError: Object of type datetime is not JSON serializable"
            channel_data[Video_Info] = {
                "Video_Id": video_id,
                "Video_Name": video_info["snippet"]["title"],
                "Video_Description": video_info["snippet"]["description"],
                "View_Count": int(video_info["statistics"]["viewCount"]),
                'Tags': video_info['snippet'].get('tags', []),
                'PublishedAt': video_plus,
                'Like_Count': video_info['statistics'].get('likeCount', 'Not Available'),
                # 'Dislike_Count': video_info['snippet']['statistics']['dislikeCount'],
                'Favorite_Count': int(video_info['statistics']['favoriteCount']),
                'Comment_Count': int(video_info['statistics'].get('commentCount', 'Not Available')),
                'Duration': video_info['contentDetails']['duration'],
                'Thumbnail': video_info['snippet']['thumbnails']['default']['url'],
                'Caption_Status': video_info['contentDetails'].get('caption', 'Not Available')
            }

            comments = get_comments(video_id)
            CID = 0
            try:
                for comment in comments:
                    Comment_id = 'Comment_Id' + str(CID)
                    #print("COMMENTS:", comment)
                    comment_id = comment['snippet']['topLevelComment']['id']
                    channel_data[Video_Info][Comment_id] = {
                        "comment": {
                            'comment_id': comment_id,
                            'comment_text': comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                            'comment_author': comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            'comment_publishedate': comment['snippet']['topLevelComment']['snippet']['publishedAt']
                        }
                    }
                    CID += 1
            except BaseException as e:
                pass
            vid += 1
        filename = f"{i.strip()}.json"
        #print(filename)
        cwd1 = os.getcwd()
        pathfile = cwd1 + "\\" + filename
        with open(fr"{pathfile}", "a") as final:
            json.dump(channel_data, final)
        from pymongo import MongoClient
        from app import client
        mydb = client["Youtube"]
        ytchnl1 = mydb["youtubechannel1"]
        mydb.ytchnl1.insert_many([channel_data])
        print("Connection Successful")

