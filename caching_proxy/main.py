from decouple import config
import redis
import logging

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

try:
    r = redis.Redis(
        host=config("REDIS_HOST",cast=str,default="localhost"),
        port=config("REDIS_PORT",cast=int,default=6379),
        password=config("REDIS_PASSWORD",cast=str,default=""),
        db=config("REDIS_DB",cast=int,default=0)
    )
    logger.info("Connection to redis successful")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    raise