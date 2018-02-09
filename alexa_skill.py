import logging
import random
import tokens
from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from TwitterAPI import TwitterAPI

api = TwitterAPI(tokens.consumer_key,tokens.consumer_secret,tokens.access_token_key, tokens.access_token_secret)

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def get_tweet():
    i_am_dev = api.request('statuses/user_timeline', {'count':4,'screen_name':'iamdevloper'})
    hipster = api.request('statuses/user_timeline', {'count': 4, 'screen_name': 'hipsterhacker'})
    honest = api.request('statuses/user_timeline', {'count': 4, 'screen_name': 'honest_update'})
    techcrunch = api.request('statuses/user_timeline', {'count': 4, 'screen_name': 'TechCrunchOnion'})

    tweets=[]

    feeds = [i_am_dev,hipster,honest,techcrunch]
    for account in feeds:
        for item in account.get_iterator():
            if 'text' in item:
                tweets.append(item)
    return random.choice(list(filter(lambda tweet: tweet if "t.co" not in tweet["text"] else None, tweets)))

@ask.launch
def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")
def give_tweet():


    tweet = get_tweet()

    round_msg = render_template('tweet', text=tweet["text"], author=tweet["user"]["name"])

    return question(round_msg)

if __name__ == '__main__':

    app.run(debug=True)
