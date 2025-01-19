import json
import os
import subprocess

# Path to the JSON file
json_file_path = "videos.json"

# Define the hashtag to filter by
target_hashtag = "#softwareengineer"

# Define output directory
output_directory = "downloaded_videos"
os.makedirs(output_directory, exist_ok=True)

# Load JSON data from the file
try:
    with open(json_file_path, "r") as file:
        data = json.load(file)
except Exception as e:
    print(f"Failed to load JSON file: {e}")
    exit()

# Process video links
favorite_videos = data.get("Favorite Videos", {}).get("FavoriteVideoList", [])
for video in favorite_videos:
    video_link = video.get("Link", "")
    
    if not video_link:
        continue

    print(f"Checking metadata for video: {video_link}")
    
    # Extract metadata using yt-dlp
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-description", "--get-title", video_link],
            capture_output=True,
            text=True,
            check=True
        )
        metadata = result.stdout.lower()  # Convert to lowercase for easier searching

        # Check if the target hashtag is in the metadata
        if target_hashtag.lower() in metadata:
            print(f"Hashtag '{target_hashtag}' found. Downloading: {video_link}")
            
            # Download the video
            subprocess.run([
                "yt-dlp",
                "--restrict-filenames",  # Sanitize filenames
                "-o", f"{output_directory}/%(title).50s.%(ext)s",  # Shortened title
                video_link
            ], check=True)
            print(f"Successfully downloaded: {video_link}")
        else:
            print(f"Skipped video: {video_link} (Hashtag not found)")
    except subprocess.CalledProcessError as e:
        print(f"Failed to process video {video_link}: {e}")

print("All downloads complete.")
