import math
import tweepy
import config
import twemoji

username = 'RafikiDev'
#Mettre le mot clé de début de game comme query
query = 'sondage from:RafikiDev OR mind from:RafikiDev' #-isquote
postClient = tweepy.Client(consumer_key=config.API_KEY,
                       consumer_secret=config.API_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET)

queryClient = tweepy.Client(bearer_token=config.BEARER_TOKEN)

response = queryClient.search_recent_tweets(query=query, max_results=10, poll_fields="voting_status", expansions=['attachments.poll_ids'])

###################################################################################################################
#Part where we quote-tweet previous rounds' results
###################################################################################################################

polls = {p['id']: p for p in response.includes['polls']}
print(polls)

winners = []
minVotes = math.inf

def build(winners):
    msg = winners[0]

    if len(winners) > 1:
        for i in range(1, len(winners) - 1):
            msg += ", " + winners[i]
        msg += " and " + winners[len(winners) - 1]

    return msg


#todo, check only one poll at a time ??!?!?!!
for poll in polls:
    #todo: maybe remove this check when we'll migrate to IDs
    if(polls[poll].voting_status == "closed"):
        for option in polls[poll].options:
            print(option["votes"])
            if(option["votes"] < minVotes):
                winners.clear()
                winners.append(option["label"])
                minVotes = option["votes"]
            elif(option["votes"] == minVotes):
                winners.append(option["label"])


endGameMessage = "People who voted for " + build(winners) + " win. There is a total of " + str(minVotes * len(winners))
if((minVotes * len(winners)) > 1):
    endGameMessage += " winners"
else:
    endGameMessage += " winner"

endGameMessage += " for this round."

#We will want to post endGameMessage in a quote retweet
print(endGameMessage)

###################################################################################################################
#Part where we post new round
###################################################################################################################

print(twemoji.pickEmoji())

postClient.create_tweet(text = "Pick your date", poll_duration_minutes=1440, poll_options=[twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji()])

#response = client.create_tweet(text= "Un sondage", poll_duration_minutes=60, poll_options=['oui', 'ok'])
#response = client.create_tweet(text = "Never forget", quote_tweet_id='1500939629096275971')

#todo: problems
#email
#comment ne pas poster plusieurs fois le résultat d'une game

#todo:
#create new email address (or figure something out)
#create new twitter account for the bot
#link the bot to this program
#setup pythonanywhere
#figure out how to only process surveys that
    #how to interval : PythonAnywhere https://www.twilio.com/blog/build-deploy-twitter-bots-python-tweepy-pythonanywhere

#resources:
#https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
#https://developer.twitter.com/en/docs/twitter-api/expansions
#https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
#Twitter API v2 Expansions (expansions are a type of parameter)















