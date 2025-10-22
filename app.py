import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# ===========================================
# 🎵 INITIAL SETUP
# ===========================================
st.set_page_config(page_title="Music Mood Dashboard", page_icon="🎧", layout="wide")

# Load environment variables
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Load data
df = pd.read_csv("spotify_cluster_data.csv")

# Sidebar - mood selection
st.sidebar.header("🎵 Explore Mood Clusters")
moods = sorted(df['cluster_label'].unique().tolist())
selected_mood = st.sidebar.selectbox("Select a Mood Cluster", moods)

# Filter data
mood_df = df[df['cluster_label'] == selected_mood]

# ===========================================
# 🎨 PAGE HEADER
# ===========================================
st.title(f"🎧 Spotify Mood Dashboard")
st.subheader(f"Mood Cluster: **{selected_mood}** 🎶")
st.caption("Explore your ML-generated music moods — interactive, visual, and dynamic!")

st.markdown("---")

# ===========================================
# 💡 KEY METRICS
# ===========================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Songs", len(mood_df))
col2.metric("Avg Energy", f"{mood_df['energy'].mean():.2f}")
col3.metric("Avg Danceability", f"{mood_df['danceability'].mean():.2f}")

style_metric_cards(background_color="#003049", border_left_color="#1DB954", border_color="#E0E0E0")

st.markdown("### 🎼 Playlist Overview")
st.dataframe(
    mood_df[['track_name', 'track_artist', 'track_album_name', 'track_href']],
    use_container_width=True
)

# ===========================================
# 📊 INTERACTIVE VISUALS
# ===========================================
st.markdown("## 📈 Mood Feature Insights")

tab1, tab2, tab3 = st.tabs(["Feature Distribution", "Energy vs Valence", "Top Artists"])

# --- Tab 1: Feature Distribution ---
with tab1:
    feature_cols = ['energy', 'valence', 'danceability', 'acousticness', 'instrumentalness', 'tempo']
    feature_means = mood_df[feature_cols].mean().reset_index()
    feature_means.columns = ['Feature', 'Mean Value']

    fig = px.bar(
        feature_means,
        x='Feature',
        y='Mean Value',
        color='Mean Value',
        color_continuous_scale='greens',
        title=f"Feature Profile for {selected_mood}",
    )
    fig.update_layout(xaxis_title="", yaxis_title="Average Value", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Energy vs Valence ---
with tab2:
    fig2 = px.scatter(
        mood_df,
        x='energy',
        y='valence',
        size='danceability',
        color='tempo',
        hover_data=['track_name', 'track_artist'],
        color_continuous_scale='Viridis',
        title="Energy vs Valence Bubble Chart"
    )
    fig2.update_layout(template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# --- Tab 3: Top Artists ---
with tab3:
    top_artists = mood_df['track_artist'].value_counts().head(10).reset_index()
    top_artists.columns = ['Artist', 'Song Count']

    fig3 = px.bar(
        top_artists,
        x='Song Count',
        y='Artist',
        orientation='h',
        color='Song Count',
        color_continuous_scale='Blues',
        title="Top Artists in this Mood Cluster"
    )
    fig3.update_layout(yaxis=dict(autorange="reversed"), template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)


# ===========================================
# 🎵 ANALYTICS EXTENSION SECTION
# ===========================================
st.markdown("---")
st.markdown("## 🧠 Deep Dive Analytics")

tab1, tab2 = st.tabs(["Feature Correlation", "Cluster Comparison"])

# ============================================================
# 🧩 TAB 1: FEATURE CORRELATION HEATMAP
# ============================================================
with tab1:
    st.markdown("### 🎚️ Feature Correlation Heatmap")

    feature_cols = ['energy', 'valence', 'danceability', 'acousticness', 'instrumentalness', 'tempo']
    corr_matrix = df[feature_cols].corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='Greens',
        title="Correlation Between Musical Features"
    )
    fig_corr.update_layout(width=700, height=600, template="plotly_white")
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("💡 Insight: Strong correlations show which musical attributes move together (e.g., energy and danceability).")

# ============================================================
# 🌀 TAB 2: CLUSTER COMPARISON
# ============================================================
with tab2:
    st.markdown("### 🌀 Compare Clusters by Feature Averages")

    cluster_means = df.groupby('cluster_label')[feature_cols].mean().reset_index()

    fig_cluster = px.line(
        cluster_means.melt(id_vars='cluster_label', var_name='Feature', value_name='Mean Value'),
        x='Feature',
        y='Mean Value',
        color='cluster_label',
        markers=True,
        title="Cluster Comparison Across Musical Features"
    )
    fig_cluster.update_layout(template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig_cluster, use_container_width=True)

    st.caption("💡 Insight: Compare how each mood cluster differs across features like energy, valence, and acousticness.")




# ===========================================
# 🎧 DOWNLOAD & PLAYLIST CREATION
# ===========================================
st.markdown("## 💾 Export & Spotify Integration")

csv = mood_df.to_csv(index=False).encode('utf-8')
st.download_button(
    f"📥 Download '{selected_mood}' Playlist",
    csv,
    file_name=f"{selected_mood}.csv",
    mime='text/csv'
)

if st.button("🎧 Create Playlist in Spotify"):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public"
        ))

        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{selected_mood} Playlist (ML Generated)",
            public=True,
            description=f"Generated from Music Cluster Analysis — {selected_mood}"
        )

        track_uris = mood_df['uri'].dropna().tolist()
        if not track_uris:
            st.warning("No valid Spotify URIs found for this cluster.")
        else:
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris[:100])
            st.success("✅ Playlist created successfully! Check your Spotify account.")
    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

