from decouple import config
import requests
import argparse
import logging

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger("tmdb_cli")

url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
secret_key = config("API_ACCESS_TOKEN",cast=str,default="")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {secret_key}"
}

parser = argparse.ArgumentParser()
# parser.add_argument("option", help="specify command", type=str)
parser.add_argument("--type", help="use type option", type=str)

arg = parser.parse_args()


if arg.type and arg.type.lower() == "playing":
    
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    option = arg.type
    logging.info(f"Args: {option}")
    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            date_max = data.get("dates")["maximum"]
            date_min = data.get("dates")["minimum"]
            page = data.get("page")
            results = data.get("results")

            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Max Date: {date_max}")
            logger.info(f"Min Date: {date_min}")
            logger.info(f"Page: {page}")
            logger.info(f"Result: {results}")
        else:
            logger.error(f"Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error: {e}")

elif arg.type and arg.type.lower() == "popular":
    
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    option = arg.type
    logging.info(f"Args: {option}")
    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            # date_max = data.get("dates")["maximum"]
            # date_min = data.get("dates")["minimum"]
            page = data.get("page")
            results = data.get("results")

            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Page: {page}")
            logger.info(f"Result: {results}")
        else:
            logger.error(f"Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error: {e}")

elif arg.type and arg.type.lower() == "top":
    
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    option = arg.type
    logging.info(f"Args: {option}")
    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            # date_max = data.get("dates")["maximum"]
            # date_min = data.get("dates")["minimum"]
            page = data.get("page")
            results = data.get("results")

            logger.info(f"Status code: {response.status_code}")
            # logger.info(f"Max Date: {date_max}")
            # logger.info(f"Min Date: {date_min}")
            logger.info(f"Page: {page}")
            logger.info(f"Result: {results}")
        else:
            logger.error(f"Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error: {e}")

elif arg.type and arg.type.lower() == "upcoming":
    
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    option = arg.type
    logging.info(f"Args: {option}")
    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            data = response.json()
            date_max = data.get("dates")["maximum"]
            date_min = data.get("dates")["minimum"]
            page = data.get("page")
            results = data.get("results")

            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Max Date: {date_max}")
            logger.info(f"Min Date: {date_min}")
            logger.info(f"Page: {page}")
            logger.info(f"Result: {results}")
        else:
            logger.error(f"Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error: {e}")

else:
    logger.error(f"Invalid option")

