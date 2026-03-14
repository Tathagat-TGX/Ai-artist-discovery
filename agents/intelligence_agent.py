import logging
import pandas as pd
import time
from tools.instagram_scraper import extract_contact_info

logging.basicConfig(level=logging.INFO)


def extract_username(url):

    if pd.isna(url):
        return None

    url = url.lower()

    
    url = url.split("?")[0]

    
    url = url.rstrip("/")

   
    return url.split("/")[-1]


def run_intelligence():

    logging.info("Intelligence Agent: Analyzing artist profiles...")

    
    df = pd.read_csv("data/artists_raw.csv")
    existing = pd.read_csv("data/starclinch_existing.csv")

    
    df["username"] = df["instagram"].apply(extract_username)
    existing["username"] = existing["instagram"].apply(extract_username)

    
    df["already_onboarded"] = df["username"].isin(existing["username"])

    
    emails = []
    phones = []
    websites = []
    followers_list = []
    posts_list = []
    bios = []

    
    for _, row in df.iterrows():

        username = row["username"]

        try:
            email, phone, website, followers, posts, bio = extract_contact_info(username)

        except Exception as e:

            print(f"Failed to scrape {username}")

            email = None
            phone = None
            website = None
            followers = None
            posts = None
            bio = None

        emails.append(email)
        phones.append(phone)
        websites.append(website)
        followers_list.append(followers)
        posts_list.append(posts)
        bios.append(bio)

        
        time.sleep(2)

    
    df["email"] = emails
    df["phone"] = phones
    df["website"] = websites
    df["followers"] = followers_list
    df["posts"] = posts_list
    df["bio"] = bios

    
    df.to_csv("data/artists_enriched.csv", index=False)

    logging.info("Intelligence Agent completed. Enriched dataset created.")
