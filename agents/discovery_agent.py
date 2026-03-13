import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tools.google_search import search_instagram_profiles

logging.basicConfig(level=logging.INFO)


# ---------- Helpers ----------

def extract_category(query):
    q = query.lower()

    if "dj" in q:
        return "DJ"
    if "anchor" in q or "emcee" in q:
        return "Anchor"
    if "singer" in q:
        return "Wedding Singer"

    return "Artist"


def extract_city(query):
    q = query.lower()

    if "delhi" in q:
        return "Delhi"
    if "mumbai" in q:
        return "Mumbai"
    if "india" in q:
        return "India"

    return "Unknown"


def get_instagram_name(profile_url):
    """
    Scrape the Instagram profile title to get the display name.
    Example title:
    'DJ Puneet Bhatia (@djpuneetbhatia) • Instagram photos...'
    """

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


# ---------- Discovery Agent ----------

def run_discovery():

    logging.info("Discovery Agent: Searching for artists...")

    queries = [
        "DJ Delhi Instagram",
        "wedding singer Mumbai Instagram",
        "anchor emcee India Instagram"
    ]

    artists = []

    for query in queries:

        links = search_instagram_profiles(query)

        for link in links:

            # Extract username from URL
            try:
                username = link.split("/")[3]
            except:
                continue

            # Try scraping real name
            real_name = get_instagram_name(link)

            if real_name is None or real_name == "":
                real_name = username.replace("_", " ").title()

            artist = {
                "name": real_name,
                "instagram": link,
                "category": extract_category(query),
                "city": extract_city(query),
                "source": "Google",
                "username": username
            }

            artists.append(artist)

    df = pd.DataFrame(artists)

    # Remove duplicates
    df = df.drop_duplicates(subset=["instagram"])

    df.to_csv("data/artists_raw.csv", index=False)

    print("Discovery Agent completed. Artists saved.")