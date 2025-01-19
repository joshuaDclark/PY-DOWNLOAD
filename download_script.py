import json
import os
import subprocess

# Load JSON data
data = {
    "Favorite Videos": {
        "App": 1,
        "FavoriteVideoList": [
            {
                "Date": "",
                "Link": ""
            },
        ]
    }
}

# Define output directory
output_directory = "downloaded_videos"
os.makedirs(output_directory, exist_ok=True)

# Process video links
favorite_videos = data["Favorite Videos"]["FavoriteVideoList"]
for video in favorite_videos:
    video_link = video["Link"]
    print(f"Downloading video from: {video_link}")
    
    # Download with a short filename
    try:
        subprocess.run([
            "yt-dlp",
            "--restrict-filenames",  # Sanitize filenames
            "-o", f"{output_directory}/%(title).50s.%(ext)s",  # Shortened title
            video_link
        ], check=True)
        print(f"Successfully downloaded: {video_link}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {video_link}: {e}")

print("All downloads complete.")
