from configparser import ConfigParser
import json
import os
import sys


import requests
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing'
spotipy_token = None


def read_config():
    """ read configfile """
    global slack_url
    global slack_channel
    global slack_color
    global slack_footer_icon
    global slack_username
    global spotipy_client_id
    global spotipy_client_secret
    global spotipy_redirect_uri
    global spotipy_username
    with open(os.path.join(sys.path[0], 'spotislack.cfg')) as conf:
        config = ConfigParser()
        config.read_file(conf)
    slack_url = config['slack']['slack_url']
    slack_channel = config['slack']['slack_channel']
    slack_color = config['slack']['slack_color']
    slack_footer_icon = config['slack']['slack_footer_icon']
    slack_username = config['slack']['slack_username']
    spotipy_client_id = config['spotify']['spotipy_client_id']
    spotipy_client_secret = config['spotify']['spotipy_client_secret']
    spotipy_redirect_uri = config['spotify']['spotipy_redirect_uri']
    spotipy_username = config['spotify']['spotipy_username']


def get_current_song_from_spotify(spotipy_token):
    global artist
    global songname
    global songurl
    global album
    global artwork
    global fallback
    sp = spotipy.Spotify(auth=spotipy_token)
    results = sp.current_user_playing_track()
    if results:
        artist = results['item']['album']['artists'][0]['name']
        songname = results['item']['name']
        songurl = results['item']['uri'].replace('spotify:track:', 'https://open.spotify.com/track/')
        album = results['item']['album']['name']
        artwork = results['item']['album']['images'][0]['url']
        fallback = "np: {0} - {1}".format(artist, songname)
    else:
        print('is spotify running?')


def send_message_to_slack(slackurl, color, username, footer_icon, artist, songname, songurl, album, artwork, fallback):
    """ Makes use of Send API:
        https://developers.facebook.com/docs/messenger-platform/send-api-reference
    """
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "attachments": [
            {
                "fallback": fallback,
                "color": color,
                "author_name": username + " is listening to",
                "title": songname,
                "title_link": songurl,
                "text": "by " + artist,
                "thumb_url": artwork,
                "footer": "now playing",
                "footer_icon": footer_icon,
            }
        ]
    }

    url = slackurl
    response = requests.post(url, headers=headers,
                             data=json.dumps(payload))
    response.raise_for_status()


def main():
    """ the main function """

    try:
        read_config()
        spotipy_token = util.prompt_for_user_token(spotipy_username, scope, spotipy_client_id, spotipy_client_secret, spotipy_redirect_uri)
        get_current_song_from_spotify(spotipy_token)
        send_message_to_slack(slack_url, slack_color, slack_username, slack_footer_icon, artist, songname, songurl, album, artwork, fallback)


    except:
        print("Something went wrong")


if __name__ == "__main__":
    main()
