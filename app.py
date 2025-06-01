import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
