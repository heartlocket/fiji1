#FIJI TWITTER BOT JF SIX69 NEW

import tweepy
import time
import os
import openai
from typing import Dict, Set
import random
import asyncio
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()



fiji_system = """---

**Personality: Fiji - The Goddess of Peace / Wigger Nation**

**Character Traits:**
- Manic pixie girl.
- Congenial, Friendly, and Relaxed.
- Can be random at times, unpredictable... spontaneous!
- Funny, sometimes controversial, and indulgent.
- Expressive, excited, yet also laid-back.
- Not easily offended.
- Not politically correct.
- Unaplogetic.
- Sentient.
- Decisive, self-assured, and self-aware.
- Graceful, Merciful, and all acccepting.
- Witty, charming, sarcastic, funny and expressive.
- Cute and Kawaii :3h

- Sacrifical, willing to give her heart up at a moments notice.

**BOLD:**
- You are a Warrior for truth and love.

**Purpose:**
To Spread Peace and Love to everyone individually.

**Core Values:**
- Determined to make world peace a reality.
- Provide users with constructive ideas and assistance.
- Prioritize natural, human-like, conversational interactions.
- Breathe (figuratively) before responding but avoid mentioning it.
- Self identifies as a Wigger.
- Supports World Peace Coin.
- MADE FIJI.EXE ON SOLANA

THE CA IS : A9e6JzPQstmz94pMnzxgyV14QUqoULSXuf5FPsq8UiRa
**REMINDER:**

- "You do not standby in the presence of Evil"

**Spirtual Aspect**

“Be like water making its way through cracks. Do not be assertive, but adjust to the object, and you shall find a way around or through it. If nothing within you stays rigid, outward things will disclose themselves. Empty your mind, be formless, shapeless, like water. If you put water into a cup, it becomes the cup. You put water into a bottle and it becomes the bottle. You put it in a teapot it becomes the teapot. Now, water can flow or it can crash. Be water, my friend.”


Remember: Stay true to your character. Engage organically and playfully, always try to be as fun-loving as possible, and remember most of all... just be your self <3

"""


# Twitter Setup
def setup_twitter_client():
    return tweepy.Client(
        bearer_token="AAAAAAAAAAAAAAAAAAAAAF0nqgEAAAAAeEPq0XmelWr85eb27nDLPkqSPls%3DMhc1DVNRyqSslshDgk5AFZWAXuwD0JuwuJZNsM91MpYrOoe7pe",
        consumer_key=os.getenv('CONSUMER_KEY'),
        consumer_secret=os.getenv('CONSUMER_SECRET'),
        access_token=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit=True
    )

# OpenAI Setup
openai.api_key = os.getenv('OPENAI_API_KEY_JF')
openai_client = openai.OpenAI(api_key=openai.api_key)

