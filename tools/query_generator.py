from openai import OpenAI
import os
from dotenv import load_dotenv
import ast
import random

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_queries(user_input):
   

    prompt = f"""
    You are an expert talent discovery assistant.

    Based on this input:
    "{user_input}"

    Generate 5 to 8 diverse Google search queries to discover artists on Instagram.

    The queries should:
    - Cover different artist categories (DJ, singer, anchor, band, performer, etc.)
    - Include different cities or locations
    - Be suitable for Google search

    Return ONLY a valid Python list of strings.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()

        
        queries = ast.literal_eval(content)

        
        if not isinstance(queries, list):
            raise ValueError("Invalid response format")

        return queries

    except Exception:
       

        categories = [
            "DJ", "wedding singer", "anchor",
            "emcee", "live band", "performer"
        ]

        cities = [
            "Delhi", "Mumbai", "Bangalore",
            "Hyderabad", "Pune", "India"
        ]

        queries = []

        for category in categories:
            city = random.choice(cities)
            queries.append(f"{category} {city} Instagram")

        return queries
