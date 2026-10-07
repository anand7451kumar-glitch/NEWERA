def can_attend(meetings):
    meetings.sort()

    for i in range(1, len(meetings)):
        previous_end = meetings[i - 1][1]
        current_start = meetings[i][0]

        if current_start < previous_end:
            return False

    return True

meetings = [[0, 30], [5, 10], [15, 20]]

print("Can attend all meetings:", can_attend(meetings))
