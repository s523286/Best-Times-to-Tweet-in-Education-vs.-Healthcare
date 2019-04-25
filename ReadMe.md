# Best Times to Tweet in Healthcare vs. Education

### Developer: Liz Conard

## Description:
This project takes tweets from major universities and healthcare companies in the Kansas City area, as well as, major universities and healthcare companies in the United States. It will produce two heat maps, one for healthcare and one for education. Pulling information from the tweets, such as favorites, retweets, and comments, the heat maps will show the "best times to tweet" during the week.

I am comparing it to the results given at this website:
- https://sproutsocial.com/insights/best-times-to-post-on-social-media/#twitter

## To Begin:
- Make sure to create a twitter developer account. Save the consumer and access keys in a python file within your folder.
- Create a .gitignore file and put the filename containing your access keys within this file.
- Create a scraper.py file and put it in your folder.
- Create a results.csv file to save your output to and place it in the same folder as everything else.
- Create a findings.ipynb file to manipulate your data in and also put it in your folder.

## Retrieving the Data:
### Contents of scraper.py
```python
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

```
#### About scraper.py
- First, the Python file clear the csv file and then write the column headers.
- We will read in the twitter api consumer keys and tokens to access my twitter developer account. If you do not have a developer account, you will need to request one before you can recreate this.
- pytz helps us convert everything to central time because twitter does not standardize time at all.
- Then, using tweepy, we pull tweets from major universities and healthcare companies.
- Finally, we call upon the fine_tweets function to pull the information we will need, from the tweets, to write out to the csv.

## Cleaning and Using the data:
### findings.ipynb
#### Read in the .csv
```python
import pandas as pd
df = pd.read_csv("results.csv")
df
```
#### Convert the "Created At" field into a datetime data type, extract the day of the week, and map it onto a new column called "weekdays"
```python
import datetime

df1 = df.copy()

df1['Created At'] = pd.to_datetime(df1['Created At'])
value = df1['Created At']
        
def weekday(date):
    if date.weekday() == 0:
        return 'Monday'
    elif date.weekday() == 1:
        return 'Tuesday'
    elif date.weekday() == 2:
        return 'Wednesday'
    elif date.weekday() == 3:
        return 'Thursday'
    elif date.weekday() == 4:
        return 'Friday'
    elif date.weekday() == 5:
        return 'Saturday'
    else:
        return 'Sunday'

df1["weekdays"] = value.map(weekday)
df1['weekdays'].head()
```
#### Now extract the time and map it onto a new column called "time"
```python
df2 = df1.copy()

def time(date):
    time2 = date.time()
    return time2

df2["time"] = value.map(time)
df2['time'].head()
```
#### Group the times into hourly buckets and map it onto a new column called "time groups"
```python
df3 = df2.copy()

def time_groups(time):
    if time >= datetime.time(0,0) and time <= datetime.time(1,0):
        return '12AM-1AM'
    elif time >= datetime.time(1,0) and time <= datetime.time(2,0):
        return '1AM-2AM'
    elif time >= datetime.time(2,0) and time <= datetime.time(3,0):
        return '2AM-3AM'
    elif time >= datetime.time(3,0) and time <= datetime.time(4,0):
        return '3AM-4AM'
    elif time >= datetime.time(4,0) and time <= datetime.time(5,0):
        return '4AM-5AM'
    elif time >= datetime.time(5,0) and time <= datetime.time(6,0):
        return '5AM-6AM'
    elif time >= datetime.time(6,0) and time <= datetime.time(7,0):
        return '6AM-7AM'
    elif time >= datetime.time(7,0) and time <= datetime.time(8,0):
        return '7AM-8AM'
    elif time >= datetime.time(8,0) and time <= datetime.time(9,0):
        return '8AM-9AM'
    elif time >= datetime.time(9,0) and time <= datetime.time(10,0):
        return '9AM-10AM'
    elif time >= datetime.time(10,0) and time <= datetime.time(11,0):
        return '10AM-11AM'
    elif time >= datetime.time(11,0) and time <= datetime.time(12,0):
        return '11AM-12PM'
    elif time >= datetime.time(12,0) and time <= datetime.time(13,0):
        return '12PM-1PM'
    elif time >= datetime.time(13,0) and time <= datetime.time(14,0):
        return '1PM-2PM'
    elif time >= datetime.time(14,0) and time <= datetime.time(15,0):
        return '2PM-3PM'
    elif time >= datetime.time(15,0) and time <= datetime.time(16,0):
        return '3PM-4PM'
    elif time >= datetime.time(16,0) and time <= datetime.time(17,0):
        return '4PM-5PM'
    elif time >= datetime.time(17,0) and time <= datetime.time(18,0):
        return '5PM-6PM'
    elif time >= datetime.time(18,0) and time <= datetime.time(19,0):
        return '6PM-7PM'
    elif time >= datetime.time(19,0) and time <= datetime.time(20,0):
        return '7PM-8PM'
    elif time >= datetime.time(20,0) and time <= datetime.time(21,0):
        return '8PM-9PM'
    elif time >= datetime.time(21,0) and time <= datetime.time(22,0):
        return '9PM-10PM'
    elif time >= datetime.time(22,0) and time <= datetime.time(23,0):
        return '10PM-11PM'
    elif time >= datetime.time(23,0) and time <= datetime.time(23,59):
        return '11PM-12AM'
    else:
        return 'other'

df3["time groups"] = df3['time'].map(time_groups)
df3
```
#### Get the value counts of "weekdays"
```python
df3['weekdays'].value_counts()
```
#### Get the value counts of "time groups"
```python
df3['time groups'].value_counts()
```
#### Renamed "time groups" to "time_groups" for manipulation purposes later
```python
df4 = df3.copy()
df5 = df4.rename(index=str, columns={"time groups": "time_groups"})
df5
```
#### Split the data frame into education and healthcare
```python
is_ed =  df5['type']== "education"
df_ed = df5[is_ed]

is_hc = df5['type']== "healthcare"
df_hc = df5[is_hc]
```
#### Notes Before Plotting
- In order to plot the heat maps(below), I had to create a "tweet efficiency score" to determine which time of day is the best to tweet. To create this score, I first took all the tweets in a given time frame on a given day of the week. I then summed all of the retweets, favorites, and replies these tweets got, and divided it by the number of total tweets in that group. I then added the total number of tweets in that group to the score again. This is because the more people are tweeting, the more people are on twitter to see other tweets.
- Because some of these numbers greatly outweighed others, I decided to group the values into buckets. The buckets differ between education and healthcare. The numbers in healthcare were much smaller than education(most likely due to twitter demographics). 
    - For education, if there were 0 tweets, the score was automatically 0. If the value was greater than or equal to 200, the score was 5. If the value was less than 200, but greater than or equal to 150, the score was 4. It keeps going down in increments of 50.
    - For healthcare, if there were 0 tweets, the score was automatically 0. If the value was greater than or equal to 50, the score was 6. If the value was less than 50, but greater than or equal to 40, the score was 5. It keeps going down in increments of 10.

