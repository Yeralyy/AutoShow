import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

""" Example. I use this script to download shows for my Jellyfin which running on my home server """

# CONFIG
MAX_THREADS = 5            # how many downloads in parallel

def download_episode(season_num, episode_num, url, SHOW_NAME):
    season_dir = f"Season {season_num}"
    os.makedirs(season_dir, exist_ok=True)

    # Jellyfin filename format: ShowName - SXXEXX.mp4
    filename = f"{SHOW_NAME} - S{season_num:02d}E{episode_num:02d}.mp4"
    filepath = os.path.join(season_dir, filename)

    print(f"Downloading {filename} from {url}")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Done: {filepath}")
    except Exception as e:
        print(f"Failed {filename}: {e}")


def main(json_file, show_name):
    # --- Load JSON ---
    with open(json_file, "r") as f:
        data = json.load(f)

    # --- Create download tasks ---
    tasks = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for season_index, (season_key, episodes) in enumerate(data.items(), start=1):
            for episode_index, (episode_key, url) in enumerate(episodes.items(), start=1):
                tasks.append(executor.submit(download_episode, season_index, episode_index, url, show_name))

        # Wait for all to finish
        for future in as_completed(tasks):
            pass

    print("All downloads complete.")

if __name__ == "__main__":
    show_name = input("Welcome, Please enter your show name: ")
    json_file = input("Enter json file name: ")

    main(json_file, show_name)
