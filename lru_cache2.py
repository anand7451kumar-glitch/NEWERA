# Every time someone requests the weather for Kolkata, your app calls an external API. Repeated requests waste time and API calls.

# Instead, you can cache the result:

# First request for Kolkata → fetch the data and save it.
# Second request for Kolkata → return the saved data instantly.
# Cache is full → remove the least recently used entry to make room.
# This is called an LRU (Least Recently Used) Cache.

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def get(self, key):
        if key not in self.cache:
            return -1

        #Mark this key as recently used
        value = self.cache.pop(key)
        self.cache[key] = value

        return value

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)

        elif len(self.cache) >= self.capacity:
            #Remove the least recently used entry
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)

        self.cache[key] = value

    def display(self):
        print("Cache:", self.cache)

#Test the cache
cache = LRUCache(3)

cache.put("Kolkata", 32)
cache.put("Delhi", 38)
cache.put("Mumbai", 30)

cache.display()

print("Kolkata temperature:", cache.get("Kolkata"))

cache.put("Chennai", 35)

cache.display()



