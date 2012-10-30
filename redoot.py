import reddit
import requests
import urllib
import json
import auth

woot_url = "http://api.woot.com/2/events.json"

def auth():
    r = reddit.Reddit(user_agent="redoot by /u/Mob_Of_One")
    r.login(username=username, password=password)
    return r

def generate_submission(woot_product):
    return woot_product['Title']

def woot_options():
    return {"site":"www.woot.com", "key":api_key}

def generate_url():
    options = woot_options()
    return woot_url + "?" + urllib.urlencode(options)

def current_woots():
    return json.loads(requests.get(generate_url()).text)

def pred_woot(woot):
    woot_type = woot['Type']
    return woot_type == 'Daily' or woot_type == 'WootOff'

def woots_that_matter(woots):
    return filter(lambda x: pred_woot(x), woots)

def need_posted(found):
    to_be_posted = {}
    for key in found.keys():
        row = found[key]
        if not row[0]:
            to_be_posted[key] = found[key]
    return to_be_posted

def submit(client, subreddit, title):
    try:
        last_post = client.submit(subreddit, title, text="Posted by redoot, made by Mob_of_One!\nFound at http://www.woot.com/")
        if last_post and last_post.permalink:
            return last_post
    except Exception as e:
        return e

def get_woot_posts(current_woots):
    client = auth()
    woot = client.get_subreddit("woot")
    posts = woot.get_new_by_date()
    found = {}
    for woot in current_woots:
        title = generate_submission(woot)
        found[title] = [False, woot]
    for post in posts:
        if post.title in found.keys():
            print "Found: %s already" % post.title
            val = found[post.title]
            val[0] = True
            found[post.title] = val
    to_be_posted = need_posted(found)
    for key in to_be_posted.keys():
        row = to_be_posted[key]
        woot = row[1]
        site = woot['Site']
        print "Posting: %s" % key
        import sys; sys.stdout = sys.__stdout__; import ipdb; ipdb.set_trace()
        response = submit(client, "woot", key)
        print "%s" % response

if __name__ == "__main__":
    woots = woots_that_matter(current_woots())
    get_woot_posts(woots)
