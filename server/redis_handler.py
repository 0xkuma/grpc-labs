from redis import Redis


class RedisHandler:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0)
        print("Redis connected")

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, ex=3600):
        self.redis.set(key, value, ex=ex)

    def delete(self, key):
        self.redis.delete(key)
