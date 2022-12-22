import random

n = int(input())

dsu = [i for i in range(n*n)]

def dsu_get(v):
    if v == dsu[v]:
        return v
    k = dsu_get(dsu[v])
    dsu[v] = k
    return k

def dsu_union(a, b):
    a = dsu_get(a)
    b = dsu_get(b)
    dsu[b] = a

def dsu_connected(a, b):
    a = dsu_get(a)
    b = dsu_get(b)
    return a == b

def get_coord(i, j):
    return i*n+j

edges = set()

for i in range(n):
    for j in range(n):
        coord = get_coord(i, j)
        if i > 0:
            edges.add((coord, get_coord(i-1, j)))
        if j > 0:
            edges.add((coord, get_coord(i, j-1)))
        if i + 1 < n:
            edges.add((coord, get_coord(i+1, j)))
        if j + 1 < n:
            edges.add((coord, get_coord(i, j+1)))

spanning_tree = []

while len(edges) > 0:
    ind = random.randint(0, len(edges)-1)
    cnt = 0
    chosen_edge = (0, 0)
    for edge in edges:
        if cnt == ind:
            chosen_edge = edge
            break
        cnt += 1
    if not dsu_connected(chosen_edge[0], chosen_edge[1]):
        spanning_tree.append(chosen_edge)
        dsu_union(chosen_edge[0], chosen_edge[1])

    edges.remove(chosen_edge)

for i in range(2*n+1):
    print('#', end='')
print()

maze = []

maze.append(['#' for i in range(2*n+1)])

for i in range(2*n):
    maze_row = []
    print('#', end='')
    maze_row.append('#')

    for j in range(2*n):
        if i % 2 == 0 and j % 2 == 0:
            maze_row.append('.')
            print('.', end='')
        elif i % 2 == 0 and j % 2 == 1 and j + 1 < 2*n:
            edg1 = (get_coord(i//2, j//2), get_coord(i//2, j//2+1))
            edg2 = (edg1[1], edg1[0])
            # print(edg1)
            if edg1 in spanning_tree or edg2 in spanning_tree:
                print('.', end='')
                maze_row.append('.')
            else:
                print('#', end='')
                maze_row.append('#')
        elif i % 2 == 1 and j % 2 == 0 and i + 1 < 2*n:
            edg1 = (get_coord(i//2, j//2), get_coord(i//2+1, j//2))
            edg2 = (edg1[1], edg1[0])
            if edg1 in spanning_tree or edg2 in spanning_tree:
                print('.', end='')
                maze_row.append('.')
            else:
                print('#', end='')
                maze_row.append('#')
        else:
            print('#', end='')
            maze_row.append('#')
    print()
    maze.append(maze_row)

print(maze)


