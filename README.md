AutoShow - Simple python script that allows you to automate show downloading from https://w140.zona.plus/tvseries/. Made for personal usage, i use it to download my favorite shows for my Jellyfin local stream. But you can still use it just to download your shows

How to use:
1. Create virtual envoirement "python3 -m venv yourvenvname" (Linux) and run "source yourvenvname/bin/activate"
2. Download libraries/dependencies "pip install -r requirements.txt"
3. Select your target show, and copy its link from https://w140.zona.plus/tvseries/. For eg: https://w140.zona.plus/tvseries/rik-i-morti
4. run "python3 main.py", and it will scrap all episodes links and save it into json file

Download show:
1. Create new directory (recommended)
2. add json file into your directory
3. In your directory, run "/path/to/AutoShow/download_script.py", and wait
4. Done, enjoy your show

