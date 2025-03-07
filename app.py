import shutil
import streamlit as st
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

    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
        'noplaylist': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com/',
        },
        'force-ipv4': True,
        'cookiefile': 'cookies.txt',
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
st.title("MYMATE")

video_url = st.text_input("Enter the video URL:")

if st.button("Download and Play"):
    if video_url.strip() == "":
        st.error("Please enter a valid YouTube video URL.")
    else:
        with st.spinner("Downloading..."):
            video_path, message = download_youtube_video(video_url)
            if video_path:
                st.success(message)
                st.video(str(video_path))
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
