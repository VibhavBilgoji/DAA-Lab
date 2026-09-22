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

    # Transcribed directly from the handwritten 10x10 matrix
    graph = [
        [INF, 61,  89,  67,  23,  68,  INF, 69,  INF, 96],
        [61,  INF, 91,  84,  37,  86,  73,  32,  13,  23],
        [89,  91,  INF, 57,  48,  96,  65,  98,  41,  INF],
        [67,  84,  57,  INF, 42,  80,  29,  24,  14,  73],
        [23,  37,  48,  42,  INF, 28,  24,  35,  86,  55],
        [68,  86,  96,  80,  28,  INF, 92,  97,  81,  14],
        [INF, 73,  65,  29,  24,  92,  INF, INF, 41,  99],
        [69,  32,  98,  24,  35,  97,  INF, INF, 93,  37],
        [INF, 13,  41,  14,  86,  81,  41,  93,  INF, INF],
        [96,  23,  INF, 73,  55,  14,  99,  37,  INF, INF]
    ]

    mst_edges, total_cost = prim(graph)

    if mst_edges == "Graph is empty or disconnected":
        print(mst_edges)
    else:
        print("=== FINAL MST RESULT ===")
        print("Edges in the MST (1-indexed):")
        for edge in mst_edges:
            print(f"({edge[0] + 1}, {edge[1] + 1})")
        print(f"Total Minimum Cost: {total_cost}")