from scrapper import ZonaShow

def main():
    show_url = input("Hello, please enter target show link (https://w140.zona.plus/tvseries/ from this website): ")
    scrapper = ZonaShow(url=show_url, headless=True) # Recommended to set headless = False
    
    scrapper.getEpisodeLinks()

    


if __name__ == "__main__":
   main() 