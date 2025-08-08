from decouple import config
import redis
import logging
import argparse
import json
import requests

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Make HTTP requests with Redis caching or clear cache")
parser.add_argument("--port",help="specify the port to make request",type=int)
parser.add_argument("--origin",help="specify the url",type=str)
parser.add_argument("--clear-cache",help="command to clear cache",type=str, default=None)

args = parser.parse_args()

if args.port:
    logger.info(f"PORT: {args.port}")
if args.origin:
    logger.info(f"ORIGIN: {args.origin}")
if args.clear_cache:
    logger.info(f"clear cache: {args.clear_cache}")

def make_request(url,cache):
    cache_content = cache.get(url)
    if cache_content is None:
        try:
            response = requests.get(url=url)
            
            if response.status_code == 200:
                logger.info(f"Making request to {url}")
                logger.info("Request successful")
                response.headers["X-Cache"] = "MISS"
                
                cache.set(url,response.content)
                cache.set(f"{url}:headers",json.dumps(dict(response.headers)))

                logger.info(f"Successfully cached {url} content")
                logger.info(f"Response headers: {response.headers}")
                return response.content, response.headers
            else:
                logger.error(f"Status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
    else:
        headers = json.loads(cache.get(f"{url}:headers"))
        headers["X-Cache"] = "HIT"
        cache.set(name=f"{url}:header",value=json.dumps(dict(headers)))
        
        logger.info(f"Response headers: {headers}")
        logger.info(f"Response content: {cache.get(url)}")
        return cache.get(url), headers

def clear_cache(cache,command):
    if command == "all":
        logger.info("Clearing cache...")
        try:
            cache.flushall()
            logger.info("Cleared cache")
        except redis.RedisError as e:
            logger.error(f"Failed to clear cache: {e}")
    else:
        logger.warning(f"Unknown clear-cache command: {command}")



try:
    r = redis.Redis(
        host=config("REDIS_HOST",cast=str,default="localhost"),
        port=config("REDIS_PORT",cast=int,default=6379),
        password=config("REDIS_PASSWORD",cast=str,default=""),
        db=config("REDIS_DB",cast=int,default=0)
    )
    
    logger.info("Connection to redis successful")
    if args.origin:
        content, headers = make_request(args.origin,cache=r)
    elif args.clear_cache:
        clear_cache(r,args.clear_cache)
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    raise