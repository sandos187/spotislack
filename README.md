# spotislack.py

This is a small script to post your current playing song from spotify to slack

## Installation
In order to use this script, you need to install some python dependencies, which is done via `pip install -r requirements.txt`

## Configuration
After that, you have to modify your configuration file. Copy `spotislack.cfg.sample` to `spotislack.cfg` and start editing:

### Slack
Visit https://api.slack.com/apps and create an app for this script. After that, you have to add an Incoming Webhook to this App.
**IMPORTANT: this only has to be done once for every workspace. If another user of your workspace already created an app for this script, ask him for the incomming webhook url.**

The Channel to which the message of this script is posted depends on the Incoming Webhook. At the moment only one Webhook is supported. Maybe this is changed in the future, so that you can set more than one webhook in the config

You can define a color for the message border and last but not least an optional icon.

You must set your username in the configfile

### Spotify
Visit https://developer.spotify.com/dashboard/login to create your own app. This is necessary to get the needed credentials for reading your personal playlist details

You will get a client id and a secret which you put into your configuration file together with your username.

On the Apps Homepage you can edit the details and add an "Redirect URI". This is a link which is called when your user ist authorized. It isn't necessary, that this URI is reacheable. Just put there some fantasy-uri.
During the Authorisation process, you will get an error message in your browser, that the URL is not reacheable, but this doesn't matter as long as you can see and copy that complete URL. You need to paste that one into your terminal for the authorisation to finish

## Usage
After the installation and configuration process, you just need to call the script from terminal, and it should post the current song to the defined channel.

## ATTENTION!
This script is far from perfect, and at this moment just a little bit more than a proof-of-concept. For example there isn't any error- and exception-handling right now. If spotify isn't running while executing this script you just get a cryptic runtime error.
Feel free to contribute an send some pull requests!

Best regards

Sandos

