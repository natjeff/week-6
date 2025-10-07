
#Exercise 1



# Define the Genius class
class Genius:
    """Class"""

    def __init__(self, access_token):
        """
        Initialize the Genius class.
        """
        # Save the access token
        self.access_token = access_token

        # Print for confirmation
        print(f"Genius initialized with access token: {self.access_token}")


# Test the Genius class
if __name__ == "__main__":
    # Create a Genius object
    genius = Genius(access_token="access_token")

    # Verify the access token was saved
    print(genius.access_token)





#Exercise 2



import requests

class Genius:
    """Class"""

    def __init__(self, access_token):
        """
        Initialize the Genius class.
        """
        self.access_token = access_token
        self.base_url = "http://api.genius.com"

    def get_artist(self, search_term):
        """
        Search for an artist and return their information as a dictionary.
        """
    
        genius_search_url = f"{self.base_url}/search?q={search_term}&access_token={self.access_token}"
        response = requests.get(genius_search_url)

        if response.status_code != 200:
            raise Exception(f"Search request failed: {response.status_code} - {response.text}")
        search_results = response.json()
        try:
            first_hit = search_results["response"]["hits"][0]["result"]
            artist_id = first_hit["primary_artist"]["id"]
        except (IndexError, KeyError):
            raise Exception("No artist found for that search term.")
        artist_url = f"{self.base_url}/artists/{artist_id}?access_token={self.access_token}"
        artist_response = requests.get(artist_url)

        if artist_response.status_code != 200:
            raise Exception(f"Artist request failed: {artist_response.status_code} - {artist_response.text}")
        return artist_response.json()


# Example usage
if __name__ == "__main__":

    genius = Genius(access_token=ACCESS_TOKEN)
    artist_info = genius.get_artist("Radiohead")

    # Print test
    print(artist_info["response"]["artist"]["name"])





#Exercise 3

import requests
import pandas as pd

class Genius:
    """Class"""

    def __init__(self, access_token):
        """
        Initialize the Genius class
        """
        self.access_token = access_token
        self.base_url = "http://api.genius.com"

    def get_artist(self, search_term):
        """
        Search for an artist
        """
        genius_search_url = f"{self.base_url}/search?q={search_term}&access_token={self.access_token}"
        response = requests.get(genius_search_url)

        if response.status_code != 200:
            raise Exception(f"Search request failed: {response.status_code} - {response.text}")

        search_results = response.json()
        try:
            first_hit = search_results["response"]["hits"][0]["result"]
            artist_id = first_hit["primary_artist"]["id"]
        except (IndexError, KeyError):
            raise Exception(f"No artist found for search term '{search_term}'.")
        artist_url = f"{self.base_url}/artists/{artist_id}?access_token={self.access_token}"
        artist_response = requests.get(artist_url)

        if artist_response.status_code != 200:
            raise Exception(f"Artist request failed: {artist_response.status_code} - {artist_response.text}")

        return artist_response.json()

    def get_artists(self, search_terms):
        """
        Take in a list of search terms 
        """
        data = []

        for term in search_terms:
            try:
                artist_data = self.get_artist(term)
                artist_info = artist_data["response"]["artist"]

                data.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count", None)
                })

            except Exception as e:
                data.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
                print(f"Error retrieving artist '{term}': {e}")

        # Create DataFrame
        df = pd.DataFrame(data, columns=["search_term", "artist_name", "artist_id", "followers_count"])
        return df


# Example usage
if __name__ == "__main__":
   
    genius = Genius(access_token=ACCESS_TOKEN)
    df = genius.get_artists(['Rihanna', 'Tycho', 'Seal', 'U2'])

    print(df)