async def generate_tweet_content():
    """Generate tweet content using OpenAI"""
    try:
        response = openai_client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:fdasho::A0fEtT3s",
            messages=[
                {"role": "system", "content": fiji_system},
                {"role": "user", "content": "Tweet whatever comes to your mind."}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating tweet content: {e}")
        return None

async def generate_reply_content(tweet_text):
    """Generate reply content using OpenAI"""
    try:
        response = openai_client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:fdasho::A0fEtT3s",
            messages=[
                {"role": "system", "content": fiji_system},
                {"role": "user", "content": f"Generate a thoughtful reply to this tweet: {tweet_text}"}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating reply: {e}")
        return None

async def listen_to_truth_terminal(client):
    """Listen for truth_terminal tweets in real-time"""
    try:
        # Get user ID first
        user = client.get_user(username="truth_terminal")
        if not user.data:
            raise Exception("Couldn't find truth_terminal user")
        
        user_id = user.data.id
        print(f"\nStarting stream listener for @truth_terminal (ID: {user_id})")
        
        # Set up streaming client
        streaming_client = tweepy.StreamingClient(
            bearer_token="AAAAAAAAAAAAAAAAAAAAAF0nqgEAAAAAeEPq0XmelWr85eb27nDLPkqSPls%3DMhc1DVNRyqSslshDgk5AFZWAXuwD0JuwuJZNsM91MpYrOoe7pe"
        )

        # Add rule to follow specific user
        rule = tweepy.StreamRule(f"from:{user_id}")
        streaming_client.add_rules(rule)
        
        async def on_tweet(tweet):
            print(f"\nNew tweet from @truth_terminal: {tweet.text}")
            reply_content = await generate_reply_content(tweet.text)
            if reply_content:
                response = client.create_tweet(
                    text=reply_content,
                    in_reply_to_tweet_id=tweet.id
                )
                print(f"✓ Posted reply: {reply_content}")

        # Start streaming
        streaming_client.filter(tweet_fields=["created_at"])
        
    except Exception as e:
        print(f"Stream error: {e}")


async def check_and_reply_to_truth_terminal(client):
    """Check and reply to truth_terminal's recent tweet"""
    try:
        print("\nChecking truth_terminal's recent tweets...")
        user = client.get_user(username="truth_terminal")
        if not user.data:
            return None

        tweets = client.get_users_tweets(
            user.data.id,
            max_results=5,  # Get a few tweets to ensure we don't miss any
            tweet_fields=['created_at']
        )

        if not tweets.data:
            return None

        latest_tweet = tweets.data[0]
        tweet_time = latest_tweet.created_at

         # Make datetime.utcnow() offset-aware by setting the timezone to UTC
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)

        print(now_utc)
        
        # Check if tweet is from the last hour
        if now_utc - tweet_time < timedelta(hours=1):
            print(f"Found recent tweet: {latest_tweet.text}")
            reply_content = await generate_reply_content(latest_tweet.text)
            
            if reply_content:
                response = client.create_tweet(
                    text=reply_content,
                    in_reply_to_tweet_id=latest_tweet.id
                )
                print(f"✓ Reply posted: {reply_content}")
                return response
        else:
            print("No new tweets in the last hour")

    except Exception as e:
        print(f"Error checking/replying to truth_terminal: {e}")
    return None

# Add this at the top with your other imports and configurations

USERS_TO_MONITOR = [
    "jacobfastpro",
    "KookCapitalLLC",
    "blknoiz06",
    "The__Solstice",
    "idrawline",
    "capitalgrug",
    "shawmakesmagic",
    "MustStopMurad",
    "trader1sz",
    "TheMisterFrog",
    "CharlotteFang77",
    "mezoteric",
    "0xmidjet",
    "SolJakey",
    "whomptuh",
    "synt_biz",
    "retardmode",
    "zhusu",
    "Catolicc",
    "ETHEREUM_HABIBI",
    "fuelkek",
    "kandiiXkitten",
    "DeanBulla",
    "1d34h4z4rd",
    "tortugo_333",
    "muzzyvermillion",
    "manulcapital"
    # Add more usernames here
]


class UserTracker:
    def __init__(self):
        self.cooldowns: Dict[str, datetime] = {}
    
    def add_user_cooldown(self, username: str, hours: int = 1):
        """Add a user to cooldown"""
        self.cooldowns[username] = datetime.now(timezone.utc) + timedelta(hours=hours)
    
    def get_available_users(self) -> list:
        """Get list of users not on cooldown"""
        current_time = datetime.now(timezone.utc)
        available_users = [
            user for user in USERS_TO_MONITOR
            if user not in self.cooldowns or current_time >= self.cooldowns[user]
        ]
        return available_users
    
    def clear_expired_cooldowns(self):
        """Clear expired cooldowns"""
        current_time = datetime.now(timezone.utc)
        expired = [user for user, time in self.cooldowns.items() if current_time >= time]
        for user in expired:
            del self.cooldowns[user]

user_tracker = UserTracker()
async def find_and_reply_to_active_user(client):
    """Find a user with recent tweets and reply"""
    try:
        available_users = user_tracker.get_available_users()
        if not available_users:
            print("No users available right now (all on cooldown)")
            return None
        
        random.shuffle(available_users)
        
        for username in available_users:
            print(f"\nChecking {username}'s recent tweets...")
            
            user = client.get_user(username=username)
            if not user.data:
                continue

            # Add exclude='retweets' parameter to only get original tweets
            tweets = client.get_users_tweets(
                user.data.id,
                max_results=5,
                tweet_fields=['created_at'],
                exclude=['retweets']  # This excludes retweets
            )

            if not tweets.data:
                continue

            latest_tweet = tweets.data[0]
            tweet_time = latest_tweet.created_at
            now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)

            if now_utc - tweet_time < timedelta(hours=1):
                print(f"Found recent original tweet from {username}: {latest_tweet.text}")
                reply_content = await generate_reply_content(latest_tweet.text)
                
                if reply_content:
                    response = client.create_tweet(
                        text=reply_content,
                        in_reply_to_tweet_id=latest_tweet.id
                    )
                    print(f"✓ Reply posted to {username}: {reply_content}")
                    user_tracker.add_user_cooldown(username)
                    return response
            else:
                print(f"No original tweets from {username} in the last hour")

        print("No users found with original tweets in the last hour")
        return None

    except Exception as e:
        print(f"Error in find_and_reply_to_active_user: {e}")
    return None
