import math
import tweepy
import config

username = 'RafikiDev'
#Mettre le mot clé de début de game comme query
query = 'sondage from:RafikiDev OR mind from:RafikiDev' #-isquote
postClient = tweepy.Client(consumer_key=config.API_KEY,
                       consumer_secret=config.API_SECRET,
                       access_token=config.ACCESS_TOKEN,
                       access_token_secret=config.ACCESS_TOKEN_SECRET)

queryClient = tweepy.Client(bearer_token=config.BEARER_TOKEN)

response = queryClient.search_recent_tweets(query=query, max_results=10, poll_fields="voting_status", expansions=['attachments.poll_ids'])

polls = {p['id']: p for p in response.includes['polls']}
print(polls)

winners = []
minVotes = math.inf

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

#todo: adapt for ties
print("People who voted for " + str(winners) + " win. " + "There is a total of " + str(minVotes) + " winners for this game!")


#response = client.create_tweet(text= "Un sondage", poll_duration_minutes=60, poll_options=['oui', 'ok'])
#response = client.create_tweet(text = "Never forget", quote_tweet_id='1500939629096275971')

#todo: problems
#email
#efficacement et proprement sélectionner un emoji
#comment ne pas poster plusieurs fois le résultat d'une game

#todo:
#create new email address (or figure something out)
#create new twitter account for the bot
#link the bot to this program
#draw an emoji
#setup pythonanywhere
#figure out how to only process surveys that
    #how to interval : PythonAnywhere https://www.twilio.com/blog/build-deploy-twitter-bots-python-tweepy-pythonanywhere

#resources:
#https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
#https://developer.twitter.com/en/docs/twitter-api/expansions
#https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
#Twitter API v2 Expansions (expansions are a type of parameter)


