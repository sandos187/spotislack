from configparser import ConfigParser
from argparse import ArgumentParser
import json
import os
import sys
import random

import requests
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing'
spotipy_token = None


def read_config():
    """ read configfile """
    global slack_token
    global slack_channel
    global slack_color
    global slack_footer_icon
    global spotipy_client_id
    global spotipy_client_secret
    global spotipy_redirect_uri
    global spotipy_username
    global spotify_artwork_fallback
    with open(os.path.join(sys.path[0], 'spotislack.cfg')) as conf:
        config = ConfigParser()
        config.read_file(conf)
    slack_token = config[slack]['slack_token']
    if argchannel is not None:
        slack_channel = argchannel
    else:
        slack_channel = config[slack]['slack_channel']
        slack_color = config[slack]['slack_color']
        slack_footer_icon = config[slack]['slack_footer_icon']
        spotipy_client_id = config['spotify']['spotipy_client_id']
        spotipy_client_secret = config['spotify']['spotipy_client_secret']
        spotipy_redirect_uri = config['spotify']['spotipy_redirect_uri']
        spotipy_username = config['spotify']['spotipy_username']
        spotify_artwork_fallback = config['spotify']['spotify_artwork_fallback']

    if slack_color == "random":
        slack_color = create_random_color()

def get_current_song_from_spotify(spotipy_token):
    if spotipy_token:
        global artist
        global songname
        global songurl
        global album
        global artwork
        global fallback
        sp = spotipy.Spotify(auth=spotipy_token)
        results = sp.current_user_playing_track()
        artist = results['item']['album']['artists'][0]['name']
        songname = results['item']['name']
        songurl = results['item']['uri'].replace('spotify:track:', 'https://open.spotify.com/track/')
        album = results['item']['album']['name']
        if not results['item']['album']['images'] or len(results['item']['album']['images']) == 0:
            artwork = spotify_artwork_fallback
        else:
            artwork = results['item']['album']['images'][0]['url']
        fallback = "np: {0} - {1}".format(artist, songname)
    else:
        print("Can't get token for", spotipy_username)


def create_random_color():
    """ returns a random color in hex format without leading #
    """
    random_hex = lambda: random.randint(0,255)
    random_color = '{:02x}{:02x}{:02x}'.format(random_hex(), random_hex(), random_hex())

    return random_color

def send_message_to_slack(token, channel, color, footer_icon, artist, songname, songurl, album, artwork, fallback):
    """ Makes use of Send API:
        https://api.slack.com/methods/chat.postMessage
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(slack_token),
    }
    payload = {
        "channel": channel,
        "as_user": 'true',
        "attachments": [
            {
                "fallback": fallback,
                "color": color,
                "author_name": artist,
                "title": songname,
                "text": album,
                "title_link": songurl,
                "thumb_url": artwork,
                "footer": "now playing",
                "footer_icon": footer_icon,
            }
        ]
    }
    url = 'https://slack.com/api/chat.postMessage'
    response = requests.post(url, headers=headers,
                             data=json.dumps(payload))
    response.raise_for_status()


def main():
    """ the main function """
    global argchannel
    global slack

    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--slack", help="overrides default slack provided in config-file", action='store', dest="argslack", type=str.lower)
    parser.add_argument(
        "-c", "--channel", help="overrides default channel provided in config-file", action='store', dest="argchannel", type=str.lower)
    args = parser.parse_args()
    slack = args.argslack
    argchannel = args.argchannel

    try:
        read_config()
        spotipy_token = util.prompt_for_user_token(
            spotipy_username, scope, spotipy_client_id, spotipy_client_secret, spotipy_redirect_uri)
        get_current_song_from_spotify(spotipy_token)

        send_message_to_slack(slack_token, slack_channel, slack_color, slack_footer_icon,
                              artist, songname, songurl, album, artwork, fallback)

    except Exception as e:
        print("ERROR: Something failed")
        print(e)


if __name__ == "__main__":
    main()
