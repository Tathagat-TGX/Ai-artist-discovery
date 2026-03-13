from openai import OpenAI
import json

client = OpenAI()

def analyze_bio(bio):

    prompt = f"""
You are an AI system that extracts structured data from Instagram bios.

Extract the following fields:

category (DJ, Singer, Anchor, etc)
city
email
phone
website

Return JSON only.

Bio:
{bio}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content

    try:
        data = json.loads(text)
    except:
        data = {
            "category": None,
            "city": None,
            "email": None,
            "phone": None,
            "website": None
        }

    return data