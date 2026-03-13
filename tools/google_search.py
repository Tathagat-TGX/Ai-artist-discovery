from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_instagram_profiles(query):

    instagram_links = []

   
    for start in range(0, 50, 10):

        params = {
            "engine": "google",
            "q": query,
            "start": start,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            link = result.get("link")

            if link and "instagram.com" in link and not any(x in link for x in ["/p/", "/reel/", "/tv/"]):
                instagram_links.append(link)

   
    return list(set(instagram_links))