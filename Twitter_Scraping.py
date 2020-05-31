import json
import tweepy
import requests
import os
from os import walk
import time

#change directory 

main_path = "path you want to save your images"

os.chdir(main_path)

#check if Twitter_images folder exists 

if not os.path.exists(main_path + "/" + "Twitter_images"):
    
    #create new folder if doesn't exists 

    os.makedirs("Twitter_images")
    os.chdir(main_path + "/" + "Twitter_images")
    current_path = main_path + "/" + "Twitter_images/"

else:

    os.chdir(main_path + "/" + "Twitter_images")
    current_path = main_path + "/" + "Twitter_images/"

#create dictionary that store your twitter credentials 

twitter_credentials = dict()


#Enter the keys 

twitter_credentials['CONSUMER_KEY'] = 'your twitter consumer key'
twitter_credentials['CONSUMER_SECRET'] = 'your twitter consumer secret'
twitter_credentials['ACCESS_KEY'] = 'your twitter access key'
twitter_credentials['ACCESS_SECRET'] = 'your twitter access secret'

with open("twitter_credentials.json" , "w") as credentials:
    json.dump(twitter_credentials, credentials, indent=1)


with open("twitter_credentials.json") as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

def get_all_tweets(screen_name):

    #Authorization and initialization

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key,access_secret)
    api = tweepy.API(auth)

    #initialization of a list to store all tweets

    alltweets = []

    new_tweets = api.user_timeline(screen_name=screen_name,count=200,include_rts=False,exclude_replies=True)

    alltweets.extend(new_tweets)

    # save id of 1 less than the oldest tweet

    oldest_tweet = alltweets[-1].id - 1

    # grabbing tweets till none are left

    while len(new_tweets) > 0:

        # The max_id param will be used subsequently to prevent duplicates

        new_tweets = api.user_timeline(screen_name=screen_name,
        count=200, include_rts=False, exclude_replies=True , max_id=oldest_tweet)
        print(len(new_tweets))

        # save most recent tweets

        alltweets.extend(new_tweets)

        # id is updated to oldest tweet - 1 to keep track

        oldest_tweet = alltweets[-1].id - 1
        print ('...%s tweets have been downloaded so far' % len(alltweets))

    #print ("{} tweets have been downloaded".format(len(alltweets)))

    media_url = []

    if not os.path.exists(screen_name):

        os.makedirs(screen_name)
        os.chdir(current_path + screen_name)

        #create a loop that stores existing files 
        filenames = []
        for (dirpath, dirnames , filenames) in walk(current_path + screen_name):
            print(dirpath, dirnames, filenames)
            filenames.extend(filenames)
    else:

        os.chdir(current_path + screen_name)

        #create a loop that stores existing files 
        filenames = []
        for (dirpath, dirnames, filenames) in walk(current_path + screen_name):
            print(dirpath, dirnames, filenames)
            filenames.extend(filenames)

    for status in alltweets:
        media = status.entities.get("media",[])
        if len(media) > 0:
            media_url.append(media[0]['media_url'])


    def download_images(media_url):

        for img_link in media_url:

            name = img_link.split("/")[-1]

            existing_filename = ""

            for filename in filenames:
                
                #if file already exist, skip the download
                if name == filename: 
                    existing_filename = filename 
                    break

            if name == existing_filename:
                continue 
            
            img_response = requests.get(img_link)
            
            with open(name,"wb") as wf:
                wf.write(img_response.content)

            print("{} has been downloaded.".format(name))

    
    download_images(media_url)

    print("All images have been downloaded successfully")


if __name__ == "__main__":

    #get execution start time 
    start_time = time.time()

    get_all_tweets(input("Enter screenname you would like to scrape their images: "))

    #show total execution time 
    print("--- %s seconds ---" % (time.time() - start_time))




            
            
    
  


