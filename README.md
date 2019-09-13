# Pushbullet-iMessage-Punisher
A python script utilizing [Pushbullet's API](https://docs.pushbullet.com/) to get back at those annoying iMessage reactions.

## How to run it
Add your Pushbullet API Access Token to the `credentials.py` file. You can get this token in your [Account Settings](https://www.pushbullet.com/#settings/account).

Run the `stream-listener.py` file (e.g. `python stream-listener.py`).

Enjoy the punishment.

## What it does
When an iPhone user uses a reaction in their Messenger app, but the receiver is an Android user (or there is an Android user in a group chat), the Android user receives an annoying text like `Loved an image` or `Liked "some other message"`.

This script utilizes Pushbullet's API to listen and watch for these messages and respond by liking a "like" or loving a "love." For example, if you receive a message like `Loved an image` the script would send a text back saying `Loved "Loved an image"`, punishing those who use these reactions and send out those annoying reaction messages.
