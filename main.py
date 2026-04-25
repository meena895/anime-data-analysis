import streamlit as st
import pandas as pd

# -----------------------
# Load dataset
# -----------------------
df = pd.read_csv("anime_cleaned.csv", encoding="ISO-8859-1")


# Convert dates if available
if "start_date" in df.columns:
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Anime Explorer", layout="wide")

# -----------------------
# Login System
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Hardcoded login (you can change this)
USERNAME = "admin"
PASSWORD = "1234"

if not st.session_state.logged_in:
    st.title("🔒 Login to Anime Explorer")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -----------------------
# Hero Section
# -----------------------
st.markdown(
    """
    <div style="text-align:center; padding: 20px;">
        <h1>🎌 Anime Explorer</h1>
        <p style="font-size:18px;">Search anime, watch trailers, and explore recommendations & latest releases.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Search Anime
# -----------------------
st.subheader("🔍 Search Anime")
search_query = st.text_input("Type anime title, genre, or theme:")

if search_query:
    results = df[
        df["title"].str.contains(search_query, case=False, na=False) |
        df["genres"].str.contains(search_query, case=False, na=False) |
        df["themes"].str.contains(search_query, case=False, na=False)
    ]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"## {row['title']}")

            cols = st.columns([1, 2])
            with cols[0]:
                if "main_picture" in df.columns and pd.notna(row.get("main_picture", None)):
                    st.image(row["main_picture"], width=220)

            with cols[1]:
                st.write(f"⭐ **Score:** {row.get('score', 'N/A')}")
                st.write(f"🎭 **Genres:** {row.get('genres', 'N/A')}")
                st.write(f"🎬 **Themes:** {row.get('themes', 'N/A')}")
                st.write(f"📺 **Episodes:** {row.get('episodes', 'N/A')}")
                st.write(f"👥 **Members:** {row.get('members', 'N/A')}")

                if "trailer_url" in df.columns and pd.notna(row.get("trailer_url", None)):
                    st.video(row["trailer_url"])

            st.markdown("---")
    else:
        st.warning("No anime found. Try another search term.")
else:
    st.info("👆 Start typing in the search bar to find anime.")

st.markdown("---")

# -----------------------
# Recommendations
# -----------------------
st.subheader("🔥 Most Watched Anime")
if "members" in df.columns:
    popular = df.sort_values(by="members", ascending=False).head(5)
    cols = st.columns(5)
    for i, (_, row) in enumerate(popular.iterrows()):
        with cols[i]:
            if pd.notna(row.get("main_picture", None)):
                st.image(row["main_picture"], use_container_width=True)
            st.caption(f"**{row['title']}**")

st.markdown("---")

# -----------------------
# Anime Calendar (Recent Releases)
# -----------------------
st.subheader("🗓️ Recent Releases / Anime Calendar")
if "start_date" in df.columns:
    recent = df.dropna(subset=["start_date"]).sort_values(by="start_date", ascending=False).head(5)
    cols = st.columns(5)
    for i, (_, row) in enumerate(recent.iterrows()):
        with cols[i]:
            if pd.notna(row.get("main_picture", None)):
                st.image(row["main_picture"], use_container_width=True)
            st.caption(f"**{row['title']}** ({row['start_date'].date()})")