#### Define the efficiency scores for both of the heat maps
```python
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday"]
time_frames = ["12AM-1AM", "1AM-2AM", "2AM-3AM", "3AM-4AM", "4AM-5AM", 
               "5AM-6AM", "6AM-7AM", "7AM-8AM", "8AM-9AM", "9AM-10AM",
               "10AM-11AM", "11AM-12PM", "12PM-1PM", "1PM-2PM", "2PM-3PM",
               "3PM-4PM", "4PM-5PM", "5PM-6PM", "6PM-7PM", "7PM-8PM",
               "8PM-9PM", "9PM-10PM", "10PM-11PM", "11PM-12AM"]

#try divinding by count out of the loop
def ed_efficiency_score(df, day, times):
    array1 = []
    #for each of the time frames
    for time in times:
        #locate the day of the week and the specific time frame, pull the data
        m1 = df.loc[(df["weekdays"]== day) & (df["time_groups"]== time),
                 ["weekdays", "time_groups", "NumRetweets", "NumFollowers",
                 "NumFavorites", "NumReplies"]]
        #If there are no tweets in that time frame
        if m1["time_groups"].count() == 0:
            instance_val = 0
            #lowest category
            sum1 = 0
        else:
            #Sum the retweets, replies, and favorites and divide by num of tweets
            instance_val = ((m1["NumRetweets"].sum()+ m1["NumFavorites"].sum() 
                             + m1["NumReplies"].sum())/m1["time_groups"].count()) + m1["time_groups"].count()
            #putting the tweets into categorical buckets
            if instance_val >= 200:
                sum1 = 5
            elif instance_val >= 150 and instance_val < 200:
                sum1 = 4
            elif instance_val >= 100 and instance_val < 150:
                sum1 = 3
            elif instance_val >= 50 and instance_val < 100:
                sum1 = 2
            else:
                sum1 = 1
        #array1.append(instance_val)
        array1.append(sum1)
    return array1

def hc_efficiency_score(df, day, times):
    array1 = []
    instance_val = 0
    #for each of the time frames
    for time in times:
        #locate the day of the week and the specific time frame, pull the data
        m1 = df.loc[(df["weekdays"]== day) & (df["time_groups"]== time),
                 ["weekdays", "time_groups", "NumRetweets", "NumFollowers",
                 "NumFavorites", "NumReplies"]]
        #If there are no tweets in that time frame
        if m1["time_groups"].count() == 0:
            #instance_val = 0
            #lowest category
            sum1 = 0
        else:
            #Sum the retweets, replies, and favorites and divide by num of tweets
            instance_val = ((m1["NumRetweets"].sum()+ m1["NumFavorites"].sum() 
                             + m1["NumReplies"].sum())/m1["time_groups"].count()) + m1["time_groups"].count()
            #putting the tweets into categorical buckets
            if instance_val >= 50:
                sum1 = 6
            elif instance_val >= 40 and instance_val < 50:
                sum1 = 5
            elif instance_val >= 30 and instance_val < 40:
                sum1 = 4
            elif instance_val >= 20 and instance_val < 30:
                sum1 = 3
            elif instance_val >= 10 and instance_val < 20:
                sum1 = 2
            else:
                sum1 = 1
        #array1.append(instance_val)
        array1.append(sum1)
    return array1
```
#### Heat map for Healthcare
```python
tweet_score = []

s_array = hc_efficiency_score(df_hc, "Sunday", time_frames)
tweet_score.append(s_array)
m_array = hc_efficiency_score(df_hc, "Monday", time_frames)
tweet_score.append(m_array)
t_array = hc_efficiency_score(df_hc, "Tuesday", time_frames)
tweet_score.append(t_array)
w_array = hc_efficiency_score(df_hc, "Wednesday", time_frames)
tweet_score.append(w_array)
th_array = hc_efficiency_score(df_hc, "Thursday", time_frames)
tweet_score.append(th_array)
f_array = hc_efficiency_score(df_hc, "Friday", time_frames)
tweet_score.append(f_array)
st_array = hc_efficiency_score(df_hc, "Saturday", time_frames)
tweet_score.append(st_array)
print(tweet_score)

fig, ax = plt.subplots(figsize=(20,50))
#(figsize=(width,height))
im = ax.imshow(tweet_score, cmap = cm.Blues)

#get rid of grid lines
ax.grid(False)

# We want to show all ticks...
ax.set_xticks(np.arange(len(time_frames)))
ax.set_yticks(np.arange(len(days_of_week)))
# ... and label them with the respective list entries
ax.set_xticklabels(time_frames)
ax.set_yticklabels(days_of_week)

plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

cbarlabel = "Efficiency Score"
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

ax.set_title("Best Times to Tweet in Healthcare")
fig.tight_layout()
plt.show()
```
#### Heat map result:
![gs1](https://github.com/44520-w19/wm-project-final-s523286/blob/master/HCheatmap.png)

#### Compare to:
![gs2](https://github.com/44520-w19/wm-project-final-s523286/blob/master/HCComparison.JPG)

### Comparison:
- The results are not the same, but they are similar. It seems that healthcare really has a wide range throughout the week where it is good to post; however, there does not seem to be many times that are significantly better than others. You can see that mid-day, as well as, mid-week seem to be the best times to post. 

#### Heat map for education
```python
tweet_score = []

s_array = ed_efficiency_score(df_ed, "Sunday", time_frames)
tweet_score.append(s_array)
m_array = ed_efficiency_score(df_ed, "Monday", time_frames)
tweet_score.append(m_array)
t_array = ed_efficiency_score(df_ed, "Tuesday", time_frames)
tweet_score.append(t_array)
w_array = ed_efficiency_score(df_ed, "Wednesday", time_frames)
tweet_score.append(w_array)
th_array = ed_efficiency_score(df_ed, "Thursday", time_frames)
tweet_score.append(th_array)
f_array = ed_efficiency_score(df_ed, "Friday", time_frames)
tweet_score.append(f_array)
st_array = ed_efficiency_score(df_ed, "Saturday", time_frames)
tweet_score.append(st_array)
print(tweet_score)

fig, ax = plt.subplots(figsize=(20,50))
#(figsize=(width,height))
im = ax.imshow(tweet_score, cmap = cm.Blues)

#get rid of grid lines
ax.grid(False)

# We want to show all ticks...
ax.set_xticks(np.arange(len(time_frames)))
ax.set_yticks(np.arange(len(days_of_week)))
# ... and label them with the respective list entries
ax.set_xticklabels(time_frames)
ax.set_yticklabels(days_of_week)

plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

cbarlabel = "Efficiency Score"
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

ax.set_title("Best Times to Tweet in Education")
fig.tight_layout()
plt.show()
```
#### Heat map result:
![gs3](https://github.com/44520-w19/wm-project-final-s523286/blob/master/Edheatmap.png)

#### Compare to:
![gs4](https://github.com/44520-w19/wm-project-final-s523286/blob/master/EdComparison.JPG)

### Comparison:
- My results here are slightly more sporadic, but a little more interesting. Education can mean multiple things. I targeted colleges because I am in college and that is where my mind went. However, this could have swung in an entirely different direction, had i targeted kindergarten through high school teachers. In the heatmap from Sprout, I see higher volumes mid-day and on weekends. This would make sense if the target audience was teachers and parents, who would be on social media most during lunch breaks and on weekends. My results are heavier in the early mornings and right after dinner time. This would make sense for colleges because many students get on social media first thing in the morning, but they also seem to get on more right after dinner when they are stuggling to get refocused into doing homework.
