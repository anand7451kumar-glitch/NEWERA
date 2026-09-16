import heapq

def network_delay(times, n, k):
    graph = [[] for _ in range(n + 1)]

    for source, target, time in times:
        graph[source].append((target, time))

    distances = [float("inf")] * (n + 1)
    distances[k] = 0

    heap = [(0, k)]

    while heap:
        current_time, node = heapq.heappop(heap)

        if current_time > distances[node]:
            continue

        for next_node, time in graph[node]:
            new_time = current_time + time

            if new_time < distances[next_node]:
                distances[next_node] = new_time
                heapq.heappush(heap, (new_time, next_node))

    max_time = max(distances[1:])

    if max_time == float("inf"):
        return -1

    return max_time

n = int(input("Enter number of nodes: "))
m = int(input("Enter number of connections: "))

times = []

for i in range(m):
    source, target, time = map(
        int,
        input("Enter source target time: ").split()
    )
    times.append([source, target, time])

k = int(input("Enter starting node: "))

print("Network delay:", network_delay(times, n, k))
