import os
import time

from emailParse import getEmailHtmlBody
from parseEmailSections import parseSections
from tweetFormatter import reviseArticleForTweet, trim, split_into_tweets
from twitterPost import TwitterPoster


def main():
    tweeter = TwitterPoster()

    body = getEmailHtmlBody()
    items = parseSections(body)
    #items = extract_table_data(body)
    for k, v in items.items():

        for item in v:
            url = item['url']
            article = item['description']

            revisedTweets = [url]
            tweets = split_into_tweets(article, 220)

            for tweet in tweets:
                try:
                    revisedTweet = reviseArticleForTweet(tweet)
                except:
                    print("*************  FAILED ******************")
                    continue
                revisedTweets.append(revisedTweet)

            for i in range(3):
                try:
                    tweeter.post_thread(revisedTweets)
                except (ValueError) as e:
                    print(f"❌ Error posting tweet: {str(e)}")
                    time.sleep(3)
                    continue
                break

            time.sleep(20)


# Example usage
if __name__ == "__main__":
    main()
