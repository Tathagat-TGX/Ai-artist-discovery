import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tools.google_search import search_instagram_profiles
from tools.query_generator import generate_queries

logging.basicConfig(level=logging.INFO)


def extract_category(query):
    """
     no hardcoding
     queries=[ dj , delhi dj mumbai instagram .....]
    """
    words = query.lower().split()

    ignore_words = ["instagram", "in", "for", "and", "near", "best"]

    for word in words:
        if word not in ignore_words:
            return word.title()

    return "Artist"


def extract_city(query):
    
    words = query.lower().split()

    known_locations = [
        "delhi", "mumbai", "bangalore",
        "hyderabad", "pune", "india"
    ]

    for word in words:
        if word in known_locations:
            return word.title()

    return "Unknown"


def get_instagram_name(profile_url):
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(profile_url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")

        if title:
            text = title.text
            name = text.split("(")[0].strip()
            return name

        return None

    except Exception:
        return None


def run_discovery():

    logging.info("Discovery Agent: Generating queries dynamically...")

    
    user_input = "Find artists for events in India"

    queries = generate_queries(user_input)

    logging.info(f"Generated Queries: {queries}")

    artists = []

    for query in queries:

        links = search_instagram_profiles(query)

        for link in links:

            try:
                username = link.split("/")[3]
            except:
                continue

            real_name = get_instagram_name(link)

            if not real_name:
                real_name = username.replace("_", " ").title()

            artist = {
                "name": real_name,
                "instagram": link,
                "category": extract_category(query),
                "city": extract_city(query),
                "source": "AI + Google",
                "username": username
            }

            artists.append(artist)

    df = pd.DataFrame(artists)

    df = df.drop_duplicates(subset=["instagram"])

    df.to_csv("data/artists_raw.csv", index=False)

    logging.info("Discovery Agent completed. Artists saved.")
