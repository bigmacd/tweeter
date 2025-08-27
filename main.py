import os
import time

from emailParse import getEmailHtmlBody
from parseEmailSections import parseSections
from tweetFormatter import reviseArticleForTweet, trim
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

            print('-' * 60)
            print(f"url: {url}")
            print(f"article: {article}")

            try:
                tweet = reviseArticleForTweet(article)
            except:
                print("*************  FAILED ******************")
                continue

            print(f"Revised: {tweet}")
            print('-' * 60)


            if len(tweet) > 280:
                tweet = trim(tweet)

            for i in range(3):
                try:
                    tweeter.post_tweet(tweet)
                except (ValueError) as e:
                    print(f"❌ Error posting tweet: {str(e)}")
                    time.sleep(3)
                    continue
                break

            time.sleep(10)

# Example usage
if __name__ == "__main__":
    main()