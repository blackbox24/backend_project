import requests
import sys
import logging


logging.basicConfig(level=logging.INFO,format="%(levelname)s %(filename)s %(message)s")
logger = logging.getLogger(__name__)

if len(sys.argv) == 2:
    username = sys.argv[1]
    url = f"https://api.github.com/users/{username}/events"

    logger.info(f"Request: {url}")

    response = requests.get(url)

    if response.status_code == 200:
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Getting {username} events ...")
        logger.info(f"Response: \n{response.json()}")
    elif response.status_code == 404:
        logger.error(f"Status code: {response.status_code}")
        logger.error("Resource cannot be found")
    else:
        logger.error(f"Status code: {response.status_code}")
        logger.error("Unable to retreive information")

else:
    logger.warning("Must provide username of github account")
    file = open("docs.txt","r")
    docs = file.read()
    logger.info(f"Documentation:\n{docs}")
    file.close()