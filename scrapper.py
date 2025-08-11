from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By 
import shutil
import time
import json

from pprint import pprint


""" MADED FOR PERSONAL USE, FEEL FREE TO MODIFY, CONTRIBUTE."""

#class ZonaMovie(): you can also write script for movie-link parsing

class ZonaShow():
    def __init__(self, url, headless=False): # init
        options = Options()
        options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"  # WARNING: Im running this program on Ubuntu machine, with firefox driver
        # so comment this line if your firefox is not snap version (or edit it = /usr/bin/firefox)
        # You using Windows? Uhhmmmm, you better download Chrome webdriver (if you use chrome) from https://sites.google.com/chromium.org/driver/
        # And then unarchive it into this repository
        if headless:
            options.add_argument("--headless")
        
        # WARNING: If you using Chrome webDriver comment line below
        self.driver = webdriver.Firefox(options=options)
        #self.driver = webdriver.Chrome() and uncomment this!
        self.url = url

    
    def getEpisodeLinks(self, seasons=False, start_season=1): # parsing and saving into json, in my case i will download them by wget 
        # seasons = parameter to determine quanity of seasons to parse
        # start_season = start point, program will parse all episod links beetwen "start_season" - "seasons"

        
        self.driver.get(self.url)
        print(f"Starting! URL = {self.url}")
        episodes = {}

        if not seasons:
            seasons = len(self.driver.find_elements(By.CLASS_NAME, "entity-season"))
            
        print(seasons)
        for season in range(start_season, seasons + 1): # for each season
            season_btn = self.driver.find_element(By.LINK_TEXT, str(season)) # finding our target season 
            season_btn.click() # going to our target season episodes
            time.sleep(5)
            episodes_count = len(self.driver.find_elements(By.CLASS_NAME, "entity-episode-name"))
            print(f"{season}/{seasons} Season")
            #print(episodes_count)
            episodes[f"Season{season}"] = {}

            #for episode in range(1, episodes_count + 1):
            episode = 1
            while episode <= episodes_count:
                
                if episode == 1: # if its 1st episode we need to click on "Play" button
                    #self.driver.find_element(By.CLASS_NAME, "vjs-big-play-button").click()
                    self.driver.execute_script(
                        f"document.querySelector('button[class=\"vjs-big-play-button\"]').click()"
                    )
                else:
                    self.driver.execute_script(
                    f"document.querySelector('span[data-episode=\"{episode}\"]').click();") # if its not 1st episode, clicking on the next
                time.sleep(3) # give episode some time to upload

                episode_link = self.driver.find_element(By.ID, "player_html5_api").get_attribute("src") # getting .mp4 link
                if (episode_link in episodes.values()): 
                    print("Same link")
                    continue
                print(F"{episode}/{episodes_count} Episode DONE: {episode_link}")
                episodes[f"Season{season}"][f"episode{episode}"] = episode_link
                episode += 1



        # im saving it to json file, but you can modify this for .txt or else
        with open(f"{self.url.split("/")[-1]}.json", 'w') as f:
            f.write(json.dumps(episodes, indent=4))
            
        print("DONE! Enjoy your JSON file")

        self.driver.quit()

       

if __name__ == "__main__":
    parser = ZonaShow(url="https://w140.zona.plus/tvseries/silikonovaya-dolina", headless=False) # great show actually
    #parser = ZonaShow(url=office_link)
    parser.getEpisodeLinks()

