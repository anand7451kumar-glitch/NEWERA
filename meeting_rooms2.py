import heapq

def min_rooms(meetings):
    meetings.sort()

    rooms = []

    for start, end in meetings:
        #Reuse a room if its meeting has finished
        if rooms and rooms[0] <= start:
            heapq.heappop(rooms)

        #Add this meeting's ending time
        heapq.heappush(rooms, end)

    return len(rooms)

meetings = [[0, 30], [5, 10], [15, 20]]

print("Minimum rooms needed:", min_rooms(meetings))