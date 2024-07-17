#!/usr/bin/python
# -*- coding: utf-8 -*-
#https://github.com/wanghaisheng/capcut-tweets-capture/new/main

import pathlib
import time
import os
import pandas as pd
from dotenv import load_dotenv
# noinspection PyPackageRequirements
from tweety import Twitter
from tweety.filters import SearchFilters
from tweety.types import Tweet
import emoji
from utils.utils import enable_max_pandas_display_size, compare_pandas_dataframes
# import requests
# import snscrape.modules.twitter as sntwitter


# old code with the now outdated snscrape module:
"""
##################### Configuration #####################
GAME = "Cyberpunk 2077"
start_date = "2020-12-09"
# end_date = "2020-12-31"
QUERY = f'{GAME} ("review bomb * " OR "sabotag*" OR "fake * " OR "boycott * ") since:{start_date}'  # until:{end_date}'

#########################################################


# probably outdated with the new twitter restrictions (must be logged in to view content) and rate limits :(
def get_tweets(game=GAME, q=QUERY):
    # For how to formulate queries, see https://twitter.com/search-advanced.
    # Use "..." for exact search, (#...) to search for hashtags, until: and since: for time search, from: for tweets
    # from user, -... to exclude words, AND / OR for boolean search and lang:en to search only in specific language.
    max_tweets = 100
    tweets_list = []

    print(f"\nScraping tweets for game \"{game}\" and query \"{q}\" ...")

    # Using TwitterSearchScraper to scrape data and append tweets to list
    twitter_gen = sntwitter.TwitterSearchScraper(q).get_items()
    # itertools.islice(twitter_gen, max_tweets)
    for i, tweet in enumerate(twitter_gen):
        if i > max_tweets:
            break
        tweets_list.append([tweet.id, tweet.date, tweet.rawContent, tweet.likeCount, tweet.replyCount,
                            tweet.retweetCount, tweet.hashtags, tweet.media, tweet.links, tweet.inReplyToTweetId,
                            tweet.inReplyToUser, tweet.mentionedUsers, tweet.retweetedTweet, tweet.url, tweet.user.id,
                            tweet.user.username, tweet.user.displayname, tweet.user.followersCount, tweet.user.created])

    print(f"\nFinished scraping tweets for game \"{game}\"")

    tweets_df = pd.DataFrame(tweets_list,
                             columns=['id', 'date', 'content', 'likeCount', 'replyCount', 'retweetCount', 'hashtags',
                                      'media', 'links', 'inReplyToTweetId', 'inReplyToUser', 'mentionedUsers',
                                      'retweetedTweet', 'url', 'user_id', 'user_name', 'user_displayname',
                                      'user_followersCount', 'user_created'])
    print(tweets_df.head(5))
    # time_period = f"{start_date}-{end_date}" if (start_date is not None and end_date is not None) else "all_time"
    tweets_df.to_csv(f'tweets_{game}_{start_date}-now.csv', index=False)
"""

"""
def use_twitter_syndication():
    # TODO how does this work ? syndication seems to cross-post tweets but no idea how i can send a query there ...
    url = "https://cdn.syndication.twimg.com/tweet-result"

    querystring = {"id": "1652193613223436289", "lang": "en"}
    # querystring = {"q": "Cyberpunk 2077", "lang": "en"}  # does not work

    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://platform.twitter.com",
        "Connection": "keep-alive",
        "Referer": "https://platform.twitter.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    pprint.pprint(response.text)
    print("\n##############################################\n")
    pprint.pprint(response.json)
"""

