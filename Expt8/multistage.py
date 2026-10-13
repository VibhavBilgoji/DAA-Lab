INF = float('inf')


def FGraph(G, k, n, p):
    cost = [None] * (n + 1)
    d = [None] * (n + 1)

    cost[n] = 0.0
    for j in range(n - 1, 0, -1):
        r = None
        best = INF
        for (v, c) in G[j]:
            if c + cost[v] < best:
                best = c + cost[v]
                r = v
        cost[j] = best
        d[j] = r

    if cost[1] < INF:
        p[1] = 1
        p[k] = n
        for j in range(2, k):
            p[j] = d[p[j - 1]]
    return cost, d


def BGraph(G, k, n, p):
    bcost = [None] * (n + 1)
    d = [None] * (n + 1)

    bcost[1] = 0.0
    for j in range(2, n + 1):
        r = None
        best = INF
        for (v, c) in G[j]:
            if bcost[v] + c < best:
                best = bcost[v] + c
                r = v
        bcost[j] = best
        d[j] = r

    if bcost[n] < INF:
        p[1] = 1
        p[k] = n
        for j in range(k - 1, 1, -1):
            p[j] = d[p[j + 1]]
    return bcost, d


def read_graph():
    k = 5
    sizes = [1, 4, 4, 4, 1]
    n = sum(sizes)                      # 14

    stage = [None] * (n + 1)
    v = 1
    for i, sz in enumerate(sizes, start=1):
        for _ in range(sz):
            stage[v] = i
            v += 1

    # (from, to, cost)
    edges = [
        # stage 1 -> 1 vertex
        (1, 2, 3), (1, 3, 9), (1, 4, 10), (1, 5, 11),
        # stage 2 -> 4 vertices
        (2, 6, 5), (2, 8, 15), (2, 9, 2),
        (3, 7, 3), (3, 8, 10), (3, 9, 6),
        (4, 6, 11), (4, 8, 5),
        (5, 6, 2), (5, 7, 14), (5, 8, 1), (5, 9, 3),
        # stage 3 -> 4 vertices
        (6, 10, 5), (6, 11, 8), (6, 12, 7), (6, 13, 2),
        (7, 10, 15), (7, 11, 3), (7, 12, 14), (7, 13, 9),
        (8, 10, 3), (8, 11, 6), (8, 13, 14),
        (9, 10, 6), (9, 11, 4), (9, 12, 6), (9, 13, 15),
        # stage 4 -> 4 vertices
        (10, 14, 13), (11, 14, 15), (12, 14, 15), (13, 14, 1),
    ]

    G = [None] + [[] for _ in range(n)]
    R = [None] + [[] for _ in range(n)]
    for i, j, c in edges:
        assert stage[j] == stage[i] + 1, f"Edge <{i},{j}> must go from stage i to i+1"
        G[i].append((j, float(c)))
        R[j].append((i, float(c)))
    return k, n, stage, G, R

def fmt(x):
    return str(int(x)) if float(x).is_integer() else str(x)


def all_paths(G, n):
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

    p = [None] * (k + 1)
    cost, d = FGraph(G, k, n, p)
    print("\nFORWARD APPROACH")
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

    p = [None] * (k + 1)
    bcost, d = BGraph(R, k, n, p)
    print("\nBACKWARD APPROACH")
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

    print("\nALL s-t PATHS")
    paths = all_paths(G, n)
    best = min((c for _, c in paths), default=None)
    for path, c in sorted(paths, key=lambda x: x[1]):
        mark = "   <-- minimum" if c == best else ""
        print(f"  {' -> '.join(map(str, path))}  (cost {fmt(c)}){mark}")
    print(f"\nTotal s-t paths: {len(paths)}")


if __name__ == "__main__":
    main()