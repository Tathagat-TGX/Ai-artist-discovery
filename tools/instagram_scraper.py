import instaloader
import re
import time


L = instaloader.Instaloader()


def extract_contact_info(username):

    email = None
    phone = None
    website = None
    followers = None
    posts = None
    bio = None

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        bio = profile.biography
        followers = profile.followers
        posts = profile.mediacount
        website = profile.external_url

        
        email_match = re.search(
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", bio
        )

        if email_match:
            email = email_match.group(0)

        
        phone_match = re.search(
            r"\+?\d[\d\s\-]{8,15}", bio
        )

        if phone_match:
            phone = phone_match.group(0)

        
        time.sleep(3)

    except Exception as e:
        print(f"Instagram scraping failed for {username}")

    return email, phone, website, followers, posts, bio
