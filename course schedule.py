from collections import deque

def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses

    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegree[course] += 1

    queue = deque()

    for i in range(num_courses):
        if indegree[i] == 0:
            queue.append(i)

    completed = 0

    while queue:
        course = queue.popleft()
        completed +=1

        for next_course in graph[course]:
            indegree[next_course] -= 1

            if indegree[next_course] == 0:
                queue.append(next_course)

    return completed == num_courses

n = int(input("Enter number of courses: "))
p = int(input("Enter number of prerequisites: "))

prerequisites = []

for i in range(p):
    course, prerequisite = map(
        int,
        input("Enter course and prerequisite: ").split()
    )
    prerequisites.append([course, prerequisite])

print("Can finish all courses:", can_finish(n, prerequisites))
