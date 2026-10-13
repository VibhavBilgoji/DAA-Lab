"""
Multistage graphs (Section 5.2): FGraph (forward approach, Algorithm 5.1)
and BGraph (backward approach, Algorithm 5.2).

All arrays are 1-indexed: index 0 holds None and is never used.

Input format
------------
k                      number of stages
s_1 s_2 ... s_k        number of vertices in each stage (s_1 = s_k = 1)
e                      number of edges
i j c                  (e lines) edge <i,j> with cost c

Vertices are numbered 1..n in order of stages (stage 1 first, then stage 2,
...). So with stage sizes 1 4 3 3 1, stage V2 = {2,3,4,5}, V3 = {6,7,8}, ...
"""

INF = float('inf')


# ---------------------------------------------------------------- Algorithm 5.1
def FGraph(G, k, n, p):
    # The input is a k-stage graph G = (V, E) with n vertices
    # indexed in order of stages. G[j] is the adjacency list of j, holding
    # (r, c[j, r]) pairs. p[1 : k] is a minimum-cost path.
    cost = [None] * (n + 1)
    d = [None] * (n + 1)

    cost[n] = 0.0
    for j in range(n - 1, 0, -1):
        # Compute cost[j].
        # Let r be a vertex such that <j, r> is an edge
        # of G and c[j, r] + cost[r] is minimum;
        r = None
        best = INF
        for (v, c) in G[j]:
            if c + cost[v] < best:
                best = c + cost[v]
                r = v
        cost[j] = best          # c[j, r] + cost[r]  (INF if j cannot reach t)
        d[j] = r

    # Find a minimum-cost path.
    if cost[1] < INF:           # guard: only trace if a path exists
        p[1] = 1
        p[k] = n
        for j in range(2, k):
            p[j] = d[p[j - 1]]
    return cost, d


# ---------------------------------------------------------------- Algorithm 5.2
def BGraph(G, k, n, p):
    # Same function as FGraph, but G here is the INVERSE adjacency list:
    # G[j] holds (r, c[r, j]) pairs for every edge <r, j>.
    bcost = [None] * (n + 1)
    d = [None] * (n + 1)

    bcost[1] = 0.0
    for j in range(2, n + 1):
        # Compute bcost[j].
        # Let r be such that <r, j> is an edge of
        # G and bcost[r] + c[r, j] is minimum;
        r = None
        best = INF
        for (v, c) in G[j]:
            if bcost[v] + c < best:
                best = bcost[v] + c
                r = v
        bcost[j] = best         # bcost[r] + c[r, j]  (INF if s cannot reach j)
        d[j] = r

    # Find a minimum-cost path.
    if bcost[n] < INF:          # guard: only trace if a path exists
        p[1] = 1
        p[k] = n
        for j in range(k - 1, 1, -1):
            p[j] = d[p[j + 1]]
    return bcost, d


# ------------------------------------------------------------------- helpers
def read_graph():
    k = int(input("Number of stages k: "))
    sizes = list(map(int, input(f"Vertices in each stage ({k} numbers): ").split()))
    if len(sizes) != k or k < 2 or sizes[0] != 1 or sizes[-1] != 1:
        raise ValueError("Need k >= 2 stage sizes with |V1| = |Vk| = 1")
    n = sum(sizes)

    stage = [None] * (n + 1)        # stage[v] = i such that v is in V_i
    v = 1
    for i, sz in enumerate(sizes, start=1):
        for _ in range(sz):
            stage[v] = i
            v += 1

    e = int(input("Number of edges: "))
    G = [None] + [[] for _ in range(n)]     # adjacency lists
    R = [None] + [[] for _ in range(n)]     # inverse adjacency lists
    print("Enter each edge as: i j cost")
    for _ in range(e):
        i, j, c = input().split()
        i, j, c = int(i), int(j), float(c)
        if not (1 <= i <= n and 1 <= j <= n) or stage[j] != stage[i] + 1:
            raise ValueError(f"Edge <{i},{j}> must go from stage i to stage i+1")
        G[i].append((j, c))
        R[j].append((i, c))
    return k, n, stage, G, R


def fmt(x):
    return str(int(x)) if float(x).is_integer() else str(x)


def all_paths(G, n):
    """Every s-to-t path with its cost (simple DFS, for display only)."""
    out = []

    def dfs(u, path, total):
        if u == n:
            out.append((path[:], total))
            return
        for (v, c) in G[u]:
            path.append(v)
            dfs(v, path, total + c)
            path.pop()

    dfs(1, [1], 0.0)
    return out


def main():
    k, n, stage, G, R = read_graph()

    # ---- forward approach
    p = [None] * (k + 1)
    cost, d = FGraph(G, k, n, p)
    print("\n================ FORWARD APPROACH (FGraph) ================")
    for i in range(1, k + 1):
        print(f"\n-- Stage V{i} --")
        for j in range(1, n + 1):
            if stage[j] != i:
                continue
            if cost[j] == INF:
                print(f"  vertex {j}: no path to t")
                continue
            path, v = [j], j
            while v != n:
                v = d[v]
                path.append(v)
            print(f"  vertex {j}: cost(j to t) = {fmt(cost[j])}, "
                  f"path = {' -> '.join(map(str, path))}")
    if cost[1] == INF:
        print("\nNo s-t path exists.")
    else:
        print(f"\nMinimum-cost s-t path: p[1:{k}] = {p[1:k + 1]}, cost = {fmt(cost[1])}")

    # ---- backward approach
    p = [None] * (k + 1)
    bcost, d = BGraph(R, k, n, p)
    print("\n================ BACKWARD APPROACH (BGraph) ================")
    for i in range(1, k + 1):
        print(f"\n-- Stage V{i} --")
        for j in range(1, n + 1):
            if stage[j] != i:
                continue
            if bcost[j] == INF:
                print(f"  vertex {j}: not reachable from s")
                continue
            path, v = [j], j
            while v != 1:
                v = d[v]
                path.insert(0, v)
            print(f"  vertex {j}: bcost(s to j) = {fmt(bcost[j])}, "
                  f"path = {' -> '.join(map(str, path))}")
    if bcost[n] == INF:
        print("\nNo s-t path exists.")
    else:
        print(f"\nMinimum-cost s-t path: p[1:{k}] = {p[1:k + 1]}, cost = {fmt(bcost[n])}")

    # ---- every s-t path
    print("\n================ ALL s-t PATHS ================")
    paths = all_paths(G, n)
    best = min((c for _, c in paths), default=None)
    for path, c in sorted(paths, key=lambda x: x[1]):
        mark = "   <-- minimum" if c == best else ""
        print(f"  {' -> '.join(map(str, path))}  (cost {fmt(c)}){mark}")
    print(f"\nTotal s-t paths: {len(paths)}")


if __name__ == "__main__":
    main()
