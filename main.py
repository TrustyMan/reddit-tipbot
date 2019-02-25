#!/usr/bin/env python2
import praw
import subprocess
import time
import os
import config

#daemon core
core = "/home/RonTipsProject/ronpaulcoind"

# bot configuration
apikey = '03LhM59M6BF4pg'
secretkey = 'wN9lCCQla2DRvkQZ60jX0-ImGEY'
botname = 'RonTips4Liberty'
bot_pw = 'Serbialovescrypto2019!'
bot_agent = 'bot by vladan'
subreddit_name = 'RonTips4Liberty'

# look for phrase and reply appropriately
def bot_login():
    print "Logging in..."
    reddit = praw.Reddit(client_id=apikey,
        client_secret=secretkey,
        username=botname,
        password=bot_pw,
        user_agent=bot_agent)
    print "Logged in!"
    return reddit

def run_bot(reddit, comments_replied_to):
    print "Searching last 1,000 comments"
    for comment in reddit.subreddit(subreddit_name).comments(limit=1000):
        # print "********************"
        # print "comment.parent_id:"
        # print comment.parent_id
        # print "comment.body:"
        # print comment.body
        # # print "comment.comments_replied_to"
        # # print comments_replied_to
        # print "comment.author"
        # print comment.author
        # print "reddit.user.me"
        # print reddit.user.me()
        # comment.mod.remove()
        if comment.id not in comments_replied_to:
            try:
                commandline = comment.body
                print 'commandline: {0}'.format(commandline)
                # print "tip:"
                # print "{0}abcdefg".format(commandline.split()[0])
                if 'tip' in commandline.lower():
                    comments_replied_to.append(comment.id)
                    with open ("comments_replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")
                    print "tip(comment)"
                    tip(reddit, comment)
                # elif commandline.split()[0] == 'gild':
                #     # gild(commandline)
            except:
                print('to frequent')
    print "Sleeping for 10 seconds..."
    #Sleep for 10 seconds...
    time.sleep(10)


def tip(reddit, comment):
    print 'it is inside tip function'
    sender = comment.author.name
    if len(comment.body.split()) == 3:
        amount = comment.body.split()[1]
        try:
            amount = float(amount)
            receiver = comment.body.split()[2]
            if receiver[0]=='/' and receiver[1]=='u' and receiver[2]=='/':
                receiver = receiver[3:]
                senderStr = 'reddit-{0}'.format(sender)
                receiverStr = 'reddit-{0}'.format(receiver)
                result = subprocess.check_output([core,"getbalance", senderStr])[:-1]
                balance = float(result)
                print "balance:"
                print balance
                print "---------------"
                print "receiver:"
                print receiverStr
                print "sender:"
                print senderStr
                if balance < amount:
                    reddit.redditor(sender).message('Tip error', "{0}, you have insufficent funds.".format(sender))
                    print "{0}, you have insufficent funds.".format(sender)
                elif receiver == sender:
                    # comment.reply("You can't tip yourself silly.")
                    reddit.redditor(sender).message('Tip error', "You can't tip yourself silly.")
                    print "You can't tip yourself silly."
                else:
                    balance = str(balance)
                    amount = str(amount)
                    # check if the receiver has wallet account
                    addresses = subprocess.check_output([core, "getaddressesbyaccount", receiverStr])
                    if len(addresses.split())==2:
                        subprocess.check_output([core,"getaccountaddress", receiverStr])
                    # send coin to custom reddit user
                    tx = subprocess.check_output([core,"move",senderStr,receiverStr,amount])[:-1]
                    # comment.reply("@{0} tipped @{1}RPC to @{2}".format(sender, amount, receiver))
                    # reddit.redditor(sender).message('Tip', "@{0} tipped @{1}RPC to @{2}".format(sender, amount, receiver))
                    reddit.redditor(receiver).message('Tipped', "{0} tipped {1}RPC to {2}".format(sender, amount, receiver))
                    print "{0} tipped {1}RPC to {2}".format(sender, amount, receiver)
            else:
                reddit.redditor(sender).message('Tip accountname format error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
                print 'Tip error: {0}'.format(comment.body)
        except ValueError:
            reddit.redditor(sender).message('Tip error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
            print 'Tip amount error: {0}'.format(comment.body)
    else:
        reddit.redditor(sender).message('Tip error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
        print 'Tip format error: {0}'.format(comment.body)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)
    return comments_replied_to

reddit = bot_login()
comments_replied_to = get_saved_comments()
# print comments_replied_to

while True:
    run_bot(reddit, comments_replied_to)