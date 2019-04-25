from twitter_keys import consumer_key, consumer_secret, access_token, access_secret
import tweepy
import csv
import pytz
import requests
from bs4 import BeautifulSoup

with open('results.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('results.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Created At', 'type', 'User Name', 'NumFollowers', 'NumRetweets', 'NumFavorites', 'NumReplies', 'statusID', 
                'link'])
f.close()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
central = pytz.timezone('US/Central')

my_tweets = api.home_timeline()
mostate_tweets = api.user_timeline('MissouriState', count = 100)
ku_tweets = api.user_timeline('KUnews', count = 100)
mu_tweets = api.user_timeline('Mizzou', count = 100)
kstate_tweets = api.user_timeline('KState', count = 100)
cerners_tweets = api.user_timeline('Cerner', count = 100)
nkc_tweets = api.user_timeline('NKCHospital', count = 100)
kumed_tweets = api.user_timeline('KUMedCenter', count = 100)
bluekc_tweets = api.user_timeline('BlueKC', count = 100)

healthcare_accounts = [cerners_tweets, nkc_tweets, kumed_tweets, bluekc_tweets]
education_accounts = [mostate_tweets, ku_tweets, mu_tweets, kstate_tweets]

epicsys_tweets = api.user_timeline('EPICSys', count = 100)
cvs_tweets = api.user_timeline('CVSHealth', count = 100)
mckesson_tweets = api.user_timeline('McKesson', count = 100)
uhg_tweets = api.user_timeline('UnitedHealthGrp', count = 100)
ucf_tweets = api.user_timeline('UCF', count = 100)
texasam_tweets = api.user_timeline('TAMU', count = 100)
ohiost_tweets = api.user_timeline('OhioState', count = 100)
florida_tweets = api.user_timeline('UF', count = 100)

healthcare_accounts2 = [epicsys_tweets, cvs_tweets, mckesson_tweets, uhg_tweets]
education_accounts2 = [ucf_tweets, texasam_tweets, ohiost_tweets, florida_tweets]

def find_tweets(accounts, atype):
    for account in accounts:
        print(account[0].author.screen_name)
        for i in range(len(account)):
            if hasattr (account[i], 'retweeted_status'):
                continue
            #if account[i].in_reply_to_screen_name is not None:
                #continue
            else:
                link = "https://twitter.com/" + account[i].author.screen_name + "/status/" + str(account[i].id)
                r = requests.get(link)
                soup = BeautifulSoup(r.text, 'html5lib')
    
                #Replies
                replies = soup.find('span', {"class": "ProfileTweet-actionCount"})
                if replies is not None:
                    num_replies = int(replies['data-tweet-stat-count'])
                else:
                    num_replies = 0
    
                #Retweets
                li = soup.find('li', {"class": "js-stat-retweets"})
                if li is not None:
                    retweets = li.find('a')
                    num_retweets = retweets['data-tweet-stat-count']
                else:
                    num_retweets = 0
        
                #Favorites
                li2 = soup.find('li', {"class": "js-stat-favorites"})
                if li2 is not None:
                    favorites = li2.find('a')
                    num_favorites = favorites['data-tweet-stat-count']
                else:
                    num_favorites = 0
    
                #Better Date Format
                central_date = central.localize(account[i].created_at)
                fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            
                #open the results file and stores it to csvFile
                #newline deletes the extra row inbetween lines
                csvFile = open('results.csv', 'a', newline = '')
                csvWriter = csv.writer(csvFile)
                #write the information we want to a csv
                csvWriter.writerow([central_date.strftime(fmt), atype, account[i].author.screen_name,
                        account[i].author.followers_count, num_retweets, num_favorites, num_replies, account[i].id, 
                        link])
                csvFile.close()

find_tweets(healthcare_accounts, "healthcare")
find_tweets(education_accounts, "education")

find_tweets(healthcare_accounts2, "healthcare")
find_tweets(education_accounts2, "education")
