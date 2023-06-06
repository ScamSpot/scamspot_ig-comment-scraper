from datetime import datetime
import logging
import os
from random import randint, choice
from instagrapi import Client
import json
from time import sleep, time
from instagrapi.exceptions import RateLimitError, ChallengeUnknownStep, UnknownError
import shutil
import random
import urllib.request
from instagrapi.types import Comment
from typing import List, Optional, Tuple


"""
TODO:
- Add only comment which are not from the account itself
"""
def extract_comment(data):
    """Extract comment"""
    data["has_liked"] = data.get("has_liked_comment")
    data["like_count"] = data.get("comment_like_count")
    return Comment(**data)


def get_media_comments(self, media_id: str) -> List[Comment]:
    params = None
    comments = []
    result = self.private_request(f"media/{media_id}/comments/", params)
    if result.get("comments"):
            for comment in result.get("comments"):
                comments.append(extract_comment(comment))
                
    while (result.get("has_more_comments") and result.get("next_max_id")) or (
        result.get("has_more_headload_comments") and result.get("next_min_id")
    ):
        try:
            if result.get("has_more_comments"):
                params = {"max_id": result.get("next_max_id")}
            else:
                params = {"min_id": result.get("next_min_id")}
            if not (
                result.get("next_max_id")
                or result.get("next_min_id")
                or result.get("comments")
            ):
                break

            sleep(randint(4, 14)/10)
            result = self.private_request(f"media/{media_id}/comments/", params)
            if result.get("comments"):
                for comment in result.get("comments"):
                    comments.append(extract_comment(comment))
                
        except Exception as e:
            print(e, media_id=media_id, **self.last_json)
    return comments
    
    
cl = Client()
username, password = "USER", "PASS" # change this to your username and password
try:
    print("Logging in with", username)
    cl.login(username, password)
    cl.dump_settings('modules/instagrapi/settings_' + username +'.json')
    
    # After the first successful login, you can save the settings and load them on the next login instead of loggin in again
    # cl.load_settings('data/instagrapi/settings_' + username +'.json')

except (RateLimitError, ChallengeUnknownStep, UnknownError):
    print("Error logging in, trying again")
    cl.login(username, password)
    cl.dump_settings('data/instagrapi/settings_' + username +'.json')

print("Logged in as", cl.user_info(cl.user_id).username)
    
accounts = []

# crypto company accounts
niche_accounts = ["coinbase", "binance", "coindesk", "coinmarketcap", "cryptocom", "bitcoinmagazine", "kucoinexchange", "krakenfx"]
accounts = accounts + niche_accounts

# crypto influencer accounts
niche_accounts = ["cryptoexplorer", "thecryptograph", "bitcoin.info.9", "cryptosharkk", "bitboy_crypto", "btcclicks", "cryptoaims", "cryptorelevant", "bitcoinpricedaily", "cryptoworld.info", "crypto.preneur"]
accounts = accounts + niche_accounts

# finance news / company accounts
niche_accounts = ["forbes", "insiderbusiness", "bloombergbusiness", "wsj", "businessweek", "insidertech", "financialtimes", "chartoftheday", "yahoofinance"]
accounts = accounts + niche_accounts

# finance influencer accounts
niche_accounts = ["finance_god", "financewithsharan", "brokemillennialblog", "wealthsimple", "successful_stocks", "humphreytalks", "daveramsey", "gpstephan", "kevinolearytv", "ramit"]
accounts = accounts + niche_accounts

# non finance / crypto accounts (4 athletes, 4 news pages, 4 photography pages, 4 lifestyle pages, 4 travel pages)
# non finance / crypto accounts (4 lifestyle pages, 4 art pages, 4 music pages, 4 design pages, 4 fashion pages, 4 entertainment pages, 4 technology pages, 4 gaming pages, 4 car pages, 4 cooking pages, 4 animals pages, 4 funny videos pages)
#niche_accounts = ["cristiano", "leomessi", "serenawilliams", "usainbolt"]
#accounts = accounts + niche_accounts
#niche_accounts = ["cnn", "bbcnews", "nytimes", "washingtonpost"]
#accounts = accounts + niche_accounts
#niche_accounts = ["natgeo", "stevemccurryofficial", "humansofny", "magnumphotos"]
#accounts = accounts + niche_accounts
#niche_accounts = ["natgeotravel", "lonelyplanet", "travelandleisure", "beautifuldestinations"]
#accounts = accounts + niche_accounts
#niche_accounts = []
#accounts = accounts + niche_accounts
#niche_accounts = []
#accounts = accounts + niche_accounts


print(accounts)
print(len(accounts))
print("#########################################")

comments_export = {}

# loop through all accounts
for account in accounts:
    
    #get account info
    user_id = cl.user_id_from_username(account)
    sleep(1)
    
    # get the last 20 posts of the account
    medias = cl.user_medias(user_id, amount=20)
    sleep(1)

    # loop through all posts
    for media in medias:
        media_id = media.pk
        
        print(account, (medias.index(media)+1), "/", len(medias), "- Getting data from the next media:", account, media_id)

        code = media.code
        url = media.thumbnail_url
        
        if url == None:
            url = cl.media_oembed("https://www.instagram.com/p/" + code + "/").dict()['thumbnail_url']
            sleep(1)
        
        # download image form url
        urllib.request.urlretrieve(url, "data/images/" + str(media_id) + ".jpg")
        sleep(1)
                
        # get all comments of the post
        comments = get_media_comments(cl, media.pk)
        
        # read dictionary from json file
        with open('data/comments.json', 'r', encoding='utf-8') as infile:
            comments_export = json.load(infile)

        # loop through all comments which are not empty
        for comment in comments:                        
            # check if valid comment object
            if "text" in comment.dict(): 
                comment_id = int(comment.pk)
                text = comment.text
                c_type = "unknown"
                                                                    
                username = comment.user.username
                
                # add the comment to the directory
                data = { "text" : text, "media" : media_id,
                        "account" : account, "type": c_type, "url": url,
                        "code": code }
                         
                # add the comment to the comments_export dictionary
                comments_export[comment_id] = data
                
            else:
                print("Problematic comment:")
                print(account, media_id, comment)
                
        #save the comments to a json file with utf-8 encoding
        print("Saving", len(comments), "comments to json file, currently containing", len(comments_export), "comments")
        with open('data/comments.json', 'w', encoding='utf-8') as outfile:
            json.dump(comments_export, outfile, indent=4)
        
        print("Sleeping for 2-8 seconds...")
        sleep(random.randint(2, 8))

    print("Sleeping for 0.5-2 minutes...")
    sleep(random.randint(0.5*60, 2*60))

