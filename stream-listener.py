# RUN THIS FILE TO START THE PUNISHMENT

import json
import pprint
import requests
import websocket
from pushbullet import Pushbullet
import sys
import punisher
import credentials

# Setup
pb = Pushbullet(credentials.api_key)
pp = pprint.PrettyPrinter(indent=4)
my_iden = pb.user_info["iden"]
device_iden = pb.devices[0].device_iden

# Startup
print("\nWelcome, %s (%s).\n" % (pb.user_info["name"], pb.user_info["iden"]))
print("\nLoading device %s (%s)...\n" % (pb.devices[0].nickname, device_iden))

# Get infos for threads
print("\nUpdating threads file...\n")

r = requests.get("https://api.pushbullet.com/v2/permanents/%s_threads" % device_iden, headers={"content-type": "text", "access-token": credentials.api_key})

deemojiied = r.text.encode('ascii', 'ignore').decode('ascii')

with open("threads.json", "w") as threads_file:
    threads_file.write(deemojiied)

threads_list = r.json()

# Open websocket connection stream
print("\nOpening websocket connection...\n")

ws = websocket.WebSocket()
ws.connect("wss://stream.pushbullet.com/websocket/" + credentials.api_key)

print("\nConnected. Beginning stream.\n")

# Stream loop listening for incoming messages
while True:
    result = ws.recv()
    result = json.loads(result)

    try:
        message = result["push"]["notifications"][0]
        thread_id = message["thread_id"]

        message_text = str(message["body"])

        if punisher.should_punish(message_text):
            # collect messages
            addresses = []

            print("\nCollecting addresses...")

            for thread in threads_list["threads"]:
                if thread["id"] == thread_id:
                    for recipient in thread["recipients"]:
                        addresses.append(recipient["address"])
                    break

            punisher.send_sms(addresses, message_text, device_iden)

    except KeyError as err:
        sys.stdout.write(".")
        sys.stdout.flush()
    except Exception as ex:
        print(str(ex))

ws.close()
