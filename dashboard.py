import streamlit as st
import pandas as pd
import subprocess

# Page configuration
st.set_page_config(
    page_title="StarClinch AI Discovery",
    page_icon="🎤",
    layout="wide"
)

# Title
st.title("StarClinch Artist Discovery System")
st.caption("AI-powered artist discovery and outreach system")

# Run pipeline button
if st.button("Run AI Discovery Pipeline"):
    subprocess.run(["python", "run_pipeline.py"])
    st.success("Pipeline executed successfully! Refreshing data...")

st.divider()

# Load discovered artists
df = pd.read_csv("data/artists_enriched.csv")

# Search artist
search_artist = st.text_input("Search Artist by Name")

# Category filter
st.subheader("Filter Artists")

category_filter = st.selectbox(
    "Select Category",
    ["All"] + sorted(df["category"].dropna().unique().tolist())
)

# Apply filters
if category_filter != "All":
    df = df[df["category"] == category_filter]

if search_artist:
    df = df[df["name"].str.contains(search_artist, case=False, na=False)]

# Metrics
total_artists = len(df)
onboarded = df["already_onboarded"].sum()
ready_for_outreach = total_artists - onboarded

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Total Artists Discovered", total_artists)
col2.metric("Already Onboarded", onboarded)
col3.metric("Ready for Outreach", ready_for_outreach)

# Discovered artists table
st.subheader("Discovered Artists")

st.dataframe(
    df,
    column_config={
        "instagram": st.column_config.LinkColumn("Instagram Profile")
    }
)

# Already onboarded artists
st.subheader("Already Onboarded Artists")
st.write(df[df["already_onboarded"] == True])

# Artists ready for outreach
st.subheader("Artists Ready for Outreach")
st.write(df[df["already_onboarded"] == False])

st.divider()

# Outreach message preview
st.subheader("Outreach Message Preview")

try:
    outreach_df = pd.read_csv("data/outreach_queue.csv")

    if not outreach_df.empty:
        st.write(outreach_df.iloc[0]["message"])
    else:
        st.write("No outreach messages generated yet.")

except:
    st.write("Run the pipeline to generate outreach messages.")

st.divider()


# Top outreach targets
st.subheader("🔥 Top Outreach Targets")

try:
    outreach_df = pd.read_csv("data/outreach_queue.csv")

    top_targets = outreach_df.sort_values(
        by="priority_score", ascending=False
    ).head(10)

    st.dataframe(
        top_targets[["name", "category", "contact_method", "priority_score"]]
    )

except:
    st.write("Run the pipeline to generate outreach leads.")

st.divider()
st.divider()

st.subheader("📩 Generated Outreach Messages")

try:
    outreach_df = pd.read_csv("data/outreach_queue.csv")

    if not outreach_df.empty:

        for _, row in outreach_df.iterrows():

            with st.expander(f"{row['name']} | {row['contact_method']} | Priority {row['priority_score']}"):

                st.markdown(f"""
**Artist:** {row['name']}  
**Category:** {row['category']}  
**Contact Method:** {row['contact_method']}  
**Contact Info:** {row['contact_info']}

### Generated Message
{row['message']}
""")

    else:
        st.info("No outreach messages generated yet.")

except:
    st.info("Run the pipeline to generate outreach messages.")

# Category analytics
st.subheader("📊 Artist Category Distribution")

category_counts = df["category"].value_counts()

st.bar_chart(category_counts)
