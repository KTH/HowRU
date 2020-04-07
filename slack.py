__author__ = 'tinglev@kth.se'

import os
import logging
from slackclient import SlackClient
import cache
import util

rtm_read_delay = 1
client = None
bot_id = None

log = logging.getLogger(__name__)

def init():
    global client, bot_id
    client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    bot_id = client.api_call("auth.test")["user_id"]
    log.debug('Bot ID is "%s"', bot_id)
    return client.rtm_connect(with_team_state=False, auto_reconnect=True)

def post_todays_question():
    question = util.get_random_question()
    low_scale = question['scale']['min']
    high_scale = question['scale']['max']
    channel = os.environ.get('SLACK_CHANNEL_FOR_QUESTION')
    send_message(
        channel, 
        f'Dagens fråga är: {question["question"]}; ' +
        f'1 - {low_scale}, 10 - {high_scale}'
    )

def post_question_summary():
    channel = os.environ.get('SLACK_CHANNEL_FOR_SUMMARY')
    mean = cache.get_mean_score()
    median = cache.get_median_score()
    count = cache.get_answer_count()
    send_message(channel, f'Svar: {count}, snitt {mean}, median {median}')
    cache.empty_all_caches()

def get_rtm_messages(events):
    messages = []
    for event in events:
        if event["type"] == "message":
            messages.append(event)
    return messages

def handle_im_created(message):
    if 'channel' in message:
        cache.add_channel_to_cache(message['channel'])

def handle_im(message):
    if 'type' in message and message['type'] == 'message':
        if 'channel' in message and cache.has_entry(message['channel']):
            if 'text' in message and message_text_is_score(message['text']):
                save_score(message['text'])
                send_message(message['channel'], 'Tack för ditt svar!')
                cache.remove_channel_from_cache(message['channel'])
            else:
                send_message(message['channel'], 'Felaktigt värde. Måste vara 1 till 10')

def message_text_is_score(text):
    try: 
        int(text)
        return True
    except ValueError:
        return False

def save_score(text):
    cache.add_score_to_cache(int(text))

def send_message(channel, message, default_message=None):
    log.debug('Sending msg to ch "%s" msg "%s"', channel, message)

    client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message or default_message
    )

def rtm_read():
    return client.rtm_read()
