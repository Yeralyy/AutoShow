import json
import os
import subprocess
import time

def main(json_file, download_dir, show_name, max_retries=5):

    # loading json
    with open(json_file, "r", encoding="utf-8") as f:
        shows = json.load(f)

    # iteration throught seasons and episodes
    for season, episodes in shows.items():
        season_dir = os.path.join(download_dir, season) # creating season directory (joining) into download_dir
        os.makedirs(season_dir, exist_ok=True)

        for ep_name, url in episodes.items(): # for {ep_name: link}
            filename = f"{show_name} - S{int(season.replace("Season", '')):02d}E{int(ep_name.replace("episode", '')):02d}.mp4" # jellyfin supported file name
            filepath = os.path.join(season_dir, filename)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 100_000_000: # if file bigger than 100mb
                print(f"Already Downloaded: {filename}")
                continue

            # attempting to download
            for attempt in range(1, max_retries + 1):
                print(f"[↓] Downloading ({attempt}/{max_retries}): {filename}")
                result = subprocess.run( # downloading using wget
                    ["wget", "-c", "-O", filepath, url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                if result.returncode == 0 and os.path.getsize(filepath) > 100_000_000: # if file bigger than 100mb
                    print(f"[✔️] Succesfully downloaded: {filename}")
                    break
                else:
                    print(f"[!] Failed to download {filename}, trying again...")
                    time.sleep(3) # delay

            else:
                print(f"[✘] Absolutely failed to download: {filename}")

if __name__ == "__main__":
    json_file = input("Enter json file name: ")
    download_dir = input("Enter the directory name to download files: ")
    show_name = input("Enter the TV Show name: ")

    main(json_file, download_dir, show_name)
