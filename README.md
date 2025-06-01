# Music-Cluster-Analysis
# 🎧 Mood-Based Music Analysis & Playlist Generator

This project analyzes songs based on their musical features (like energy, valence, and acousticness), clusters them into mood categories, and creates curated playlists for each mood. It includes an interactive Streamlit web app for exploring the playlists and mood profiles.

---

📌 Features

- 🎶 Cluster songs by mood using audio features
- 🔍 Analyze song characteristics like energy, danceability, and valence
- 📊 Visualize mood profiles with radar and bar charts
- 🎼 Generate and download playlists for each mood
- 🌐 Interactive Streamlit app for exploring songs by cluster

---

## 🚀 Tech Stack

- Python
- Pandas for data manipulation
- Scikit-learn for KMeans clustering
- Matplotlib / Seaborn for visualization
- Streamlit for web app interface

---

## 🎯 Mood Clusters Used

Each song was assigned to one of the following clusters based on its features:

1. 'Feel-good Hits' | High energy, high valence — perfect for upbeat moods |
2. 'Chill & Acoustic' | Low energy, high acousticness — calm and emotional |
3. 'Angry / Intense' | High energy, low valence — aggressive and fast |
4. 'Balanced / Versatile Mix' | Medium values across features — versatile listening |

---

## 📷 Screenshots

<img width="1437" alt="Screenshot 2025-05-31 at 7 33 59 PM" src="https://github.com/user-attachments/assets/aebd1f64-099a-497f-9635-16b693752556" />

<img width="1440" alt="Screenshot 2025-05-31 at 7 34 12 PM" src="https://github.com/user-attachments/assets/b807e75d-0e82-4e2f-8424-ab4ba95d26ca" />

![image](https://github.com/user-attachments/assets/70a43ba9-2f2d-480e-87a0-08c93cf5871a)

![image](https://github.com/user-attachments/assets/9f6491c8-1576-45f0-b513-4c4aa13b8812)


---

▶️ Running the App

1. Install dependencies:

   pip install pandas
   pip install seaborn
   pip install matplotlib
   pip install numpy
   pip install streamlit

2. Run the app:

   streamlit run app.py

3. Open in your browser and interact!


📥 Dataset
Used a Kaggle dataset containing audio features for thousands of Spotify tracks:

1. Energy
2. Valence
3. Danceability
4. Acousticness
5. Instrumentalness
6. Tempo

Link for the kaggle dataset: https://www.kaggle.com/datasets/solomonameh/spotify-music-dataset

💡 Future Ideas

1. Add Spotify login to use real user data
2. Add emotion tagging via NLP on lyrics
3. Deploy live with Streamlit Cloud or Hugging Face Spaces
4. Auto-update playlists via Spotify API



Built with love and a lot of music 🎶 by Lisha Choudhary


