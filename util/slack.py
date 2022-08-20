import requests

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

myToken = "xoxb-3963479472818-3957191170422-zzsqS0r3UecaJT6MbthvTz6q"

post_message(myToken,"#공모전","test")
