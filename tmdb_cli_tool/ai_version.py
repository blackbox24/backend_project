from decouple import config
import requests
import argparse
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger("tmdb_cli")

# TMDB API base URL and endpoints
BASE_URL = "https://api.themoviedb.org/3/movie/"
ENDPOINTS = {
    "playing": "now_playing",
    "popular": "popular",
    "top": "top_rated",
    "upcoming": "upcoming"
}

def fetch_tmdb_data(endpoint: str, api_key: str, language: str = "en-US", page: int = 1) -> Optional[Dict]:
    """Fetch data from the TMDB API for the specified endpoint."""
    url = f"{BASE_URL}{endpoint}?language={language}&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        return None

def format_movie_data(data: Dict) -> str:
    """Format movie data for user-friendly output."""
    output = []
    results = data.get("results", [])
    for movie in results[:5]:  # Limit to first 5 movies for brevity
        output.append(f"Title: {movie['title']}, Release: {movie.get('release_date', 'N/A')}, Rating: {movie.get('vote_average', 'N/A')}")
    return "\n".join(output) if output else "No movies found."

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch movie data from TMDB API")
    parser.add_argument("--type", choices=ENDPOINTS.keys(), required=True, help="Movie category to fetch")
    parser.add_argument("--language", default="en-US", help="Language for results (e.g., en-US)")
    parser.add_argument("--page", type=int, default=1, help="Page number for paginated results")
    args = parser.parse_args()

    # Load API key
    api_key = config("API_ACCESS_TOKEN", cast=str, default="")
    if not api_key:
        logger.error("API_ACCESS_TOKEN is not set in the environment.")
        return

    # Fetch data from TMDB
    logger.info(f"Fetching {args.type} movies...")
    endpoint = ENDPOINTS.get(args.type.lower())
    data = fetch_tmdb_data(endpoint, api_key, args.language, args.page)

    if data:
        logger.info(f"Status code: 200")
        if "dates" in data:
            logger.info(f"Date range: {data['dates']['minimum']} to {data['dates']['maximum']}")
        logger.info(f"Page: {data.get('page')}")
        logger.info(f"Total results: {len(data.get('results', []))}")
        
        # Print formatted output for the user
        print(f"\n{args.type.capitalize()} Movies:")
        print(format_movie_data(data))
    else:
        logger.error("Failed to retrieve movie data.")

if __name__ == "__main__":
    main()