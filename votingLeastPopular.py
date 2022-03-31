import math
import tweepy
import config
import twemoji
import time

username = 'RafikiDev'
#Mettre le mot clé de début de game comme query
#query = 'sondage from:RafikiDev OR mind from:RafikiDev' #-isquote
postClient = tweepy.Client(consumer_key=config.API_KEY,
                       consumer_secret=config.API_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET)

#auth = tweepy.OAuth1UserHandler(consumer_key=config.API_KEY, consumer_secret=config.API_SECRET)
#auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
#api = tweepy.API(auth)

queryClient = tweepy.Client(bearer_token=config.BEARER_TOKEN)
#response = queryClient.search_recent_tweets(query=query, max_results=10, poll_fields="voting_status", expansions=['attachments.poll_ids'])

###################################################################################################################
#Part where we quote-tweet previous rounds' results
###################################################################################################################

def build(winners):
    msg = winners[0]
    if len(winners) > 1:
        for i in range(1, len(winners) - 1):
            msg += ", " + winners[i]
        msg += " and " + winners[len(winners) - 1]
    return msg

def postPoll():
    #poll_duration_minutes=1440
    response = postClient.create_tweet(text = "Which emoji will get the least votes", poll_duration_minutes=5, poll_options=[twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji()])
    return response.data["id"]

def postResults(tweetID):
    tweet = queryClient.get_tweet(tweetID, expansions=["attachments.poll_ids"])
    options = tweet.includes["polls"][0].options

    winners = []
    minVotes = math.inf

    for option in options:
        if(option["votes"] < minVotes):
            winners.clear()
            winners.append(option["label"])
            minVotes = option["votes"]
        elif(option["votes"] == minVotes):
            winners.append(option["label"])

    postClient.create_tweet(text=build(winners), quote_tweet_id=tweetID)

polls = [0,0,0,0]

while(1):
    poll = polls.pop(0)
    print(poll)
    if(poll != 0):
        postResults(poll)

    polls.append(postPoll())

    time.sleep(75)



















#polls = {p['id']: p for p in response.includes['polls']}
#print(polls)

#winners = []
#minVotes = math.inf


#todo, check only one poll at a time ??!?!?!!
#for poll in polls:
 #   #todo: maybe remove this check when we'll migrate to IDs
  #  if(polls[poll].voting_status == "closed"):
   #     for option in polls[poll].options:
    #        print(option["votes"])
     #       if(option["votes"] < minVotes):
      #          winners.clear()
       #         winners.append(option["label"])
        #        minVotes = option["votes"]
         #   elif(option["votes"] == minVotes):
          #      winners.append(option["label"])


#endGameMessage = "People who voted for " + build(winners) + " win. There is a total of " + str(minVotes * len(winners))
#if((minVotes * len(winners)) > 1):
#    endGameMessage += " winners"
#else:
#    endGameMessage += " winner"

#endGameMessage += " for this round."

#We will want to post endGameMessage in a quote retweet
#print(endGameMessage)

###################################################################################################################
#Part where we post new round
###################################################################################################################

#print(twemoji.pickEmoji())

#postClient.create_tweet(text = "Pick your date", poll_duration_minutes=1440, poll_options=[twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji(), twemoji.pickEmoji()])

#response = postClient.create_tweet(text = "Getting closer (?)")
#print(response)
#print(response.data["id"])

#tweet = api.get_status(1504268182353334279)
#print(tweet.text)

#todo:
#comment ne pas poster plusieurs fois le résultat d'une game
#heroku


