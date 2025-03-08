import streamlit as st
import shutil
import yt_dlp
import os
from pathlib import Path

def is_ffmpeg_installed():
    """Check if ffmpeg is installed."""
    return shutil.which("ffmpeg") is not None

def download_youtube_video(url, output_path='downloads'):
    """Download a YouTube video and return its path."""
    if not is_ffmpeg_installed():
        return None, "FFmpeg is not installed. Please install FFmpeg to enable video merging."

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'geo_bypass': True,  # Bypass geo-restrictions
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'Downloaded Video')
            video_file = Path(ydl.prepare_filename(info_dict)).with_suffix('.mp4')
            return video_file, f"Video '{video_title}' downloaded successfully!"
    except Exception as e:
        return None, f"An error occurred: {e}"

# Streamlit UI
st.title("YouTube Video Downloader")
video_url = st.text_input("Enter the YouTube video URL:")

if st.button('Download'):
    if video_url.strip() == "":
        st.error("Please enter a valid YouTube video URL.")
    else:
        with st.spinner('Downloading...'):
            video_path, message = download_youtube_video(video_url)
            if video_path:
                st.success(message)
                st.video(str(video_path))
                st.markdown(f"[Download the video here](./{video_path})")
            else:
                st.error(message)
