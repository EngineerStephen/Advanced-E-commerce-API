from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

redis_storage = Redis(host='localhost', port=5000)

limiter = Limiter(
    key_func = get_remote_address,
    storage_uri="redis://localhost:5000"
)