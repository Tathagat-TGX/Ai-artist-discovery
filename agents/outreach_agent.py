import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)


# Function to generate personalized outreach message
def generate_message(name, category):

    return f"""
Hi {name},

This is Abhishek from StarClinch, Asia’s largest artist booking platform.

We came across your profile and believe you would be a great fit for corporate and private events booked through our platform.

We would love to invite you to join the StarClinch Club.

You can complete your profile here:
https://artist.starclinch.com

Looking forward to connecting.

Best  
Abhishek  
Artist Manager – StarClinch
"""


def run_outreach():

    logging.info("Outreach Agent generating outreach messages...")

    # Load enriched dataset
    df = pd.read_csv("data/artists_enriched.csv")

    outreach_rows = []

    for _, row in df.iterrows():

        # Skip already onboarded artists
        if row["already_onboarded"]:
            continue

        # Determine best contact method
        if pd.notna(row["email"]):
            contact_method = "email"
            contact_info = row["email"]

        elif pd.notna(row["phone"]):
            contact_method = "whatsapp"
            contact_info = row["phone"]

        else:
            contact_method = "instagram_dm"
            contact_info = row["instagram"]

        # Generate outreach message
        message = generate_message(row["name"], row["category"])

        # -------- Intelligent Priority Scoring --------
        score = 0

        # followers signal
        if pd.notna(row.get("followers")):
            score += min(int(row["followers"]) // 1000, 50)

        # email bonus
        if pd.notna(row["email"]):
            score += 20

        # website bonus
        if pd.notna(row["website"]):
            score += 10

        priority_score = score
        # ----------------------------------------------

        outreach_rows.append({
            "name": row["name"],
            "category": row["category"],
            "contact_method": contact_method,
            "contact_info": contact_info,
            "priority_score": priority_score,
            "message": message
        })

    # Convert to dataframe
    out_df = pd.DataFrame(outreach_rows)

    # Sort by priority (highest first)
    out_df = out_df.sort_values(by="priority_score", ascending=False)

    # Save outreach queue
    out_df.to_csv("data/outreach_queue.csv", index=False)

    logging.info("Outreach queue generated successfully.")