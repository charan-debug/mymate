import streamlit as st
import yt_dlp
import os
from pathlib import Path

def download_youtube_video(url, output_path='downloads'):
    """Download a YouTube video and return its path."""
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'Downloaded Video')
            video_file = Path(ydl.prepare_filename(info_dict)).with_suffix('.mp4')
            return video_file, f"Video '{video_title}' downloaded successfully!"
    except Exception as e:
        return None, f"An error occurred: {e}"

# Streamlit App
st.title("YouTube Video Downloader & Player")

# Input for YouTube URL
video_url = st.text_input("Enter the YouTube video URL:")

# Download and Play Button
if st.button("Download and Play"):
    if video_url.strip() == "":
        st.error("Please enter a valid YouTube video URL.")
    else:
        with st.spinner("Downloading..."):
            video_path, message = download_youtube_video(video_url)
            if video_path:
                st.success(message)
                
                # Display the video in the Streamlit app
                st.video(str(video_path))
                
                # Provide a download link
                with open(video_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    st.download_button(
                        label="Download Video",
                        data=video_bytes,
                        file_name=video_path.name,
                        mime="video/mp4"
                    )
            else:
                st.error(message)
