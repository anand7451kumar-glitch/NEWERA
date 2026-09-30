from collections import OrderedDict

cache = OrderedDict()
capacity = 3


def get(key):
    if key not in cache:
        return -1

    cache.move_to_end(key)
    return cache[key]


def put(key, value):
    if key in cache:
        cache.move_to_end(key)

    cache[key] = value

    if len(cache) > capacity:
        cache.popitem(last=False)


put("A", 10)
put("B", 20)
put("C", 30)

print(cache)

print("Get A:", get("A"))

put("D", 40)

print(cache)
print("Get B:", get("B"))