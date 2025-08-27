
import os

from openai import OpenAI
    

def trim(tweet):
    # get the hashtags starting from the end (in case there is a # in the article)
    lastTag = len(tweet)
    while True:
        tag = tweet[:lastTag].rfind('#')
        if tag == -1:
            break
        lastTag = tag - 1



    if lastTag == -1:
        hashtags = None
        hashtagLength = len(tweet)
    else:
        hashtags = tweet[lastTag:]
        hashtagLength = len(hashtags)

    tweetLen = len(tweet[:lastTag])
    while (tweetLen + hashtagLength) > 280:
        lastTag = tweet[:lastTag].rfind(' ')
        tweetLen = len(tweet[:lastTag])

    return tweet[:lastTag] + hashtags


def reviseArticleForTweet(article: str) -> str:
    client = OpenAI(
            api_key = os.environ.get("openaiApiKey", None),
    )

    messages = []
    messages.append({"role": "system", "content": "You are a helpful assistant that revises text to fit into a single tweet of 280 characters."})
    messages.append({"role": "user", "content": article})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=70
        )
        tweet = response.choices[0].message.content.strip()
        return tweet 
    except Exception as e: 
        print(f"Error revising article: {e}")
        raise

if __name__ == "__main__":

    ######################################
    # Test Code
    articles = [
        """article: Hundreds of TeslaMate setups are exposed online with no authentication, 
        leaking GPS, vehicle, and charging data. Attackers can track vehicle locations and 
        patterns, presenting serious privacy and physical security risks for Tesla owners. 
        The fix is to secure deployments with authentication and firewalls.
        """,

        '''article: Researchers found critical vulnerabilities in Axis Communications' 
        surveillance camera systems that could allow hackers to remotely access, control, 
        and disable cameras at thousands of organizations. Axis has released security patches, 
        and users are advised to update their systems right away to prevent exploitation.''',
        
        '''article: Security researchers found malicious npm packages "solana-pump-test" and 
        "solana-spl-sdk" posing as Solana SDK components but stealing cryptocurrency data from 
        Russian developers. These infostealers send data to US servers, suggesting possible 
        state-sponsored activity targeting Russia's ransomware ecosystem relying on cryptocurrency. 
        The attacker, using the handle "cryptohan," promotes these packages that expose password files, 
        exchange credentials, and wallet data from infected systems.
        ''',

        '''article: A federal class-action lawsuit accuses Otter.ai of violating privacy laws by 
        secretly recording and using meeting participants' voices to train its AI without consent, 
        particularly affecting non-account holders who join virtual meetings. The Otter Notetaker 
        bot can automatically join meetings linked to workplace calendars and record all participants, 
        with the lawsuit citing cases where sensitive business discussions were inadvertently captured 
        and shared. With 25 million users and over 1 billion meetings processed, the case could set a 
        precedent for AI transcription services' consent requirements and data usage practices.
        '''
        ]

    testMessages = [
    #                                                                                                       1                                                                                                   2                                                                                                   3     
    #             1         2         3         4         5         6         7         8         9         0         1         2         3         4         5         6         7         8         9         0         1         2         3         4         5         6         7         8         9         0
    #    123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
            "Researchers found critical vulnerabilities in Axis Communications' surveillance camera systems, allowing hackers to remotely access, control, and disable cameras at thousands of organizations. Axis released security patches; users must update systems immediately to prevent exploitation. #CyberSecurity",
            "Researchers found critical vulnerabilities in Axis Communications' surveillance camera systems, allowing hackers to remotely access, control, and disable cameras at thousands of organizations. Axis released security patches; users must update systems immediately to prevent exploitation.",
            "Researchers found critical vulnerabilities in Axis Communications' surveillance camera systems, allowing hackers to remotely access, control, and disable cameras at thousands of organizations. Axis released security patches; users must update systems immediately to prevent exploitation. #Cyber #Security",
            "Researchers found critical vulnerabilities in Axis Communications' surveillance camera systems, allowing hackers to remotely access, control, and disable cameras at thousands of organizations. Axis released security patches; users must update systems immediately to prevent exploitation. #CyberSecurity"
    ]

    for message in testMessages:
        x = trim(message)
        print(f"Trimmed Message: {x}, Trimmed Message Length: {len(x)}")

    # End of Test Code
    ###############################################################

    for article in articles:
        try:
            tweet = reviseArticleForTweet(article)
            print(f"Revised: {tweet}")
        except Exception as e:
            print(f"Error revising article: {e}")
            continue

        if len(tweet) > 280:
            tweet = trim(tweet)
            print(f"Tweet is too long {len(tweet)}, skipping...")
            continue # hashtags are at tweet[hash:]
