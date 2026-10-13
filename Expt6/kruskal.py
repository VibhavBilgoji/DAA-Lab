INF = float('inf')

def partition(edges, cost, low, high):
    pivot = cost[edges[high][0]][edges[high][1]]
    i = low - 1
    for j in range(low, high):
        if cost[edges[j][0]][edges[j][1]] <= pivot:
            i += 1
            edges[i], edges[j] = edges[j], edges[i]
    edges[i + 1], edges[high] = edges[high], edges[i + 1]
    return i + 1

def quick_sort(edges, cost, low, high):
    if low < high:
        pi = partition(edges, cost, low, high)
        quick_sort(edges, cost, low, pi - 1)
        quick_sort(edges, cost, pi + 1, high)

def Find(i, parent):
    while parent[i] > 0:
        i = parent[i]
    return i

def Union(i, j, parent):
    parent[j] = i

def print_step(step_count, u, v, weight, accepted, mincost, parent, n):
    status = "ACCEPTED" if accepted else "REJECTED (Cycle)"
    print(f"Step {step_count:2d} | Edge ({u:2d}, {v:2d}) w={weight:2d} -> {status:<16} | Running Cost: {mincost:3d}")
    parent_str = " ".join(f"{parent[k]:3d}" for k in range(1, n + 1))
    print(f"        parent: [{parent_str}]\n")

def print_t_table(t, n):
    print("\n" + "-" * 30)
    print("   Final MST Edges (t)     ")
    print("-" * 30)
    print("Row (i) |  t[i, 1]|  t[i, 2]")
    print("-" * 30)
    for i in range(1, n): print(f"   {i:<4} |    {t[i][1]:<4} |    {t[i][2]:<4}")
    print("-" * 30)

def Kruskal(E, cost, n, t):
    quick_sort(E, cost, 0, len(E) - 1)
    parent = [-1] * (n + 1)
    i = 0
    mincost = 0.0
    step_count = 0
    for u, v in E:
        if i == n - 1: break
        step_count += 1
        edge_weight = cost[u][v]
        j = Find(u, parent)
        k = Find(v, parent)
        if j != k:
            i += 1
            t[i][1] = u
            t[i][2] = v
            mincost += edge_weight
            Union(j, k, parent)
            print_step(step_count, u, v, edge_weight, True, int(mincost), parent, n)
        else:
            print_step(step_count, u, v, edge_weight, False, int(mincost), parent, n)
    if i != n - 1:
        print("\nNo spanning tree exists.")
        return 0
    return mincost

n = 10
cost = [[INF] * (n + 1) for _ in range(n + 1)]
raw_edges = [
    (1, 2, 61), (1, 3, 89), (1, 4, 67), (1, 5, 23), (1, 6, 68), (1, 8, 69), (1, 10, 96),
    (2, 3, 91), (2, 4, 84), (2, 5, 37), (2, 6, 86), (2, 7, 73), (2, 8, 32), (2, 9, 13), (2, 10, 23),
    (3, 4, 57), (3, 5, 48), (3, 6, 96), (3, 7, 65), (3, 8, 98), (3, 9, 41),
    (4, 5, 42), (4, 6, 80), (4, 7, 29), (4, 8, 24), (4, 9, 14), (4, 10, 73),
    (5, 6, 28), (5, 7, 24), (5, 8, 35), (5, 9, 86), (5, 10, 55),
    (6, 7, 92), (6, 8, 97), (6, 9, 81), (6, 10, 14),
    (7, 9, 41), (7, 10, 99),
    (8, 9, 93), (8, 10, 37)
]
E = []
for u, v, w in raw_edges:
    cost[u][v] = w
    cost[v][u] = w
    E.append((u, v))
t = [[0, 0, 0] for _ in range(n)]
final_cost = Kruskal(E, cost, n, t)
print(f"\nFinal Minimum Cost = {int(final_cost)}")
print_t_table(t, n)