"""
async def test_twscrape():
    query = '(Hogwarts Legacy) AND ("review bomb*" OR "ReviewBomb*" OR "review-bomb*" OR "fake review*" OR spam OR ' \
            'fake") lang:en since:2023-02-06 until:2023-02-24'

    api = API()

    # Add accounts
    # TODO login does not work for some reason
    await api.pool.add_account("MM", "masterarbeit.1", "Michael.Meckl@stud.uni-regensburg.de", "Murtagh.1899#")
    await api.pool.login_all()

    # tweet_list = await gather(api.search(query, limit=20))  # list[Tweet]
    # await api.tweet_details(tweet_id)  # Tweet
    # await api.user_by_id(user_id)  # User

    # to use break in the async loop, use this construct:
    # from contextlib import aclosing
    # async with aclosing(api.search(query, limit=20)) as gen:
    #     async for tweet in gen:
    #         if tweet.id < 200:
    #             break

    q = "Hogwarts Legacy AND review bomb lang:en since:2023-02-06 until:2023-02-24"
    async for tweet in api.search(q, limit=20):
        print(tweet.id, tweet.user.username, tweet.rawContent)
        print(tweet.dict())
"""


def analyze_emojis(text_with_emojis: str):
    # convert all emojis to text and return all found emojis as a separate list
    number_emojis = emoji.emoji_count(text_with_emojis, unique=False)
    if number_emojis == 0:
        return text_with_emojis, []

    emoji_list = [found_emoji.chars for found_emoji in
                  emoji.analyze(text_with_emojis, non_emoji=False, join_emoji=True)]

    # print(emoji.distinct_emoji_list(text_with_emojis))
    cleaned_text = emoji.demojize(text_with_emojis, language='alias')
    return cleaned_text, emoji_list


def process_tweet_list(tweets: list[Tweet]):
    tweets_list = []

    tweet: Tweet
    for tweet in tweets:
        try:
            print(tweet)
            # if tweet.is_retweet:
            #     continue  # skip all retweets by default ?
            # print(tweet.comments)

            # todo every tweet has 0 comments even if it's not true :(
            if len(tweet.comments) > 0:
                print("Comments:")
                for comment in tweet.iter_comments(pages=1, wait_time=2):
                    # TODO what to do with comments? add all top-level replies as well? only add the ones
                    #  containing special keywords in their text ?
                    # tweets_list.append(...)
                    print(comment)
                    break  # for testing only the first
                print(f"\nFinished extracting comments for tweet {tweet}")

            cleaned_text, emojis_list = analyze_emojis(tweet.text)

            tweets_list.append(
                [tweet.id, tweet.date, cleaned_text, emojis_list, tweet.likes, tweet.reply_counts, tweet.retweet_counts,
                 tweet.hashtags, tweet.user_mentions, tweet.replied_to, tweet.retweeted_tweet,
                 tweet.quoted_tweet, len(tweet.comments),
                 tweet.author.id, tweet.author.name, tweet.author.username, tweet.author.followers_count,
                 tweet.author.friends_count, tweet.author.verified, tweet.author.created_at]
            )
        except Exception as e:
            print("ERROR in processing tweet: ", e)
            continue

    result_df = pd.DataFrame(tweets_list,
                             columns=['id', 'created_at', 'content', 'used_emojis', 'like_count', 'reply_count',
                                      'retweet_count', 'hashtags', 'mentioned_users', 'is_reply_to_tweet',
                                      'retweeted_tweet', 'quoted_tweet', 'num_comments',
                                      'author_id', 'author_name', 'author_username', 'author_followers_count',
                                      'author_friends_count', 'author_verified', 'author_created_at'])
    print(f"{result_df.head(3)} \n")
    return result_df


