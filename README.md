🎧 AI Artist Discovery & Outreach System

An AI-powered multi-agent pipeline that automatically discovers artists online, analyzes their profiles, and generates prioritized outreach messages.

The system simulates how a talent discovery team (e.g., event platforms, talent marketplaces) can scale artist discovery and onboarding using automation and intelligent prioritization.

🚀 Quick Start (3 Commands)
git clone https://github.com/Tathagat-TGX/Ai-artist-discovery.git
cd Ai-artist-discovery
pip install -r requirements.txt
python run_pipeline.py

Optional: run the dashboard

streamlit run dashboard.py
🧠 System Overview

The system uses three specialized agents, each responsible for a stage in the discovery pipeline.

Artist Discovery
      ↓
Profile Intelligence
      ↓
Outreach Generation

Each stage processes data and passes it to the next agent.

🏗 Architecture
                Google Search
                     │
                     ▼
        ┌─────────────────────────┐
        │   Agent 1: Discovery    │
        │ Find artist profiles    │
        └──────────┬──────────────┘
                   │
                   ▼
        ┌─────────────────────────┐
        │ Agent 2: Intelligence   │
        │ Extract contact details │
        │ & filter duplicates     │
        └──────────┬──────────────┘
                   │
                   ▼
        ┌─────────────────────────┐
        │  Agent 3: Outreach      │
        │ Generate messages &     │
        │ prioritize artists      │
        └──────────┬──────────────┘
                   │
                   ▼
            Outreach Queue
📁 Repository Structure
Ai-artist-discovery
│
├── agents
│   ├── discovery_agent.py
│   ├── intelligence_agent.py
│   └── outreach_agent.py
│
├── tools
│   ├── google_search.py
│   ├── instagram_scraper.py
│   └── llm_analyzer.py
│
├── data
│   ├── artists_raw.csv
│   ├── artists_enriched.csv
│   ├── outreach_queue.csv
│   └── starclinch_existing.csv
│
├── dashboard.py
├── run_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Full Setup & Run
1️⃣ Clone repository
git clone https://github.com/Tathagat-TGX/Ai-artist-discovery.git
cd Ai-artist-discovery
2️⃣ Create virtual environment

Mac/Linux

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the pipeline
python run_pipeline.py
🤖 Agent Details
Agent 1 — Artist Discovery

File

agents/discovery_agent.py

Purpose

Search the web for artists and extract Instagram profiles.

Example search queries:

DJ India Instagram
Singer India Instagram
Anchor India Instagram

Output

data/artists_raw.csv

Example:

name,instagram_url,category
DJ Rahul,https://instagram.com/djrahul,dj
Singer Meera,https://instagram.com/meerasings,singer
Agent 2 — Profile Intelligence & Filtering

File

agents/intelligence_agent.py

Uses:

tools/instagram_scraper.py
tools/llm_analyzer.py

Purpose

Extract useful contact information from profiles.

Extracted fields:

email

phone number

website

bio

follower count (if available)

Duplicate filtering

Artists already onboarded are filtered using:

data/starclinch_existing.csv

Output

data/artists_enriched.csv

Example:

name,email,phone,website,followers
DJ Rahul,rahul@email.com,,djrahul.com,25000
Singer Meera,,+919876543210,,8000
Agent 3 — Outreach & Prioritisation

File

agents/outreach_agent.py

Purpose

Generate outreach messages and prioritize artists.

Priority scoring logic
score = 0

if followers:
    score += min(followers // 1000, 50)

if email:
    score += 20

if website:
    score += 10
Contact rules
Contact Available	Method
Email	Email outreach
Phone	WhatsApp outreach
None	Instagram DM

Output

data/outreach_queue.csv

Example:

name,contact_channel,priority_score,outreach_message
DJ Rahul,email,45,"Hi Rahul, we discovered your work and would love to collaborate."
📊 Dashboard

Run:

streamlit run dashboard.py

Dashboard allows teams to:

View discovered artists

Filter by category

Review outreach messages

Monitor artist priority

📂 Output Files

Generated datasets:

data/artists_raw.csv
data/artists_enriched.csv
data/outreach_queue.csv

These files allow reviewers to validate pipeline outputs.

🧪 Verification / What To Check
Step 1

Run pipeline

python run_pipeline.py
Step 2

Verify output files exist

data/artists_raw.csv
data/artists_enriched.csv
data/outreach_queue.csv
Step 3

Open outreach queue

Check:

priority_score

outreach_message

contact_channel

📋 Assignment Requirements Mapping
Requirement	Implementation
Artist discovery	agents/discovery_agent.py
Instagram extraction	tools/google_search.py
Profile enrichment	agents/intelligence_agent.py
Email / phone extraction	tools/llm_analyzer.py
Duplicate filtering	data/starclinch_existing.csv
Outreach prioritization	agents/outreach_agent.py
Outreach message generation	agents/outreach_agent.py
Output datasets	data/*.csv
🧪 What I Tested

Pipeline tested with:

python run_pipeline.py

Example result:

10 artists discovered
6 enriched with contact info
5 added to outreach queue
⚠️ Known Limitations

Instagram scraping may fail for private profiles

Contact extraction depends on profile bio availability

Search results depend on Google indexing

🔮 Future Improvements

Automated email outreach

More advanced LLM-based profile analysis

City-based filtering

Database storage

Async scraping for faster discovery


✅ Reviewer Quick Checklist

Run:

git clone repo

pip install -r requirements.txt

python run_pipeline.py

streamlit run dashboard.py


Check outputs:

data/artists_raw.csv

data/artists_enriched.csv

data/outreach_queue.csv

Verify:

discovery works

enrichment works

outreach queue generated
