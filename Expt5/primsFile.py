def prim(cost_matrix: list[list[int]]):
    n = len(cost_matrix)

    t = [[0, 0] for _ in range(n - 1)]
    near = [0] * n
    mincost = 0

    def print_state(step, edge_count):
        print(f"--- Step {step} ---")
        mst_so_far = [(t[idx][0] + 1, t[idx][1] + 1) for idx in range(edge_count)]
        print(f"MST Edges:  {mst_so_far}")

        vertices_display = [v for v in range(1, n + 1)]
        print(f"Vertices:   {vertices_display}")

        near_display = [0 if near[v] == -1 else near[v] + 1 for v in range(n)]
        print(f"Near Array: {near_display}")

        weights_display = []
        for v in range(n):
            if near[v] == -1:
                weights_display.append(0)
            else:
                weight = cost_matrix[v][near[v]]
                weights_display.append(weight if weight != float('inf') else 'INF')
        print(f"Weights:    {weights_display}\n")

    min_val = float('inf')
    k, l = -1, -1
    for i in range(n):
        for j in range(i + 1, n):
            if cost_matrix[i][j] < min_val:
                min_val = cost_matrix[i][j]
                k, l = i, j

    if k == -1 or l == -1:
        return "Graph is empty or disconnected", 0

    t[0][0], t[0][1] = k, l
    mincost += cost_matrix[k][l]

    for i in range(n):
        if cost_matrix[i][l] < cost_matrix[i][k]:
            near[i] = l
        else:
            near[i] = k

    near[k] = near[l] = -1

    print_state(1, 1)

    for i in range(1, n - 1):

        j = -1
        min_val = float('inf')
        for v in range(n):
            if near[v] != -1 and cost_matrix[v][near[v]] < min_val:
                min_val = cost_matrix[v][near[v]]
                j = v

        if j == -1:
            break

        t[i][0] = j
        t[i][1] = near[j]
        mincost += cost_matrix[j][near[j]]

        near[j] = -1

        for v in range(n):
            if near[v] != -1 and cost_matrix[v][near[v]] > cost_matrix[v][j]:
                near[v] = j

        print_state(i + 1, i + 1)

    return t, mincost

if __name__ == "__main__":
    INF = float('inf')
    graph = [
        [INF, 14 , 60, 10, 71, 50, 44, INF, 47, INF],
        [14, INF, 78, 43, 41, 18, 28, 56, 72, 60],
        [60, 78, INF, 55, 88, 72, 39, 95, 77, 51],
        [10, 43, 55, INF, 12, 17, INF, 11, INF, 42],
        [71, 41, 88, 12, INF, 81, 61, 22, 54, 92],
        [50, 18, 72, 17, 81, INF, INF, 44, 54, 58],
        [44, 28, 39, INF, 61, INF, INF, 27, 88, 97],
        [INF, 56, 95, 11, 22, 44, 27, INF, 30, 31],
        [47, 72, 77, INF, 54, 54, 88, 30, INF, 21],
        [INF, 60, 51, 42, 92, 58, 97, 31, 21, INF]
    ]

    mst_edges, total_cost = prim(graph)

    print("=== FINAL MST RESULT ===")
    print("Edges in the MST (1-indexed):")
    for edge in mst_edges:
        print(f"({edge[0] + 1}, {edge[1] + 1})")
    print(f"Total Minimum Cost: {total_cost}")