def extract_tweets_loop(app: Twitter, query: str, csv_file_path: str):
    cursor = None
    load_more = True
    # num_retries = 0
    # max_retries = 3

    while load_more:
        try:
            # ! ca. 820 tweets can be fetched per 15 min interval before getting rate-limited
            tweets = app.search(query, pages=1, wait_time=2, cursor=cursor, filter_=SearchFilters.Latest())
            print(f"\n{tweets}")
            cursor = tweets.cursor
            print("Cursor: ", cursor)

            #  reset retries
            # num_retries = 0

            tweets_df = process_tweet_list(tweets)
            tweets_df.to_csv(csv_file_path, mode="a", index=False, header=not os.path.exists(csv_file_path))

            if not tweets.is_next_page:
                load_more = False

            while tweets.is_next_page:
                print("\nLoading next page ...")
                time.sleep(3)
                next_page = tweets.get_next_page()
                # pprint.pprint(next_page)

                if len(next_page) == 0:
                    load_more = False
                    break

                cursor = tweets.cursor
                print("next page cursor: ", cursor)

                tweets_df = process_tweet_list(next_page)
                # only append to csv file so the already fetched tweets won't be overriden
                tweets_df.to_csv(csv_file_path, mode="a", index=False, header=not os.path.exists(csv_file_path))

        except Exception as e:
            print("ERROR while fetching tweets: ", e)

            if str(e).startswith("Unknown"):
                # try again in a few minutes as we were probably rate-limited
                """
                if num_retries < max_retries:
                    # start with 3 minutes and double each time until max reached
                    wait_time = 180 + num_retries * 180
                    print(f"Unknown error occurred! Waiting for {int(wait_time / 60)} minutes before retrying ...")
                    print("Current cursor: ", cursor)
                    time.sleep(wait_time)
                    num_retries += 1
                    print("Trying again ...")
                else:
                    load_more = False
                    print("\nStopping because max_retries exceeded!")
                """

                print("Unknown error occurred! Waiting for 15 minutes before retrying ...")
                print("Current cursor: ", cursor)
                time.sleep(900)
                print("Trying again ...")
            else:
                load_more = False


