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

    def fetch_tv_shows(self, section_id):
        """Fetch all TV shows from a specific section"""
        url = f"{self.base_url}/library/sections/{section_id}/all?type=1"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('MediaContainer', {}).get('Metadata', [])
        else:
            response.raise_for_status()

    def fetch_episodes_for_series(self, series_id):
        """Fetch all episodes for a specific TV series"""
        url = f"{self.base_url}/library/metadata/{series_id}/allLeaves"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('MediaContainer', {}).get('Metadata', [])
        else:
            response.raise_for_status()

    def update_all_episodes_date(self, section_id, series_id, new_date):
        """Update the addedAt date for all episodes in a series"""
        episodes = self.fetch_episodes_for_series(series_id)
        updated_count = 0
        failed_count = 0
        
        for episode in episodes:
            try:
                episode_id = episode.get('ratingKey')
                # Use type=4 for episodes
                self.update_added_date(section_id, episode_id, "4", new_date)
                updated_count += 1
            except Exception as e:
                print(f"Failed to update episode {episode.get('title', 'Unknown')}: {e}")
                failed_count += 1
        
        return updated_count, failed_count

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

    def fetch_seasons(self, section_id):
        url = f"{self.base_url}/library/sections/{section_id}/all?type=2"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('MediaContainer', {}).get('Metadata', [])
        else:
            response.raise_for_status()