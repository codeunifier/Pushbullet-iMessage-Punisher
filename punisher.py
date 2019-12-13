import requests
import pprint
import uuid
import credentials

pp = pprint.PrettyPrinter(indent=4)

# Determines if incoming message is worthy of punishment
def should_punish(message):
    return message.startswith('Liked') or message.startswith('Disliked') or message.startswith('Loved ') or message.startswith('Laughed at') or message.startswith('Emphasized') or message.startswith('Questioned')

# Returns the punished message
def get_punished_message(message):
    split = message.split(" ")

    if split[0] == "Laughed":
        return "Laughed at \"" + message + "\""
    else:
        return split[0] + " \"" + message + "\""

# Sends an SMS through pushbullet's api
def send_sms(addresses, message, device_iden):
    print('Punishing: %s' % message)

    message = get_punished_message(message)

    # have to create a new guid for each message
    guid = str(uuid.uuid4()).replace("-", "")

    body = {
        "data": {
            "addresses": addresses,
            "message": message,
            "target_device_iden": device_iden,
            "guid": guid
        }
    }

    r_options = requests.options(
        "https://api.pushbullet.com/v3/create-text",
    )

    if r_options.status_code != 200:
        print("Error with options call: %s" % (r_options.status_code))

    r = requests.post(
        "https://api.pushbullet.com/v3/create-text",
        json=body,
        headers={"content-type": "application/json", "access-token": credentials.api_key, "Authorization": "Basic M0JzMXl1ZFh3dWFpbUtpeVlSVlBlZzFVMUU0VThKOVc6"}
    )

    if r.status_code != 200:
        print("Error with create text call: %s" % (r.status_code))
