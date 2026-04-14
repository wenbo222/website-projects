# Sample BFS
# Demonstration of the BFS algorithm for finding the shortest path between two nodes in a graph.
# Also supports grids with walls in between.
# Wenbo

import collections

# Sample graph
graph={'A': ['B', 'C'],
       'B': ['A', 'D', 'E'],
       'C': ['A', 'F'],
       'D': ['B'],
       'E': ['B', 'F'],
       'F': ['C', 'E']}

# Sample grid
walls={frozenset({(1,1),(1,2)}),
       frozenset({(2,1),(2,2)}),
       frozenset({(3,1),(3,2)})}

def bfs_shortest_path_grid(row, column, walls, start, goal):
    """
    bfs_shortest_path_grid(int, int, set of frozensets, tuple, tuple) -> list
    Finds the shortest path between start and goal nodes using BFS.
    """

    graph={}
    for i in range(row): # convert grid to graph
        for j in range(column):
            offsets=[(0,1),(0,-1),(1,0),(-1,0)]
            neighbours=[]
            for offset in offsets:
                new_i=i+offset[0]
                new_j=j+offset[1]
                if 0<=new_i<row and 0<=new_j<column and frozenset({(i, j), (new_i, new_j)}) not in walls:
                    neighbours.append((new_i,new_j))
            graph[(i,j)]=neighbours
    return bfs_shortest_path_graph(graph, start, goal)

def bfs_shortest_path_graph(graph, start, goal):
    """
    bfs_shortest_path(dictionary, string, string) -> list
    Finds the shortest path between start and goal nodes using BFS.
    """

    if start==goal:
        return [start]

    explored=set()
    # Queue stores full paths (lists of nodes) so we can track the exact route taken
    queue=collections.deque([[start]])
    while queue:
        path=queue.popleft()
        node=path[-1]
        # Skip already explored nodes to prevent infinite loops in cyclic graphs
        if node not in explored:
            neighbors=graph[node]
            for neighbor in neighbors:
                new_path=list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor==goal:
                    return new_path
            explored.add(node)

if __name__=="__main__":
    # Test sample graph
    start_node='A'
    end_node='F'
    path_graph=bfs_shortest_path_graph(graph, start_node, end_node)
    if path_graph:
        print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(path_graph)}")
    else:
        print(f"No path found from {start_node} to {end_node}")

    # Test sample grid
    start_node=(0,0)
    end_node=(3,3)
    path_grid=bfs_shortest_path_grid(4, 4, walls, start_node, end_node)
    if path_grid:
        print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(str(p) for p in path_grid)}")
    else:
        print(f"No path found from {start_node} to {end_node}")