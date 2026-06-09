/**
 * Finds the shortest path between start and goal nodes using BFS on a graph.
 * @param {Object} graph - Node key string -> array of neighbor key strings
 * @param {string} start - Start node key string
 * @param {string} goal - Goal node key string
 * @returns {Array<string>|null} Shortest path of node key strings
 */
export function bfsShortestPathGraph(graph, start, goal) {
    if (start===goal) {
        return [start];
    }
    
    const explored = new Set();
    const queue = [[start]]; // Queue stores full paths (lists of nodes) so we can track the exact route taken
    while (queue.length>0) {
        const path = queue.shift();
        const node = path[path.length-1];
        // Skip already explored nodes to prevent infinite loops in cyclic graphs
        if (!explored.has(node)) {
            const neighbors = graph[node] || [];
            for (const neighbor of neighbors) {
                const newPath = [...path, neighbor];
                queue.push(newPath);
                if (neighbor===goal) {
                    return newPath;
                }
            }
            explored.add(node);
        }
    }
    return null;
}

/**
 * Finds the shortest path between start and goal nodes using BFS on a grid.
 * @param {number} row - Grid row count
 * @param {number} column - Grid column count
 * @param {Set<string>} walls - Set of undirected edge key strings "r1,c1-r2,c2"
 * @param {Array<number>} start - [row, col] of start node
 * @param {Array<number>} goal - [row, col] of goal node
 * @returns {Array<Array<number>>|null} Shortest path of [row, col] coordinates
 */
export function bfsShortestPathGrid(row, column, walls, start, goal) {
    const graph = {};
    for (let i=0; i<row; i++) {
        for (let j=0; j<column; j++) {
            const nodeKey = JSON.stringify([i, j]);
            const offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]];
            const neighbours = [];
            for (const offset of offsets) {
                const new_i = i+offset[0];
                const new_j = j+offset[1];
                if (new_i>=0 && new_i<row && new_j>=0 && new_j<column) {
                    const edgeKey = getEdgeKey(i, j, new_i, new_j);
                    if (!walls.has(edgeKey)) {
                        neighbours.push(JSON.stringify([new_i, new_j]));
                    }
                }
            }
            graph[nodeKey] = neighbours;
        }
    }
    
    const startStr = JSON.stringify(start);
    const goalStr = JSON.stringify(goal);
    const pathStrList = bfsShortestPathGraph(graph, startStr, goalStr);
    if (!pathStrList) return null;
    return pathStrList.map(str => JSON.parse(str));
}

/**
 * Generates a unique, order-independent string representation of an edge.
 * Equivalent to a frozenset containing two coordinates.
 */
export function getEdgeKey(r1, c1, r2, c2) {
    const p1 = `${r1},${c1}`;
    const p2 = `${r2},${c2}`;
    return p1<p2 ? `${p1}-${p2}` : `${p2}-${p1}`;
}
