import redis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to the Redis database
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),  
    port=os.getenv("REDIS_PORT"),         
    db=os.getenv("REDIS_DATABASE")            
)

def test_redis_connection():
    try:
        # Test the connection by pinging the Redis server
        redis_client.ping()
        print("Connected to Redis successfully!")
        return True
    except redis.ConnectionError:
        print("Failed to connect to Redis.")
    except redis.TimeoutError:
        print("Connection to Redis timed out.")
    except redis.ResponseError:
        print("Response error from Redis.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")