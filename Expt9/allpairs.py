INF = float('inf')

def print_matrices(A, P, n, k):
    print(f"---------- k = {k} -----------")
    print("Cost Matrix (A):")
    for i in range(1, n + 1):
        row_str = " ".join(f"{A[i][j]:>4}" if A[i][j] != INF else " inf" for j in range(1, n + 1))
        print(f"  {row_str}")

    print("Precedence Matrix (P):")
    for i in range(1, n + 1):
        row_str = " ".join(f"{P[i][j]:>4}" for j in range(1, n + 1))
        print(f"  {row_str}")
    print()

def get_path(P, s, t):
    if s == t:
        return str(s)
    if P[s][t] == 0 or P[s][t] == '-':
        return "-"

    path = []
    curr = t
    while curr != s and curr != 0 and curr != '-':
        path.append(curr)
        curr = P[s][curr]

    if curr == 0 or curr == '-':
        return "-"

    path.append(s)
    return " -> ".join(map(str, reversed(path)))

def AllPathsAndPrecedence(cost, n):
    A = [[0] * (n + 1) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            A[i][j] = cost[i][j]
            if cost[i][j] != INF and cost[i][j] != 0:
                P[i][j] = i
            else:
                P[i][j] = '-' if i == j else 0

    print_matrices(A, P, n, 0)

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
                    P[i][j] = P[k][j]

        print_matrices(A, P, n, k)

    print("-" * 55)
    print(f"{'Source':<8} | {'Destination':<12} | {'Distance':<10} | {'Path'}")
    print("-" * 55)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j: continue
            d_str = str(A[i][j]) if A[i][j] != INF else "INF"
            p_str = get_path(P, i, j)
            print(f"{i:<8} | {j:<12} | {d_str:<10} | {p_str}")


if __name__ == "__main__":
    n = 6
    cost = [
        [INF, INF, INF, INF, INF, INF, INF],
        [INF, 0, 34, 25, 6, 49, 9],
        [INF, 45, 0, 18, 6, 5, 20],
        [INF, 19, 8, 0, 38, 26, 29],
        [INF, 13, 14, 6, 0, 15, 47],
        [INF, 37, 39, 27, 18, 0, 6],
        [INF, 53, 26, 26, 13, 6, 0],
    ]

    AllPathsAndPrecedence(cost, n)