def get_tweets_tweety():
    # the until - date is always exclusive! (i.e. the day after)
    # general queries for review bombing and fake reviews
    games_general = {
        "Cyberpunk 2077": [
            'Cyberpunk 2077 review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR'
            ' manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
            # "Cyberpunk 2077 review since:2020-12-09 until:2021-01-01",
            # "Cyberpunk 2077 review since:2022-03-01 until:2022-04-01",
            # "Cyberpunk 2077 review since:2023-01-01 until:2023-02-01",
        ],
        "Witcher": [
            'Witcher review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR'
            ' manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Gwent": [
            '(Gwent OR Thronebreaker) review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR '
            'controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "STALKER": [
            '("STALKER" OR "S.T.A.L.K.E.R") review (bomb OR bombs OR bombing OR boycott OR boycotting OR '
            'controvers OR controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR '
            'hate)',
        ],
        "Frostpunk": [
            'Frostpunk review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR'
            ' manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "CDPR": [
            '("CD Projekt Red" OR "CD Project Red" OR CDPR) review (bomb OR bombs OR bombing OR boycott OR boycotting '
            'OR controvers OR controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR '
            'hate)',
        ],
        "Ukraine_Russia_ReviewBomb": [
            '(russia OR ukraine) AND review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR '
            'controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Borderlands 3": [
            'Borderlands review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR'
            ' manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
            # 'Borderlands review since:2019-04-01 until:2019-05-01',
            # 'Borderlands review since:2020-03-01 until:2020-04-01',
        ],
        "Metro Exodus": [
            '("metro exodus" OR metro) AND review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR '
            'controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Firewatch": [
            'Firewatch review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR '
            'manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Overwatch 2": [
            'Overwatch 2 review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR '
            'manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "The Elder Scrolls V Skyrim": [
            'Skyrim review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers OR '
            'controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Bethesda Creation Club": [
            '(Skyrim OR "Fallout 4" OR "creation club") AND review (bomb OR bombs OR bombing OR boycott OR boycotting '
            'OR controvers OR controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR '
            'hate)',
        ],
        "Grand Theft Auto V": [
            '("Grand Theft Auto V" OR "Grand Theft Auto 5" OR GTA5 OR GTAV) AND review (bomb OR bombs OR bombing OR '
            'boycott OR boycotting OR controvers OR controversy OR manipulate OR manipulation OR fake OR sabotage OR '
            'sabotaging OR spam OR hate)',
        ],
        "Total War Rome II": [
            '("Total War Rome" OR "Rome II" OR TW:RII) AND review (bomb OR bombs OR bombing OR boycott OR boycotting '
            'OR controvers OR controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR '
            'hate)',
        ],
        "Mortal Kombat 11": [
            '("Mortal Kombat 11" OR MK11) AND review (bomb OR bombs OR bombing OR boycott OR boycotting OR controvers '
            'OR controversy OR manipulate OR manipulation OR fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
        "Assassins Creed Unity": [
            '("assassins creed unity" OR "assassin\'s creed unity" OR "AC Unity" OR "AC:Unity") AND review (bomb OR '
            'bombs OR bombing OR boycott OR boycotting OR controvers OR controversy OR manipulate OR manipulation OR '
            'fake OR sabotage OR sabotaging OR spam OR hate)',
        ],
    }

    # queries specifically for certain review bombings
    games_specific = {
        "Cyberpunk 2077": [
            '"Cyberpunk 2077" (lie OR fraud OR scam OR broken OR disappoint OR disappointment OR disappointing)'
            ' since:2020-12-09 until:2021-01-01',
            '"Cyberpunk 2077" (negative OR hate OR review) (lie OR fraud OR scam OR broken OR disappoint OR'
            ' disappointment OR disappointing) since:2020-12-09 until:2021-01-01',
            '"Cyberpunk 2077" (award OR "Steam Awards" OR "Labor of Love") since:2023-01-01 until:2023-02-01',
        ],
        "Ukraine_Russia_ReviewBomb": [
            '(ReviewBomb OR "review bombing" OR "negative game review") AND (russia OR ukraine) since:2022-02-24'
            ' until:2022-04-01',
            '("CD Projekt Red" OR "CD Project Red" OR CDPR OR Witcher OR Gwent OR Thronebreaker OR "Cyberpunk 2077" '
            'OR Frostpunk OR ("STALKER" OR "S.T.A.L.K.E.R")) AND (russia OR ukraine) since:2022-02-24 until:2022-04-01',
            '("CD Projekt Red" OR "CD Project Red" OR CDPR OR Witcher OR Gwent OR Thronebreaker OR "Cyberpunk 2077"'
            ' OR Frostpunk OR ("STALKER" OR "S.T.A.L.K.E.R")) AND (sales OR support) AND (russia OR ukraine)'
            ' since:2022-02-24 until:2022-04-01',
        ],
        "Borderlands 3": [
            '(borderlands 3) AND ("epic store" OR "epic games") since:2019-04-01 until:2019-05-01',
            '(borderlands 3) AND ("epic store" OR "epic games") since:2020-03-01 until:2020-04-01',
        ],
        "Metro Exodus": [
            '("metro exodus" OR metro) AND ("epic store" OR "epic games") since:2019-01-20 until:2019-03-01',
            '("metro exodus" OR metro) AND ("epic store" OR "epic games") since:2020-02-01 until:2020-03-01',
        ],
        "Firewatch": [
            'Firewatch (DCMA OR pewdiepie) since:2017-09-10 until:2017-11-01',
        ],
        "Overwatch 2": [
            '"Overwatch 2" (promise OR shutdown OR greed OR monetization OR microtransaction) since:2023-08-10 '
            'until:2023-09-01',
            '"Overwatch 2" (promise OR shutdown OR greed OR monetization OR microtransaction) since:2022-10-04 '
            'until:2022-11-01',
            '"Overwatch 2" (review (bomb OR bombs OR bombing)) since:2023-08-10 until:2023-09-01',
            '"Overwatch 2" (review (bomb OR bombs OR bombing)) since:2022-10-04 until:2022-11-01',
        ],
        "The Elder Scrolls V Skyrim": [
            'Skyrim ("paid mod" OR bethesda OR greed) since:2015-04-22 until:2015-05-23',
        ],
        "Bethesda Creation Club": [
            '(Skyrim OR "Fallout 4") AND ("creation club" OR "paid mod" OR bethesda OR greedy) since:2017-08-27 '
            'until:2017-12-01',
        ],
        "Grand Theft Auto V": [
            '("Grand Theft Auto V" OR "Grand Theft Auto 5" OR GTA5 OR GTAV) AND (openiv OR ban OR "cease-and-desist" '
            'OR mod OR "take-two" OR "take 2") since:2017-06-13 until:2017-07-14',
        ],
        "Total War Rome II": [
            '("Total War Rome" OR "Rome II" OR TW:RII) AND (accurate OR accuracy OR "female general" OR feminist '
            'OR agenda) since:2018-09-21 until:2018-11-01',
            '("Total War Rome" OR "Rome II" OR TW:RII) AND (accurate OR accuracy OR "female general" OR "female '
            'spawn" OR feminist OR agenda OR politic) since:2018-09-21 until:2018-11-01',
            '("Total War Rome" OR "Rome II" OR TW:RII) AND (accurate OR accuracy OR "female general" OR "female '
            'spawn" OR feminist OR agenda)',
        ],
        "Mortal Kombat 11": [
            '("Mortal Kombat 11" OR MK11) AND (microtransaction OR sjw OR propaganda OR woke OR ending) '
            'since:2019-04-21 until:2019-05-22',
        ],
        "Assassins Creed Unity": [
            '("assassins creed unity" OR "assassin\'s creed unity" OR "AC Unity" OR "AC:Unity") AND ("notre-dame" OR '
            'fire OR donation OR positive) since:2019-04-16 until:2019-05-20',
        ],
    }

    # TODO apparently exact search with quotation marks does not work anymore (April 2024)  -> can this be fixed?

    #################################################################
    # twitter authentication
    load_dotenv(dotenv_path="twitter_credentials.env")

    app = Twitter("session")
    app.sign_in(os.getenv('ACCOUNT_1_USERNAME'), os.getenv('ACCOUNT_1_PASSWORD'))  # test account
    # app.sign_in(os.getenv('ACCOUNT_2_USERNAME'), os.getenv('ACCOUNT_2_PASSWORD'))  # test account 2
    app.connect()

    use_single_query = False
    use_specific_queries = True
    #################################################################

    if use_single_query:
        # only for easy testing with a specific game and query
        game = "Cyberpunk 2077"
        query = "Cyberpunk 2077 since:2023-08-01"
        print(f"Running single query \"{query}\"\n")

        csv_out_path = f"tweets_{game}.csv"
        extract_tweets_loop(app, query, csv_out_path)
    else:
        # create a new folder for the downloaded tweets
        Output_Folder = pathlib.Path(__file__).parent / "extracted_tweets"
        if not Output_Folder.is_dir():
            Output_Folder.mkdir()

        games = games_specific if use_specific_queries else games_general
        for game in games:
            queries = games[game]
            for i, query in enumerate(queries):
                print(f"Searching with query: \"{query}\"\n")
                query_tag = "specific" if use_specific_queries else "general"
                csv_out_path = Output_Folder / f"tweets_{game}--query_{i+1}--{query_tag}.csv"

                extract_tweets_loop(app, query, csv_out_path)
                print(f"\nFinished with query \"{query}\" for game {game}\n######################################\n")

            print(f"\nFinished with game {game}\n######################################\n")


"""
def compare_result_dataframes():
    df_2 = pd.read_csv("./tweets_Metro Exodus_query_0.csv")
    df_3 = pd.read_csv("./tweets_Metro Exodus_query_1.csv")
    df_4 = pd.read_csv("./tweets_Metro Exodus_query_2.csv")
    compare_pandas_dataframes(df_2, df_3, merge_column="id", df_1_name="df_2-3", df_2_name="df_3-2")
    compare_pandas_dataframes(df_2, df_4, merge_column="id", df_1_name="df_2-4", df_2_name="df_4-2")
"""


if __name__ == "__main__":
    enable_max_pandas_display_size()
    get_tweets_tweety()
