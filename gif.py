
import requests
import json
class GIF_API:
    
    def __init__(self):
        with open("gifs_token.txt", 'r') as f:
            self.headers = { 'Gifs-API-Key': f.read().strip(), 'Content-Type': "application/json" }

    def make_request(self, url):
        return requests.get(url).json()

    def get_gif(self, url):
        r = requests.post("https://api.gifs.com/media/import", headers=self.headers, json={"source": url})
        return r