import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PlexAPI:
    def __init__(self, base_url=None, token=None):
        if base_url is None:
            base_url = os.environ.get("PLEX_BASE_URL")
        if token is None:
            token = os.environ.get("PLEX_TOKEN")
        self.base_url = base_url
        self.token = token

    def _get_headers(self):
        return {
            'X-Plex-Token': self.token,
            'Accept': 'application/json'
        }

    def fetch_movies(self):
        url = f"{self.base_url}/library/sections/1/all"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('MediaContainer', {}).get('Metadata', [])
        else:
            response.raise_for_status()

    def get_all_movies(self):
        return self.fetch_movies()

    def update_added_date(self, section_id, item_id, type_id, new_date):
        url = f"{self.base_url}/library/sections/{section_id}/all"
        params = {
            'type': type_id,
            'id': item_id,
            'addedAt.value': new_date,
            'X-Plex-Token': self.token
        }
        response = requests.put(url, params=params, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()