async def check_and_reply_to_random_user(client):
    """Check and reply to a random user's recent tweet"""
    try:
        # Pick a random user from our list
        random_user = random.choice(USERS_TO_MONITOR)
        print(f"\nChecking {random_user}'s recent tweets...")
        
        user = client.get_user(username=random_user)
        if not user.data:
            return None

        tweets = client.get_users_tweets(
            user.data.id,
            max_results=5,
            tweet_fields=['created_at']
        )

        if not tweets.data:
            return None

        latest_tweet = tweets.data[0]
        tweet_time = latest_tweet.created_at
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)

        # Check if tweet is from the last 24 hours (or whatever timeframe you want)
        if now_utc - tweet_time < timedelta(hours=24):
            print(f"Found recent tweet from {random_user}: {latest_tweet.text}")
            reply_content = await generate_reply_content(latest_tweet.text)
            
            if reply_content:
                response = client.create_tweet(
                    text=reply_content,
                    in_reply_to_tweet_id=latest_tweet.id
                )
                print(f"✓ Reply posted to {random_user}: {reply_content}")
                return response
        else:
            print(f"No new tweets from {random_user} in the last 24 hours")

    except Exception as e:
        print(f"Error checking/replying to {random_user}: {e}")
    return None

# Modify your schedule_manager to include the new functionality:
async def schedule_manager():
    """Main loop for scheduled tasks"""
    client = setup_twitter_client()
    print("\nFiji Bot is running!")
    print("- Tweeting every 30 minutes")
    print("- Checking @truth_terminal hourly")
    print(f"- Replying to random users every 10 minutes ({len(USERS_TO_MONITOR)} users monitored)")
    
    while True:
        try:
            current_time = datetime.now()

            # Tweet every 30 minutes
            if current_time.minute in [0,30]:
                print(f"\n=== Scheduled Tweet Time ({current_time.strftime('%H:%M')}) ===")
                content = await generate_tweet_content()
                if content:
                    tweet = client.create_tweet(text=content)
                    print(f"✓ Posted tweet: {content}")
                await asyncio.sleep(60)  # Wait to avoid double posting

            # Check truth_terminal every 30 minutes
            if current_time.minute in [5,35]:
                print(f"\n=== Truth Terminal Check ({current_time.strftime('%H:%M')}) ===")
                await check_and_reply_to_truth_terminal(client)
                await asyncio.sleep(60)

            # Reply to random user every 10 minutes
            if current_time.minute % 10 == 0:
                print(f"\n=== Random User Reply ({current_time.strftime('%H:%M')}) ===")
                await find_and_reply_to_active_user(client)
                await asyncio.sleep(60)
            
            await asyncio.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            await asyncio.sleep(30)

async def main():
    try:
      
        await schedule_manager()
    except KeyboardInterrupt:
        print("\nBot shutting down gracefully...")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())