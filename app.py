import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Load your preprocessed CSV
df = pd.read_csv("spotify_cluster_data.csv")

# Sidebar mood selector
moods = df['cluster_label'].unique().tolist()
selected_mood = st.sidebar.selectbox("🎧 Select a Mood Cluster", sorted(moods))

# Filter by selected mood
mood_df = df[df['cluster_label'] == selected_mood]

# Show title
st.title(f"🎵 Playlist: {selected_mood}")
st.write(f"Total songs: {len(mood_df)}")

# Display playlist table
st.dataframe(mood_df[['track_name', 'track_artist', 'track_album_name', 'track_href']])

# Download playlist
csv = mood_df.to_csv(index=False).encode('utf-8')
st.download_button(
    f"📥 Download '{selected_mood}' Playlist",
    csv,
    file_name=f"{selected_mood}.csv",
    mime='text/csv'
)

st.dataframe(mood_df[['track_name', 'track_artist', 'track_album_name', 'track_href']])

import spotipy
from spotipy.oauth2 import SpotifyOAuth

if st.button("🎧 Create Playlist in Your Spotify"):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-public"
))


        user_id = sp.me()['id']

        #Create the playlist
        playlist = sp.user_playlist_create(
            user=user_id,
            name="Feel-Good Hits (ML Generated)",
            public=True,
            description="Generated using my mood-based clustering project 🎶"
        )

        #Get track URIs from the DataFrame
        track_uris = df[df['cluster_label'] == "Feel-Good Hits"]['uri'].dropna().tolist()

        if not track_uris:
            st.warning("No valid Spotify URIs found in this cluster.")
        else:
            # Add tracks (Spotify limits to 100 at a time)
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris[:100])
            st.success("🎉 Playlist created successfully! Check your Spotify account.")

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")



# Radar chart of mood features
features = ['energy', 'valence', 'danceability', 'acousticness', 'instrumentalness', 'tempo']
cluster_mean = mood_df[features].mean()

angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
stats = cluster_mean.tolist()
stats += stats[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, stats, linewidth=2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), features)
plt.title(f"Mood Profile: {selected_mood}")
st.pyplot(fig)
