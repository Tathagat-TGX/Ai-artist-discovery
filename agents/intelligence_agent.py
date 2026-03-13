import logging
import pandas as pd
import time
from tools.instagram_scraper import extract_contact_info

logging.basicConfig(level=logging.INFO)


def extract_username(url):

    if pd.isna(url):
        return None

    url = url.lower()

    # remove query parameters
    url = url.split("?")[0]

    # remove trailing slash
    url = url.rstrip("/")

    # extract username
    return url.split("/")[-1]


def run_intelligence():

    logging.info("Intelligence Agent: Analyzing artist profiles...")

    # load datasets
    df = pd.read_csv("data/artists_raw.csv")
    existing = pd.read_csv("data/starclinch_existing.csv")

    # extract usernames
    df["username"] = df["instagram"].apply(extract_username)
    existing["username"] = existing["instagram"].apply(extract_username)

    # detect already onboarded artists
    df["already_onboarded"] = df["username"].isin(existing["username"])

    # prepare enrichment columns
    emails = []
    phones = []
    websites = []
    followers_list = []
    posts_list = []
    bios = []

    # scrape instagram profiles
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

        # delay to avoid Instagram blocking
        time.sleep(2)

    # attach enriched data
    df["email"] = emails
    df["phone"] = phones
    df["website"] = websites
    df["followers"] = followers_list
    df["posts"] = posts_list
    df["bio"] = bios

    # save enriched dataset
    df.to_csv("data/artists_enriched.csv", index=False)

    logging.info("Intelligence Agent completed. Enriched dataset created.")