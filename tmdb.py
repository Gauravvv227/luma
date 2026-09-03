
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_API_KEY ="77f42ff7f601d41681a28acc2fff7b8c"
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE = "https://image.tmdb.org/t/p/w500"
def get_movie_details(title):
    try:
        search = requests.get(f"{TMDB_BASE}/search/movie", params={
            "api_key": TMDB_API_KEY,
            "query": title
        }, timeout=3)
        results = search.json()

        if not results['results']:
            return {"title": title, "overview": "N/A", "rating": "N/A", "poster": None, "year": "N/A", "streaming": []}

        movie = results['results'][0]
        movie_id = movie['id']

        try:
            providers_resp = requests.get(f"{TMDB_BASE}/movie/{movie_id}/watch/providers", params={
                "api_key": TMDB_API_KEY
            }, timeout=3)
            providers_data = providers_resp.json()
            country_data = providers_data.get('results', {}).get('IN',
                           providers_data.get('results', {}).get('US', {}))
            streaming = [p['provider_name'] for p in country_data.get('flatrate', [])]
        except Exception:
            streaming = []

        return {
            "title": movie['title'],
            "overview": movie['overview'],
            "rating": movie['vote_average'],
            "poster": TMDB_IMAGE + movie['poster_path'] if movie.get('poster_path') else None,
            "year": movie['release_date'][:4] if movie.get('release_date') else "N/A",
            "streaming": streaming
        }

    except Exception:
        return {
            "title": title,
            "overview": "Details unavailable in your region.",
            "rating": "N/A",
            "poster": None,
            "year": "N/A",
            "streaming": []
        }